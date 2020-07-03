# imports

import json
import sys

from bokeh.embed import components

import electmap as emap
import twtanalysis as twt


# starting Flask app
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def chart():
    #print("hello there", file=sys.stderr)
    plot = emap.create_chart()
    script, div = components(plot)

    #twtplot_ey = twt.get_candidate_election_yearmonth_sent_plot()
    #twtscript_ey, twtdiv_ey = components(twtplot_ey)
    #twtplot_epe = twt.get_candidate_economy_party_env_sent_plot()
    #twtscript_epe, twtdiv_epe = components(twtplot_epe)
    #twtplot_hij = twt.get_candidate_health_imm_job_sent_plot()
    #twtscript_hij, twtdiv_hij = components(twtplot_hij)

    #return render_template("index.html", count="5", 
    #    map_div=div, map_script=script, 
    #    twtdiv_ey=twtdiv_ey, twtscript_ey=twtscript_ey,
    #    twtdiv_epe=twtdiv_epe, twtscript_epe=twtscript_epe,
    #    twtdiv_hij=twtdiv_hij, twtscript_hij=twtscript_hij)

    return render_template("index.html", count="5", 
        map_div=div, map_script=script)

    # text = print("hello hello testing")
    # return text



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
