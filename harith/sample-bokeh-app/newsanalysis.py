import numpy as np # we will use this later, so import it now
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row


def plot_chart(rep_con_df, rep_lib_df, dem_con_df, dem_lib_df, rep_cand, dem_cand, title):
    
    rep_con_df['date'] = pd.to_datetime(rep_con_df['date'].astype(str), errors='coerce')
    rep_lib_df['date'] = pd.to_datetime(rep_lib_df['date'].astype(str), errors='coerce')
    dem_con_df['date'] = pd.to_datetime(dem_con_df['date'].astype(str), errors='coerce')
    dem_lib_df['date'] = pd.to_datetime(dem_lib_df['date'].astype(str), errors='coerce')
    
    rep_con_mean = round(rep_con_df["score"].mean(), 4)
    dem_lib_mean = round(dem_lib_df["score"].mean(), 4)
    dem_con_mean = round(dem_con_df["score"].mean(), 4)
    rep_lib_mean = round(rep_lib_df["score"].mean(), 4)
    
    #title = title + '| ' + rep_cand + ': ' + str(round((rep_con_mean + rep_lib_mean)/2, 4)) + ' & ' + \
    #dem_cand + ': ' + str(round((dem_con_mean + dem_lib_mean)/2, 4))
    title = title + '| ' + rep_cand + ': ' + str(rep_con_mean) + '(F),' + str(rep_lib_mean) + '(C) & '
    title = title + dem_cand + ': ' + str(dem_con_mean) + '(F),' + str(dem_lib_mean) + '(C)'
                         
    
    p = figure(x_axis_type="datetime", title=title, plot_height=250, plot_width=550)
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Sentiment Score'
    
    p.line(rep_con_df.date, rep_con_df.score, line_color="darkred", line_width=1, line_alpha=0.6, legend_label='TF')
    p.line(rep_lib_df.date, rep_lib_df.score, line_color="orange", line_width=1, line_alpha=0.6, legend_label='TC')
    p.circle(rep_con_df.date, rep_con_df.score, fill_color="darkred", size=3, color="darkred")
    p.circle(rep_lib_df.date, rep_lib_df.score, fill_color="orange", size=3, color="orange")

    p.line(dem_con_df.date, dem_con_df.score, line_color="lightblue", line_width=1, line_alpha=0.6, legend_label='BF')
    p.line(dem_lib_df.date, dem_lib_df.score, line_color="blue", line_width=1, line_alpha=0.6, legend_label='BC')
    p.circle(dem_con_df.date, dem_con_df.score, fill_color="lightblue", size=3, color="lightblue")
    p.circle(dem_lib_df.date, dem_lib_df.score, fill_color="blue", size=3, color="blue")

    p.legend.location = "bottom_left"
    p.legend.label_text_font_size = '8pt'

    p.toolbar.logo = None
    p.toolbar_location = None
    
    return p


def get_candidate_plot():
    df_trump_c = pd.read_csv('data/newssentdata/candidates/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/cnn/biden/headlines.csv')

    df_trump_f = pd.read_csv('data/newssentdata/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_cand = plot_chart(df_trump_f, df_trump_c, df_biden_f, df_biden_c, 'Trump', 'Biden', "Candidate ")

    # show the results
    return p_2020_cand

def get_candidate_economy_plot():
    df_trump_c = pd.read_csv('data/newssentdata/economy/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/economy/cnn/biden/headlines.csv')

    df_trump_f = pd.read_csv('data/newssentdata/economy/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/economy/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_econ = plot_chart(df_trump_c, df_trump_f, df_biden_c, df_biden_f, 'Trump', 'Biden', "Econ ")

    return p_2020_econ

def get_candidate_env_plot():
    df_trump_c = pd.read_csv('data/newssentdata/environment/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/environment/cnn/biden/headlines.csv')

    df_trump_f = pd.read_csv('data/newssentdata/environment/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/environment/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_env = plot_chart(df_trump_f, df_trump_c, df_biden_f, df_biden_c, 'Trump', 'Biden', "Env ")

    return p_2020_env


def get_candidate_party_plot():
    df_trump_c = pd.read_csv('data/newssentdata/party/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/party/cnn/biden/headlines.csv')

    df_trump_f = pd.read_csv('data/newssentdata/party/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/party/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_party = plot_chart(df_trump_c, df_trump_f, df_biden_c, df_biden_f, 'Trump', 'Biden', "Party ")

    return p_2020_party


def get_candidate_health_plot():
    df_trump_c = pd.read_csv('data/newssentdata/health/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/health/cnn/biden/headlines.csv')

    df_trump_f = pd.read_csv('data/newssentdata/health/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/health/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_h = plot_chart(df_trump_f, df_trump_c, df_biden_f, df_biden_c, 'Trump', 'Biden', "Health ")

    return p_2020_h

def get_candidate_imm_plot():
    df_trump_c = pd.read_csv('data/newssentdata/immigration/cnn/trump/headlines.csv')
    df_biden_c = pd.read_csv('data/newssentdata/immigration/cnn/biden/headlines.csv')

    df_trump_f = pd.read_csv('data/newssentdata/immigration/fox-news/trump/headlines.csv')
    df_biden_f = pd.read_csv('data/newssentdata/immigration/fox-news/biden/headlines.csv')

    #print(df_trump.head())

    p_2020_j = plot_chart(df_trump_c, df_trump_f, df_biden_c, df_biden_f, 'Trump', 'Biden', "Imm ")

    return p_2020_j