# Docker setup for CadetHub

JupyterHub image version: 3.0.0
JupyterLab image version: scipy-notebook:hub-3.0.0  + cadet (conda) + Cadet-Process

## Prerequisites
Ensure that you have `docker` and `docker-compose` and appropriate access to the `docker` group.

# Usage

Rename and copy `jupyterhub_config_template.py` if it doesn't already exist in the `jupyterhub_data` folder: 

```
cp jupyterhub/jupyterhub_config_template.py jupyterhub_data/jupyterhub_config.py
```

## jhub

Now we can run `./jhub --up` to build and start our containers.

The `jhub` script is just a convenience layer on top of docker-compose, with some additional functionality. Run `./jhub -h` for further help.

We may also directly use `docker compose` to do our bidding. 

## Hub Configuration
Configuring the hub involves modifying keys in `jupyterhub_data/jupyterhub_config.py`. Primarily we may be interested in the following: 

```
c.Authenticator.allowed_users    = { 'rao', 'test' }
c.Authenticator.admin_users      = { 'rao' }
c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
c.Spawner.mem_limit              = '10G'
c.Spawner.cpu_limit              = 1
```

The state of the hub is stored in the `jupyterhub_data` folder alongside this config. Deleting data in this folder will affect the state of the hub.

## Container Environments
The hub and user containers are separate. Dockerfiles in the folders `jupyterhub` and `jupyterlab` can be used to update the respective environments.

## User data
User data is stored in docker volumes named `jupyterhub-user-{username}`. You can run `./jhub --backup-user-data` and `./jhub --restore-user-data` as needed. All users work in the `/home/jovyan` directory as per jupyter defaults. Further customization in username is possible, but ultimately unnecessary.

# Design decisions and notes
- [This](https://opendreamkit.org/2018/10/17/jupyterhub-docker/) blog post was used as a guide to setup this repository.
- `jupyterhub_data` is mounted as a local folder instead of a docker volume since this way we can modify the `jupyterhub_config.py` directly within the `jupyterhub_data` folder quite easily and just `docker-compose up` our containers. With docker volumes, the volume would have to be deleted, for a `COPY` statement in the dockerfile to work. This entails losing all the hub databases and state.
- The containerized traefik service was removed since we run an apache server already. Config files are still left in the repository.
- Currently, users have full network access from their notebook environments. If restrictions are to be placed, please see the "Block networking" section in the above blog post.
- If reduction in image sizes is desired, one could use [jupyter/minimal-notebook](https://hub.docker.com/r/jupyter/minimal-notebook/tags/) for the lab environment. For further reduction, we could explore using `nix` to create the images by building a static version of cadet instead of using conda. 

# Issues
- Admin control panel doesn't work the same as TLJH. Quick investigation reveals that this has happened for multiple reasons to other users. Further investigation pending. For now, users can be added manually to the config file and the hub can be restarted.
