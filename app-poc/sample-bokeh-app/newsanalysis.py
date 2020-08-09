import numpy as np # we will use this later, so import it now
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row


def plot_chart(rep_df, dem_df, rep_cand, dem_cand, title):
    
    rep_df['date'] = pd.to_datetime(rep_df['date'].astype(str), errors='coerce')
    dem_df['date'] = pd.to_datetime(dem_df['date'].astype(str), errors='coerce')
    
    rep_mean = round(rep_df["score"].mean(), 4)
    dem_mean = round(dem_df["score"].mean(), 4)
    
    title = title + ' -> ' + rep_cand + ': ' + str(rep_mean) + ' & ' + dem_cand + ': ' + str(dem_mean) 

    p = figure(x_axis_type="datetime", title=title, plot_height=200, plot_width=350)
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Sentiment Score'
    
    p.line(rep_df.date, rep_df.score, line_color="red", line_width=1, line_alpha=0.6)
    p.circle(rep_df.date, rep_df.score, fill_color="red", size=3, color="red")

    p.line(dem_df.date, dem_df.score, line_color="blue", line_width=1, line_alpha=0.6)
    p.circle(dem_df.date, dem_df.score, fill_color="blue", size=3, color="blue")
   
    #p.legend.location = "bottom_left"
    #p.legend.label_text_font_size = '8pt'

    p.toolbar.logo = None
    p.toolbar_location = None
    
    return p


def get_candidate_plot():
    df_trump_c = pd.read_csv('data/newssentdata/candidates/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/cnn/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_cand_c = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Candidate - CNN ")

    df_trump_f = pd.read_csv('data/newssentdata/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_cand_f = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Candidate - FOX")

    # show the results
    return p_2020_cand_c, p_2020_cand_f

def get_candidate_economy_plot():
    df_trump_c = pd.read_csv('data/newssentdata/economy/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/economy/cnn/biden/headlines.csv')

    p_2020_econ_c = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Econ - CNN")

    df_trump_f = pd.read_csv('data/newssentdata/economy/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/economy/fox-news/biden/headlines.csv')

    p_2020_econ_f = plot_chart(df_trump_f, df_biden_f, 'Trump', 'Biden', "Econ - FOX")

    return p_2020_econ_c, p_2020_econ_f

def get_candidate_env_plot():
    df_trump_c = pd.read_csv('data/newssentdata/environment/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/environment/cnn/biden/headlines.csv')

    p_2020_env_c = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Env - CNN")

    df_trump_f = pd.read_csv('data/newssentdata/environment/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/environment/fox-news/biden/headlines.csv')

    p_2020_env_f = plot_chart(df_trump_f, df_biden_f, 'Trump', 'Biden', "Env - FOX")

    return p_2020_env_c, p_2020_env_f


def get_candidate_party_plot():
    df_trump_c = pd.read_csv('data/newssentdata/party/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/party/cnn/biden/headlines.csv')

    p_2020_party_c = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Party - CNN")

    df_trump_f = pd.read_csv('data/newssentdata/party/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/party/fox-news/biden/headlines.csv')

    p_2020_party_f = plot_chart(df_trump_f, df_biden_f, 'Trump', 'Biden', "Party - FOX")

    return p_2020_party_c, p_2020_party_f


def get_candidate_health_plot():
    df_trump_c = pd.read_csv('data/newssentdata/health/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/health/cnn/biden/headlines.csv')

    p_2020_h_c = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Health - CNN")

    df_trump_f = pd.read_csv('data/newssentdata/health/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/health/fox-news/biden/headlines.csv')

    p_2020_h_f = plot_chart(df_trump_f, df_biden_f, 'Trump', 'Biden', "Health - FOX")

    return p_2020_h_c, p_2020_h_f

def get_candidate_imm_plot():
    df_trump_c = pd.read_csv('data/newssentdata/immigration/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/immigration/cnn/biden/headlines.csv')

    p_2020_imm_c = plot_chart(df_trump_c, df_biden_c, 'Trump', 'Biden', "Imm - CNN")

    df_trump_f = pd.read_csv('data/newssentdata/immigration/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/immigration/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_imm_f = plot_chart(df_trump_f, df_biden_f, 'Trump', 'Biden', "Imm - FOX")

    return p_2020_imm_c, p_2020_imm_f