def do_line_plot(df, x_lo, x_mid, x_hi, y, y_err, ax,
                 colour="blue", label="Central Scale"):
    ax.plot(df[x_mid], df[y], color=colour, label=label, linewidth=0.7)

    ax.plot(df[x_mid], df["scale_up"], color=colour,
            label="_nolegend_", alpha=0.5, linewidth=0.5)
    ax.plot(df[x_mid], df["scale_down"], color=colour,
            label="_nolegend_", alpha=0.5, linewidth=0.5)

    ax.fill_between(df[x_mid], df["scale_up"], df["scale_down"],
                    color=colour, alpha=0.2)
    ax.errorbar(df[x_mid], df[y], df[y_err],
                color=colour, label="_nolegend_")


def do_hist_plot(df, x_lo, x_mid, x_hi, y, y_err, ax,
                 colour="blue", label="Central Scale"):
    ax.plot(df[x_hi], df[y],
            drawstyle="steps-pre", color=colour, label="_nolegend_")
    ax.plot(df[x_lo], df[y],
            drawstyle="steps-post", color=colour, label=label)

    ax.plot(df[x_hi], df["scale_up"],
            drawstyle="steps-pre", color=colour, label="_nolegend_",
            alpha=0.5, linewidth=0.5)
    ax.plot(df[x_lo], df["scale_up"],
            drawstyle="steps-post", color=colour, label="_nolegend_",
            alpha=0.5, linewidth=0.5)

    ax.plot(df[x_hi], df["scale_down"],
            drawstyle="steps-pre", color=colour, label="_nolegend_",
            alpha=0.5, linewidth=0.5)
    ax.plot(df[x_lo], df["scale_down"],
            drawstyle="steps-post", color=colour, label="_nolegend_",
            alpha=0.5, linewidth=0.5)

    ax.fill_between(df[x_hi], df["scale_up"], df["scale_down"], step="pre",
                    color=colour, alpha=0.1)
    # [:2] such that we don't double fill_between certain entries...
    ax.fill_between(df[x_lo][:2], df["scale_up"][:2], df["scale_down"][:2],
                    step="post", color=colour, alpha=0.1)

    ax.errorbar(df[x_mid], df[y], df[y_err],
                color=colour, label="_nolegend_",
                fmt="o", markersize=0)
