FROM jupyter/scipy-notebook:hub-3.0.0

RUN rm -rf ${HOME}/work

RUN conda install -c conda-forge --quiet --yes \
    'cadet' && \
    conda clean --all -fy

RUN pip install CADET-Process

RUN git clone https://github.com/modsim/CADET-Tutorial
