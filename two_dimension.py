#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import requried libraries and Bokeh functions
import os

from bokeh.embed import components
from bokeh.models import Button, CustomJS
from bokeh.io import curdoc
from bokeh.io import output_notebook
import numpy as np
import pandas as pd
import math
import scipy.integrate as integrate
from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, ColumnDataSource, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import transform
from bokeh.palettes import Viridis256

np.set_printoptions(threshold=np.inf)
pd.options.display.max_seq_items = 2000

import timeit

start = timeit.timeit()
import bokeh.plotting.figure as bk_figure
from bokeh.io import curdoc, show
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler

# output_file('2D_Bokeh.html')
# output_notebook()
# Set initial data
v = 2.55
a = 0.1
time = 20
bt = Button(label='Generate Plot')



# calculate the Z data values and return a dataframe

def calculate_z(v, a, time):
    x = np.linspace(2, 10000, 100)
    y = np.linspace(-2000, 2000, 100)
    C = np.zeros([len(x), len(y)])

    b = 20
    t = time * 365
    for i in range(0, len(x)):
        DL = (v * 0.83 * (math.log10(x[i])) ** 2.414)
        Dt = a * DL
        for j in range(0, len(y)):
            def f(r):
                return math.exp((-((x[i] - (v * r)) ** 2) / (4 * DL * r)) - (((y[j]) ** 2) / (4 * Dt * r))) * (1 / r)

            results, err = integrate.quad(f, 0, t)
            C[i, j] = ((5 * 2 * 10 ** 8 / b) / (4 * math.pi * ((DL * Dt) ** 0.5))) * results
    CC = np.transpose(C)
    CCC = np.clip(CC, 0, 5)

    df = pd.DataFrame(
        CCC,
        columns=x,
        index=y)
    df.columns.name = 'x'
    df.index.name = 'y'
    df = df.stack().rename("value").reset_index()

    return x, y, df


# calculate the dataframe
x, y, df = calculate_z(v, a, time)
source = ColumnDataSource(data=dict(df))
# colormap =cm.get_cmap("BuPu")
# bokehpalette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]


colors = ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']
mapper = LinearColorMapper(palette=Viridis256, low=df.value.min(), high=df.value.max())

plot = figure(title="Concentration Signals (2 Dimension)")
plot.rect(x="x", y="y", width=(max(x) - min(x)) / len(x), height=(max(y) - min(y)) / len(y), source=source,
          fill_color=transform('value', mapper), line_color=None)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0), ticker=BasicTicker(desired_num_ticks=10))
# color_bar.set_label('Concentration')
plot.xaxis.axis_label = 'Horizontal Distance (m)'
plot.yaxis.axis_label = 'Vertical Distance (m)'
plot.add_layout(color_bar, 'right')

# Set up widgets aka. sliders and text box
text = TextInput(title="title", value='Concentration Signals (2 Dimension)')
vv = Slider(title="Velocity (m/day)", value=2.55, start=0.1, end=5, step=1)
tt = Slider(title="Time (Year)", value=20, start=1, end=100, step=5)
aa = Slider(title="Dispersion Factor", value=0.1, start=0.05, end=0.2, step=0.05)


# bb = Slider(title="Aquifer Thickness (m)", value=1.52, start=1, end=50, step=1)
def update_title(attrname, old, new):
    plot.title.text = text.value


def update_data():
    # Get the current slider values
    v = vv.value
    time = tt.value
    a = aa.value
    # b = bb.value

    # Generate the new curve using the new dataframe
    x, y, df = calculate_z(v, a, time)
    source.data = dict(df)


text.on_change('value', update_title)
# update data on button press
bt.on_click(update_data)


# Set up layouts and add to document
inputs = widgetbox(text, vv, tt, aa, bt)
layout = row(plot, widgetbox(text, vv, tt, aa, bt))

# curdoc().add_root(layout)
# curdoc().title = "Concentration Signals"

"""
Export bokeh objects for use in html
"""

script, div = components({
    "Plot": plot,
    "Inputs": inputs
})

filename = "app/templates/bokeh_output/2d_scripts.html"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(script)

filename = "app/templates/bokeh_output/2d_div.html"
os.makedirs(os.path.dirname(filename), exist_ok=True)
f = open(filename, "w")
for key, value in div.items():
    f.write(str(value))
f.close()
