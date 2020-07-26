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
import time
from bokeh.events import Tap

def make_dataset_state(cnt_data, yr, shouldGetAll):
    merged_select = []

    if shouldGetAll:
        merged_select = cnt_data
    else:
        yr_selected = cnt_data["YEAR"] == yr
        merged_select = cnt_data[yr_selected]

    merged_json = json.loads(merged_select.to_json())
    json_data = json.dumps(merged_json)
    return(json_data)

def make_dataset_cnt(st_data, yr, state_fips, shouldGetAll):
    merged_select = []

    # create 2000 election year data frame
    if shouldGetAll:
        merged_select = st_data
    else:
        yr_selected = st_data["YEAR"] == yr
        merged_select = st_data[yr_selected]
        merged_select = merged_select.loc[merged_select["STATE_FIPS"].isin([state_fips])]

    merged_json = json.loads(merged_select.to_json())
    json_data = json.dumps(merged_json)
    return(json_data)

def make_plot_st(geo_src):
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
           toolbar_location = "below")

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


def make_plot_cnt(geo_src):
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

    #taptool = TapTool()


    # create figure object
    plot = figure(title = 'Test Bokeh Map',
               plot_height = 600 ,
               plot_width = 950,
               toolbar_location = 'below')

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None

    #plot.patches('xs','ys', source = geosource_states,fill_alpha=0.0,
    #          line_color="#884444", line_width=2, line_alpha=0.3)

    # add patch renderer to figure.
    county = plot.patches('xs','ys', source = geo_src,
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

    #plot.add_tools(taptool)


    #plot.js_on_event(Tap, callbackStateClick)

    return plot

#TODO: obsolete
def update(attr, old, new):
        new_src = make_dataset(int(new))

        geo_src.geojson = new_src

        p = make_plot()
        controls = WidgetBox(year_select)
        layout = row(p, controls)
        curdoc().clear()
        curdoc().add_root(layout)

def get_county_data():

    pd.set_option("display.max_columns", None)
    combined_df = pd.read_csv("data/elections/Input_Output_Jul07.csv", encoding = "ISO-8859-1")
    combined_df['FIPS']=combined_df['STATE_FIPS']*1000 + combined_df['COUNTY_FIPS']
    counties_usa = gpd.read_file("bokeh/cb_2018_us_county_20m.shp")
    counties_usa["GEOID"] = counties_usa["GEOID"].astype("float64")
    merged_counties = counties_usa.merge(combined_df, left_on="GEOID", right_on="FIPS")
    merged_counties = merged_counties.loc[~merged_counties["STATE"].isin(["Alaska", "Hawaii"])]

    return merged_counties

def get_state_data():
    state_data = "data/elections/state_aggregated_0723.csv"
    state_df = pd.read_csv(state_data, encoding = "ISO-8859-1")
    states_usa = gpd.read_file("bokeh/cb_2018_us_state_20m.shp")
    states_usa = states_usa.loc[~states_usa["NAME"].isin(["Alaska", "Hawaii"])]
    states_usa["STATEFP"] = states_usa["STATEFP"].astype("int64")
    merged_states = states_usa.merge(state_df, left_on="STATEFP", right_on="STATE_FIPS")
    return merged_states

def init_data():
    merged_counties = get_county_data()
    merged_states = get_state_data()

    return merged_counties, merged_states

def get_electmap_with_controls():

    #start = time.time()
    merged_cnt_data, merged_st_data = init_data()
    #end = time.time()
    #print("init_data time={}".format(str(end-start)))

    year_select = Slider(start = 2000, end = 2020,
                         step = 4, value = 2000,
                         title = 'Election Year')

    st_fips = 4

    #start = time.time()
    geo_src_c = GeoJSONDataSource(geojson = make_dataset_cnt(merged_cnt_data, year_select.value, 0, True))
    geo_src_s = GeoJSONDataSource(geojson = make_dataset_state(merged_st_data, year_select.value, True))
    #end = time.time()
    #print("geo_src time={}".format(str(end-start)))

    #start = time.time()
    curr_geo_src_c = GeoJSONDataSource(geojson = make_dataset_cnt(merged_cnt_data, 2000, st_fips, False))
    curr_geo_src_s = GeoJSONDataSource(geojson = make_dataset_state(merged_st_data, 2000, False))
    #end = time.time()
    #print("curr_geo_src time={}".format(str(end-start)))

    #slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")


    callbackSelector = CustomJS(
        args=dict(
            source_s=geo_src_s, currsource_s=curr_geo_src_s, source_c=geo_src_c, currsource_c=curr_geo_src_c), 
            code="""

    //var c_data = source_s.data;
    var yr = cb_obj.value;

    for(var key in source_s.data){
      currsource_s.data[key] = [];
    }

    for (var i = 0; i <= source_s.data['YEAR'].length; i++){
        if (source_s.data['YEAR'][i] == yr){
            for(var key in source_s.data){
                currsource_s.data[key].push(source_s.data[key][i]);
            }
        }
    }

    var st_fip = currsource_c.data['STATE_FIPS'][0];

    console.log(st_fip);

    for (var i = 0; i <= source_c.data['YEAR'].length; i++){
        if (source_c.data['YEAR'][i] == yr && source_c.data['STATE_FIPS'][i] == st_fip){
            for(var key in source_c.data){
                currsource_c.data[key].push(source_c.data[key][i]);
            }
        }
    }

    currsource_s.change.emit();
    currsource_c.change.emit();

    """)

    year_select.js_on_change('value', callbackSelector)


    

    #curr_geo_src_s.js_on_event('value', callbackStateClick)

    #start = time.time()
    p_c = make_plot_cnt(curr_geo_src_c)
    p_s = make_plot_st(curr_geo_src_s)


    callbackStateClick = CustomJS(
        args=dict(
            source=curr_geo_src_s, source_c=geo_src_c, source_curr_c=curr_geo_src_c), 
            code="""

    var st_fip = 0;

    for(var key in source.data){
        if (key == 'STATE_FIPS')
        {
            st_fip = source.data['STATE_FIPS'][source.selected.indices[0]];
        }
    }

    for(var key in source_c.data){
      source_curr_c.data[key] = [];
    }

    for (var i = 0; i <= source_c.data['YEAR'].length; i++){
        if (source_c.data['STATE_FIPS'][i] == st_fip){
            for(var key in source_c.data){
                source_curr_c.data[key].push(source_c.data[key][i]);
            }
        }
    }

    source_curr_c.change.emit();

    """)

    taptool = TapTool(callback=callbackStateClick)

    p_s.add_tools(taptool)


    #p_s.js_on_event('value', callbackStateClick)

    controls = WidgetBox(year_select)
    layout = row(p_s, p_c, controls)
    #end = time.time()
    #print("plot time={}", str(end-start))


    return layout

    #curdoc().add_root(layout)
