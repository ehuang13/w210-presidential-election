FROM continuumio/miniconda

ENV BK_VERSION=1.4.0
ENV PY_VERSION=3.7
ENV NUM_PROCS=4
ENV BOKEH_RESOURCES=cdn

RUN apt-get install git bash

RUN git clone https://github.com/ehuang13/w210-presidential-election.git
RUN cd harith/sample-bokeh-app
RUN conda install --yes --quiet python=${PY_VERSION} pyyaml jinja2 bokeh=${BK_VERSION} numpy "nodejs>=8.8" pandas requests scikit-learn matplotlib lxml
RUN conda install -c anaconda lxml
RUN conda clean -ay

EXPOSE 8080

CMD bokeh serve --port 8080 \
    harith/harith/sample-bokeh-app/main.py