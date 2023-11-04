import { MAX_NUMBER_OF_SELECTED_DOCUMENTS } from "~/hooks/useDocumentSelector";
import { BackendDocument, BackendDocumentType } from "~/types/backend/document";
import { SecDocument, DocumentType } from "~/types/document";
import { documentColors } from "~/utils/colors";
import _ from "lodash";

export const fromBackendDocumentToFrontend = (
  backendDocuments: BackendDocument[]
) => {
  // sort by created_at so that de-dupe filter later keeps oldest duplicate docs
  backendDocuments = _.sortBy(backendDocuments, 'created_at');
  let frontendDocs: SecDocument[] = backendDocuments
  .filter((backendDoc) => 'sec_document' in backendDoc.metadata_map)
  .map((backendDoc, index) => {
    const backendDocType = backendDoc.metadata_map.sec_document.doc_type;
    const frontendDocType =
      backendDocType === BackendDocumentType.TenK
        ? DocumentType.TenK
        : DocumentType.TenQ;

    // we have 10 colors for 10 documents
    const colorIndex = index < 10 ? index : 0;
    return {
      id: backendDoc.id,
      url: backendDoc.url,
      ticker: backendDoc.metadata_map.sec_document.company_ticker,
      fullName: backendDoc.metadata_map.sec_document.company_name,
      year: String(backendDoc.metadata_map.sec_document.year),
      docType: frontendDocType,
      color: documentColors[colorIndex],
      quarter: backendDoc.metadata_map.sec_document.quarter || "",
    } as SecDocument;
  });
  // de-dupe hotfix
  const getDocDeDupeKey = (doc: SecDocument) => `${doc.ticker}-${doc.year}-${doc.quarter || ''}`;
  frontendDocs = _.chain(frontendDocs).sortBy(getDocDeDupeKey).sortedUniqBy(getDocDeDupeKey).value();

  return frontendDocs;
};
