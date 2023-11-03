import { backendUrl } from "~/config";
import type { Message } from "~/types/conversation";
import { BackendDocumentType, type BackendDocument } from "~/types/backend/document";
import { SecDocument } from "~/types/document";
import { fromBackendDocumentToFrontend } from "./utils/documents";

interface CreateConversationPayload {
  id: string;
}

interface GetConversationPayload {
  id: string;
  messages: Message[];
  documents: BackendDocument[];
}

interface GetConversationReturnType {
  messages: Message[];
  documents: SecDocument[];
}

class BackendClient {
  private async get(endpoint: string) {
    const url = backendUrl + endpoint;
    const res = await fetch(url);

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res;
  }

  private async post(endpoint: string, body?: any) {
    const url = backendUrl + endpoint;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res;
  }

  public async createConversation(documentIds: string[]): Promise<string> {
    const endpoint = "api/conversation/";
    const payload = { document_ids: documentIds };
    const res = await this.post(endpoint, payload);
    const data = (await res.json()) as CreateConversationPayload;

    return data.id;
  }

  public async fetchConversation(
    id: string
  ): Promise<GetConversationReturnType> {
    const endpoint = `api/conversation/${id}`;
    const res = await this.get(endpoint);
    const data = (await res.json()) as GetConversationPayload;

    const newData = [];
    for (let i = 0; i < data.documents.length; i++) {
      const element = data.documents[i];
      // if (element) {
      //   element.url = "https://mock-data-20scoops.s3.ap-southeast-1.amazonaws.com/APznzaae_PHPfTErTBgZWvRwZsEkVhu5EEW445RNiEIFiQNNzhHfPD5UWHsEIzfPFaQG4GQxvqeLlbALtsCuA0CIwe1RXUIq8u0Bvq6aa-FYhHNxAWnTez0B2VsRaE33JblvzQGW47XITwA5N-PE4OZpCJMDThoBmKJof6rq3vVPIdSwNQrNCKcNDdXKqcKqy0TES3CVioBuUmBPOhnt6kqV9eK3UL1lLxjAUHmirXu3b42h.pdf";
      // }
      if (element?.metadata_map) {
        element.metadata_map.sec_document = {
          year: 2021,
          doc_type: BackendDocumentType.TenK,
          company_name: `Book ${i}`,
          company_ticker: `BK_${i}`,
          quarter: 1
        };
      }
      newData.push(element);
    }

    return {
      messages: data.messages,
      documents: fromBackendDocumentToFrontend(newData as BackendDocument[]),
    };
  }

  public async fetchDocuments(): Promise<SecDocument[]> {
    const endpoint = `api/document/`;
    const res = await this.get(endpoint);
    const data = (await res.json()) as BackendDocument[];
    const newData = [];
    for (let i = 0; i < data.length; i++) {
      const element = data[i];
      // if (element) {
      //   element.url = "https://mock-data-20scoops.s3.ap-southeast-1.amazonaws.com/APznzaae_PHPfTErTBgZWvRwZsEkVhu5EEW445RNiEIFiQNNzhHfPD5UWHsEIzfPFaQG4GQxvqeLlbALtsCuA0CIwe1RXUIq8u0Bvq6aa-FYhHNxAWnTez0B2VsRaE33JblvzQGW47XITwA5N-PE4OZpCJMDThoBmKJof6rq3vVPIdSwNQrNCKcNDdXKqcKqy0TES3CVioBuUmBPOhnt6kqV9eK3UL1lLxjAUHmirXu3b42h.pdf";
      // }
      if (element?.metadata_map) {
        element.metadata_map.sec_document = {
          year: 2021,
          doc_type: BackendDocumentType.TenK,
          company_name: `Book ${i}`,
          company_ticker: `BK_${i}`,
          quarter: 1
        };
      }
      newData.push(element);
    }
    const docs = fromBackendDocumentToFrontend(newData as BackendDocument[]);
    return docs;
  }
}

export const backendClient = new BackendClient();
