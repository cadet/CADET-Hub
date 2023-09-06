import os
import sys
import yaml
from jupyterhub.auth import DummyAuthenticator
from pathlib import Path

c = get_config()

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

c.Authenticator.allowed_users = { 'rao', 'siska', 'test', 'lion', 'seal'}
c.Authenticator.admin_users = { 'rao', 'siska' }

c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
# c.JupyterHub.authenticator_class = DummyAuthenticator

c.Spawner.mem_limit = '10G'
c.Spawner.cpu_limit = 1

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

c.JupyterHub.hub_ip          = os.environ['HUB_IP']
c.DockerSpawner.image        = os.environ['DOCKER_JUPYTER_IMAGE']
# c.DockerSpawner.image_whitelist        = { 
#                                           'CADET-4.3.0': 'cadetlab_img', 
#                                           'Minimal': 'jupyter/minimal-notebook',
#                                           'Base': 'jupyter/base-notebook'
#                                           }
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']

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

c.JupyterHub.load_groups ={
    # collaborative accounts
    "collaborative": [],
}

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
    },
]

projects_yaml = Path(__file__).parent.resolve().joinpath("projects.yaml")
with projects_yaml.open() as f:
    project_config = yaml.safe_load(f)

for project_name, project in project_config["projects"].items():
    members = project.get("members", [])
    print(f"Adding project {project_name} with members {members}")
    c.JupyterHub.load_groups[project_name] = members
    collab_user = f"{project_name}-collab"
    c.Authenticator.allowed_users.append(
        {"collab_user"}
    )
    c.JupyterHub.load_groups["collaborative"].append(collab_user)
    c.JupyterHub.load_roles.append(
        {
            "name": f"collab-access-{project_name}",
            "scopes": [
                "admin-ui",
                f"admin:servers!user={collab_user}",
                f"list:users!user={collab_user}",
                f"access:servers!user={collab_user}",
            ],
            "groups": [project_name],
        }
    )

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

def pre_spawn_hook(spawner):
    group_names = {group.name for group in spawner.user.groups}
    if "collaborative" in group_names:
        spawner.log.info(f"Enabling RTC for user {spawner.user.name}")
        spawner.args.append("--LabApp.collaborative=True")


c.Spawner.pre_spawn_hook = pre_spawn_hook