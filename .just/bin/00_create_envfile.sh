#!/usr/bin/env bash

PROJECT_ROOT=$(dirname "$(pwd)")

# Create .env file from .env.example
if [ ! -e "${PROJECT_ROOT}/.env" ]; then
    echo ">>> Create .env file"
    cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
fi
# Update .env file with UID/GID of current user
uid=$(id -u)
gid=$(id -g)
sed -i "s/UID=.*/UID=$uid/" "${PROJECT_ROOT}/.env"
sed -i "s/GID=.*/GID=$gid/" "${PROJECT_ROOT}/.env"

# Create temporary folder
FOLDERS_LIST=("server" "db")
for folder in ${FOLDERS_LIST[@]}; do
    mkdir -p "${PROJECT_ROOT}/tmp/${folder}"
    touch "${PROJECT_ROOT}/tmp/${folder}/.bash_history"
    if [ ${folder} == "db" ]; then
        mkdir -p "${PROJECT_ROOT}/tmp/${folder}/data"
    fi
done