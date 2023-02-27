FROM ucphhpc/python-notebook:latest

#RUN rm -rf ${HOME}/work

RUN mamba install -c conda-forge --quiet --yes \
    'cadet' && \
    mamba clean --all -fy

RUN conda run -n python3 pip3 install CADET-Process nbformat CADETMatch

#RUN git clone https://github.com/modsim/CADET-Tutorial

