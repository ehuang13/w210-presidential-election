
import geopandas as gpd
import pandas as pd

from bokeh.io import show, curdoc
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.transform import cumsum


# plot counties US map visualization
def create_chart():

    # read in combined dataset
    combined_df = pd.read_csv("https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/data/combined_jun13.csv")

    # read in counties shapefile from US Census Bureau
    counties_usa = gpd.read_file("bokeh/cb_2018_us_county_20m.shp")

    # cast GEOID data type to float64 instead of str for merging
    counties_usa["GEOID"] = counties_usa["GEOID"].astype("float64")

    # merge counties shapefile with combined_df
    merged_counties = counties_usa.merge(combined_df, left_on="GEOID", right_on="FIPS")

    # drop Alaska and Hawaii
    merged_counties = merged_counties.loc[~merged_counties["STATE"].isin(["Alaska", "Hawaii"])]

    # create 2000 election year data frame
    yr2000 = merged_counties["YEAR"] == 2000
    merged_2000 = merged_counties[yr2000]

    # input GeoJSON source that contains features for plotting
    geosource_2000 = GeoJSONDataSource(geojson = merged_2000.to_json())

    # define color palettes
    palette = brewer["GnBu"][8]

    # use reverse order so higher values are darker
    palette = palette[::-1]

    # instantiate LineraColorMapper and manually set low/high end for colorbar
    color_mapper = LinearColorMapper(palette = palette, low = 0,
                                     high = 2.371175e+04)

    # create color slider bar at the bottom of chart
    color_bar = ColorBar(color_mapper = color_mapper,
                         label_standoff = 8,
                         width = 500, height = 20,
                         border_line_color = None,
                         location = (0,0),
                         orientation = "horizontal")

    # create figure object
    plot = figure(title = "Total # of Votes Cast by County in 2000 Presidential Election",
               plot_height = 600, plot_width = 950,
               toolbar_location = "below",
               tools = "pan, wheel_zoom, reset")

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None

    # add patch renderer to figure
    counties = plot.patches("xs","ys", source = geosource_2000,
                       fill_color = {"field": "COUNTY_TOTALVOTES",
                                     "transform": color_mapper},
                       line_color = "gray",
                       line_width = 0.25,
                       fill_alpha = 1)

    # create hover tool
    plot.add_tools(HoverTool(renderers = [counties],
                          tooltips = [("County","@NAME"),
                                   ("Votes", "@COUNTY_TOTALVOTES")]))

    # specify colorbar layout
    plot.add_layout(color_bar, "below")

    return plot