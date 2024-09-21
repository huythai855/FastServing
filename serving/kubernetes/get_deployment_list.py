import  subprocess
import os

deployments = {}
kubeconfig_path_global = os.yaml_template_path = os.path.join(os.path.dirname(__file__), '.kubeconfig')

def get_kubectl_deployments(kubeconfig_path=kubeconfig_path_global):
    try:
        apply_command = f"kubectl --kubeconfig {kubeconfig_path}  get deployments"
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

def parse_deployments(output):
    lines = output.strip().split('\n')
    headers = lines[0].split()
    deployments = {}
    for line in lines[1:]:
        values = line.split()
        deployment_name = values[0]
        deployments[deployment_name] = {
            headers[i]: values[i] for i in range(1, len(headers))
        }
    return deployments

def update_deployment_list(kubeconfig_path=kubeconfig_path_global):
    output = get_kubectl_deployments(kubeconfig_path)
    print("Output: ", output)
    if output:
        global deployments
        deployments = parse_deployments(output)
        print("Deployments updated successfully.")
        print(deployments)
        return deployments
    else:
        print("Failed to update deployments.")


# Example usage
# update_deployment_list(kubeconfig_path)