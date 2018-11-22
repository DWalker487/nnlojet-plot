#!/usr/bin/python3
""" Example script to interface pandas with NNLOJET result files.
For more info, run
        python3 nnlojet_plot.py --help
"""
import argparse as ap
import config
import matplotlib.pyplot as plt
import os
import plot_types as pt
import utilities as util

PLOT_MODES = {"hist": pt.do_hist_plot,
              "h": pt.do_hist_plot,
              "l": pt.do_line_plot,
              "line": pt.do_line_plot}


def read_args():
    """ Function wrapping all command line argument parsing. """
    parser = ap.ArgumentParser(description="NNLOJET data functionality.")
    parser.add_argument("infiles", help="NNLOJET infile(s) to plot.", nargs="+")
    parser.add_argument("--mode", "-m", help="Plot mode: histogram plot or line plot",
                        choices=PLOT_MODES.keys(), default="hist")
    parser.add_argument("--ratio", "-r", help="Plot the ratio of all input files to this file")
    parser.add_argument("--savefig", "-s", help="Save figure to file with given name")
    args = parser.parse_args()
    return args


def colour_gen():
    """ Generator that iterates through a colour set."""
    while True:
        for col in config.ALLOWED_COLOURS:
            yield col


def plot_scale_variation(df, ax=None, colour="blue", name="Central Scale",
                         mode="hist"):
    """ Example plot function, with choice of histogram or line type plot.
    plt.show() must be called afterwards."""
    if ax is None:
        fig, ax = plt.subplots()
    x_lo, x_mid, x_hi, y, y_err = df.columns[0:5]
    PLOT_MODES[mode](df, x_lo, x_mid, x_hi, y, y_err, ax,
                     label=name, colour=colour)
    ax.set_xlim((data[data.columns[0]].min(), data[data.columns[2]].max()))
    x_mid_name = "_".join(x_mid.split("_")[:-1])
    ax.set_xlabel(x_mid_name)
    ax.set_title(x_mid_name)
    ax.set_ylabel("dsigma/d{0}".format(x_mid_name))
    plt.legend()


if __name__ == "__main__":
    args = read_args()
    fig, ax = plt.subplots()
    colours = colour_gen()
    alldata = {}
    for NNLOJETfile in args.infiles:
        data = util.load_NNLOJET_file(NNLOJETfile)
        alldata[NNLOJETfile] = data
        plot_scale_variation(data, ax, colour=next(colours),
                             name=os.path.basename(NNLOJETfile),
                             mode=args.mode)

    if args.savefig is not None:
        plt.savefig(args.savefig)
    if args.ratio is not None:
        colours = colour_gen()
        fig, ax = plt.subplots()
        baseline = alldata[args.ratio]
        for fname in alldata.keys():
            values = alldata[fname]
            ratio_df = util.ratio_NNLOJET_files(values, baseline)
            fname = "{0}/{1}".format(os.path.basename(fname),
                                     os.path.basename(args.ratio))
            plot_scale_variation(ratio_df, ax, colour=next(colours),
                                 name=fname,
                                 mode=args.mode)
    if args.savefig is not None:
        name_pieces = args.savefig.split(".")
        ratio_fname = ".".join(name_pieces[:-1])+"_ratio." + name_pieces[-1]
        plt.savefig(ratio_fname)
    plt.show()
