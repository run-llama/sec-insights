from typing import List, Iterator, cast
import logging

# This is from the unofficial polygon.io client: https://polygon.readthedocs.io/
from polygon.reference_apis import ReferenceClient
from polygon.reference_apis.reference_api import AsyncReferenceClient

# This is from the official polygon.io client: https://polygon-api-client.readthedocs.io/
from polygon.rest.models import StockFinancial

from app.schema import (
    Document as DocumentSchema,
    DocumentMetadataKeysEnum,
    SecDocumentMetadata,
)
from llama_index.tools import FunctionTool, ToolMetadata, QueryEngineTool
from llama_index.indices.service_context import ServiceContext
from llama_index.agent import OpenAIAgent
from app.core.config import settings
from app.chat.utils import build_title_for_document


logger = logging.getLogger(__name__)


from typing import List


def describe_financials(financials: StockFinancial) -> str:
    sentences: List[str] = []

    company = financials.company_name
    fiscal_year = financials.fiscal_year
    fiscal_period = financials.fiscal_period

    sentences.append(
        f"For {company} in fiscal year {fiscal_year} covering the period {fiscal_period}:"
    )

    income_statement = financials.financials.income_statement

    if income_statement:
        revenues = income_statement.revenues
        if revenues:
            revenue_str = f"{revenues.label}: {revenues.value} {revenues.unit}"
            sentences.append(f"Revenues were {revenue_str}.")

        expenses = income_statement.operating_expenses
        if expenses:
            expenses_str = f"{expenses.label}: {expenses.value} {expenses.unit}"
            sentences.append(f"Operating expenses were {expenses_str}.")

        gross_profit = income_statement.gross_profit
        if gross_profit:
            gross_profit_str = f"{gross_profit.value} {gross_profit.unit}"
            sentences.append(f"Gross profit was {gross_profit_str}.")

    net_income = (
        financials.financials.comprehensive_income.comprehensive_income_loss_attributable_to_parent
    )
    if net_income:
        net_income_str = f"{net_income.label}: {net_income.value} {net_income.unit}"
        sentences.append(f"Net income was {net_income_str}.")

    cash_flows = financials.financials.cash_flow_statement
    if cash_flows:
        operating_cash_flows = cash_flows.net_cash_flow
        if operating_cash_flows:
            operating_str = f"{operating_cash_flows.label}: {operating_cash_flows.value} {operating_cash_flows.unit}"
            sentences.append(f"Net cash from operating activities was {operating_str}.")

        financing_cash_flows = cash_flows.net_cash_flow_from_financing_activities
        if financing_cash_flows:
            financing_str = f"{financing_cash_flows.label}: {financing_cash_flows.value} {financing_cash_flows.unit}"
            sentences.append(f"Net cash from financing activities was {financing_str}.")

    return " ".join(sentences)


def get_tool_metadata_for_document(doc: DocumentSchema) -> ToolMetadata:
    doc_title = build_title_for_document(doc)
    name = f"extract_json_from_sec_document[{doc_title}]"
    description = f"Returns basic financial data extracted from the SEC filing document {doc_title}"
    return ToolMetadata(
        name=name,
        description=description,
    )


def get_polygon_io_sec_tool(document: DocumentSchema) -> FunctionTool:
    sec_metadata = SecDocumentMetadata.parse_obj(
        document.metadata_map[DocumentMetadataKeysEnum.SEC_DOCUMENT]
    )
    tool_metadata = get_tool_metadata_for_document(document)

    async def extract_data_from_sec_document(*args, **kwargs) -> List[str]:
        try:
            client = ReferenceClient(
                api_key=settings.POLYGON_IO_API_KEY,
                connect_timeout=10,
                read_timeout=10,
                max_connections=20,
                use_async=True,
            )
            client = cast(AsyncReferenceClient, client)
            response_dict = await client.get_stock_financials_vx(
                ticker=sec_metadata.company_ticker,
                period_of_report_date=str(sec_metadata.period_of_report_date.date()),
                limit=100,  # max limit is 100
            )
            stock_financials = []
            for result_dict in response_dict["results"]:
                stock_financials.append(StockFinancial.from_dict(result_dict))

            descriptions = []
            for stock_financial in stock_financials:
                description = describe_financials(stock_financial)
                logger.debug(
                    "Built the following description for document_id=%s: %s",
                    str(document.id),
                    description,
                )
                descriptions.append(description)
            return descriptions
        except:
            logger.error(
                "Error retrieving data from polygon.io for document_id %s",
                str(document.id),
                exc_info=True,
            )
            return ["No answer found."]

    def sync_func_placeholder(*args, **kwargs) -> None:
        raise NotImplementedError(
            "Sync function was called for document_id=" + str(document.id)
        )

    return FunctionTool.from_defaults(
        fn=sync_func_placeholder,
        async_fn=extract_data_from_sec_document,
        description=tool_metadata.description,
    )


def get_api_query_engine_tool(
    document: DocumentSchema, service_context: ServiceContext
) -> QueryEngineTool:
    polygon_io_tool = get_polygon_io_sec_tool(document)
    tool_metadata = get_tool_metadata_for_document(document)
    doc_title = build_title_for_document(document)
    agent = OpenAIAgent.from_tools(
        [polygon_io_tool],
        llm=service_context.llm,
        callback_manager=service_context.callback_manager,
        system_prompt=f"You are an agent that is asked quantitative questions about a SEC filing named {doc_title} and you answer them by using your tools.",
    )
    return QueryEngineTool.from_defaults(
        query_engine=agent,
        name=tool_metadata.name,
        description=tool_metadata.description,
    )
