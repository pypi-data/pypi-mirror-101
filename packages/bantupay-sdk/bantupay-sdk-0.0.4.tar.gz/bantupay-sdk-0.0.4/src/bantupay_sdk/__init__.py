from stellar_sdk import Keypair, TransactionEnvelope
import json
import base64


def account():
    keypair = Keypair.random()
    return {"secret": keypair.secret, "publicKey": keypair.public_key}


def sign_http(uri, body, secretKey):
    try:
        if not uri:
            raise Exception("uri field is requreid")

        if not secretKey:
            raise Exception("secretKey field is required")

        string_body = body if body else ""

        if body:
            if type(body) is dict:
                string_body = json.dumps(body, separators=(",", ":"))
            else:
                try:
                    string_body = json.loads(body)
                    string_body = json.dumps(string_body, separators=(",", ":"))
                except json.decoder.JSONDecodeError:
                    raise Exception(
                        "Expeting JSON string to be encolosed in double quotes"
                    )

        key_pair = Keypair.from_secret(secretKey)
        data = uri + string_body
        signed_data = key_pair.sign(data.encode())
        signed_data = base64.b64encode(signed_data).decode()
        return signed_data
    except Exception as e:
        return e


def sign_txn(secretKey, transactionXDR, networkPhrase):
    try:
        if not networkPhrase:
            raise Exception("networkPhrase field is required")

        if not transactionXDR:
            raise Exception("transactionXDR field is required")

        if not secretKey:
            raise Exception("secretKey field is required")

        key_pair = Keypair.from_secret(secretKey)
        txn = TransactionEnvelope.from_xdr(transactionXDR, networkPhrase)
        txn_signature = key_pair.sign(txn.hash())
        txn_signature = base64.b64encode(txn_signature).decode()

        return txn_signatur

    except Exception as e:
        return e
