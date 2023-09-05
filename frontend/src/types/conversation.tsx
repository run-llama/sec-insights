import { DocumentColorEnum } from "~/utils/colors";

export enum MESSAGE_STATUS {
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  ERROR = "ERROR",
}

export enum ROLE {
  USER = "user",
  ASSISTANT = "assistant",
}

export enum MessageSubprocessSource {
  PLACEHOLDER = "placeholder",
}

export interface hasId {
  id: string;
}

export interface Citation {
  documentId: string;
  snippet: string;
  pageNumber: number;
  ticker: string;
  displayDate: string;
  color: DocumentColorEnum;
}

export interface Conversation extends hasId {
  messages?: Message[];
}

export interface Message extends hasId {
  content: string;
  role: ROLE;
  status: MESSAGE_STATUS;
  conversationId: string;
  sub_processes?: MessageSubProcess[];
  created_at: Date;
}
export interface MessageSubProcess extends hasId {
  messageId: string;
  content: string;
  source: MessageSubprocessSource;
  metadata_map?: MetaDataMap;
}

export interface ParsedData {
  content?: string;
  status?: string;
}

export interface MetaDataMap {
  sub_question?: SubQuestion;
  sub_questions?: SubQuestion[];
}

export interface SubQuestion {
  question: string;
  answer?: string;
  citations?: BackendCitation[];
}

export interface BackendCitation {
  document_id: string;
  page_number: number;
  score: number;
  text: string;
}
