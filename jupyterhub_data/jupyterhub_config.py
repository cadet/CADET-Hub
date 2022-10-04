import os
import sys
from jupyterhub.auth import DummyAuthenticator

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

c.Authenticator.allowed_users = { 'rao', 'test' }
c.Authenticator.admin_users = { 'rao' }

c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'

c.Spawner.mem_limit = '10G'
c.Spawner.cpu_limit = 1

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

c.JupyterHub.hub_ip          = os.environ['HUB_IP']
c.DockerSpawner.image        = os.environ['DOCKER_JUPYTER_IMAGE']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}

# Delete containers when servers are stopped.
c.DockerSpawner.remove = True

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
NOTEBOOK_DIR = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = NOTEBOOK_DIR

# # Mount the real user's Docker volume on the host to the notebook user's
# # notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': NOTEBOOK_DIR }


c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
        # "admin": True,
    }
]
