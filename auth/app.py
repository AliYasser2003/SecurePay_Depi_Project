import base64
import hashlib
import hmac
import os
import secrets
import threading
import time
from urllib.parse import urlencode

import requests
from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

CLIENT_ID = "2mo4po3b967c65k30ql0dg4c7p"
REGION = "us-east-1"
DOMAIN = "securepay-week2-107759015479"
BASE_URL = f"https://{DOMAIN}.auth.{REGION}.amazoncognito.com"
REDIRECT_URI = "http://localhost:8000/callback"

# Temporary in-memory state for this local demonstration.
PKCE_VERIFIERS = {}
TOKENS = {}


@app.get("/")
def home():
    return """
    <h1>SecurePay Authentication</h1>
    <p><a href="/login">Sign in with Amazon Cognito</a></p>
    """


@app.get("/login")
def login():
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).decode().rstrip("=")

    PKCE_VERIFIERS[state] = verifier

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    return redirect(f"{BASE_URL}/oauth2/authorize?{urlencode(params)}")


@app.get("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"<h1>Authentication failed</h1><p>{error}</p>", 400

    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return "Missing authorization code or state.", 400

    verifier = PKCE_VERIFIERS.pop(state, None)
    if not verifier:
        return "Invalid or expired login state. Please log in again.", 400

    response = requests.post(
        f"{BASE_URL}/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": verifier,
        },
        timeout=15,
    )

    if not response.ok:
        return (
            "<h1>Token exchange failed</h1>"
            f"<pre>{response.status_code}: {response.text}</pre>"
        ), 400

    tokens = response.json()
    TOKENS["access_token"] = tokens.get("access_token")
    TOKENS["id_token"] = tokens.get("id_token")
    print("Access token received:", bool(TOKENS["access_token"]))
    print("ID token received:", bool(TOKENS["id_token"]))
    return """
    <h1>SecurePay Login Successful</h1>
    <p>Amazon Cognito authenticated you and issued tokens.</p>
    <p>For this local demo, tokens are held in server memory.</p>
    <p>Restarting the application clears them.</p>
    """


@app.get("/logout")
def logout():
    TOKENS.clear()
    params = {
        "client_id": CLIENT_ID,
        "logout_uri": "http://localhost:8000/",
    }
    return redirect(f"{BASE_URL}/logout?{urlencode(params)}")

@app.get("/debug/token")
def debug_token():
    if not TOKENS.get("access_token"):
        return {"error": "No access token. Please log in first."}, 401

    return {
        "access_token": TOKENS.get("access_token"),
        "id_token": TOKENS.get("id_token"),
    }


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
