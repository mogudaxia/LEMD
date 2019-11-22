import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components


def create_figure(dist, title, bins):
    hist, edges = np.histogram(dist, bins=bins)
    p = figure(title=title, plot_height=400, plot_width=600, tools='', background_fill_color="#fafafa")
    p.quad(bottom=0, top=hist, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.xaxis.axis_label = "Distance"
    p.yaxis.axis_label = "Count"
    p.grid.grid_line_color = "white"

    return components(p)
