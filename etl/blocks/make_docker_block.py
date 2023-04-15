from prefect.infrastructure.docker import DockerContainer


docker_block = DockerContainer(
    image='kjoconnell/carbon-emissions-analysis-pipeline:v12',
    image_pull_policy='ALWAYS',
    auto_remove=True,
)

docker_block.save('de-zoomcamp-docker', overwrite=True)