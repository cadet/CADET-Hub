FROM jupyter/scipy-notebook:hub-3.0.0

RUN conda install -c conda-forge --quiet --yes \
    'cadet' \
    'rich' && \
    conda clean --all -fy

RUN pip install CADET-Process
