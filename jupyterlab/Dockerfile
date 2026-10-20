FROM quay.io/jupyter/scipy-notebook:lab-4.6.4

RUN rm -rf ${HOME}/work

# RUN mamba install -c conda-forge "jupyterlab<4" jupyterlab-git jupyter-resource-usage ipywidgets ipykernel
RUN mamba install -y -n base -c conda-forge \
    jupyter \
    'jupyterlab=4.6' \
    jupytext \
    jupyterlab-myst \
    jupyterlab-slideshow \
    jupyter-resource-usage \
    ipywidgets \
    ipykernel \
    notebook \
    nbgitpuller \
    nb_conda_kernels \
    anywidget \
    ipympl \
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

# Pinned to the commits of the CADET-Workshop environment.yml.
ARG cadet_process_ref=a65245e3c0cae8d885a805162fc6ee21201f6eca
ARG cadet_gui_ref=289901c3993487d654c9223017315c01a54d1093
RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@${cadet_process_ref}"
RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/cadet/CADET-GUI.git@${cadet_gui_ref}"


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

