from flask import Blueprint, request, jsonify
from serving.models.deployment import Deployment
# from serving.kubernetes.get_deployment_list import deployments
from serving.kubernetes.get_deployment_list import update_deployment_list as k8s_update_deployment_list, deployments
from serving.kubernetes.get_deployment_detail import get_deployment_detail as k8s_get_deployment_detail
from serving.kubernetes.create_deployment import create_deployment as k8s_create_deployment
from datetime import datetime

deployment_bp = Blueprint("deployments", __name__)

# 0. Health check
@deployment_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "code": 200,
        "message":"FastServing is running!"}
    )

# 1. List all deployments
@deployment_bp.route("/", methods=["GET"])
def list_deployments():
    deployments = k8s_update_deployment_list()
    print("list_deployments", deployments)
    deployment_list = [{name: details} for name, details in deployments.items()]
    return jsonify(deployment_list), 200


# 2. Create a new deployment
@deployment_bp.route("/create", methods=["POST"])
def create_deployment():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    model_url = data.get("model_url")
    image_url = data.get("image_url")
    port = data.get("port")
    print(f"Creating deployment: {name}, {description}, {model_url}, {image_url}")

    deployments = k8s_update_deployment_list()

    if name in deployments.keys():
        return jsonify({"error": "Deployment with this name already exists"}), 400

    # Create a new deployment
    new_deployment = Deployment(name, description, model_url, image_url)
    new_deployment.created_at = datetime.utcnow()
    # Trigger Kubernetes API call here to create the deployment (K8s integration part)
    k8s_create_deployment(name, image_url, model_url, port)

    return jsonify(new_deployment.__dict__), 201


# 3. Get details of a specific deployment
@deployment_bp.route("/detail/<string:name>", methods=["GET"])
def get_deployment(name):
    deployments = k8s_update_deployment_list()
    print("get_deployment", deployments)
    deployment = deployments.get(name)
    if not deployment:
        return jsonify({"error": "Deployment not found"}), 404
    return jsonify(deployment), 200

@deployment_bp.route("/describe/<string:name>", methods=["GET"])
def get_deployment_describe(name):
    print("get_deployment_describe")
    detail = k8s_get_deployment_detail(name)
    return detail, 200


# 4. Get logs of a deployment
@deployment_bp.route("/<string:name>/logs", methods=["GET"])
def get_deployment_logs(name):
    deployment = deployments.get(name)
    if not deployment:
        return jsonify({"error": "Deployment not found"}), 404

    # Fetch logs from Kubernetes (K8s integration part)
    logs = deployment.log  # Placeholder

    return jsonify({"name": name, "logs": logs}), 200


# 5. Delete a deployment
@deployment_bp.route("/<string:name>", methods=["DELETE"])
def delete_deployment(name):
    if name not in deployments:
        return jsonify({"error": "Deployment not found"}), 404

    # Trigger Kubernetes API call to delete the deployment (K8s integration part)
    del deployments[name]

    return jsonify({"message": "Deployment deleted"}), 200
