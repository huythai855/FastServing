from keras.src.legacy.backend import update
import subprocess

class Deployment:
    def __init__(self, name, description, model_url, image_url, status="pending"):
        self.name = name
        self.description = description
        self.model_url = model_url
        self.image_url = image_url
        self.status = status
        self.log = ""
        self.created_at = None