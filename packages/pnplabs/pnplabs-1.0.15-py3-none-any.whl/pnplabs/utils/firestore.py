import json
import requests

from requests.exceptions import HTTPError
from google.oauth2.credentials import Credentials
from google.cloud.firestore import Client

FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"
FB_API_KEY = "AIzaSyA59_DoB7koBFkXDrwtO_orgJ3GDkZyO8M"
PNP_API_KEY = "06fba83f-0a08-4feb-b03c-8d642569325e"


def get_token_and_user_id_with_pnp_api_key(api_key):
    request_url = "https://us-central1-pnplabs-be.cloudfunctions.net/tokener"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"apiKey": api_key})

    resp = requests.post(request_url, headers=headers, data=data)
    # Check for errors
    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)

    return resp.json()


def sign_in_with_token(token, api_key=FB_API_KEY):
    request_url = "%s:signInWithCustomToken?key=%s" % (FIREBASE_REST_API, api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"token": token, "returnSecureToken": True})

    resp = requests.post(request_url, headers=headers, data=data)
    # Check for errors
    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)

    return resp.json()


def refresh_token(refresh_token, api_key=FB_API_KEY):
    refresh_request_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"refresh_token": refresh_token, "grant_type": "refresh_token"})

    resp = requests.post(refresh_request_url, headers=headers, data=data)
    # Check for errors
    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)

    return resp.json()


def get_uid(api_key):
    firebase_token_and_user_id = get_token_and_user_id_with_pnp_api_key(api_key)
    firebase_user_id = firebase_token_and_user_id["userId"]
    return firebase_user_id


def get_db_client(api_key):
    # print(f"pnplabs api key: {api_key}")

    firebase_token_and_user_id = get_token_and_user_id_with_pnp_api_key(api_key)
    firebase_token = firebase_token_and_user_id["token"]
    firebase_user_id = firebase_token_and_user_id["userId"]
    # print(f"Firebase token: {firebase_token}")
    # print(f"Firebase user id: {firebase_user_id}")

    firebase_sign_in_response = sign_in_with_token(firebase_token)
    firebase_oauth2_token = firebase_sign_in_response['idToken']

    # Use google.oauth2.credentials and the response object to create the correct user credentials
    google_firestore_credentials = Credentials(
            token=firebase_oauth2_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id="105641275062017409334",
    )

    db_client = Client(
        project="pnplabs-be",
        credentials=google_firestore_credentials
    )

    return db_client