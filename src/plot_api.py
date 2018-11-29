import matplotlib.pyplot as plt
import src.plot_modes as pm


def plot_scale_variation(df, ax=None, colour="blue", name="Central Scale",
                         mode="hist", ylabel=None, grid=False, logx=False,
                         logy=False, do_title=True, figsize=(10, 10)):
    """ Example plot function, with choice of histogram or line type plot.
    plt.show() must be called afterwards."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    x_lo, x_mid, x_hi, y, y_err = df.columns[0:5]
    pm.PLOT_MODES[mode](df, x_lo, x_mid, x_hi, y, y_err, ax,
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
    ax.legend()
