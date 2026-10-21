import os
import sys
from pathlib import Path

import yaml

c = get_config()  # type: ignore  # noqa

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = "/lab"

c.JupyterHub.authenticator_class = "firstuseauthenticator.FirstUseAuthenticator"

c.Spawner.mem_limit = "400G"
c.Spawner.cpu_limit = 80

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

# Workshop settings per group (optional `workshop` entry of a project), applied in pre_spawn_hook
workshops = {}

for project_name, project in project_config["projects"].items():
    members = project.get("members") or []
    if "workshop" in project:
        workshops[project_name] = project["workshop"]
        print(f"Group {project_name} is a workshop group: {project['workshop']}")
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
            "--timeout=40000",
        ],
        # "admin": True,
    }
]


def apply_workshop(spawner, group_name, workshop):
    """Set up the server of a workshop participant.

    The teaching and solution branches are cloned on the first start (`workshop-pull` in the
    JupyterLab image), and resources are limited per participant.
    """
    spawner.log.info(f"Workshop {group_name} for user {spawner.user.name}")
    if "repository" in workshop:
        spawner.environment = {
            **spawner.environment,
            "WORKSHOP_REPOSITORY": workshop["repository"],
            "WORKSHOP_BRANCH": workshop.get("branch", ""),
            "WORKSHOP_FOLDER": workshop.get("folder", ""),
            "WORKSHOP_SOLUTION_BRANCH": workshop.get("solution_branch", ""),
            "WORKSHOP_SOLUTION_FOLDER": workshop.get("solution_folder", ""),
        }
    if "image" in workshop:
        spawner.image = workshop["image"]
    if "mem_limit" in workshop:
        spawner.mem_limit = workshop["mem_limit"]
    if "cpu_limit" in workshop:
        spawner.cpu_limit = workshop["cpu_limit"]


def pre_spawn_hook(spawner):
    group_names = {group.name for group in spawner.user.groups}
    if "collaborative" in group_names:
        spawner.log.info(f"Enabling RTC for user {spawner.user.name}")
        spawner.args.append("--LabApp.collaborative=True")

    workshop_groups = sorted(group_names & workshops.keys())
    if len(workshop_groups) > 1:
        spawner.log.warning(
            f"User {spawner.user.name} is in several workshop groups {workshop_groups}; "
            f"using {workshop_groups[0]}"
        )
    if workshop_groups:
        apply_workshop(spawner, workshop_groups[0], workshops[workshop_groups[0]])


c.Spawner.pre_spawn_hook = pre_spawn_hook
