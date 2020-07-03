import numpy as np # we will use this later, so import it now
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row

def plot_chart(rep_df, dem_df, rep_cand, dem_cand, title):
    
    rep_df['date'] = pd.to_datetime(rep_df['date'].astype(str), errors='coerce')
    dem_df['date'] = pd.to_datetime(dem_df['date'].astype(str), errors='coerce')
    
    title = title + '| ' + rep_cand + ': ' + str(round(rep_df["scores"].mean(), 4)) + ' & ' + dem_cand + ': ' + str(round(dem_df["scores"].mean(), 4))
    
    p = figure(x_axis_type="datetime", title=title, plot_height=200, plot_width=310)
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

    p.toolbar.logo = None
    p.toolbar_location = None
    
    return p
    
def get_candidate_election_yearmonth_sent_plot():

    df_trump = pd.read_csv('data/twtsentdata/candidate/2020/trump/2020_trump.csv')
    df_biden = pd.read_csv('data/twtsentdata/candidate/2020/biden/2020_biden.csv')

    p_2020_cand = plot_chart(df_trump, df_biden, 'Trump', 'Biden', "2020 ")

    df_trump_16 = pd.read_csv('data/twtsentdata/candidate/2016/trump/2016_trump.csv')
    df_hillary = pd.read_csv('data/twtsentdata/candidate/2016/hillary/2016_hillary.csv')

    p_2016_cand = plot_chart(df_trump_16, df_hillary, 'Trump', 'Hillary', "2016 ")

    df_obama = pd.read_csv('data/twtsentdata/candidate/2012/obama/2012_obama.csv')
    df_romney = pd.read_csv('data/twtsentdata/candidate/2012/romney/2012_romney.csv')

    p_2012_cand = plot_chart(df_obama, df_romney, 'Romney', 'Obama', "2012 ")

    # put all the plots in an HBox
    p = row(p_2020_cand, p_2016_cand, p_2012_cand)

    return p


def get_candidate_economy_party_env_sent_plot():
    df_trump_econ = pd.read_csv('data/twtsentdata/economy/trump/2020_trump_economy.csv')
    df_biden_econ = pd.read_csv('data/twtsentdata/economy/biden/2020_biden_economy.csv')

    plot_econ = plot_chart(df_trump_econ, df_biden_econ, 'Trump', 'Biden', "Economy ")

    df_trump_party = pd.read_csv('data/twtsentdata/party/trump/2020_trump_republican.csv')
    df_biden_party = pd.read_csv('data/twtsentdata/party/biden/2020_biden_democrat.csv')

    plot_party = plot_chart(df_trump_party, df_biden_party, 'Trump', 'Biden', "Party ")

    df_trump_env = pd.read_csv('data/twtsentdata/environment/trump/2020_trump_environment.csv')
    df_biden_env = pd.read_csv('data/twtsentdata/environment/biden/2020_biden_environment.csv')

    plot_env = plot_chart(df_trump_env, df_biden_env, 'Trump', 'Biden', "Environ ")

    # put all the plots in an HBox
    p = row(plot_econ, plot_party, plot_env)

    # show the results
    #show(p)

    return p


def get_candidate_health_imm_job_sent_plot():
    df_trump_health = pd.read_csv('data/twtsentdata/health/trump/2020_trump_health.csv')
    df_biden_health = pd.read_csv('data/twtsentdata/health/biden/2020_biden_health.csv')

    plot_health = plot_chart(df_trump_health, df_biden_health, 'Trump', 'Biden', "Health ")

    df_trump_imm = pd.read_csv('data/twtsentdata/immigration/trump/2020_trump_immigration.csv')
    df_biden_imm = pd.read_csv('data/twtsentdata/immigration/biden/2020_biden_immigration.csv')

    plot_imm = plot_chart(df_trump_imm, df_biden_imm, 'Trump', 'Biden', "Immi ")

    df_trump_job = pd.read_csv('data/twtsentdata/job/trump/2020_trump_job.csv')
    df_biden_job = pd.read_csv('data/twtsentdata/job/biden/2020_biden_job.csv')

    plot_job = plot_chart(df_trump_job, df_biden_job, 'Trump', 'Biden', "Job ")

    # put all the plots in an HBox
    p = row(plot_health, plot_imm, plot_job)

    # show the results
    #show(p)
    return p