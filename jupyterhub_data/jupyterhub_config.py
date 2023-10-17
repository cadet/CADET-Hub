import os
import sys
from pathlib import Path

import yaml

c = get_config()  # type: ignore  # noqa

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = "/lab"

c.JupyterHub.authenticator_class = "firstuseauthenticator.FirstUseAuthenticator"

c.Spawner.mem_limit = "30G"
c.Spawner.cpu_limit = 4

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

c.JupyterHub.hub_ip = os.environ["HUB_IP"]
c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_IMAGE"]
# c.DockerSpawner.image_whitelist        = {
#                                           'CADET-4.3.0': 'cadetlab_img',
#                                           'Minimal': 'jupyter/minimal-notebook',
#                                           'Base': 'jupyter/base-notebook'
#                                           }
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]

# Delete containers when servers are stopped.
c.DockerSpawner.remove = True

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
NOTEBOOK_DIR = os.environ.get("DOCKER_NOTEBOOK_DIR") or "/home/jovyan"
c.DockerSpawner.notebook_dir = NOTEBOOK_DIR

# # Mount the real user's Docker volume on the host to the notebook user's
# # notebook directory in the container
c.DockerSpawner.volumes = {
    "jupyterhub-user-{username}": NOTEBOOK_DIR,
    "/opt/cadet/": {"bind": "/opt/cadet", "mode": "ro"},
}

c.JupyterHub.load_groups = {
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
print("Loading users and groups from yaml file.")

admin_users = project_config["projects"]["admin"]["members"]
c.Authenticator.admin_users.update(admin_users)
print("Add users with admin privilege.")

for project_name, project in project_config["projects"].items():
    members = project.get("members", [])
    c.Authenticator.allowed_users.update(members)
    print(f"Adding {project_name} members: {members} to the list to allowed users.")
    c.JupyterHub.load_groups[project_name] = members
    print(f"Create group {project_name} and assign {members}")
    if project_name.endswith(("collab", "collaboration")):
        collab_user = f"{project_name}-user"
        c.Authenticator.allowed_users.add(collab_user)
        print(f"Adding a RTC user for project {project_name} to the list of allowed users.")
        c.JupyterHub.load_groups["collaborative"].append(collab_user)
        c.JupyterHub.load_roles.append(
            {
                "name": f"rtc-{project_name}",
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
            "-m",
            "jupyterhub_idle_culler",
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
