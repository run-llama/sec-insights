import cmd
import requests
from sseclient import SSEClient
import json
import random
from urllib.parse import quote


def sse_with_requests(url, headers) -> requests.Response:
    """Get a streaming response for the given event feed using requests."""
    return requests.get(url, stream=True, headers=headers)


class DocumentPickerCmd(cmd.Cmd):
    prompt = "(Pick📄) "

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.documents = None
        self.selected_documents = []

    def do_fetch(self, args):
        "Get 5 documents: fetch"
        response = requests.get(f"{self.base_url}/api/document/")
        if response.status_code == 200:
            self.documents = random.choices(response.json(), k=5)
            for idx, doc in enumerate(self.documents):
                print(f"[{idx}]: {doc['url']}")
        else:
            print(f"Error: {response.text}")

    def do_select(self, document_idx):
        "Select a document by its index: select <Index>"
        if self.documents is None:
            print("Please fetch documents first: fetch")
            return
        try:
            idx = int(document_idx)
            if idx < len(self.documents):
                self.selected_documents.append(self.documents[idx])
                print(f"Selected document: {self.documents[idx]['url']}")
            else:
                print("Invalid index. Use the GET command to view available documents.")
        except ValueError:
            print("Invalid index. Please enter a number.")

    def do_select_id(self, document_id):
        "Select a document by it's ID"
        if not document_id:
            print("Please enter a valid document ID")
        else:
            self.selected_documents.append({"id": document_id})
            print(f"Selected document ID {document_id}")

    def do_finish(self, args):
        "Finish the document selection process: FINISH"
        if len(self.selected_documents) > 0:
            return True
        else:
            print("No documents selected. Use the SELECT command to select documents.")

    def do_quit(self, args):
        "Quits the program."
        print("Quitting document picker.")
        raise SystemExit


class ConversationCmd(cmd.Cmd):
    prompt = "(Chat🦙) "

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.conversation_id = None
        self.document_ids = []

    def do_pick_docs(self, args):
        "Pick documents for the new conversation: pick_docs"
        picker = DocumentPickerCmd(self.base_url)
        try:
            picker.cmdloop()
        except KeyboardInterrupt:
            picker.do_quit("")
        except Exception as e:
            print(e)
            picker.do_quit("")
        self.document_ids = [doc["id"] for doc in picker.selected_documents]

    def do_create(self, args):
        "Create a new conversation: CREATE"
        req_body = {"document_ids": self.document_ids}
        response = requests.post(f"{self.base_url}/api/conversation/", json=req_body)
        if response.status_code == 200:
            self.conversation_id = response.json()["id"]
            print(f"Created conversation with ID {self.conversation_id}")
        else:
            print(f"Error: {response.text}")

    def do_detail(self, args):
        "Get the details of the current conversation: DETAIL"
        if not self.conversation_id:
            print("No active conversation. Use CREATE to start a new conversation.")
            return
        response = requests.get(
            f"{self.base_url}/api/conversation/{self.conversation_id}"
        )
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Error: {response.text}")

    def do_delete(self, args):
        "Delete the current conversation: DELETE"
        if not self.conversation_id:
            print("No active conversation to delete.")
            return
        response = requests.delete(
            f"{self.base_url}/api/conversation/{self.conversation_id}"
        )
        if response.status_code == 204:
            print(f"Deleted conversation with ID {self.conversation_id}")
            self.conversation_id = None
        else:
            print(f"Error: {response.text}")

    def do_message(self, message):
        "Send a user message to the current conversation and get back the AI's response: MESSAGE <Your message>"
        if not self.conversation_id:
            print("No active conversation. Use CREATE to start a new conversation.")
            return
        message = quote(message.strip())  # URI encode the message
        url = f"{self.base_url}/api/conversation/{self.conversation_id}/message?user_message={message}"
        headers = {"Accept": "text/event-stream"}
        response = sse_with_requests(url, headers)
        messages = SSEClient(response).events()
        message_idx = 0
        final_message = None
        for msg in messages:
            print(f"\n\n=== Message {message_idx} ===")
            msg_json = json.loads(msg.data)
            print(msg_json)
            final_message = msg_json.get("content")
            message_idx += 1

        if final_message is not None:
            print(f"\n\n====== Final Message ======")
            print(final_message)

    def do_quit(self, args):
        "Quits the program."
        print("Quitting.")
        raise SystemExit


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the chat terminal.")
    parser.add_argument(
        "--base_url",
        type=str,
        default="http://localhost:8000",
        help="an optional base url for the API endpoints",
    )
    args = parser.parse_args()

    cmd = ConversationCmd(args.base_url)
    try:
        cmd.cmdloop()
    except KeyboardInterrupt:
        cmd.do_quit("")
    except Exception as e:
        print(e)
        cmd.do_quit("")
