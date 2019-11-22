import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components

def create_figure(dist, bins):
    hist, edges = np.histogram(dist, bins=bins)
    p = figure(plot_height = 400, plot_width = 600)
    p.quad(bottom=0, top=hist, left=edges[:-1], right=edges[1:])
    p.xaxis.axis_label = "Distance"
    p.yaxis.axis_label = "Count"
    
    return components(p)
