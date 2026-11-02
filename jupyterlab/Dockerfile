FROM quay.io/jupyter/scipy-notebook:lab-4.6.4

RUN rm -rf ${HOME}/work

# Frontend extensions pinned to the versions the workshop was tested with; the widget
# frontends (jupyterlab_widgets, anywidget, ipympl) must match the kernel packages below.
RUN mamba install -y -n base -c conda-forge \
    jupyter \
    'jupyterlab=4.6.4' \
    'jupytext=1.19.6' \
    'jupyterlab-myst=2.7.0' \
    'jupyterlab-slideshow=0.3.4' \
    jupyter-resource-usage \
    'ipywidgets=8.1.9' \
    'jupyterlab_widgets=3.0.17' \
    ipykernel \
    notebook \
    nbgitpuller \
    nb_conda_kernels \
    'anywidget=0.11.0' \
    'ipympl=0.10.0' \
    && python -m pip install --no-cache-dir git-credential-helpers

RUN jupyter server extension enable nb_conda_kernels
RUN jupyter labextension disable @jupyterlab/git

# Larger text while presenting with jupyterlab-slideshow. JupyterLab looks for custom.css in
# ~/.jupyter/custom (hidden by the home volume) and in jupyter_server's static/custom.
COPY --chown=${NB_UID}:${NB_GID} custom.css /tmp/custom.css
RUN custom_dir="$(python -c 'import jupyter_server, os; print(os.path.join(os.path.dirname(jupyter_server.__file__), "static", "custom"))')" && \
    mkdir -p "${custom_dir}" && \
    mv /tmp/custom.css "${custom_dir}/custom.css" && \
    printf '%s\n' '{"LabApp": {"custom_css": true}}' > "${CONDA_DIR}/etc/jupyter/jupyter_lab_config.json"

# Workshop groups: clone the workshop repository on the first server start (see projects.yaml).
COPY --chmod=0755 workshop-pull /usr/local/bin/workshop-pull
COPY --chmod=0644 50-workshop-pull.sh /usr/local/bin/before-notebook.d/50-workshop-pull.sh


#####################
# CADET WORKSHOP KERNEL
#####################

# The kernel for the CADET-Workshop notebooks. Exact versions of the workshop's environment.yml
# (https://github.com/cadet/CADET-Workshop), in which all notebooks were tested, so a rebuild does
# not change what participants get. JupyterLab extensions (jupytext, myst, slideshow) are in base.
ARG workshop_env=0_CADET_Workshop
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${workshop_env}" -c conda-forge \
    'python=3.12.15' \
    'cadet=5.1.1' \
    'anywidget=0.11.0' \
    'h5py=3.16.0' \
    'ipykernel=7.4.0' \
    'ipympl=0.10.0' \
    'ipywidgets=8.1.9' \
    'joblib=1.6.0' \
    'matplotlib-base=3.11.2' \
    'numba=0.68.0' \
    'numpy=2.2.6' \
    'openpyxl=3.1.5' \
    'pandas=2.3.3' \
    'pathos=0.3.5' \
    'psutil=7.2.2' \
    'scipy=1.17.1' \
    'traitlets=5.16.1' \
    pip && \
    mamba clean --all -f -y

# CADET-Process: tag workshop-2026 (dev a65245e plus the cyclic fractionation fix, PR #458).
# CADET-GUI: tag workshop-2026 plus following the notebook's light/dark theme.
# Commits instead of tag names, so a moved tag changes nothing.
ARG workshop_cadet_process_ref=758eaebdf09af25358ba198020f8b9c0e7d6619b
ARG workshop_cadet_gui_ref=bb5539ea8610a64d678f6339bc7eb388c637e7a2
RUN "${CONDA_DIR}/envs/${workshop_env}/bin/pip" install --quiet --no-cache-dir \
    "git+https://github.com/fau-advanced-separations/CADET-Process.git@${workshop_cadet_process_ref}" \
    "git+https://github.com/cadet/CADET-GUI.git@${workshop_cadet_gui_ref}" \
    'addict==2.3.0' \
    'CADET-Python==1.3.0' \
    'corner==2.3.0' \
    'hopsy==1.7.0' \
    'pipefunc==0.93.2' \
    'pymoo==0.6.2'


#####################
# CADET LATEST KERNEL
#####################

ARG cadet_env=1_CADET_5.1.1_LATEST
ARG cadet_py_ver=3.12

RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${cadet_env}" python=${cadet_py_ver} \
    'ipython' \
    'ipykernel' \
    'ipympl' \
    'ipywidgets' \
    'imageio'\
    'opencv'\
    'openpyxl' \
    'scipy'\
    'cadet==5.1.1' -c conda-forge && \
    mamba clean --all -f -y

RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@dev"


#####################
# CADET 5.1.0 KERNEL (older workshops)
#####################

ARG cadet_env=3_CADET_5.1.0
ARG cadet_py_ver=3.12

RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${cadet_env}" python=${cadet_py_ver} \
    'ipython' \
    'ipykernel' \
    'ipympl' \
    'ipywidgets' \
    'imageio'\
    'opencv'\
    'openpyxl' \
    'scipy'\
    'cadet==5.1.0' -c conda-forge && \
    mamba clean --all -f -y

RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@7336c1e06f4a4c9efab9a8895025da77c9394694"


#####################
# CADET 4.4.0 KERNEL (older workshops)
#####################

ARG old_cadet_env=4_CADET_4.4.0
ARG old_cadet_py_ver=3.11

RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${old_cadet_env}" python=${old_cadet_py_ver} \
    'ipython' \
    'ipykernel' \
    'cadet==4.4.0' -c conda-forge && \
    mamba clean --all -f -y

RUN "${CONDA_DIR}/envs/${old_cadet_env}/bin/pip" install --quiet --no-cache-dir cadet-python==0.14.1 cadet-process==0.9.1


# Workshop groups: copy the workshop material from the read-only host mount on the first server
# start (see projects.yaml). At the end of the file so changing it does not rebuild the kernels.
COPY --chmod=0755 workshop-material /usr/local/bin/workshop-material
COPY --chmod=0644 55-workshop-material.sh /usr/local/bin/before-notebook.d/55-workshop-material.sh

# Workshop groups: "Update workshop" card in the Launcher, which archives or deletes the workshop
# folders and clones them again (see projects.yaml). JupyterLab is pinned again so the install
# cannot move it.
RUN mamba install -y -n base -c conda-forge \
    'jupyterlab=4.6.4' \
    'jupyter_app_launcher=0.3.2' \
    && mamba clean --all -f -y
COPY --chmod=0755 workshop-update /usr/local/bin/workshop-update
# Without --chmod, which would also apply to the created folder and make the file unreadable
COPY jp_app_launcher_workshop.yml /opt/workshop-launcher/jp_app_launcher_workshop.yml
