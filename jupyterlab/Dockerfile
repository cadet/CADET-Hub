FROM quay.io/jupyter/scipy-notebook:lab-4.5.5

RUN rm -rf ${HOME}/work

# RUN mamba install -c conda-forge "jupyterlab<4" jupyterlab-git jupyter-resource-usage ipywidgets ipykernel
RUN mamba install -n base -c conda-forge \
    jupyter \
    jupyterlab \
    jupytext \
    jupyterlab-myst \
    jupyter-resource-usage \
    ipywidgets \
    ipykernel \
    notebook \
    nbgitpuller \
    nb_conda_kernels -y

RUN jupyter server extension enable nb_conda_kernels
RUN jupyter labextension disable @jupyterlab/git

#####################
# CADET LATEST KERNEL
#####################

# name your environment and choose the python version
ARG cadet_env=CADET_5.1.0
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

RUN "${CONDA_DIR}/envs/${cadet_env}/bin/pip" install --quiet --no-cache-dir "git+https://github.com/fau-advanced-separations/CADET-Process.git@dev"

#####################
# CADET 4.4.0
#####################

# name your environment and choose the python version
ARG old_cadet_env=CADET_4.4.0
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
    numpy \
    matplotlib \
    seaborn \
    pandas \
    scikit-learn \
    xarray -c conda-forge && \
    mamba clean --all -f -y


#USER root
#RUN "${CONDA_DIR}/envs/${planalyze_env}/bin/python" -m ipykernel install --name="${planalyze_env}" --display-name="${planalyze_env}" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#USER ${NB_UID}

RUN "${CONDA_DIR}/envs/${planalyze_env}/bin/pip" install calibr8

# any additional pip installs can be added by uncommenting the following line
# RUN "${CONDA_DIR}/envs/${planalyze_env}/bin/pip" install --quiet --no-cache-dir

# if you want this environment to be the default one, uncomment the following line:
# RUN echo "conda activate ${planalyze_env}" >> "${HOME}/.bashrc"

#USER root

# Ensure jovyan has ownership over the kernels directory
#RUN chown -R ${NB_UID}:users /usr/local/share/jupyter/kernels

# Copy the kernel startup script
#COPY start-kernel.sh /usr/local/bin/start-kernel.sh
#RUN chmod +x /usr/local/bin/start-kernel.sh

# Ensure Jupyter starts using our custom script
#CMD ["start-kernel.sh"]
#USER ${NB_UID}

# Register all Conda envs as Jupyter kernels (system-wide)
#RUN for env in $(ls -d ${CONDA_DIR}/envs/*); do \
#        if [ -d "$env" ]; then \
#            env_name=$(basename "$env"); \
#            "$env/bin/python" -m ipykernel install --prefix="${CONDA_DIR}" --name "$env_name" --display-name "Python ($env_name)"; \
#        fi; \
#    done
