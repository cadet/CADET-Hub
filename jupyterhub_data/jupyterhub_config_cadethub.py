# Configuration file for jupyterhub.
import os

c = get_config()

c.JupyterHub.spawner_class = "jhub.SwarmSpawner"

c.JupyterHub.authenticator_class = "jhubauthenticators.DummyAuthenticator"
c.DummyAuthenticator.password = "password"

c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.hub_ip = "0.0.0.0"

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 5
c.SwarmSpawner.http_timeout = 60 * 1

c.SwarmSpawner.notebook_dir = "~/work"
c.SwarmSpawner.jupyterhub_service_name = "jupyterhub"
c.SwarmSpawner.networks = ["cadethub_default"]

c.SwarmSpawner.use_user_options = True

# always stop spawned server to prevent ghost servers
c.JupyterHub.cleanup_servers = True

c.SwarmSpawner.images = [
    {"image": "ucphhpc/base-notebook:latest", "name": "Python Notebook"},
    {"image": "cadet-test", "name": "Cadet Notebook"}
]

# add user data volume
mounts = [{'type' : 'volume',
        'source' : 'cadethub-user-{username}',
        'target' : '/home/jovyan/work',}]

# mount user data volume by default in all containers
c.SwarmSpawner.container_spec = {
    "mounts": mounts,
}
