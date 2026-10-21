FROM quay.io/jupyter/scipy-notebook:lab-4.6.4

RUN rm -rf ${HOME}/work

# RUN mamba install -c conda-forge "jupyterlab<4" jupyterlab-git jupyter-resource-usage ipywidgets ipykernel
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
# CADET-GUI: tag workshop-2026. Commits instead of tag names, so a moved tag changes nothing.
ARG workshop_cadet_process_ref=758eaebdf09af25358ba198020f8b9c0e7d6619b
ARG workshop_cadet_gui_ref=289901c3993487d654c9223017315c01a54d1093
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

# name your environment and choose the python version
ARG cadet_env=1_CADET_5.1.1_LATEST
ARG cadet_py_ver=3.12

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
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

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml "/home/${NB_USER}/tmp/"
# RUN cd "/home/${NB_USER}/tmp/" && \
#     mamba env create -p "${CONDA_DIR}/envs/${planalyze_env}" -f environment.yml && \
#     mamba clean --all -f -y

# create Python kernel and link it to jupyter
# NOTE: Contrary to popular instruction, we do not install it as --user since we use containers and our home directory is a docker volume.

#USER root
#RUN "${CONDA_DIR}/envs/${cadet_env}/bin/python" -m ipykernel install --name="${cadet_env}" --display-name="${cadet_env}" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#USER ${NB_UID}

RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@dev"


#####################
# CADET GUI KERNEL
#####################

# name your environment and choose the python version
ARG cadet_env=2_CADET_GUI
ARG cadet_py_ver=3.12

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${cadet_env}" python=${cadet_py_ver} \
    'ipython' \
    'ipykernel' \
    'ipympl' \
    'ipywidgets' \
    'imageio'\
    'opencv'\
    'openpyxl'\
    'scipy'\
    'anywidget'\
    'cadet==5.1.1' -c conda-forge && \
    mamba clean --all -f -y

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml "/home/${NB_USER}/tmp/"
# RUN cd "/home/${NB_USER}/tmp/" && \
#     mamba env create -p "${CONDA_DIR}/envs/${planalyze_env}" -f environment.yml && \
#     mamba clean --all -f -y

# create Python kernel and link it to jupyter
# NOTE: Contrary to popular instruction, we do not install it as --user since we use containers and our home directory is a docker volume.

#USER root
#RUN "${CONDA_DIR}/envs/${cadet_env}/bin/python" -m ipykernel install --name="${cadet_env}" --display-name="${cadet_env}" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#USER ${NB_UID}

# Current development versions for working with the GUI; the workshop has its own kernel above.
RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@dev"
RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/cadet/CADET-GUI.git@main"


#####################
# CADET WS 25 Kernel
#####################

# name your environment and choose the python version
ARG cadet_env=3_CADET_5.1.0
ARG cadet_py_ver=3.12

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
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

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml "/home/${NB_USER}/tmp/"
# RUN cd "/home/${NB_USER}/tmp/" && \
#     mamba env create -p "${CONDA_DIR}/envs/${planalyze_env}" -f environment.yml && \
#     mamba clean --all -f -y

# create Python kernel and link it to jupyter
# NOTE: Contrary to popular instruction, we do not install it as --user since we use containers and our home directory is a docker volume.

#USER root
#RUN "${CONDA_DIR}/envs/${cadet_env}/bin/python" -m ipykernel install --name="${cadet_env}" --display-name="${cadet_env}" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#USER ${NB_UID}

RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@7336c1e06f4a4c9efab9a8895025da77c9394694"


#####################
# CADET 4.4.0
#####################

# name your environment and choose the python version
ARG old_cadet_env=4_CADET_4.4.0
ARG old_cadet_py_ver=3.11

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${old_cadet_env}" python=${old_cadet_py_ver} \
    'ipython' \
    'ipykernel' \
    'cadet==4.4.0' -c conda-forge && \
    mamba clean --all -f -y

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml "/home/${NB_USER}/tmp/"
# RUN cd "/home/${NB_USER}/tmp/" && \
#     mamba env create -p "${CONDA_DIR}/envs/${planalyze_env}" -f environment.yml && \
#     mamba clean --all -f -y

# create Python kernel and link it to jupyter
# NOTE: Contrary to popular instruction, we do not install it as --user since we use containers and our home directory is a docker volume.

#USER root
#RUN "${CONDA_DIR}/envs/${old_cadet_env}/bin/python" -m ipykernel install --name="${old_cadet_env}" --display-name="${old_cadet_env}" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#USER ${NB_UID}

RUN "${CONDA_DIR}/envs/${old_cadet_env}/bin/pip" install --quiet --no-cache-dir cadet-python==0.14.1 cadet-process==0.9.1

