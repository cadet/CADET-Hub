FROM jupyter/scipy-notebook:hub-3.0.0

RUN rm -rf ${HOME}/work

RUN mamba install -c conda-forge "jupyterlab<4" jupyterlab-git jupyter-resource-usage ipywidgets ipykernel
RUN mamba install -c conda-forge "cadet=4.4.0"
RUN pip install environment_kernels nbgitpuller

#####################
# CADET LATEST KERNEL
#####################

# name your environment and choose the python version
ARG cadet_env=CADET
ARG cadet_py_ver=3.11

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${cadet_env}" python=${cadet_py_ver} \
    'ipython' \
    'ipykernel' \
    'nb_conda_kernels' \
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

USER root
RUN "${CONDA_DIR}/envs/${cadet_env}/bin/python" -m ipykernel install --name="${cadet_env}" --display-name="${cadet_env}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
USER ${NB_UID}
 
RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir 'CADET-Process==0.9.1'

##################
# PLANALYZE KERNEL
##################

# name your environment and choose the python version
ARG planalyze_env=Planalyze
ARG planalyze_py_ver=3.11

# you can add additional libraries you want mamba to install by listing them below the first line and ending with "&& \"
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/${planalyze_env}" python=${planalyze_py_ver} \
    ipython \
    ipykernel \
    nb_conda_kernels \
    numpy \
    matplotlib \
    seaborn \
    pandas \
    scikit-learn \
    xarray -c conda-forge && \
    mamba clean --all -f -y


USER root
RUN "${CONDA_DIR}/envs/${planalyze_env}/bin/python" -m ipykernel install --name="${planalyze_env}" --display-name="${planalyze_env}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
USER ${NB_UID}

RUN "${CONDA_DIR}/envs/${planalyze_env}/bin/pip" install calibr8
 
# any additional pip installs can be added by uncommenting the following line
# RUN "${CONDA_DIR}/envs/${planalyze_env}/bin/pip" install --quiet --no-cache-dir

# if you want this environment to be the default one, uncomment the following line:
# RUN echo "conda activate ${planalyze_env}" >> "${HOME}/.bashrc"
