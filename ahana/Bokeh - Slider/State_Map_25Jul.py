# imports
import geopandas as gpd
import pandas as pd
import json
from bokeh.io import show, curdoc
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,TapTool,
                          LinearColorMapper, Slider, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.models.widgets import RadioButtonGroup, Slider, RangeSlider, Tabs
#from bokeh.sampledata.us_states import data as states


# set pandas to display all columns in dataframe
pd.set_option("display.max_columns", None)

#Combining county data
total_data = "Input_Output_Jul07.csv"
total_df = pd.read_csv(total_data, encoding = "ISO-8859-1")
total_df["FIPS"] = total_df["STATE_FIPS"]*1000 + total_df["COUNTY_FIPS"]
counties_usa = gpd.read_file("bokeh/cb_2018_us_county_20m.shp")
counties_usa["GEOID"] = counties_usa["GEOID"].astype("float64")
merged_counties = counties_usa.merge(total_df, left_on="GEOID", right_on="FIPS")
#print("Merged Counties Dataframe Dimensions: {}".format(merged_counties.shape))
merged_counties.head()
# drop Alaska and Hawaii
merged_counties = merged_counties.loc[~merged_counties["STATE"].isin(["Alaska", "Hawaii"])]

#Combining State Data
state_data = "state_aggregated_0723.csv"
state_df = pd.read_csv(state_data, encoding = "ISO-8859-1")
states_usa = gpd.read_file("bokeh/cb_2018_us_state_20m.shp")
print("States shapefile dimension: {}".format(states_usa.shape))
states_usa = states_usa.loc[~states_usa["NAME"].isin(["Alaska", "Hawaii"])]
states_usa["STATEFP"] = counties_usa["STATEFP"].astype("int64")
merged_states = states_usa.merge(state_df, left_on="STATEFP", right_on="STATE_FIPS")
print("Merged States Dataframe Dimensions: {}".format(merged_states.shape))

state_fips = 4

def make_dataset(yr = 2008):
# create 2000 election year data frame
    yr_selected = merged_states["YEAR"] == yr
    merged_select = merged_states[yr_selected]
    # Convert to json
    merged_json = json.loads(merged_select.to_json())
    #Convert to json preferred string like object
    json_data = json.dumps(merged_json)
    return(json_data)

def make_dataset_county(yr = 2008, state_fips = 4):
    yr_selected = merged_counties["YEAR"] == yr
    county_select = merged_counties[yr_selected]
    county_select = county_select.loc[county_select["STATE_FIPS"].isin([state_fips])]
    merged_json = json.loads(county_select.to_json())
    #Convert to json preferred string like object
    json_data = json.dumps(merged_json)
    return(json_data)

def make_plot():
# define color palettes
    palette = brewer["GnBu"][8]

# use reverse order so higher values are darker
    palette = palette[::-1]

# instantiate LineraColorMapper and manually set low/high end for colorbar

    color_mapper = LinearColorMapper(palette = palette, low = -1,
                                 high = 1)

    # create color slider bar at the bottom of chart
    color_bar = ColorBar(color_mapper = color_mapper,
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0),
                     orientation = "horizontal")

# create figure object
    plot = figure(title = "Margin of Victory in Presidential Elections",
           plot_height = 600, plot_width = 950,
           toolbar_location = "below",
           tools = "pan, wheel_zoom, reset, tap")

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None

# add patch renderer to figure
    states = plot.patches("xs","ys", source = geo_src,
                       fill_color = {'field' :'MARGIN_VICTORY', 'transform' : color_mapper},
                       line_color = "gray",
                       line_width = 0.25,
                       fill_alpha = 1)
# create hover tool
    plot.add_tools(HoverTool(renderers = [states],
                      tooltips = [("State","@STATE"),
                               ("Rep Votes", "@TOTAL_REP_VOTES"), ("Dem Votes","@TOTAL_DEM_VOTES")]))

    plot.add_layout(color_bar, "below")

    return plot

def make_plot_county():
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
    plot = figure(title = 'Test Bokeh Map',
               plot_height = 600 ,
               plot_width = 950,
               toolbar_location = 'below',
               tools = "pan, wheel_zoom, reset, tap")
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None

    #plot.patches('xs','ys', source = geosource_states,fill_alpha=0.0,
    #          line_color="#884444", line_width=2, line_alpha=0.3)

    # add patch renderer to figure.
    county = plot.patches('xs','ys', source = geo_src_county,
                       fill_color = {"field": "COUNTY_TOTALVOTES",
                                     "transform": color_mapper},
                       line_color = "gray",
                       line_width = 0.25,
                       fill_alpha = 1)
    # create hover tool
    plot.add_tools(HoverTool(renderers = [county],
                          tooltips = [('County','@NAME'),
                                    ('Dem Votes','@DEM_VOTES'),
                                     ('Rep Votes','@REP_VOTES')]))


    return plot

def update(attr, old, new):
        new_src = make_dataset(yr = int(new))
        geo_src.geojson = new_src

        #new_src_state = make_dataset_county(int(new),state_fips)
        #geo_src_county.geojson = new_src_state

        #p = make_plot()
        p2 = make_plot_county()
        p2 = column(p2,WidgetBox(year_select))
        layout = row(p2)
        curdoc().clear()
        curdoc().add_root(layout)

# Creating the slider object
year_select = Slider(start = 2000, end = 2020,
                         step = 4, value = 2000,
                         title = 'Election Year')
year_select.on_change('value', update)

geo_src = GeoJSONDataSource(geojson = make_dataset(yr = year_select.value))
geo_src_county = GeoJSONDataSource(geojson = make_dataset_county(year_select.value,state_fips))

tap = TapTool()
def function_geosource(attr, old, new):
    try:
        selected_index = geo_src.selected.indices[0]
        state_fips = states_usa.iloc[selected_index]['STATEFP']
#        geo_src_county = GeoJSONDataSource(geojson = make_dataset_county(year_select.value,state_fips))
#        p = make_plot()
#        p2 = make_plot_county()
#        p = column(p,WidgetBox(year_select))
#        layout = row(p,p2)
#        curdoc().clear()
#        curdoc().add_root(layout)
        print(state_fips)
        return(state_fips)
    except IndexError:
        pass

state_fips = geo_src.selected.on_change('indices', function_geosource)

#p = make_plot()
p2 = make_plot_county()
p2 = column(p2,WidgetBox(year_select))
layout = row(p2)
curdoc().add_root(layout)
