FROM quay.io/jupyter/scipy-notebook:lab-4.5.5

RUN rm -rf ${HOME}/work

# RUN mamba install -c conda-forge "jupyterlab<4" jupyterlab-git jupyter-resource-usage ipywidgets ipykernel
RUN mamba install -y -n base -c conda-forge \
    jupyter \
    jupyterlab \
    jupytext \
    jupyterlab-myst \
    jupyter-resource-usage \
    ipywidgets \
    ipykernel \
    notebook \
    nbgitpuller \
    nb_conda_kernels \
    anywidget \
    && python -m pip install --no-cache-dir git-credential-helpers

RUN jupyter server extension enable nb_conda_kernels
RUN jupyter labextension disable @jupyterlab/git


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

