import pickle
import base64


def serialize(obj) -> str:
    """Serialize an object to a base64-encoded pickle string."""
    return base64.b64encode(pickle.dumps(obj)).decode()


def deserialize(data: str):
    """Deserialize a base64-encoded pickle string back to an object."""
    decoded = base64.b64decode(data)
    return pickle.loads(decoded)
