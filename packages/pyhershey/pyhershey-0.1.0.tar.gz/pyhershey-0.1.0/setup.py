import pathlib

from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyhershey',
    version='0.1.0',
    author='viggge',
    url='https://gitlab.com/viggge/pyhershey',
    project_urls={
        'Bug Reports': 'https://gitlab.com/viggge/pyhershey/-/issues',
        'Source': 'https://gitlab.com/viggge/pyhershey',
        'Documentation': "https:/pyhershey.readthedocs.io/en/latest/",
    },
    license="GPLv3",
    description="pyhershey enable simple usage of Hershey fonts within python.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={'pyhershey': ['database.toml.xz', 'py.typed']},
    install_requires=[
        'toml'
    ],
    extras_require = {
        'display':  ['matplotlib'],
        'docs': ['sphinx', 'pydata_sphinx_theme', 'sphinx-autoapi', 'matplotlib', 'sphinxcontrib-images']
    },
    python_requires='>=3.8',
)