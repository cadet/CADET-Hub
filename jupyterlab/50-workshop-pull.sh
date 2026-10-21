# Sourced by the docker-stacks start script before JupyterLab starts.
# A failed clone must not prevent the server from starting, so only report it.
/usr/local/bin/workshop-pull || echo "workshop-pull: cloning the workshop repository failed; use the nbgitpuller link instead."
