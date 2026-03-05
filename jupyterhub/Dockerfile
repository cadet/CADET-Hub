# Pin to an explicit Hub build tag (or use a digest)
FROM jupyterhub/jupyterhub:5.4.3-8

# Pin deps for reproducibility
RUN pip install --no-cache-dir --upgrade \
    pyyaml \
    dockerspawner==14.0.0 \
    oauthenticator==17.3.0 \
    jupyterhub-idle-culler==1.4.0 \
    jupyterhub-firstuseauthenticator==1.1.1
