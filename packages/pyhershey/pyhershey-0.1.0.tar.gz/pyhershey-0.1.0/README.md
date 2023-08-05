# pyhershey

Hershey fonts are a collection of different vector fonts developed 1967 by Dr. Allen Vincent Hershey at the US Naval
Weapons Laboratory. These fonts come in different styles and include Latin, Greek, Cyrillic and Japanese (kanji,
hiragana and katakana) characters and a lot of other symbols. The fonts' data are available under some restrictions.
See font-data/LICENSE and [here](http://www.ghostscript.com/doc/current/Hershey.htm). But basically, the fonts can be
used in any project.

Special about these fonts is that all glyphs are build up by straight line segments which makes
their look rather special. Nevertheless, there can be cases where this feature could be highly useful and, of course, it
has also some kind of style. To get an impression of the fonts, see the documentation of this package.

This package enables you to use this fonts in your python project in an easy way.
The only requirement is python >= 3.8.
To install it, run

```
pip install pyhershey[display]
```

This installs the package and matplotlib for displaying the glyphs. If you don't need it, just install the package without ``[display]``

The example below shows how to use the library.

```python
from pyhershey import glyph_factory
from pyhershey.show import show_glyph

a = glyph_factory.from_ascii('a', 'roman_simplex')

show_glyph(a)
```

For further details, see the documentation.

The library is licensed under the GPL3 license (see LICENSE.txt in the root directory).
The font data in the font-data directory has its own license which is given in font-data/LICENSE.

