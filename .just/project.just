# +---------------------------------------------------------------------------
# : Project specific recipes
# +---------------------------------------------------------------------------
# Build or rebuild services
build *OPTIONS:
    @docker compose build {{OPTIONS}}

# Create and start containers (detached)
up *OPTIONS:
    @docker compose up -d {{OPTIONS}}

# Stop and remove containers, networks
down:
    @docker compose down

# Stop and remove containers, networks, remove orphans and volumes
down-pp:
    @docker compose down --remove-orphans --volumes

# Restart containers
restart: && down up
    echo "Done."

# List containers
ps *OPTIONS:
    @docker compose ps {{OPTIONS}}

# Restart service containers
#restart:
#    @docker compose restart

# Watch build context for service and rebuild/refresh containers when files are updated
watch:
    @docker compose watch

# Execute a COMMAND in CONTAINER container
exec CONTAINER *COMMAND:
    @docker compose exec {{CONTAINER}} {{COMMAND}}

# Launch SHELL in CONTAINER
shell CONTAINER SHELL="bash": 
    @docker compose exec {{CONTAINER}} {{SHELL}}

# Display tdout logs in CONTAINER 
logs CONTAINER:
    @docker compose logs -f -n 40 {{CONTAINER}}

# Clean Bash History file
history-clean CONTAINER:
    @echo -n > ./tmp/{{CONTAINER}}/.bash_history

# Create API project
create_api:
    echo ">>> Project Create <<<"
    ./.just/bin/03_create_empty_project.sh

[private]
@help:
    echo "🛟  Project Help 🛟"
    just --list --list-heading '' --list-prefix "    ↪ " --justfile {{justfile()}}

# Setting up the project
[private]
@setup:
    echo ">>> Project Setup <<<"
    ./bin/00_create_envfile.sh

