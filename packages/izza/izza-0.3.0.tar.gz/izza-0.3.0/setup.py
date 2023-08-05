# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izza',
 'izza.exploration',
 'izza.modeling',
 'izza.modeling.feature_eng',
 'izza.validation']

package_data = \
{'': ['*']}

install_requires = \
['MiniSom>=2.2.8,<3.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'izza',
    'version': '0.3.0',
    'description': 'my machine learning toolkit',
    'long_description': '# Izza \n\nIzza is my personal data science and machine learning toolbox.\n\nThere is mainly personal function for data visualisation: \n\n| function name | presentation |\n|--|--|\n| pca_visualisation| a pca visualtion (2 components) |\n| missingData| a tables showing missing data by features |\n| camembert_plot| a camembert plot |\n| kohohen maps|a kohohen maps with percentage of target class by neuron|\n| activation_frequencies| activation frequencies for a kohohen map |\n\nThere is methods to do model evaluation : \n\n\n| function name | presentation |\n|--|--|\n| fun_precision | precision at a determined percentage using predicted probabilities |\n| fun_recall| recall at a determined percentage using predicted probabilities |\n| f_macro_score | scorer allowing to find whether some clusters contain enough precision and recall for the target class|\n| precision_macro_score| scorer allowing to find whether some clusters contain enough precision for the target class |\n| recall_macro_score | scorer allowing to find whether some clusters contain enough recall for the target class|\n| viable_clusters| function allowing to know the interessing clusters found using the f_macro score.|\n\n\n\n',
    'author': 'Ismael Lachheb',
    'author_email': 'ismael.lachheb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
