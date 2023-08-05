import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.ticker as ticker

from .glyph import Glyph


def plot_glyph(glyph: Glyph, ax: axes.Axes) -> None:
    """
    Plots a :class:`~pyhershey.glyph.Glyph` to matplotlib axis object.

    Args:
        glyph (:class:`~pyhershey.glyph.Glyph`): :class:`~pyhershey.glyph.Glyph` to be plotted
        ax (:class:`matplotlib.axes.Axes`): matplotlib :class:`matplotlib.axes.Axes` object to be plotted on

    """
    # baseline
    ax.plot([-37, 37], [0, 0], 'c-', linewidth=1)
    # segments
    for segment in glyph.segments_as_ndarray():
        ax.plot(segment[:, 0], segment[:, 1], 'ko-', linewidth=1, markersize=3, fillstyle='none')

    # plot left and right limits
    ax.plot([glyph.left]*2, [5, 15], 'k--',  linewidth=1)
    ax.plot([glyph.right]*2, [5, 15], 'k--',  linewidth=1)

    ax.set_xlim(-17, 17)
    ax.set_ylim(-12, 32)

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))

    # ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=5)

    ax.set_aspect('equal')


def show(glyph: Glyph) -> None:
    """
    Displays a :class:`~pyhershey.glyph.Glyph` with `matplotlib`.

    Args:
        glyph: :class:`~pyhershey.glyph.Glyph` to be displayed

    """
    fig, ax = plt.subplots()
    plot_glyph(glyph, ax)
    plt.tight_layout()
    plt.show()
