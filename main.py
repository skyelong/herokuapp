# -*- coding: utf-8 -*-

##Interactive bokeh for cross location selection
import numpy as np
import pandas as pd
from bokeh.io import curdoc,show
from bokeh.layouts import row,column, widgetbox
from bokeh.models import ColumnDataSource,LabelSet,Div,PointDrawTool,PolyDrawTool,PolyEditTool,PolySelectTool,CustomJS
from bokeh.models.widgets import Slider, TextInput,Button,CheckboxGroup,RadioButtonGroup,RadioGroup,Select,DataTable, TableColumn
from bokeh.plotting import figure
import scipy.spatial as spatial

df = pd.read_csv('/Users/samirakumar/Desktop/Samir/Crosses/crosses_updated.csv')
headers = ["cross_id", "x", "y","pass_end_x", "pass_end_y"]
crosses = pd.DataFrame(df, columns=headers)

source = ColumnDataSource({
    'x': [89], 'y': [9.5], 'color': ['dodgerblue']
})

ix = source.data['x']
iy = source.data['y']
points = np.array(crosses[['x','y']])

t1 = np.vstack((ix, iy)).T
t2=np.vstack((crosses.x,crosses.y)).T

point_tree = spatial.cKDTree(t2)

ax=(point_tree.query_ball_point(t1, 6)).tolist()

cx=crosses.pass_end_x[ax[0]]
cy=crosses.pass_end_y[ax[0]]

source2 = ColumnDataSource({
    'cx': [cx], 'cy': [cy]
})

source2 = ColumnDataSource(data=dict(cx=cx,cy=cy))

# Set up plot

plot = figure(plot_height=600, plot_width=800,
              tools="reset,save",
              x_range=[0,100], y_range=[0,100],toolbar_location="below",toolbar_sticky=False)
plot.image_url(url=["myapp/static/images/base.png"],x=0,y=0,w=100,h=100,anchor="bottom_left")


st=plot.scatter('x','y',source=source,size=20,fill_color='deepskyblue',line_color='black',line_width=3)
plot.scatter('cx','cy',source=source2,size=10,fill_color='orangered')

# plot.rect('cx','cy',width=1,height=1,source=source2,fill_color='orangered')


plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None
plot.axis.visible=False

draw_tool = PointDrawTool(renderers=[st])
draw_tool.add=False
columns = [
    #TableColumn(field="x", title="x"),
   # TableColumn(field="y", title="y")
]

data_table = DataTable(
    source=source,
    #columns=columns,
    row_headers=False,
    width=800,
    editable=False,
)

def on_change_data_source(attr, old, new):
    ix = source.data['x']
    iy = source.data['y']

    t1 = np.vstack((ix, iy)).T
    t2 = np.vstack((crosses.x, crosses.y)).T

    point_tree = spatial.cKDTree(t2)

    ax = (point_tree.query_ball_point(t1, 6)).tolist()
    cx = crosses.pass_end_x[ax[0]]
    cy = crosses.pass_end_y[ax[0]]

    source2.data=dict(cx=cx,cy=cy)
    # plot.scatter('cx','cy',source=source2)

source.on_change('data', on_change_data_source)

plot.add_tools(draw_tool)
plot.toolbar.active_tap = draw_tool
div = Div(text="""<b>Where do teams cross?</b></br></br>Interactive tool to get cross end locations based on user input. The tool uses cKDTree to calculate the 
nearest cross start locations and plots the corresponding end locations<br>This was created by <b>Samira Kumar</b></br>""",
width=600, height=80)

layout=column(div,plot,data_table)
curdoc().add_root(layout)
curdoc().title = "Where do teams cross?"

