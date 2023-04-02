from prefect.deployments import Deployment
from load_data import load_data_parent_flow
from prefect.infrastructure.docker import DockerContainer


docker_container_block = DockerContainer.load('de-zoomcamp-docker')

docker_deployment = Deployment.build_from_flow(
    flow=load_data_parent_flow,
    name='docker-flow',
    infrastructure=docker_container_block,
)


if __name__ == '__main__':
    docker_deployment.apply()