import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    K8S_API_URL = os.environ.get("K8S_API_URL", "http://k8s.api.local")

config = Config()
