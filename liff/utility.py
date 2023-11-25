from flask import request, abort


def validate_line_signature(func):
    def wrapper(*args, **kwargs):
        # Get the request body
        body = request.get_data(as_text=True)

        # Get the X-Line-Signature header value from the request
        signature = request.headers.get("X-Line-Signature")

        # Validate the signature
        if not is_valid_signature(body, signature):
            print("Invalid signature")
            abort(400, "Invalid signature")

        # Continue processing the webhook event
        return func(*args, **kwargs)

    return wrapper


def is_valid_signature(body, signature):
    import config
    import hashlib
    import hmac
    import base64

    # Convert the Channel Secret to bytes
    channel_secret_bytes = bytes(config.LIFF_CHANEL_SECRET, "utf-8")

    # Compute the HMAC-SHA256 signature of the request body
    body_digest = hmac.new(
        channel_secret_bytes, body.encode("utf-8"), hashlib.sha256
    ).digest()

    # Encode the digest in Base64
    calculated_signature = base64.b64encode(body_digest).decode("utf-8")

    # Compare the calculated signature with the received signature
    return calculated_signature == signature
