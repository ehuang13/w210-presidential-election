## prereqs

1. `pip install bokeh --user`
2. download sample data: `python -c "import bokeh.sampledata; bokeh.sampledata.download()"`
3. update value of environment variable `BOKEH_ALLOW_WS_ORIGIN` in app.yaml to your app-engine hostname. 

## how to run
go to directory `harith` and run: `bokeh serve sample-bokeh-app --show`
