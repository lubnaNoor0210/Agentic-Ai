import base64
import mimetypes

def encode_image_to_base64(path):
    """Reads and encodes an image as a base64 string"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_mime_type(path):
    """Guesses MIME type of the image"""
    return mimetypes.guess_type(path)[0] or "image/png"