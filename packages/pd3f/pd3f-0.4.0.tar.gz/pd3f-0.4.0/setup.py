# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pd3f']

package_data = \
{'': ['*']}

install_requires = \
['clean-text[gpl]',
 'dehyphen>=0.3.0,<0.4.0',
 'joblib',
 'parsr-client==3.1',
 'shapely',
 'textdistance']

setup_kwargs = {
    'name': 'pd3f',
    'version': '0.4.0',
    'description': 'Reconstruct the original continuous text from PDFs with language models',
    'long_description': '# `pd3f-core` [![PyPI](https://img.shields.io/pypi/v/pd3f.svg)](https://pypi.org/project/pd3f/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pd3f.svg)](https://pypi.org/project/pd3f/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pd3f)](https://pypistats.org/packages/pd3f)\n\n_Experimental, use with care._\n\n`pd3f-core` is Python package to **reconstruct** the original **continuous text** from **PDFs** with language models.\n`pd3f-core` assumes your PDF is either text-based or already OCRd.\n`pd3f-core` is at the heart of [pd3f](https://github.com/pd3f/pd3f): a full Docker-based text extraction pipeline (including OCR).\n\n`pd3f-core` first uses [Parsr](https://github.com/axa-group/Parsr) to chunk PDFs into lines and paragraphs.\nThen, it uses the Python package [dehyphen](https://github.com/jfilter/dehyphen) to reconstruct the paragraphs in the most probable way.\nThe probability is derived by calculating the [perplexity](https://en.wikipedia.org/wiki/Perplexity) with [Flair](https://github.com/flairNLP/flair)\'s character-based [language models](https://machinelearningmastery.com/statistical-language-modeling-and-neural-language-models/).\nUnnecessary hyphens are removed, space or new lines are kept or dropt depending on the surround words.\n\nIt\'s mainly developed for German but should work with other languages as well.\nThe project is still in an early stage.\nExpect rough edges and rapid changes.\n\n## Documentation\n\nAPI Documentation of pd3f-core: <https://pd3f.github.io/pd3f-core/index.html>\n\nDocumentation of pd3f (the ): <https://pd3f.com/docs/>\n\n## Features\n\n### Dehyphenation of Lines\n\nCheck if two lines can be joined by removing hyphens (\'-\').\n\n### Reasonable Joining of Lines\n\nDecide between adding a simple space (\' \') or a new line (\'\\n\') when joining lines.\n\n### Reverse Page Break (Experimental)\n\nCheck if the last paragraph of a page und the first paragraph of the following page can be joined.\n\n### Footnote to Endnotes (Experimental)\n\nIn order to join paragraphs (and reverse page breaks), detect footnotes and turn them into endnotes.\nFor now, the footnotes are pulled to the end of a file.\n\n### Deduplication of Pager Header / Footer (Experimental)\n\nIf the header or the footer are the same for all pages, only display them once.\nHeaders are pulled to the start of the document and footer to the end.\nSome heuristic based on the similarity of footers are used. (Jaccard distance for text, and compare overlapping shapes)\n\n<!-- TODO -->\n<!-- Special case for OCRd PDFs: Choose the Header / Footer with the best Flair score to display.\nSince header / footer are small, the OCR may fail to get the text output. -->\n\n## Installation\n\n```bash\npip install pd3f\n```\n\nor\n\n```bash\npoetry add pd3f\n```\n\n## Usage\n\nStart a local Parsr instance:\n\n```bash\ndocker-compose up\n```\n\n(You may also use tunnel a remote Parsr instance ([script](./scripts/locale_parsr.sh)) or choose a remote address.)\n\n```python\nfrom pd3f import extract\n\ntext, tables = extract(file_path, tables=False, experimental=False, force_gpu=False, lang="multi", fast=False, parsr_location="localhost:3001")\n```\n\nExplanations of the paramaters in the docs: https://pd3f.github.io/pd3f-core/export.html#pd3f.export.extract\n\n### GPU Support (CUDA)\n\nUsing CUDA speeds up the evaluation with Flair.\nBut you need an (expensive) GPU.\nYou need to set up your GPU with CUDA.\n[Here a guide for Ubuntu 18.04](https://towardsdatascience.com/deep-learning-gpu-installation-on-ubuntu-18-4-9b12230a1d31)\n\n1. install [conda (via miniconda)](https://docs.conda.io/en/latest/miniconda.html) and [poetry](https://python-poetry.org/docs/)\n2. create a new conda enviroment & activate it\n3. Install [PyTorch](https://pytorch.org/) with CUDA: `conda install pytorch torchvision cudatoolkit=10.2 -c pytorch` (example)\n4. Install `pd3f-core` with poetry: `poetry add pd3f`\n\nPoetry realizes that it is run within a conda virtual env so it doesn\'t create a new one.\nSince setting up CUDA is hard, install it with the most easy way (with conda).\n\n## Background\n\n### Parsr Config\n\nAt the heart of `pd3f-core` is the JSON output of Parsr.\nSome comments on how and why certain things were chosen.\n[Parsr\'s documentation about the different modules](https://github.com/axa-group/Parsr/tree/master/server/src/processing)\n\nParsr has several module to classify paragraphs into certain types.\nThey offer a list detections as well as an heading detection.\nIn my experience, the accuracy is too low for both, so we don\'t use it right now.\nThis also means all the extracted (output) text is flat (no headings, different formattings etc.).\n\nWe enable Drawing + Image Detection because we may need to understand what paragraph is following which other one.\nThis may be helpful when to decide whether to join paragraphs.\nBut it\'s dropped when activating the `fast` setting.\n\nIn the JSON output is a field `pageNumber`.\nThis comes from the page detection module.\nSo `pageNumber` is derived from header / footer of each page.\nSo it may be different\xa0from the index in the page array.\nDon\'t relay on `pageNumber` in the JSON output.\n\n`words-to-line-new` has be used like this.\nThere is no error but the accuracy decreases if it used otherwise.\n\n```json\n"words-to-line-new",\n[\n    "reading-order-detection",\n```\n\nDon\'t do OCR with Parsr because the results are worse than OCRmyPDF (because the latter uses image preprocessing).\n\n## Future Work / TODO\n\n-   make reverse page break work without requiring the experimental features\n\n## Developement\n\nInstall and use [poetry](https://python-poetry.org/).\n\n## License\n\nAffero General Public License 3.0\n',
    'author': 'Johannes Filter',
    'author_email': 'hi@jfilter.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pd3f/pd3f-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
