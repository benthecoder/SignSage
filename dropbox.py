import os
from pprint import pprint
from dropbox_sign import ApiClient, ApiException, Configuration, apis
from dotenv import load_dotenv

load_dotenv()

DROPBOX_SIGN_API_KEY = os.getenv("DROPBOX_SIGN_API_KEY")


class DropboxSignClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.config = Configuration(username=self.api_key)

    def get_account(self, email):
        with ApiClient(self.config) as api_client:
            account_api = apis.AccountApi(api_client)
            try:
                return account_api.account_get(email_address=email)
            except ApiException as e:
                print(f"Exception when calling Dropbox Sign API: {e}")
                return None

    def list_signature_requests(self, account_id=None, page=1):
        with ApiClient(self.config) as api_client:
            signature_request_api = apis.SignatureRequestApi(api_client)
            try:
                response = signature_request_api.signature_request_list(
                    account_id=account_id, page=page
                )
                return self._parse_signature_request(response)
            except ApiException as e:
                print(f"Exception when calling Dropbox Sign API: {e}")

    @staticmethod
    def _parse_signature_request(response):
        return [
            {
                "title": request["title"],
                "signature_id": request["signature_request_id"],
                "requester": request["requester_email_address"],
                "url": request["signing_url"],
            }
            for request in response.get("signature_requests", [])
        ]

    def download_file(self, signature_request_id, fname="file.pdf"):
        with ApiClient(self.config) as api_client:
            signature_request_api = apis.SignatureRequestApi(api_client)
            try:
                response = signature_request_api.signature_request_files(
                    signature_request_id, file_type="pdf"
                )
                with open(fname, "wb") as file:
                    file.write(response.read())

                with open(fname, "rb") as file:
                    return file.read()
            except ApiException as e:
                print(f"Exception when calling Dropbox Sign API: {e}")


if __name__ == "__main__":
    client = DropboxSignClient(DROPBOX_SIGN_API_KEY)
    pprint(client.list_signature_requests())
    client.download_file("acf6e8691b99a8ce7610187c577e67b2d375d803")
