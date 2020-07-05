# imports
import geopandas as gpd
import pandas as pd
import json
from bokeh.io import show, curdoc
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.models.widgets import RadioButtonGroup, Slider, RangeSlider, Tabs


# set pandas to display all columns in dataframe
pd.set_option("display.max_columns", None)

# read in combined dataset
# load in Ahana's final merged dataset
#total_data = "https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/data/combined_jun22.csv"
#combined_df = pd.read_csv(total_data, encoding = "ISO-8859-1")

combined_df = pd.read_csv("https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/data/combined_jun13.csv")

winning_party_binary = pd.get_dummies(combined_df["WINNING_PARTY"], drop_first = True)
combined_df["WINNING_PARTY_BINARY"] = winning_party_binary

# read in counties shapefile from US Census Bureau
counties_usa = gpd.read_file("bokeh/cb_2018_us_county_20m.shp")
print("Counties Shapefile Dimensions: {}".format(counties_usa.shape))
counties_usa.head()

# cast GEOID data type to float64 instead of str for merging
counties_usa["GEOID"] = counties_usa["GEOID"].astype("float64")

# merge counties shapefile with combined_df
merged_counties = counties_usa.merge(combined_df, left_on="GEOID", right_on="FIPS")
print("Merged Counties Dataframe Dimensions: {}".format(merged_counties.shape))
merged_counties.head()

# try to visualize Bladen county
#merged_counties.iloc[0]["geometry"]

# drop Alaska and Hawaii
merged_counties = merged_counties.loc[~merged_counties["STATE"].isin(["Alaska", "Hawaii"])]

# input GeoJSON source that contains features for plotting
#geosource_counties = GeoJSONDataSource(geojson = merged_counties.to_json())

def make_dataset(yr = 2000):
# create 2000 election year data frame
    yr_selected = merged_counties["YEAR"] == yr
    merged_select = merged_counties[yr_selected]
    # Bokeh uses geojson formatting, representing geographical features, with json
    # Convert to json
    merged_json = json.loads(merged_select.to_json())
    #Convert to json preferred string like object
    json_data = json.dumps(merged_json)
    # input GeoJSON source that contains features for plotting
    #geosource_select = GeoJSONDataSource(geojson = merged_select.to_json())
    return(json_data)

def make_plot():
# define color palettes
    palette = brewer["RdYlBu"][8]

# use reverse order so higher values are darker
    palette = palette[::-1]

# instantiate LineraColorMapper and manually set low/high end for colorbar
    color_mapper = LinearColorMapper(palette = palette, low = 1,
                                 high = 0)

# create figure object
    plot = figure(title = "Republican or Democrat Win by County in Presidential Election",
           plot_height = 600, plot_width = 950,
           toolbar_location = "below",
           tools = "pan, wheel_zoom, reset")

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None

# add patch renderer to figure
    counties = plot.patches("xs","ys", source = geo_src,
                       fill_color = {'field' :'WINNING_PARTY_BINARY', 'transform' : color_mapper},
                       line_color = "gray",
                       line_width = 0.25,
                       fill_alpha = 1)
# create hover tool
    plot.add_tools(HoverTool(renderers = [counties],
                      tooltips = [("County","@NAME"),
                               ("Rep Votes", "@REP_VOTES"), ("Dem Votes","@DEM_VOTES")]))
    return plot

def update(attr, old, new):
        print("hello")
        print(old)
        print(new)
        new_src = make_dataset(yr = int(new))

        geo_src.geojson = new_src

        p = make_plot()
        controls = WidgetBox(year_select)
        layout = row(p, controls)
        curdoc().clear()
        curdoc().add_root(layout)


year_select = Slider(start = 2000, end = 2016,
                         step = 4, value = 2000,
                         title = 'Election Year')
year_select.on_change('value', update)

geo_src = GeoJSONDataSource(geojson = make_dataset(yr = year_select.value))
#geo_src = make_dataset(yr = year_select.value)
#geo_src = GeoJSONDataSource(geojson = src.to_json())

p = make_plot()
controls = WidgetBox(year_select)
layout = row(p, controls)
curdoc().add_root(layout)
