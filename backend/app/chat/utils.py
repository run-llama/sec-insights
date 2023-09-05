from app.schema import (
    Document as DocumentSchema,
    DocumentMetadataKeysEnum,
    SecDocumentMetadata,
)


def build_title_for_document(document: DocumentSchema) -> str:
    if DocumentMetadataKeysEnum.SEC_DOCUMENT not in document.metadata_map:
        return "No Title Document"

    sec_metadata = SecDocumentMetadata.parse_obj(
        document.metadata_map[DocumentMetadataKeysEnum.SEC_DOCUMENT]
    )
    time_period = (
        f"{sec_metadata.year} Q{sec_metadata.quarter}"
        if sec_metadata.quarter is not None
        else str(sec_metadata.year)
    )
    return f"{sec_metadata.company_name} ({sec_metadata.company_ticker}) {sec_metadata.doc_type.value} ({time_period})"
