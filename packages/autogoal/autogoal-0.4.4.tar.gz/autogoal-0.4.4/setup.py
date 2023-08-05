# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogoal',
 'autogoal.contrib',
 'autogoal.contrib.gensim',
 'autogoal.contrib.keras',
 'autogoal.contrib.nltk',
 'autogoal.contrib.regex',
 'autogoal.contrib.sklearn',
 'autogoal.contrib.spacy',
 'autogoal.contrib.streamlit',
 'autogoal.contrib.telegram',
 'autogoal.contrib.torch',
 'autogoal.contrib.wikipedia',
 'autogoal.datasets',
 'autogoal.datasets.ehealthkd20',
 'autogoal.experimental',
 'autogoal.grammar',
 'autogoal.kb',
 'autogoal.logging',
 'autogoal.ml',
 'autogoal.sampling',
 'autogoal.search',
 'autogoal.utils']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'enlighten>=1.4.0,<2.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'psutil>=5.6.7,<6.0.0',
 'pydot>=1.4.1,<2.0.0',
 'pyyaml>=5.2,<6.0',
 'rich>=8.0.0,<9.0.0',
 'scipy>=1.5.2,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0',
 'tqdm>=4.50.2,<5.0.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{'contrib': ['gensim>=3.8.1,<4.0.0',
             'jupyterlab>=1.2.4,<2.0.0',
             'keras>=2.3.1,<3.0.0',
             'nltk>=3.4.5,<4.0.0',
             'nx_altair>=0.1.4,<0.2.0',
             'python-telegram-bot>=12.4.2,<13.0.0',
             'scikit-learn>=0.22,<0.23',
             'seqlearn>=0.2,<0.3',
             'sklearn_crfsuite>=0.3.6,<0.4.0',
             'spacy>=2.2.3,<3.0.0',
             'streamlit>=0.59.0,<0.60.0',
             'transformers>=2.3.0,<3.0.0',
             'wikipedia>=1.4.0,<2.0.0'],
 'dev': ['codecov>=2.0.15,<3.0.0',
         'markdown-include>=0.5.1,<0.6.0',
         'mkdocs>=1.0.4,<2.0.0',
         'mkdocs-material>=4.6.0,<5.0.0',
         'mypy>=0.761,<0.762',
         'pylint>=2.4.4,<3.0.0',
         'pytest>=5.3.2,<6.0.0',
         'pytest-cov>=2.8.1,<3.0.0',
         'typer-cli>=0.0.11,<0.0.12'],
 'gensim': ['gensim>=3.8.1,<4.0.0'],
 'keras': ['keras>=2.3.1,<3.0.0'],
 'nltk': ['nltk>=3.4.5,<4.0.0'],
 'sklearn': ['scikit-learn>=0.22,<0.23',
             'seqlearn>=0.2,<0.3',
             'sklearn_crfsuite>=0.3.6,<0.4.0'],
 'spacy': ['spacy>=2.2.3,<3.0.0'],
 'streamlit': ['nx_altair>=0.1.4,<0.2.0', 'streamlit>=0.59.0,<0.60.0'],
 'telegram': ['python-telegram-bot>=12.4.2,<13.0.0'],
 'wikipedia': ['wikipedia>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'autogoal',
    'version': '0.4.4',
    'description': 'Automatic Generation Optimization And Learning',
    'long_description': '![AutoGOAL Logo](https://autogoal.github.io/autogoal-banner.png)\n\n[<img alt="PyPI" src="https://img.shields.io/pypi/v/autogoal">](https://pypi.org/project/autogoal/) [<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/autogoal">](https://pypi.org/project/autogoal/) [<img alt="PyPI - License" src="https://img.shields.io/pypi/l/autogoal">](https://autogoal.github.io/contributing) [<img alt="GitHub stars" src="https://img.shields.io/github/stars/autogoal/autogoal?style=social">](https://github.com/autogoal/autogoal/stargazers) [<img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/auto_goal?label=Followers&style=social">](https://twitter.com/auto_goal)\n\n[<img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/autogoal/autogoal/CI/main?label=unit tests&logo=github">](https://github.com/autogoal/autogoal/actions)\n[<img src="https://codecov.io/gh/autogoal/autogoal/branch/main/graph/badge.svg" />](https://codecov.io/gh/autogoal/autogoal/)\n[<img alt="Docker Image Size (CPU)" src="https://img.shields.io/docker/image-size/autogoal/autogoal/latest">](https://hub.docker.com/r/autogoal/autogoal)\n[<img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/autogoal/autogoal">](https://hub.docker.com/r/autogoal/autogoal)\n\n# AutoGOAL\n\n> Automatic Generation, Optimization And Artificial Learning\n\nAutoGOAL is a Python library for automatically finding the best way to solve a given task.\nIt has been designed mainly for _Automated Machine Learning_ (aka [AutoML](https://www.automl.org))\nbut it can be used in any scenario where you have several possible ways to solve a given task.\n\nTechnically speaking, AutoGOAL is a framework for program synthesis, i.e., finding the best program to solve\na given problem, provided that the user can describe the space of all possible programs.\nAutoGOAL provides a set of low-level components to define different spaces and efficiently search in them.\nIn the specific context of machine learning, AutoGOAL also provides high-level components that can be used as a black-box in almost any type of problem and dataset format.\n\n## ⭐ Quickstart\n\nAutoGOAL is first and foremost a framework for Automated Machine Learning.\nAs such, it comes pre-packaged with hundreds of low-level machine learning\nalgorithms that can be automatically assembled into pipelines for different problems.\n\nThe core of this functionality lies in the [`AutoML`](https://autogoal.github.io/api/autogoal.ml#automl) class.\n\nTo illustrate the simplicity of its use we will load a dataset and run an automatic classifier in it.\nThe following code will run for approximately 5 minutes on a classic dataset.\n\n```python\nfrom autogoal.datasets import cars\nfrom autogoal.kb import (MatrixContinuousDense, \n                         Supervised, \n                         VectorCategorical)\nfrom autogoal.ml import AutoML\n\n# Load dataset\nX, y = cars.load()\n\n# Instantiate AutoML and define input/output types\nautoml = AutoML(\n    input=(MatrixContinuousDense, \n           Supervised[VectorCategorical]),\n    output=VectorCategorical\n)\n\n# Run the pipeline search process\nautoml.fit(X, y)\n\n# Report the best pipeline\nprint(automl.best_pipeline_)\nprint(automl.best_score_)\n```\n\nSensible defaults are defined for each of the many parameters of `AutoML`.\nMake sure to [read the documentation](https://autogoal.github.io/guide/) for more information.\n\n## ⚙️ Installation\n\nThe easiest way to get AutoGOAL up and running with all the dependencies is to pull the development Docker image, which is somewhat big:\n\n    docker pull autogoal/autogoal\n\nInstructions for setting up Docker are available [here](https://www.docker.com/get-started).\n\nOnce you have the development image downloaded, you can fire up a console and use AutoGOAL interactively.\n\n![](https://autogoal.github.io/shell.svg)\n\nIf you prefer to not use Docker, or you don\'t want all the dependencies, you can also install AutoGOAL directly with pip:\n\n    pip install autogoal\n\nThis will install the core library but you won\'t be able to use any of the underlying machine learning algorithms until you install the corresponding optional dependencies. You can install them all with:\n\n    pip install autogoal[contrib]\n\nTo fine-pick which dependencies you want, read the [dependencies section](https://autogoal.github.io/dependencies/).\n\n> ⚠️ **NOTE**: By installing through `pip` you will get the latest release version of AutoGOAL, while by installing through Docker, you will get the latest development version. \n>\n> The development version is mostly up-to-date with the `main` branch, hence it will probably contain more features, but also more bugs, than the release version.\n\n## 💻 CLI\n\nYou can use AutoGOAL directly from the CLI. To see options just type:\n\n    autogoal\n\nUsing the CLI you can train and use AutoML models, download datasets and inspect the contrib libraries without writing a single line of code.\n\n![](https://autogoal.github.io/shell/autogoal_cli.svg)\n\nRead more in the [CLI documentation](https://autogoal.github.io/cli).\n\n## \U0001f929 Demo\n\nAn online demo app is available at [autogoal.github.io/demo](https://autogoal.github.io/demo).\nThis app showcases the main features of AutoGOAL in interactive case studies.\n\nTo run the demo locally, simply type:\n\n    docker run -p 8501:8501 autogoal/autogoal\n\nAnd navigate to [localhost:8501](http://localhost:8501).\n\n## ⚖️ API stability\n\nWe make a conscious effort to maintain a consistent public API across versions, but the private API can change at any time.\nIn general, everything you can import from `autogoal` without underscores is considered public. \n\nFor example:\n\n```python\n# "clean" imports are part of the public API\nfrom autogoal import optimize   \nfrom autogoal.ml import AutoML  \nfrom autogoal.contrib.sklearn import find_classes\n\n# public members of public types as well\nautoml = AutoML\nautoml.fit(...) \n\n# underscored imports are part of the private API\nfrom autogoal.ml._automl import ...\nfrom autogoal.contrib.sklearn._generated import ...\n\n# as well as private members of any type\nautoml._input_type(...)\n\n```\n\nThese are our consistency rules:\n\n- Major breaking changes are introduced between major version updates, e.g., `x.0` and `y.0`. These can be additions, removals, or modifications of any kind in any part of the API.\n\n- Between minor version updates, e.g., `1.x` and `1.y`, you can expect to find new functionality, but anything you can use from the   public API will still be there with a consistent semantic (save for bugfixes).\n\n- Between micro version updates, e.g., `1.3.x` and `1.3.y`, the public API is frozen even for additions.\n\n- The private API can be changed at all times.\n\n⚠️ While AutoGOAL is on public beta (versions `0.x`) the public API is considered unstable and thus everything can change. However, we try to keep breaking changes to a minimum.\n\n## 📚 Documentation\n\nThis documentation is available online at [autogoal.github.io](https://autogoal.github.io). Check the following sections:\n\n- [**User Guide**](https://autogoal.github.io/guide/): Step-by-step showcase of everything you need to know to use AuoGOAL.\n- [**Examples**](https://autogoal.github.io/examples/): The best way to learn how to use AutoGOAL by practice.\n- [**API**](https://autogoal.github.io/api/autogoal): Details about the public API for AutoGOAL.\n\nThe HTML version can be deployed offline by downloading the [AutoGOAL Docker image](https://hub.docker.com/autogoal/autogoal) and running:\n\n    docker run -p 8000:8000 autogoal/autogoal mkdocs serve -a 0.0.0.0:8000\n\nAnd navigating to [localhost:8000](http://localhost:8000).\n\n## 📃 Publications\n\nIf you use AutoGOAL in academic research, please cite the following paper:\n\n```bibtex\n@article{estevez2020general,\n  title={General-purpose hierarchical optimisation of machine learning pipelines with grammatical evolution},\n  author={Est{\\\'e}vez-Velarde, Suilan and Guti{\\\'e}rrez, Yoan and Almeida-Cruz, Yudivi{\\\'a}n and Montoyo, Andr{\\\'e}s},\n  journal={Information Sciences},\n  year={2020},\n  publisher={Elsevier},\n  doi={10.1016/j.ins.2020.07.035}\n}\n```\n\nThe technologies and theoretical results leading up to AutoGOAL have been presented at different venues:\n\n- [Optimizing Natural Language Processing Pipelines: Opinion Mining Case Study](https://link.springer.com/chapter/10.1007/978-3-030-33904-3_15) marks the inception of the idea of using evolutionary optimization with a probabilistic search space for pipeline optimization.\n\n- [AutoML Strategy Based on Grammatical Evolution: A Case Study about Knowledge Discovery from Text](https://www.aclweb.org/anthology/P19-1428/) applied probabilistic grammatical evolution with a custom-made grammar in the context of entity recognition in medical text.\n\n- [General-purpose Hierarchical Optimisation of Machine Learning Pipelines with Grammatical Evolution](https://doi.org/10.1016/j.ins.2020.07.035) presents a more uniform framework with different grammars in different problems, from tabular datasets to natural language processing.\n\n- [Solving Heterogeneous AutoML Problems with AutoGOAL](https://www.automl.org/wp-content/uploads/2020/07/AutoML_2020_paper_20.pdf) is the first actual description of AutoGOAL as a framework, unifying the ideas presented in the previous papers.\n\n## 🤝 Contribution\n\nCode is licensed under MIT. Read the details in the [collaboration section](https://autogoal.github.io/contributing).\n\nThis project follows the [all-contributors](https://allcontributors.org) specification. Any contribution will be given credit, from fixing typos, to reporting bugs, to implementing new core functionalities. \n\nHere are all the current contributions. \n\n> **🙏 Thanks!**\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://github.com/sestevez"><img src="https://avatars3.githubusercontent.com/u/6156391?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Suilan Estevez-Velarde</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/commits?author=sestevez" title="Code">💻</a> <a href="https://github.com/autogoal/autogoal/commits?author=sestevez" title="Tests">⚠️</a> <a href="#ideas-sestevez" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/autogoal/autogoal/commits?author=sestevez" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://apiad.net"><img src="https://avatars3.githubusercontent.com/u/1778204?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alejandro Piad</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/commits?author=apiad" title="Code">💻</a> <a href="https://github.com/autogoal/autogoal/commits?author=apiad" title="Tests">⚠️</a> <a href="https://github.com/autogoal/autogoal/commits?author=apiad" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/yudivian"><img src="https://avatars1.githubusercontent.com/u/5324359?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yudivián Almeida Cruz</b></sub></a><br /><a href="#ideas-yudivian" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/autogoal/autogoal/commits?author=yudivian" title="Documentation">📖</a></td>\n    <td align="center"><a href="http://orcid.org/0000-0002-4052-7427"><img src="https://avatars2.githubusercontent.com/u/25705914?v=4?s=100" width="100px;" alt=""/><br /><sub><b>ygutierrez</b></sub></a><br /><a href="#ideas-joogvzz" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/autogoal/autogoal/commits?author=joogvzz" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/EEstevanell"><img src="https://avatars0.githubusercontent.com/u/45082075?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ernesto Luis Estevanell Valladares</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/commits?author=EEstevanell" title="Code">💻</a> <a href="https://github.com/autogoal/autogoal/commits?author=EEstevanell" title="Tests">⚠️</a></td>\n    <td align="center"><a href="http://alexfertel.netlify.app"><img src="https://avatars3.githubusercontent.com/u/22298999?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alexander Gonzalez</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/commits?author=alexfertel" title="Code">💻</a> <a href="https://github.com/autogoal/autogoal/commits?author=alexfertel" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://www.linkedin.com/in/anshu-trivedi-501a7b146/"><img src="https://avatars1.githubusercontent.com/u/47869948?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Anshu Trivedi</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/commits?author=AnshuTrivedi" title="Code">💻</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="http://alxrcs.github.io"><img src="https://avatars1.githubusercontent.com/u/8171561?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alex Coto</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/commits?author=alxrcs" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/geblanco"><img src="https://avatars3.githubusercontent.com/u/6652222?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Guillermo Blanco</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/issues?q=author%3Ageblanco" title="Bug reports">🐛</a> <a href="https://github.com/autogoal/autogoal/commits?author=geblanco" title="Code">💻</a> <a href="https://github.com/autogoal/autogoal/commits?author=geblanco" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/yacth"><img src="https://avatars3.githubusercontent.com/u/71322097?v=4?s=100" width="100px;" alt=""/><br /><sub><b>yacth</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/issues?q=author%3Ayacth" title="Bug reports">🐛</a> <a href="https://github.com/autogoal/autogoal/commits?author=yacth" title="Code">💻</a></td>\n    <td align="center"><a href="https://sourceplusplus.com"><img src="https://avatars0.githubusercontent.com/u/3278877?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Brandon Fergerson</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/issues?q=author%3ABFergerson" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="https://adityanikhil.github.io/main/"><img src="https://avatars2.githubusercontent.com/u/30192967?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Aditya Nikhil</b></sub></a><br /><a href="https://github.com/autogoal/autogoal/issues?q=author%3AAdityaNikhil" title="Bug reports">🐛</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n \n',
    'author': 'Suilan Estevez-Velarde',
    'author_email': 'suilanestevez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://autogoal.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
