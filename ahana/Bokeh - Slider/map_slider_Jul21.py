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

#del states["HI"]
#del states["AK"]
#state_xs = [states[code]["lons"] for code in states]
#state_ys = [states[code]["lats"] for code in states]

# read in combined dataset
# load in Ahana's final merged dataset
#total_data = "https://raw.githubusercontent.com/ehuang13/w210-presidential-election/master/data/combined_jun22.csv"
#combined_df = pd.read_csv(total_data, encoding = "ISO-8859-1")

#combined_df = pd.read_csv("combined_jul05.csv")
total_data = "combined_jul05.csv"
total_df = pd.read_csv(total_data, encoding = "ISO-8859-1")

F20_data = "F20_predictions_0703_new.csv"
F20_df = pd.read_csv(F20_data, encoding = "ISO-8859-1")

combined_df = pd.concat([total_df,F20_df])
#winning_party_binary = pd.get_dummies(combined_df["WINNING_PARTY"], drop_first = True)
#combined_df["WINNING_PARTY_BINARY"] = winning_party_binary
combined_df['FIPS']=combined_df['STATE_FIPS']*1000 + combined_df['COUNTY_FIPS']
combined_df = combined_df.loc[~combined_df["STATE_FIPS"].isin( [2, 15])]

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

# drop Alaska and Hawaii
merged_counties = merged_counties.loc[~merged_counties["STATE"].isin(["Alaska", "Hawaii"])]

# read in states shapefile from US Census Bureau
states_usa = gpd.read_file("bokeh/cb_2018_us_state_20m.shp")
print("States shapefile dimension: {}".format(states_usa.shape))
states_usa.head()
states_usa = states_usa.loc[~states_usa["NAME"].isin(["Alaska", "Hawaii"])]
geosource_states = GeoJSONDataSource(geojson = states_usa.to_json())


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
           tools = "pan, wheel_zoom, reset, tap")

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.patches("xs","ys", source = geosource_states, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)

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

def make_plot_criteria(field_name):
    # define color palettes
        palette = brewer["GnBu"][8]

    # use reverse order so higher values are darker
        palette = palette[::-1]

    # instantiate LineraColorMapper and manually set low/high end for colorbar
        color_mapper = LinearColorMapper(palette = palette, low = 1,
                                     high = 1500000)
        color_bar = ColorBar(color_mapper = color_mapper,
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0),
                     orientation = "horizontal")
        verbage = format_df.loc[format_df['field'] == field_name, 'verbage'].iloc[0]
    # create figure object
        plot = figure(title = verbage + " by County in Presidential Election",
               plot_height = 650, plot_width = 950,
               toolbar_location = "below",
               tools = "pan, wheel_zoom, reset, tap")

        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.patches("xs","ys", source = geosource_states, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)

    # add patch renderer to figure
        counties = plot.patches("xs","ys", source = geo_src,
                           fill_color = {'field' : field_name, 'transform' : color_mapper},
                           line_color = "gray",
                           line_width = 0.25,
                           fill_alpha = 1)
    # create hover tool
        plot.add_tools(HoverTool(renderers = [counties],
                          tooltips = [("County","@NAME"),
                                   ("Rep Votes", "@REP_VOTES"), ("Dem Votes","@DEM_VOTES")]))
        plot.add_layout(color_bar, "below")
        return plot

def update(attr, old, new):
        new_src = make_dataset(yr = int(new))
        geo_src.geojson = new_src

        p = make_plot()
        p2 = make_plot_criteria(input_field)
        p = column(p,WidgetBox(year_select))
        p2 = column(p2,WidgetBox(select))
        layout = row(p,p2)
        curdoc().clear()
        curdoc().add_root(layout)

def update_2(attr, old, new):
        print(old)
        print(new)
        input_field = format_df.loc[format_df['verbage'] == new, 'field'].iloc[0]
        p = make_plot()
        p2 = make_plot_criteria(input_field)
        p = column(p,WidgetBox(year_select))
        p2 = column(p2,WidgetBox(select))
        layout = row(p,p2)
        curdoc().clear()
        curdoc().add_root(layout)
# Creating the slider object
year_select = Slider(start = 2000, end = 2020,
                         step = 4, value = 2000,
                         title = 'Election Year')
year_select.on_change('value', update)

#Creating the dropdown
select = Select(title='Select Criteria',value = 'Total Votes', options=['Total Votes','Republican Votes','Democrat Votes'])
select.on_change('value',update_2)

format_data = [('COUNTY_TOTALVOTES', 0, 1500000,'0,0', 'Total Votes'),
('REP_VOTES', 0, 1500000,'0,0', 'Republican Votes'),
('DEM_VOTES', 0, 1500000,'0,0', 'Democrat Votes')
]
#Create a DataFrame object from the dictionary
format_df = pd.DataFrame(format_data, columns = ['field' , 'min_range', 'max_range' , 'format', 'verbage'])
input_field = format_df.loc[format_df['verbage'] == select.value, 'field'].iloc[0]

geo_src = GeoJSONDataSource(geojson = make_dataset(yr = year_select.value))

#callback = CustomJS(code="alert('you tapped a state!')")
#tap = TapTool(callback=callback)
tap = TapTool()
def function_geosource(attr, old, new):
    try:
        selected_index = geosource_states.selected.indices[0]
        state_name = states_usa.iloc[selected_index]['NAME']
        print(state_name)
    except IndexError:
        pass

geosource_states.selected.on_change('indices', function_geosource)

p = make_plot()
p2 = make_plot_criteria(input_field)
#controls = WidgetBox(year_select)
#controls_2=WidgetBox(select)
p = column(p,WidgetBox(year_select))
p2 = column(p2,WidgetBox(select))
layout = row(p,p2)
curdoc().add_root(layout)
