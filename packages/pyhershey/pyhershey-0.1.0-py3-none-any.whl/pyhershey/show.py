from typing import Dict, List, Optional, Tuple

try:
    import matplotlib.pyplot as plt
    import matplotlib.axes as axes
    import matplotlib.ticker as ticker
except ImportError as ie:
    raise RuntimeError('Matplotlib not found. Please install it manually.') from ie

from pyhershey.glyph_view import GlyphView


def plot_glyph(glyph: GlyphView, ax: axes.Axes, with_marks: bool = True, pos: Optional[Tuple[float, float]] = None) -> None:
    """
    Plots a :class:`~pyhershey.glyph.Glyph` to matplotlib axis object.

    Args:
        glyph (:class:`~pyhershey.glyph.Glyph`): :class:`~pyhershey.glyph.Glyph` to be plotted
        ax (:class:`matplotlib.axes.Axes`): matplotlib :class:`matplotlib.axes.Axes` object to be plotted on
        with_marks (bool): print marks with baseline and left and right advance

    Returns:
        None

    """
    if not pos:
        pos = (0, 0)

    if with_marks:
        # baseline
        ax.plot([-37, 37], [0, 0], 'c-', linewidth=1)

        # plot left and right limits
        ax.plot([-glyph.advance_width / 2]*2, [5, 15], 'k--',  linewidth=1)
        ax.plot([glyph.advance_width / 2]*2, [5, 15], 'k--',  linewidth=1)

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
    
    # segments
    for segment in glyph.segments:
        # TODO: or use numpy directly!?

        x = [point[0] - glyph.advance_width / 2 + pos[0] for point in segment]
        y = [point[1]  + pos[1] for point in segment]

        ax.plot(x, y, 'ko-', linewidth=1, markersize=3)  # fillstyle='none'


def show_glyph(glyph: GlyphView, with_marks: bool = True) -> None:
    """
    Displays a :class:`~pyhershey.glyph.Glyph` with `matplotlib`.

    Args:
        glyph (Glyph): glyph to be displayed
        with_marks (bool): print marks with baseline and left and right advance

    """
    fig, ax = plt.subplots()
    plot_glyph(glyph, ax, with_marks)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()


def show_shaped_glyphs(shaped_text: List[Dict]):
    """
    Displays shaped glyphs returned by the :func:`~pyhershey.shape_text.shape_text` function.

    """
    fig, ax = plt.subplots()

    for shaped_glyph in shaped_text:
        plot_glyph(shaped_glyph['glyph'], ax, with_marks=False, pos=shaped_glyph['pos'])

    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()