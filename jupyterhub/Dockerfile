# Do not forget to pin down the version
FROM jupyterhub/jupyterhub:4.0
# Install dependencies (for advanced authentication and spawning)
RUN pip install \
    pyyaml \
    dockerspawner==12.1.0 \
    oauthenticator==15.1.0 \
    jupyterhub-idle-culler==1.2.1 \
    jupyterhub-firstuseauthenticator==1.0.0
