import lzma
from typing import List, Iterable, Optional
import toml
import importlib.resources as pkg_resources
import copy

from pyhershey.glyph_view import GlyphView


class GlyphFactory:
    """
    This class manages the access to glyph database.
    """

    def __init__(self, database_file: str):
        """
        Args:
            database_file (str): filename of the compressed database

        Raises:
            RuntimeError: if the database is corrupted.
            FileNotFoundError: if the database is not found.

        """
        try:
            compressed_database = pkg_resources.read_binary('pyhershey', database_file)
            self._database = toml.loads(
                lzma.decompress(compressed_database).decode('utf-8')
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f'The database seems to be missing. Reinstall the package to fix the problem.'
            ) from e
        except Exception as e:
            raise RuntimeError(
                f'Your database seems to be corrupted. Reinstall the package to fix the problem.'
            ) from e

    def from_index(self, index: int) -> GlyphView:
        """
        Creates a :class:`~pyhershey.glyph.Glyph` with given index.

        Args:
            index (int): index of glyph. See docs for complete list all glyphs.

        Returns:
            :class:`~pyhershey.glyph.Glyph`

        """
        try:
            return GlyphView(
                index, copy.deepcopy(self._database['glyphs'][str(index)])
            )
        except KeyError as e:
            raise ValueError(f'Glyph with index {index} is not in glyph database.') from e

    def from_ascii(self, char: str, mapping: str) -> GlyphView:
        """Creates a :class:`~pyhershey.glyph.Glyph` with given ascii value, font style and font type.

        Additionally, "°" can be passed as char.

        Args:
            char (str): ascii character
            mapping (str): ascii mapping to be used

        Returns:
            :class:`~pyhershey.glyph.Glyph`

        Raises:
            ValueError: if mapping does not exist, ascii character is not found in mapping or chr is not an ascii character.

        """
        ascii_index = ord(char) - 32  # chr(32) is the first printable ascii char
        if ascii_index == 144:  # == ord('°') - 32
            ascii_index = 97

        elif not(0 <= ascii_index <= 97):
            raise ValueError('char must be printable (hence, ord(" ") < ord(char) < ord("~") or char == "°").')

        try:
            mapping_dict = self._database['mappings'][mapping]
        except KeyError as key_error:
            raise ValueError(f'Mapping "{mapping}" does not exist.') from key_error

        try:
            glyph_index = mapping_dict[ascii_index]
        except KeyError as key_error:
            raise ValueError(f'ASCII charactor "{char}" ({ascii_index}) not found in mapping.') from key_error

        return self.from_index(glyph_index)

    @property
    def ascii_mappings(self) -> List[str]:
        """List[str]: list of all ascii mappings"""
        return list(self._database['mappings'].keys())

    @property
    def collections(self) -> List[str]:
        """List[str]: list of all collections"""
        return list(self._database['collections'].keys())

    def index_iterator(self, subset: Optional[str] = None) -> Iterable[int]:
        """
        Generator function yielding the indices of the passed subset. Subset must be in :meth:`collections` or in
        :meth:`ascii_mappings`. If no subset is specified, all glyphs are used.

        Args:
            subset (Optional[str]): name of the collection or mapping

         Yields:
             int: the next glyph index

        Raises:
            ValueError: if subset does not exist.

        """
        if not subset:
            # todo: proper error handling
            glyph_indices = self._database['glyphs'].keys()
        elif subset in self._database['mappings']:
            glyph_indices = self._database['mappings'][subset]
        elif subset in self._database['collections']:
            glyph_indices = self._database['collections'][subset]
        else:
            raise ValueError(f'Subset "{subset}"" neither in ascii mappings nor in in collections')

        for glyph_index in glyph_indices:
            yield int(glyph_index)

    def iterator(self, subset: Optional[str] = None) -> Iterable[GlyphView]:
        """
        Generator function yielding the glyphs of the passed subset. Subset must be in :attr:`collections` or in
        :attr:`ascii_mappings`. If no subset is specified, all glyphs are used.

        Args:
            subset (Optional[str]): name of the collection or mapping

         Yields:
             :class:`~pyhershey.glyph.Glyph`

        """
        for glyph_index in self.index_iterator(subset):
            yield self.from_index(glyph_index)


_database_file: str = 'database.toml.xz'

glyph_factory: GlyphFactory = GlyphFactory(_database_file)
"""Instance of :class:`~pyhershey.glyphfactory.GlyphFactory` with loaded database"""
