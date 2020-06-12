FROM continuumio/miniconda

ENV BK_VERSION=1.4.0
ENV PY_VERSION=3.7
ENV NUM_PROCS=4
ENV BOKEH_RESOURCES=cdn

RUN apt-get install git bash

RUN git clone https://github.com/ehuang13/w210-presidential-election.git
RUN cd w210-presidential-election/harith
#RUN cd harith/sample-bokeh-app
RUN conda install --yes --quiet python=${PY_VERSION} pyyaml jinja2 bokeh=${BK_VERSION} numpy "nodejs>=8.8" pandas requests scikit-learn matplotlib lxml
RUN conda install -c anaconda lxml
RUN conda clean -ay

EXPOSE 8080

RUN python -c "import bokeh.sampledata; bokeh.sampledata.download()"
RUN cd w210-presidential-election/harith
CMD bokeh serve --port 8080 w210-presidential-election/harith/sample-bokeh-app
#CMD bokeh serve --port 8080 sample-bokeh-app