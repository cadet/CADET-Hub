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

# overwriting resource specs for cadet
resource_spec_cadet = {
                'cpu_limit' : int(1 * 1e9), # (int) – CPU limit in units of 10^9 CPU shares.
                'mem_limit' : int(2048 * 1e6), # (int) – Memory limit in Bytes.
                'cpu_reservation' : int(1 * 1e9), # (int) – CPU reservation in units of 10^9 CPU shares.
                'mem_reservation' : int(512 * 1e6), # (int) – Memory reservation in Bytes
                }

c.SwarmSpawner.images = [
    {"image": "ucphhpc/base-notebook:latest", "name": "Python Notebook"},
    {"image": "cadet-test", "name": "Cadet Notebook",
    "resource_spec": resource_spec_cadet}
]

# add user data volume
mounts = [{'type' : 'volume',
        'source' : 'cadethub-user-{username}',
        'target' : '/home/jovyan/work',}]

# mount user data volume by default in all containers
c.SwarmSpawner.container_spec = {
    "mounts": mounts,
}

# default resource specs (can be overwritten by custom image specs)
c.SwarmSpawner.resource_spec = {
                'cpu_limit' : int(1 * 1e9), # (int) – CPU limit in units of 10^9 CPU shares.
                'mem_limit' : int(512 * 1e6), # (int) – Memory limit in Bytes.
                'cpu_reservation' : int(1 * 1e9), # (int) – CPU reservation in units of 10^9 CPU shares.
                'mem_reservation' : int(512 * 1e6), # (int) – Memory reservation in Bytes
                }