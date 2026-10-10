# Commands

## Start the local stack

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/start-dev.sh
```

## Check ports

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/check-ports.sh
```

## Start a Quick Tunnel

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/start-tunnel.sh
```

## Stop PocketBase

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && docker compose down
```

## Watch PocketBase logs

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && docker compose logs -f pocketbase
```

## Create the first PocketBase superuser

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && docker compose exec pocketbase /pocketbase/pocketbase superuser create you@example.com your-password
```

## Verify Docker itself

```bash
PATH='/Applications/Docker.app/Contents/Resources/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin' docker run --rm hello-world
```

## Verify the local skill install

```bash
ls -ld '${DEVELOPMENT_STUDIO_ROOT}/skills/local-app-pipeline'
```

## Validate the skill

```bash
python3 '${SKILL_VALIDATOR}' '${LOCAL_APP_PIPELINE_ROOT}/skill/local-app-pipeline'
```

## Run the skill verification helper

```bash
'${LOCAL_APP_PIPELINE_ROOT}/skill/local-app-pipeline/scripts/verify-local-app-pipeline.sh'
```
