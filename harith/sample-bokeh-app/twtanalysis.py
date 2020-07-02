


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
    p = figure(x_axis_type="datetime", title=title, plot_height=350, plot_width=900)
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Sentiment Score'

    p.line(rep_df.date, rep_df.scores, line_color="red", 
           line_width=4, line_alpha=0.6, 
           legend_label= rep_cand + ' (' + str(round(rep_df["scores"].mean(), 5)) + ')')
    p.circle(rep_df.date, rep_df.scores, fill_color="red", size=5, color="red")

    p.line(dem_df.date, dem_df.scores, line_color="blue", 
           line_width=4, line_alpha=0.6, 
           legend_label= dem_cand + ' (' + str(round(df_biden["scores"].mean(), 5))  + ')')
    p.circle(dem_df.date, dem_df.scores, fill_color="blue", size=5, color="blue")

    p.legend.location = "bottom_right"

    return p
    #show(p)

def get_candidate_sent():
    # read in combined dataset
    combined_df = pd.read_csv("https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/data/combined_jun13.csv")

    df_trump = get_plot_data('data2/sentiment/candidate/2020/trump/2020_trump.csv')
    df_biden = get_plot_data('data2/sentiment/candidate/2020/biden/2020_biden.csv')

    plot_chart(df_trump, df_biden, 
    'Trump', 'Biden', "Candidate Sentiment - 2020 - Last 30 Days")