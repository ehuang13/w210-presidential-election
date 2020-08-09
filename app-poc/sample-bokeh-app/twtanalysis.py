import numpy as np # we will use this later, so import it now
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
from bokeh.io import curdoc
from bokeh.models import BoxAnnotation, Toggle
from datetime import datetime, date
import newsanalysis as ns

def plot_chart(rep_df, dem_df, rep_cand, dem_cand, title, chart_b_color):
    
    rep_df['date'] = pd.to_datetime(rep_df['date'].astype(str), errors='coerce')
    dem_df['date'] = pd.to_datetime(dem_df['date'].astype(str), errors='coerce')
    
    title = title + '| ' + rep_cand + ': ' + str(round(rep_df["scores"].mean(), 4)) + ' & ' + dem_cand + ': ' + str(round(dem_df["scores"].mean(), 4))
    
    p = figure(x_axis_type="datetime", title=title, plot_height=200, plot_width=350)
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Sentiment Score'
    
    p.line(rep_df.date, rep_df.scores, line_color="red", 
           line_width=1, line_alpha=0.6)
    p.circle(rep_df.date, rep_df.scores, fill_color="red", size=5, color="red")

    p.line(dem_df.date, dem_df.scores, line_color="blue", 
           line_width=1, line_alpha=0.6)
    p.circle(dem_df.date, dem_df.scores, fill_color="blue", size=5, color="blue")

    #p.legend.location = "bottom_left"
    #p.legend.label_text_font_size = '8pt'

    if chart_b_color != None:
       p.background_fill_color = chart_b_color
       p.background_fill_alpha = 0.5

    red_box = BoxAnnotation(left=date(2016, 11, 2), right=date(2016, 11, 10), fill_color='red', fill_alpha=0.1)
    p.add_layout(red_box)

    blue_box = BoxAnnotation(left=date(2012, 11, 1), right=date(2012, 11, 8), fill_color='blue', fill_alpha=0.1)
    p.add_layout(blue_box)

    p.toolbar.logo = None
    p.toolbar_location = None
    
    return p
    
def get_candidate_election_yearmonth_sent_plot():

    df_trump = pd.read_csv('data/twtsentdata/candidate/2020/trump/2020_trump.csv')
    df_biden = pd.read_csv('data/twtsentdata/candidate/2020/biden/2020_biden.csv')

    p_2020_cand = plot_chart(df_trump, df_biden, 'Trump', 'Biden', "2020 ", None)

    df_trump_16 = pd.read_csv('data/twtsentdata/candidate/2016/trump/2016_trump.csv')
    df_hillary = pd.read_csv('data/twtsentdata/candidate/2016/hillary/2016_hillary.csv')

    p_2016_cand = plot_chart(df_trump_16, df_hillary, 'Trump', 'Hillary', "2016 ", None)

    df_obama = pd.read_csv('data/twtsentdata/candidate/2012/obama/2012_obama.csv')
    df_romney = pd.read_csv('data/twtsentdata/candidate/2012/romney/2012_romney.csv')

    p_2012_cand = plot_chart(df_obama, df_romney, 'Romney', 'Obama', "2012 ", None)

    # put all the plots in an HBox
    p = row(p_2012_cand, p_2016_cand, p_2020_cand)

    return p

def get_candidate_economy_plot():
    df_trump_econ = pd.read_csv('data/twtsentdata/economy/trump/2020_trump_economy.csv')
    df_biden_econ = pd.read_csv('data/twtsentdata/economy/biden/2020_biden_economy.csv')

    plot_econ = plot_chart(df_trump_econ, df_biden_econ, 'Trump', 'Biden', "Econ ", None)

    ns_econ_c, ns_econ_f = ns.get_candidate_economy_plot()

    # put all the plots in an HBox
    p = row(plot_econ, ns_econ_c, ns_econ_f)

    # show the results
    #show(p)

    return p

def get_candidate_party_plot():
    
    df_trump_party = pd.read_csv('data/twtsentdata/party/trump/2020_trump_republican.csv')
    df_biden_party = pd.read_csv('data/twtsentdata/party/biden/2020_biden_democrat.csv')

    plot_party = plot_chart(df_trump_party, df_biden_party, 'Trump', 'Biden', "Party ", None)
    
    ns_party_c, ns_party_f = ns.get_candidate_party_plot()

    # put all the plots in an HBox
    p = row(plot_party, ns_party_c, ns_party_f)

    # show the results
    #show(p)

    return p


def get_candidate_env_plot():
    
    df_trump_env = pd.read_csv('data/twtsentdata/environment/trump/2020_trump_environment.csv')
    df_biden_env = pd.read_csv('data/twtsentdata/environment/biden/2020_biden_environment.csv')

    plot_env = plot_chart(df_trump_env, df_biden_env, 'Trump', 'Biden', "Env ", None)

    ns_env_c, ns_env_f = ns.get_candidate_env_plot()

    # put all the plots in an HBox
    p = row(plot_env, ns_env_c, ns_env_f)

    # show the results
    #show(p)

    return p


def get_candidate_health_plot():
    df_trump_health = pd.read_csv('data/twtsentdata/health/trump/2020_trump_health.csv')
    df_biden_health = pd.read_csv('data/twtsentdata/health/biden/2020_biden_health.csv')

    plot_health = plot_chart(df_trump_health, df_biden_health, 'Trump', 'Biden', "Health ", None)

    ns_health_c, ns_health_f = ns.get_candidate_health_plot()

    # put all the plots in an HBox
    p = row(plot_health, ns_health_c, ns_health_f)

    # show the results
    #show(p)
    return p

def get_candidate_imm_plot():
    
    df_trump_imm = pd.read_csv('data/twtsentdata/immigration/trump/2020_trump_immigration.csv')
    df_biden_imm = pd.read_csv('data/twtsentdata/immigration/biden/2020_biden_immigration.csv')

    plot_imm = plot_chart(df_trump_imm, df_biden_imm, 'Trump', 'Biden', "Imm ", None)

    ns_imm_c, ns_imm_f = ns.get_candidate_imm_plot()

    # put all the plots in an HBox
    p = row(plot_imm, ns_imm_c, ns_imm_f)

    # show the results
    #show(p)
    return p

def get_candidate_job_plot():
    
    df_trump_job = pd.read_csv('data/twtsentdata/job/trump/2020_trump_job.csv')
    df_biden_job = pd.read_csv('data/twtsentdata/job/biden/2020_biden_job.csv')

    plot_job = plot_chart(df_trump_job, df_biden_job, 'Trump', 'Biden', "Job ", None)

    # put all the plots in an HBox
    p = row(plot_job)

    # show the results
    #show(p)
    return p