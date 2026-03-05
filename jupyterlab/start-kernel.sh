#!/bin/bash

echo "Detecting installed Jupyter kernels in /usr/local/share/jupyter/kernels/..."

# Ensure NB_UID can modify kernel.json
chown -R ${NB_UID}:users /usr/local/share/jupyter/kernels/

# Loop through all system-wide kernels
for KERNEL_DIR in /usr/local/share/jupyter/kernels/*; do
    if [ -d "$KERNEL_DIR" ]; then
        KERNEL_NAME=$(basename "$KERNEL_DIR")
        KERNEL_JSON="$KERNEL_DIR/kernel.json"

        echo "Processing kernel: $KERNEL_NAME"

        # Convert kernel name to match Conda environment name (Handle uppercase names)
        MATCHING_ENV=$(conda env list | awk '{print $1}' | grep -i "^$KERNEL_NAME$")

        if [ -z "$MATCHING_ENV" ]; then
            echo "Warning: No matching Conda environment found for kernel $KERNEL_NAME"
            continue
        fi

        ENV_PATH="/opt/conda/envs/$MATCHING_ENV/bin"

        if [ -f "$KERNEL_JSON" ]; then
            echo "Updating $KERNEL_JSON with Conda environment variables"

            # Ensure file is writable by NB_UID
            chmod 666 "$KERNEL_JSON"

            # Use jq to inject the correct Conda variables
            jq --arg path "$ENV_PATH:$PATH" \
               --arg env "$MATCHING_ENV" \
               --arg prefix "/opt/conda/envs/$MATCHING_ENV" \
               '.env |= . + {"PATH": $path, "CONDA_DEFAULT_ENV": $env, "CONDA_PREFIX": $prefix}' "$KERNEL_JSON" > temp.json

            # Move the modified file safely
            mv temp.json "$KERNEL_JSON"

            # Debugging: Show modified kernel.json
            cat "$KERNEL_JSON"
        else
            echo "Warning: No kernel.json found in $KERNEL_DIR"
        fi
    fi
done

# Ensure Conda environment activation before Jupyter starts
export CONDA_DEFAULT_ENV=$MATCHING_ENV
export CONDA_PREFIX="/opt/conda/envs/$MATCHING_ENV"
export PATH="/opt/conda/envs/$MATCHING_ENV/bin:$PATH"

echo "Using Conda environment: $CONDA_DEFAULT_ENV"

echo "Stopping any existing Jupyter processes..."
pkill -9 jupyter || true

echo "Restarting Jupyter Notebook..."
exec start-notebook.sh

