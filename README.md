# Docker setup for CadetHub

# Usage

Rename and copy `jupyterhub_config_template.py`: 

```
cp jupyterhub/jupyterhub_config_template.py jupyterhub_data/jupyterhub_config.py
```

Now we can run `./jhub --up` to build and start our containers.

# Design decisions
- The `jupyterhub_data` is mounted as a local folder instead of a docker volume since this way we can modify the `jupyterhub_config.py` directly within the `jupyterhub_data` folder quite easily and just `docker-compose up` our containers. With docker volumes, the volume would have to be deleted, for a `COPY` statement in the dockerfile to work. This entails losing all the hub databases and state.

# Issues
- Admin control panel doesn't work the same as TLJH
