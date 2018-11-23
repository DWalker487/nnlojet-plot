#!/usr/bin/python3
""" Example script to interface pandas with NNLOJET result files.
For more info, run
        python3 nnlojet_plot.py --help
"""
import argparse as ap
import config
import matplotlib.pyplot as plt
import os
import src.plot_types as pt
import src.plot_modes as pm
import src.plot_api as papi
import src.utilities as util


def read_args():
    """ Function wrapping all command line argument parsing. """
    parser = ap.ArgumentParser(description="NNLOJET data functionality.")
    parser.add_argument("infiles",
                        help="NNLOJET infile(s) to plot.", nargs="+")
    parser.add_argument("--mode", "-m",
                        help="Plot mode: histogram plot or line plot",
                        choices=pm.PLOT_MODES.keys(), default="hist")
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
    colours = util.colour_gen(config.ALLOWED_COLOURS)
    alldata = {}
    for NNLOJETfile in args.infiles:
        data = util.load_NNLOJET_file(NNLOJETfile)
        alldata[NNLOJETfile] = data
        papi.plot_scale_variation(data, ax, colour=next(colours),
                                  name=os.path.basename(NNLOJETfile),
                                  mode=args.mode, grid=args.grid, logy=args.logy,
                                  logx=args.logx, figsize=config.FIGSIZE)

    if args.savefig is not None and not args.combine:
        plt.savefig(args.savefig)

    if args.ratio is not None:
        colours = util.colour_gen(config.ALLOWED_COLOURS)
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
            papi.plot_scale_variation(ratio_df, ax, colour=next(colours),
                                      name=fname, mode=args.mode,
                                      ylabel=ylabel,
                                      grid=args.grid, logx=args.logx,
                                      do_title=False, figsize=config.FIGSIZE)

    if args.savefig is not None:
        if not args.combine: # Save ratio as separate figure
            name_pieces = args.savefig.split(".")
            ratio_fname = ".".join(name_pieces[:-1])+"_ratio." + name_pieces[-1]
            plt.savefig(ratio_fname)
        else:
            plt.savefig(args.savefig)

    if not args.noshow:
        plt.show()
