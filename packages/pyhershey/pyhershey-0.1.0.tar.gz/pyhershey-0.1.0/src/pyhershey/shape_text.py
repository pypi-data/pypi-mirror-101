from typing import List, Dict, Any, Optional

from pyhershey.glyph_factory import glyph_factory


def shape_text(
    text: str,
    mapping: str,
    advance_height: float,
    font_size: float = 1,
    text_align: str = 'left',
    const_advance_width: Optional[float] = None
) -> List[Dict[str, Any]]:
    """Very basic text shaping for ascii text

    Args:
        text (str): text to be shaped. New lines should be marked with ``\\n``.
        mapping (str): the ascii to hershey mapping to be used (cf. :attr:`~pyhershey.glpyh_factory.GlyphFactory.ascii_mappings`)
        advance_hight (float): the distance between two consecutive base lines. Does not scale with font_size!
        font_size (float, optional): the font size to be used. Default to 1.
        text_align (str, optional): the text alignment. Can be "left", "center" or "right". Default to "left".
        const_advance_width (float, optional): if given, the text advance width is constant (monospaced). Default to None.

    Raises:
        ValueError: if text_align is not "left", "center" or "right".

    Returns:
        List[Dict[str, any]]: list with dictionary for every glyph of style ``[{'glyph': <GlyphView>, 'pos': <Tuple[float, float]>}, ...]``.

    """
    if not text:
        return []

    if text[-1] != '\n':
        text += '\n'

    if text_align not in ['left', 'center', 'right']:
        raise ValueError('text_align must be "left", "center" or "right".')

    shaped_text = []

    current_pos = (0., 0.)
    current_row: List[Dict[str, Any]] = []

    
    for char in text:
        if char == '\n':
            if current_row:
                if text_align == 'center':
                    mean_x = sum([shaped_glyph['pos'][0] for shaped_glyph in current_row]) / len(current_row)
                    mapper = lambda pos: (pos[0] - mean_x, pos[1])
                elif text_align == 'right':
                    max_x = current_row[-1]['pos'][0]

                    mapper = lambda pos: (pos[0] - max_x, pos[1])
                else:
                    mapper = lambda pos: pos

                for shaped_glyph in current_row:
                    shaped_text.append({'glyph': shaped_glyph['glyph'], 'pos': mapper(shaped_glyph['pos'])})
                
                current_row = []

            current_pos = (0, current_pos[1] - advance_height)
        else:
            glyph = glyph_factory.from_ascii(char, mapping)
            glyph.font_size = font_size

            current_row.append({'glyph': glyph, 'pos': current_pos})
            if const_advance_width:
                current_pos = (current_pos[0] + const_advance_width, current_pos[1])
            else:
                current_pos = (current_pos[0] + glyph.advance_width, current_pos[1])
    
    return shaped_text
