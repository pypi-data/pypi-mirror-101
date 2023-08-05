from typing import List, Dict, Tuple, Optional, Union, Any

import numpy as np  # type: ignore
import nptyping as npt  # type: ignore

from .transformation import Trafo, Transformation

PointTypeInt = Tuple[int, int]
"""point type (int) for type hints"""

SegmentTypeInt = List[List[PointTypeInt]]
"""segment type (int) for type hints"""


class Glyph(Transformation):
    """
    Class is used to represent glyphs.
    """
    def __init__(self, index: int, left_adv: int, right_adv: int, segments: SegmentTypeInt):
        """
        Args:
            index (int): glyph index
            left_adv (int): left advance (distance from glyph's center to previous character)
            right_adv (int): right advance (distance from glyph's center to  next character)
            segments (SegmentType): list of segments
        """
        super().__init__()

        self._index = index
        self._left_adv = float(abs(left_adv))
        self._right_adv = float(abs(right_adv))

        self._segments: List[npt.NDArray[(Any, 2), float]] = []
        for segment in segments:
            self._segments.append(
                np.pad(np.asarray(segment, dtype=float), [(0, 0), (0, 1)], 'constant', constant_values=(1.,))
            )


    @staticmethod
    def _apply_trafo(segments, trafo):
        transf_segments = []
        for i in range(len(segments)):
            transf_segments.append(trafo.apply(segments[i]))
        return transf_segments

    @staticmethod
    def _calc_bounding_box(
            segments: List[npt.NDArray[(Any, 2), float]]
    ) -> Optional[Tuple[npt.NDArray[2, float], npt.NDArray[2, float]]]:
        if len(segments) > 0:
            flattened = np.vstack(segments)
            min_x = np.min(flattened[:, 0])
            max_x = np.max(flattened[:, 0])
            min_y = np.min(flattened[:, 1])
            max_y = np.max(flattened[:, 1])
            return np.array((min_x, min_y)),  np.array((max_x, max_y))
        else:
            return None

    @classmethod
    def _from_dict(cls, index: int, glyph_dict: Dict[str, Any]):
        return cls(index, glyph_dict['left_pos'], glyph_dict['right_pos'], glyph_dict['segments'])

    @property
    def index(self) -> int:
        """int: index"""
        return self._index

    @property
    def left_adv(self) -> float:
        """float: left advance (see :meth:`__init__` for definition)"""
        return self._left_adv

    @property
    def right_adv(self) -> float:
        """float: right advance (see :meth:`__init__` for definition)"""
        return self._right_adv

    @property
    def center(self) -> Optional[npt.NDArray[2, float]]:
        bbox: Optional[npt.NDArray[2, float], npt.NDArray[2, float]] = self.bounding_box
        if bbox:
            ll, ur = bbox
            return (ur + ll) / 2
        return None

    @property
    def segments(self) -> List[npt.NDArray[(Any, 2), float]]:
        """SegmentType: list of segments"""
        return [segment[:, :2] for segment in self._apply_trafo(self._segments, self)]

    @property
    def bounding_box(self) -> Optional[Union[npt.NDArray[2, float], npt.NDArray[2, float]]]:
        """Optional[Tuple[PointType, PointType]]: lower left and upper right positions of glyph's bounding box.
        If the glyph is empty, the bounding box is `None`."""
        return self._calc_bounding_box(self.segments)

    def shift(self, t: npt.NDArray[2, float]):
        return super().shift(t)

    def _parse_origin(self, origin: Union[str, npt.NDArray[2, float]]):
        if isinstance(origin, str):
            if origin == 'local':
                return self.center
            elif origin == 'global':
                return 0., 0.
            else:
                raise ValueError
        else:
            return origin

    def rotate(self, angle: float, origin: Union[str, npt.NDArray[2, float]] = 'local'):
        return super().rotate(angle, self._parse_origin(origin))

    def scale(self, s, origin: Union[str, npt.NDArray[2, float]] = 'local'):
        return super().scale(s, self._parse_origin(origin))

    def reflect(self, axis, origin: Union[str, npt.NDArray[2, float]] = 'local'):
        return super().reflect(axis, self._parse_origin(origin))
