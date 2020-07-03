import numpy as np # we will use this later, so import it now
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row

def get_and_clean_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['created_at'].astype(str), errors='coerce')
    return data

def get_mean_scores_by_date(df):
    df['date'] = df['date'].dt.date
    df2 = df.groupby('date')['scores'].mean().to_frame().reset_index()
    return df2

def get_plot_data(path):
    df = get_and_clean_data(path)
    df = get_mean_scores_by_date(df)
    
    return df[['date', 'scores']]

def plot_chart(rep_df, dem_df, rep_cand, dem_cand, title):
    
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

    df_trump = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/candidate/2020/trump/2020_trump.csv')
    df_biden = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/candidate/2020/biden/2020_biden.csv')

    p_2020_cand = plot_chart(df_trump, df_biden, 'Trump', 'Biden', "2020 ")

    df_trump_16 = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/candidate/2016/trump/2016_trump.csv')
    df_hillary = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/candidate/2016/hillary/2016_hillary.csv')

    p_2016_cand = plot_chart(df_trump_16, df_hillary, 'Trump', 'Hillary', "2016 ")

    df_obama = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/candidate/2012/obama/2012_obama.csv')
    df_romney = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/candidate/2012/romney/2012_romney.csv')

    p_2012_cand = plot_chart(df_obama, df_romney, 'Romney', 'Obama', "2012 ")

    # put all the plots in an HBox
    p = row(p_2020_cand, p_2016_cand, p_2012_cand)

    return p


def get_candidate_economy_party_env_sent_plot():
    df_trump_econ = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/economy/trump/2020_trump economy.csv')
    df_biden_econ = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/economy/biden/2020_biden economy.csv')

    plot_econ = plot_chart(df_trump_econ, df_biden_econ, 'Trump', 'Biden', "Economy ")

    df_trump_party = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/party/trump/2020_trump republican.csv')
    df_biden_party = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/party/biden/2020_biden democrat.csv')

    plot_party = plot_chart(df_trump_party, df_biden_party, 'Trump', 'Biden', "Party ")

    df_trump_env = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/environment/trump/2020_trump environment.csv')
    df_biden_env = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/environment/biden/2020_biden environment.csv')

    plot_env = plot_chart(df_trump_env, df_biden_env, 'Trump', 'Biden', "Environ ")

    # put all the plots in an HBox
    p = row(plot_econ, plot_party, plot_env)

    # show the results
    #show(p)

    return p


def get_candidate_health_imm_job_sent_plot():
    df_trump_health = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/health/trump/2020_trump health.csv')
    df_biden_health = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/health/biden/2020_biden health.csv')

    plot_health = plot_chart(df_trump_health, df_biden_health, 'Trump', 'Biden', "Health ")

    df_trump_imm = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/immigration/trump/2020_trump immigration.csv')
    df_biden_imm = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/immigration/biden/2020_biden immigration.csv')

    plot_imm = plot_chart(df_trump_imm, df_biden_imm, 'Trump', 'Biden', "Immi ")

    df_trump_job = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/job/trump/2020_trump job.csv')
    df_biden_job = get_plot_data('https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/rishi/twitter2/twtsentdata/job/biden/2020_biden job.csv')

    plot_job = plot_chart(df_trump_job, df_biden_job, 'Trump', 'Biden', "Job ")

    # put all the plots in an HBox
    p = row(plot_health, plot_imm, plot_job)

    # show the results
    #show(p)
    return p