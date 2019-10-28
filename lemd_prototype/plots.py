import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

def get_test_figures():
    plt.plot([1,2,3,4])
    bytes_image = BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

def plot_dist(dist):
    rc = {"font.family":"serif", "mathtext.fontset":"stix"}
    plt.rcParams.update(rc)
    plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    
    hist_start = 0.0
    hist_end = 0.5
    hist_segs = 25
    bins = np.linspace(hist_start, hist_end, hist_segs)
    d_hist = plt.hist(dist, bins, label = "Input Structure")
    for i in range(len(d_hist[0])):
        if d_hist[0][i] != 0:
            plt.text(d_hist[1][i] - 0.001, d_hist[0][i] + 0.8, str(int(d_hist[0][i])), fontsize=12) 
    
    plt.xlabel(r"Distance", fontsize=18)
    plt.ylabel(r"Count", fontsize=18)
    plt.legend(fontsize=12)
    plt.tick_params(axis="x", labelsize=12)
    plt.tick_params(axis="y", labelsize=12)
    bytes_image = BytesIO()
    plt.tight_layout()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
