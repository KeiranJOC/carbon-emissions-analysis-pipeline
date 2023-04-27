deploy_infrastructure:
	terraform -chdir=terraform apply

deploy_docker: deploy_infrastructure
	docker build -t "${GCP_CONTAINER_REPOSITORY_ADDRESS}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}" .
	docker push ${GCP_CONTAINER_REPOSITORY_ADDRESS}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}

create_blocks: deploy_docker
	python blocks/create_blocks.py

deploy_flows: create_blocks deploy_docker
	python deploy_flows.py

launch_agent: deploy_flows
	prefect agent start -q ${PREFECT_WORK_QUEUE_NAME}

setup: launch_agent