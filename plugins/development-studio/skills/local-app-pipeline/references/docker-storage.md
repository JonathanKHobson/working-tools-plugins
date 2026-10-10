# Docker Storage

## Expected target

Docker Desktop should keep its disk image under:

`${LOCAL_APP_PIPELINE_DOCKER_STORAGE}`

## Known incomplete state

If Docker still uses:

`~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw`

then the migration is incomplete and the setup should not be described as fully finished.

## Required manual path

`Docker Desktop > Settings > Resources > Advanced > Disk image location > Browse > ${LOCAL_APP_PIPELINE_DOCKER_STORAGE} > Apply & Restart`

## Verification cues

- Docker still launches normally
- `docker run --rm hello-world` succeeds
- the external DockerDesktop directory is populated
- the internal `Docker.raw` is no longer the active storage path
