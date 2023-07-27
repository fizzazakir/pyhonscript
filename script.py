
# deployment_automation.py

import os
import time
from kubernetes import client, config, utils

def deploy_microservice(service_name, image, replicas, namespace):
    # Load Kubernetes configuration from the default location
    config.load_kube_config()

    # Initialize Kubernetes API client
    api_instance = client.AppsV1Api()

    # Define the deployment spec
    deployment_spec = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=service_name, namespace=namespace),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels={'app': service_name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={'app': service_name}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=service_name,
                            image=image,
                            ports=[client.V1ContainerPort(container_port=80)],
                            # Add more container configurations as needed
                        )
                    ]
                )
            )
        )
    )

    try:
        # Create or update the deployment
        api_instance.create_namespaced_deployment(namespace=namespace, body=deployment_spec)

        # Wait for the deployment to be ready
        while True:
            deployment_status = api_instance.read_namespaced_deployment_status(service_name, namespace)
            if deployment_status.status.available_replicas == replicas:
                print(f"{service_name} deployment is ready with {replicas} replicas.")
                break
            time.sleep(5)

    except Exception as e:
        print(f"Error deploying {service_name}: {e}")

if __name__ == "__main__":
    # Example usage
    service_name = "webapp"
    image = "your-registry/your-webapp-image:latest"
    replicas = 3
    namespace = "default"

    deploy_microservice(service_name, image, replicas, namespace)
