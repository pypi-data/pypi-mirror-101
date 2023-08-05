from __future__ import annotations
from typing import Optional, Union

import numpy as np  # type: ignore


class Transformation:
    """This class can be used to construct affine transformation for two
    dimensional homogeneous coordinates (e.g. coordinates of the form form
    $(x, y, 1)$.

    """
    def __init__(self):
        self._matrices = []

    @property
    def matrices(self):
        """List[np.ndarray]: List of 3x3 affine transformation matrices, sorted
        by order of application."""
        return self._matrices

    def apply(self, vectors: np.ndarray) -> np.ndarray:
        """
        Apply transformations to array of two dimensional homogeneous
        coordinates.

        Args:
            vectors (np.ndarray): coordinates with shape (Any, 3) with
                                  `vectors[:, 2] == 1`.

        Returns:
            np.ndarray: Transformed coordinates.
        """
        for matrix in self._matrices:
            vectors = (matrix @ vectors.T).T
        return vectors

    def shift(self, t: np.ndarray) -> Transformation:
        """
        Add shift given by `t = (tx, ty)`.
        Args:
            t (ndarray): shift vector with shape (2,).

        Returns:
            Transformation: self
        """
        t = np.asarray(t)
        if t.shape != (2,):
            raise ValueError

        m = np.eye(3)
        m[:2, 2] = t

        self._matrices.append(m)
        return self

    def rotate(
            self,
            angle: float,
            origin: Optional[np.ndarray] = None
    ) -> Transformation:
        """
        Add counterclockwise rotation given ba angle `angle` and origin
        `origin`. If `origin` is `None`, `(0, 0)` will be used as origin.

        Args:
            angle (floats): rotation angle.
            origin (np.ndarray, optional): origin of rotation with shape (2,),
                                           default to `None`

        Returns:
            Transformation: self
        """
        angle = float(angle)
        origin = np.asarray(origin)
        if origin.shape != (2,):
            raise ValueError

        m = np.eye(3)
        m[0, 0] = m[1, 1] = np.cos(angle)
        m[1, 0] = np.sin(angle)
        m[0, 1] = -m[1, 0]

        self.shift(-origin)
        self._matrices.append(m)
        self.shift(origin)
        return self

    def scale(
            self,
            s: Union[float, np.ndarray],
            origin: Optional[np.ndarray] = None
    ):
        """
        Scale by `s` isotropically or `s = (sx, sy)` about `origin`. If `origin`
        is `None`, `(0, 0)` will be used as origin.

        Args:
            s (float or np.ndarray): scale factor or scale vector of shape (2,)
            origin (np.ndarray, optional):  origin of scaling with shape (2,),
                                            default to `None`

        Returns:
            Transformation: self
        """
        try:
            s = float(s)
            s = np.array((s, s))
        except TypeError:
            s = np.asarray(s)
            if s.shape != (2,):
                raise ValueError

        origin = np.asarray(origin)
        if origin.shape != (2,):
            raise ValueError

        m = np.eye(3)
        m[0, 0] = s[0]
        m[1, 1] = s[1]
        self.shift(-origin)
        self._matrices.append(m)
        self.shift(origin)
        return self

    def reflect(self, axis: np.ndarray) -> Transformation:
        """
        Reflect about axis `axis = (x,y)`.

        Args:
            axis (np.ndarray): reflection axis. Note, that axis will be
                               normalized.

        Returns:
            Transformation: self
        """
        axis = np.asarray(axis, dtype=float)
        if axis.shape != (2,):
            raise ValueError

        m = np.eye(3)
        m[1, 1] = -1.

        u = np.zeros(3)
        u[:2] = axis / np.sqrt(axis[0]*axis[0] + axis[1]*axis[1])
        v = np.array([-u[1], u[0], 0.])

        r = np.asarray([u, v, np.array([0., 0., 1.])])

        self._matrices.append(r.T @ (m @ r))

        return self

    def affine(self, m: np.ndarray) -> Transformation:
        """
        Apply affine transformation matrix `m`. Note, that `m`'s last row should
        be $(0, 0, 1)$

        Args:
            m (np.ndarray): matrix of shape (3, 3)

        Returns:
            Transformation: self
        """
        m = np.asarray(m, dtype=float)
        if m.shape != (3, 3):
            raise ValueError
        self._matrices.append(m)
        return self


Trafo = Transformation
"""Shorthand alias for Transformation"""
