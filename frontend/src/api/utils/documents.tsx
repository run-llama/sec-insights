import { MAX_NUMBER_OF_SELECTED_DOCUMENTS } from "~/hooks/useDocumentSelector";
import { BackendDocument, BackendDocumentType } from "~/types/backend/document";
import { SecDocument, DocumentType } from "~/types/document";
import { documentColors } from "~/utils/colors";

export const fromBackendDocumentToFrontend = (
  backendDocuments: BackendDocument[]
) => {
  const frontendDocs: SecDocument[] = [];
  backendDocuments.map((backendDoc, index) => {
    const backendDocType = backendDoc.metadata_map.sec_document.doc_type;
    const frontendDocType =
      backendDocType === BackendDocumentType.TenK
        ? DocumentType.TenK
        : DocumentType.TenQ;

    // we have 10 colors for 10 documents
    const colorIndex = index < 10 ? index : 0;
    const payload = {
      id: backendDoc.id,
      url: backendDoc.url,
      ticker: backendDoc.metadata_map.sec_document.company_ticker,
      fullName: backendDoc.metadata_map.sec_document.company_name,
      year: String(backendDoc.metadata_map.sec_document.year),
      docType: frontendDocType,
      color: documentColors[colorIndex],
      quarter: backendDoc.metadata_map.sec_document.quarter || "",
    } as SecDocument;
    frontendDocs.push(payload);
  });
  return frontendDocs;
};
