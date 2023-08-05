from __future__ import annotations

from typing import Dict, Any, Tuple


class GlyphView:
    """
        Class contains glyph info. See `<https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/TextAndWebiPhoneOS/TypoFeatures/TextSystemFeatures.html>`_
        for definition of the provided glyph metrics.
    """
    def __init__(self, index: int, database_item: Dict[str, Any]):
        """Create a GlyphView. Should not be called by the user.

            Args:
                index (int): glyph index
                database_item (Dict[str, Any]): a reference to the database dictionary
        """
        self._index = index
        self._database_item = database_item

        self._font_size: float = 1.

    def clone(self, reset: bool = False) -> GlyphView:
        """Clone a GlyphView.

            Args:
                reset (bool, optional): if False, the current font size is inhereted and otherwise set to 1. Default to False.
        """
        if reset:
            return GlyphView(self._index, self._database_item)
        else:
            new_view = GlyphView(self._index, self._database_item)
            new_view._font_size = self._font_size
            return new_view

    @property
    def index(self) -> int:
        """glyph index"""
        return self._index

    @property
    def segments(self) -> Tuple:
        """Tuple: segments of the glyph scaled to current font size."""
        return tuple((tuple((self._font_size * point[0], self._font_size * point[1]) for point in seg) for seg in self._database_item['segments']))

    @property
    def bounding_box(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Tuple[Tuple[float, float], Tuple[float, float]]: bounding box (lower left, upper right) scaled to current font size."""
        min_x, min_y = self._database_item['bounding_box'][0]
        max_x, max_y = self._database_item['bounding_box'][1]

        return (self._font_size * min_x, self._font_size * min_y), (self._font_size * max_x, self._font_size * max_y)

    @property
    def width(self) -> float:
        """float: width of bounding box scaled to current font size"""
        return self._font_size * self._database_item['width']

    @property
    def height(self) -> float:
        """float: height of bounding box scaled to current font size"""
        return self._font_size * self._database_item['height']

    @property
    def left_bearing(self) -> float:
        """float: leaft bearing scaled to current font size"""
        return self._font_size * self._database_item['left_bearing']

    @property
    def right_bearing(self) -> float:
        """float: right bearing scaled to current font size"""
        return self._font_size * self._database_item['right_bearing']

    @property
    def ascent(self) -> float:
        """float:ascent scaled to current font size"""
        return self._font_size * self._database_item['ascent']

    @property
    def descent(self) -> float:
        """float: descent scaled to current font size"""
        return self._font_size * self._database_item['descent']

    @property
    def advance_width(self) -> float:
        """float: advance width scaled to current font size"""
        return self._font_size * self._database_item['advance_width']

    @property
    def font_size(self):
        """float: font size"""
        return self._font_size

    @font_size.setter
    def font_size(self, value: float):
        self._font_size = float(value)

        if self._font_size <= 0.:
            raise ValueError('font size must be greater than 0.')
