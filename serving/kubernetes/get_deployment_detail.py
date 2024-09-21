import  subprocess
import os
import re
import json

deployments = {}
kubeconfig_path_global = os.yaml_template_path = os.path.join(os.path.dirname(__file__), '.kubeconfig')

def get_kubectl_deployments_detail(kubeconfig_path=kubeconfig_path_global, deployment_name=None):
    try:
        apply_command = f"kubectl --kubeconfig {kubeconfig_path}  describe deployment {deployment_name}"
        print(apply_command)
        result = subprocess.run(
            apply_command,
            shell=True,
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running kubectl: {e}")
        return None




def parse_deployment_info(deployment_str):
    # Tách các dòng từ chuỗi
    lines = deployment_str.split("\n")
    print("Lines: ", lines)
    print("Line length", len(lines))

    for line in lines:
        print(line)

    # Dictionary để chứa dữ liệu được phân tích
    deployment_data = {}

    # Hàm tiện ích để loại bỏ tiền tố và lấy giá trị
    def extract_value(line, delimiter=":"):
        return line.split(delimiter, 1)[-1].strip()

    # Bắt đầu phân tích từng dòng
    for line in lines:
        if line.startswith("Name:"):
            deployment_data["name"] = extract_value(line)
        elif line.startswith("Namespace:"):
            deployment_data["namespace"] = extract_value(line)
        elif line.startswith("CreationTimestamp:"):
            deployment_data["creation_timestamp"] = extract_value(line)
        elif line.startswith("Labels:"):
            deployment_data["labels"] = extract_value(line)
        elif line.startswith("Annotations:"):
            deployment_data["annotations"] = extract_value(line)
        elif line.startswith("Selector:"):
            deployment_data["selector"] = extract_value(line)
        elif line.startswith("Replicas:"):
            deployment_data["replicas"] = extract_value(line)
        elif line.startswith("StrategyType:"):
            deployment_data["strategy_type"] = extract_value(line)
        elif line.startswith("MinReadySeconds:"):
            deployment_data["min_ready_seconds"] = extract_value(line)
        elif line.startswith("RollingUpdateStrategy:"):
            deployment_data["rolling_update_strategy"] = extract_value(line)
        elif line.startswith("Pod Template:"):
            # Parse Pod Template section
            deployment_data["pod_template"] = {}
        elif line.strip().startswith("Labels:") and "pod_template" in deployment_data:
            deployment_data["pod_template"]["labels"] = extract_value(line)
        elif line.strip().startswith("Containers:"):
            deployment_data["pod_template"]["containers"] = {}
        elif line.strip().startswith("new-rain:") and "containers" in deployment_data["pod_template"]:
            container_name = extract_value(line, delimiter=":").strip()
            deployment_data["pod_template"]["containers"]["name"] = container_name
        elif line.strip().startswith("Image:") and "containers" in deployment_data["pod_template"]:
            deployment_data["pod_template"]["containers"]["image"] = extract_value(line)
        elif line.strip().startswith("Port:") and "containers" in deployment_data["pod_template"]:
            deployment_data["pod_template"]["containers"]["port"] = extract_value(line)
        elif line.strip().startswith("Host Port:") and "containers" in deployment_data["pod_template"]:
            deployment_data["pod_template"]["containers"]["host_port"] = extract_value(line)
        elif line.strip().startswith("Liveness:") and "containers" in deployment_data["pod_template"]:
            deployment_data["pod_template"]["containers"]["liveness_probe"] = extract_value(line)
        elif line.strip().startswith("Readiness:") and "containers" in deployment_data["pod_template"]:
            deployment_data["pod_template"]["containers"]["readiness_probe"] = extract_value(line)
        elif line.strip().startswith("Mounts:") and "containers" in deployment_data["pod_template"]:
            deployment_data["pod_template"]["containers"]["mounts"] = extract_value(line)
        elif line.startswith("Volumes:"):
            deployment_data["volumes"] = {}
        # elif line.strip().startswith("model-volume:"):
        #     deployment_data["volumes"]["name"] = extract_value(line, delimiter=":")
        # elif line.strip().startswith("Type:") and "volumes" in deployment_data:
        #     deployment_data["volumes"]["type"] = extract_value(line)
        # elif line.strip().startswith("SizeLimit:") and "volumes" in deployment_data:
        #     deployment_data["volumes"]["size_limit"] = extract_value(line)
        elif line.startswith("Node-Selectors:"):
            deployment_data["node_selectors"] = extract_value(line)
        elif line.startswith("Tolerations:"):
            deployment_data["tolerations"] = extract_value(line)
        elif line.startswith("Conditions:"):
            deployment_data["conditions"] = []
        elif line.strip().startswith("Type"):
            continue  # Bỏ qua tiêu đề của bảng conditions
        elif re.match(r"^\s+\w+", line):  # Condition dòng dữ liệu
            condition_data = line.strip().split()
            if len(condition_data) == 3:
                deployment_data["conditions"].append({
                    "type": condition_data[0],
                    "status": condition_data[1],
                    "reason": condition_data[2]
                })
        elif line.startswith("OldReplicaSets:"):
            deployment_data["old_replica_sets"] = extract_value(line)
        elif line.startswith("NewReplicaSet:"):
            deployment_data["new_replica_set"] = extract_value(line)
        elif line.startswith("Events:"):
            deployment_data["events"] = extract_value(line)

    print(deployment_data)
    print(json.dumps(deployment_data, indent=4))
    return json.dumps(deployment_data, indent=4)



def get_deployment_detail(deployment_name):
    detail = get_kubectl_deployments_detail(kubeconfig_path_global, deployment_name)
    return parse_deployment_info(detail)
    # return get_kubectl_deployments_detail(kubeconfig_path_global, deployment_name)