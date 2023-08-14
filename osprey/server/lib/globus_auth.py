import os, json
from globus_sdk import NativeAppAuthClient, AccessTokenAuthorizer

# Permanent
# OSPREY_DIR = os.path.join(os.path.expanduser("~"), ".local/share/osprey")
# TODO: Change this 
OSPREY_DIR = '/app/osprey/server'
TOKENS_FILE = os.path.join(OSPREY_DIR, "tokens.json")

_TIMER_CLIENT_UUID: str = "524230d7-ea86-4a52-8312-86065a9e0417"
_REDIRECT_URI = "https://auth.globus.org/v2/web/auth-code"
_CLIENT_ID: str = "c78511ef-8cf7-4802-a7e1-7d56e27b1bf8"

def authenticate(client: NativeAppAuthClient, scope: str):
    """Perform Globus Authentication."""

    client.oauth2_start_flow(
        redirect_uri=_REDIRECT_URI, 
        refresh_tokens=True,
        requested_scopes=scope
    )

    url = client.oauth2_get_authorize_url()
    print("Please visit the following url to authenticate:")
    print(url)

    auth_code = input("Enter the auth code:")
    auth_code = auth_code.strip()
    return client.oauth2_exchange_code_for_tokens(auth_code)

def create_token_file(client: NativeAppAuthClient, scope: str | None = None) -> AccessTokenAuthorizer:
    tokens = authenticate(client, scope)
    timer_access_token = tokens.by_resource_server[_TIMER_CLIENT_UUID]["access_token"]
    authorizer = AccessTokenAuthorizer(access_token=timer_access_token)

    with open(TOKENS_FILE, "w+") as f:
        json.dump(tokens.by_resource_server[_TIMER_CLIENT_UUID], f)

    return authorizer

if __name__ == "__main__":
    if not os.path.exists(TOKENS_FILE):
        client = NativeAppAuthClient(client_id=_CLIENT_ID)
        _TIMER_SCOPE = f"https://auth.globus.org/scopes/{_TIMER_CLIENT_UUID}/timer"
        create_token_file(client, _TIMER_SCOPE)

