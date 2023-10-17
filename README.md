# Docker-based JupyterHub
IBG-1's JupyterHub is a multi-user Hub that spawns and manages JupyterLab instances within Docker containers, allowing the deployment of personalized programming environments.
IBG-1's JupyterHub is currently deployed on machine `IBT012`.
It can be accessed via `jupyter2.cadet-web.de` and `ibt012.ibt.kfa-juelich.de:8082` (from within the FZJ network)

## Prerequisites for setup
JupyterHub and the JupyterLab instances that it spawns are deployed as Docker applications.
The ability to perform `docker-compose` and access to the `docker` group are prerequisites to deploying JupyterHub.
This is easily achieved by following these steps:

1. Login to `IBT012`
2. Switch to user `jupyterhub`
   ```
   sudu su jupyterhub
   ```
3. Start or stop `jupyterhub_hub` container with `jhub`

## jhub
The `jhub` script is just a convenience layer on top of docker-compose, with additional functionality. Run `./jhub --help` for further help.

__To build and start our containers, run__
```
./jhub --up
```
__If you want to build a new image without using cache, run__
```
./jhub --build
```
__To shut down JupyterHub (e.g., for maintenance, updates), run__
```
./jhub --down
```
__Additional available flags are__
```
--nuke-user-data # Remove all user data volumes
--backup-user-data # Backup all user data from home folder
--restore-user.data # Restore all user data from home folder
```
An abrupt alternative to `./jhub --down` is `docker kill jupyterhub_hub`.
After this command `./jhub --up` may blocked because the proxy is still running. To fix this, remove `jupyterhub_data/jupyterhub-proxy.pid`.

# Configuring the settings
__The current implementation of JupyterHub was adapted from [this opendreamkit blog post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/).__ It is helpful; feel free to refer to it or the [JupyterHub documentation](https://jupyterhub.readthedocs.io/en/stable/tutorial/index.html) regarding all modification considerations.

The hub and the user containers are separate. Dockerfiles in the directories `jupyterhub`and `jupyterlab` can be used to update the respective environments.

## Configuring the Hub

Configuring the hub involves modifying keys in `jupyterhub_data/jupyterhub_config.py`.
Primarily, we may be interested in the following:
```
# ATTENTION, ALLOWED_USERS & ADMINS ARE NO DEFINED IN A SEPARATE YAML FILE (jupyterhub_data/projects.yaml)
# SEE ACCOUNTS & PERMISSIONS

c.Authenticator.allowed_users    = { 'rao', 'test' }
c.Authenticator.admin_users      = { 'rao' }
c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
c.Spawner.mem_limit              = '10G'
c.Spawner.cpu_limit              = 1
```
#### Accounts & Permissions
We opted to utilize a yaml file to maintain a more structed overview of users, group affiliations (important for real-time collaboration) and admin permissions. The respective `projects.yaml` file is located in the `jupyterhub_data` directory.

The `projects.yaml` however, is not a single source of truth once the hub is deployed. Users with admin privileges may utilize the admin panel to add user accounts and manage group affiliations.

The state ([database of user accounts etc.](https://jupyterhub.readthedocs.io/en/stable/explanation/database.html#default-backend-sqlite)) of the hub is stored in the `jupyterhub_data` folder alongside the `jupyterhub_config`. Deleting data in this folder will affect the state of the hub.

#### User data
User data is stored in docker volumes named `jupyterhub-user-{username}`. You can run `./jhub --backup-user-data` and `./jhub --restore-user-data` as needed. All users work in the `/home/jovyan` directory as per jupyter defaults. Further customization in username is possible but ultimately unnecessary.

Since user data is stored in docker volumes, the data will persist even if respective user account are deleted. To delete user data the docker volumes have to be removed separately.
```
docker volume ls
docker volume rm <volume_name>
```

#### Computational resources
The allocated memory and CPU for every user are set in the `jupyterhub_config.py`.
```
c.Spawner.mem_limit              = '10G'
c.Spawner.cpu_limit              = 1
```
With this example, we would allow up to 10 GB of RAM and 1 CPU core per user. These settings should be considered wisely.
Keep in mind:
> When tasks don’t get enough CPU, things are slow. When they don’t get enough memory, things are broken.

For considerations regarding capacity planning, refer to [this article](https://jupyterhub.readthedocs.io/en/stable/explanation/capacity-planning.html).

### Real-Time Collaboration
Design decisions regarding real-time collaboration in JupyterHub were informed by the [JupyterHub documentation](https://jupyterhub.readthedocs.io/en/stable/tutorial/collaboration-users.html).

Real-time collaboration is realized with shared, dedicated collaboration accounts. These collaboration accounts are automatically generated for every group defined in the `projects.yaml` ending with the suffix "collab".
Alternatively, accounts can be added to the `collaborative` group via the admin panel.

This current version of real-time collaboration requires password sharing. Of course, this is not acceptable for all users. In these cases, one will have to make do with screen sharing.


## Configuring JupyterLab

To modify the notebook environments the users interact with, one must change the JupyterLab Dockerfile in the jupyterlab directory. To avoid a previously described situation as ***dependency hell***, we opted to provide dedicated kernels for our software libraries.

* CADET & CADET-Process
* Planalyze

This Dockerfile example can be used as a template to generate further kernels and/or add additional dependecies.

>__NOTE:__ It is best practise to pin the desired versions of the referenced packages in your Dockerfile. This way you will not be suprised by breaking changes!

```
# name kernel/environment & choose python version
ARG env_name = KERNEL_NAME
ARG py_ver = 3.10

# conda/mamba installs
RUN mamba create --quiet --yes -p "{CONDA_DIR}/envs/${env_name}" python=${py_ver} \
    'ipython' \
    'matplotlib' \
    'cadet>=4.3.0' -c conda-forge && \
    mamba clean --all -f -y

# pip installs
USER root
RUN "${CONDA_DIR}/envs/${env_name}/bin/python" -m ipykernel install --name=${env_name}" --display-name=${env_name}" && \
    fix-permissions "${env_name}" && \
    fix-permissions "/home/${NB_USER}"
USER ${NB_UID}

RUN "{CONDA_DIR}/envs/${env_name}/bin/pip" install --quiet --no-cache-dir \
    'CADET-Process'

```

### JupyterLab Extensions
The following JupyterLab extensions are installed:
+ jupyterlab-git
+ nbgitpuller
+ jupyter-resource-usage

Additional extensions can be installed via the Dockerfile.

# Design decisions and notes

- `jupyterhub_data` is mounted as a local folder instead of a docker volume since this way, we can modify the `jupyterhub_config.py` directly within the `jupyterhub_data` folder quite quickly and just `docker-compose up` our containers. With docker volumes, the volume would have to be deleted for a `COPY` statement in the dockerfile to work. This entails losing all the hub databases and states.
- The containerized traefik service was removed since we run an apache server already. Config files are still left in the repository.
- Currently, users have full network access from their notebook environments. If restrictions are to be placed, please see the "Block networking" section in the above blog post.
- If a reduction in image sizes is desired, one could use [jupyter/minimal-notebook](https://hub.docker.com/r/jupyter/minimal-notebook/tags/) for the lab environment.
