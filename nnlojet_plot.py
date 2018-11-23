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
import matplotlib

PLOT_MODES = {"hist": pt.do_hist_plot,
              "h": pt.do_hist_plot,
              "l": pt.do_line_plot,
              "line": pt.do_line_plot}



def read_args():
    """ Function wrapping all command line argument parsing. """
    parser = ap.ArgumentParser(description="NNLOJET data functionality.")
    parser.add_argument("infiles",
                        help="NNLOJET infile(s) to plot.", nargs="+")
    parser.add_argument("--mode", "-m",
                        help="Plot mode: histogram plot or line plot",
                        choices=PLOT_MODES.keys(), default="hist")
    parser.add_argument("--ratio", "-r",
                        help="Plot the ratio of all input files to this file")
    parser.add_argument("--grid", "-g", action="store_true",
                        help="Add a grid to the plot")
    parser.add_argument("--savefig", "-s",
                        help="Save figure to file with given name")
    parser.add_argument("--logx", action="store_true",
                        help="Plot output with logarithmic x values")
    parser.add_argument("--logy", action="store_true",
                        help="Plot output with logarithmic y values")
    parser.add_argument("--combine","-c", action="store_true",
                        help="Plot ratio one the same figure as the original plot. Only has an effect in combination with the --ratio command")
    parser.add_argument("--noshow", action="store_true", default=False,
                        help="Include this flag to not display the figures.")
    args = parser.parse_args()

    if args.combine and not args.ratio:
        args.combine = False

    return args


def colour_gen():
    """ Generator that iterates through a colour set."""
    while True:
        for col in config.ALLOWED_COLOURS:
            yield col


def plot_scale_variation(df, ax=None, colour="blue", name="Central Scale",
                         mode="hist", ylabel=None, grid=False, logx=False,
                         logy=False, do_title=True):
    """ Example plot function, with choice of histogram or line type plot.
    plt.show() must be called afterwards."""
    if ax is None:
        fig, ax = plt.subplots(figsize=config.FIGSIZE)
    x_lo, x_mid, x_hi, y, y_err = df.columns[0:5]
    PLOT_MODES[mode](df, x_lo, x_mid, x_hi, y, y_err, ax,
                     label=name, colour=colour)
    ax.set_xlim((df[df.columns[0]].min(), df[df.columns[2]].max()))
    x_mid_name = "_".join(x_mid.split("_")[:-1])
    ax.set_xlabel(x_mid_name)
    if do_title:
        ax.set_title(x_mid_name)
    if ylabel is None:
        ax.set_ylabel("dsigma/d{0}".format(x_mid_name))
    else:
        ax.set_ylabel(ylabel)
    if grid:
        ax.grid()
    if logx:
        ax.set_xscale("log", nonposx='clip')
    if logy:
        ax.set_yscale("log", nonposy='clip')
    plt.legend()


if __name__ == "__main__":
    args = read_args()
    if args.combine:
        fig, axes = plt.subplots(nrows=2, sharex=True,
                                 gridspec_kw={'height_ratios': [3, 1]},
                                 figsize=config.FIGSIZE)
        fig.subplots_adjust(hspace=0)
        ax = axes[0]
    else:
        fig, ax = plt.subplots(figsize=config.FIGSIZE)
    colours = colour_gen()
    alldata = {}
    for NNLOJETfile in args.infiles:
        data = util.load_NNLOJET_file(NNLOJETfile)
        alldata[NNLOJETfile] = data
        plot_scale_variation(data, ax, colour=next(colours),
                             name=os.path.basename(NNLOJETfile),
                             mode=args.mode, grid=args.grid, logy=args.logy,
                             logx=args.logx)

    if args.savefig is not None and not args.combine:
        plt.savefig(args.savefig)

    if args.ratio is not None:
        colours = colour_gen()
        if args.combine:
            ax = axes[1]
        else:
            fig, ax = plt.subplots(figsize=config.FIGSIZE)
        baseline = alldata[args.ratio]
        for fname in alldata.keys():
            values = alldata[fname]
            ratio_df = util.ratio_NNLOJET_files(values, baseline)
            fname = "{0}/{1}".format(os.path.basename(fname),
                                     os.path.basename(args.ratio))
            ylabel = "Ratio to {0}".format(os.path.basename(args.ratio))
            plot_scale_variation(ratio_df, ax, colour=next(colours),
                                 name=fname, mode=args.mode, ylabel=ylabel,
                                 grid=args.grid, logx=args.logx, do_title=False)

    if args.savefig is not None:
        if not args.combine: # Save ratio as separate figure
            name_pieces = args.savefig.split(".")
            ratio_fname = ".".join(name_pieces[:-1])+"_ratio." + name_pieces[-1]
            plt.savefig(ratio_fname)
        else:
            plt.savefig(args.savefig)

    if not args.noshow:
        plt.show()
