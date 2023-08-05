# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.autodoc_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.0', 'pydantic>=1.0']

setup_kwargs = {
    'name': 'autodoc-pydantic',
    'version': '0.1.1',
    'description': 'Seamlessly integrate pydantic models in your Sphinx documentation.',
    'long_description': "# autodoc_pydantic\n\n[![PyPI version](https://badge.fury.io/py/autodoc-pydantic.svg)](https://badge.fury.io/py/autodoc-pydantic)\n![Master](https://github.com/mansenfranzen/autodoc_pydantic/actions/workflows/tests.yml/badge.svg)\n![Python](https://img.shields.io/badge/python-3.6+-blue.svg)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/30a083d784f245a98a0d5e6857708cc8)](https://www.codacy.com/gh/mansenfranzen/autodoc_pydantic/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mansenfranzen/autodoc_pydantic&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/30a083d784f245a98a0d5e6857708cc8)](https://www.codacy.com/gh/mansenfranzen/autodoc_pydantic/dashboard?utm_source=github.com&utm_medium=referral&utm_content=mansenfranzen/autodoc_pydantic&utm_campaign=Badge_Coverage)\n\nYou love [pydantic](https://pydantic-docs.helpmanual.io/) :heart: and you want to document your models and configuration settings with [sphinx](https://www.sphinx-doc.org/en/master/)? \n\nPerfect, let's go. But wait, sphinx' [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) does not integrate too well with pydantic models :confused:. \n\nDon't worry - just `pip install autodoc_pydantic` :relaxed:.\n\n## Features\n\n- :speech_balloon: provides default values, alias and constraints for model fields\n- :link: adds references between validators and corresponding fields\n- :page_with_curl: includes collapsable model json schema\n- :surfer: natively integrates with autodoc extension\n- :paperclip: defines explicit pydantic prefixes for models, settings, fields, validators and model config\n- :clipboard: shows summary section for model configuration and validators\n- :eyes: hides overloaded and redundant model class signature\n- :books: sorts fields, validators and model config within models by type\n- 🍀 Supports `pydantic >= 1.0.0` and `sphinx >= 3.4.0`\n\nAll of these addons are completely configurable.\n\n## Installation\n\n1. Install via `pip install autodoc_pydantic`\n2. Add `'sphinxcontrib.autodoc_pydantic'` to the `extensions` list in `conf.py`:\n\n   ```python\n   extensions = ['sphinxcontrib.autodoc_pydantic']\n   ```\n\n3. Configure `autodoc_pydantic` in `conf.py`:\n\n   ```python\n   autodoc_pydantic_field_show_constraints = True\n   autodoc_pydantic_model_show_schema = True\n   ```\n \n## Usage\n\nThe standard `automodule` directive already understands pydantic models that it encounters by default. No more tweaks are required.\n\n```rest\n.. automodule:: package.module\n   :members:\n```\n\nAdditionally, autodoc_pydantic provides specific directives for models, settings, fields, validators and class config:\n\n```rest\n.. autopydantic_model:: package.module.MyModel\n   :members:\n   \n.. autopydantic_settings:: package.module.MySettings\n   :members:\n   \n.. autopydantic_field:: package.module.MyModel.foobar\n\n.. autopydantic_validator:: package.module.MyModel.validator\n\n.. autopydantic_class_config:: package.module.MyModel.Config\n   :members:\n```\n \n## Configuration\n\n### General \n\n- `autodoc_pydantic_show_config` = *True*: By default document `Config` class as class members. If *False*, hides it completely.\n- `autodoc_pydantic_show_validators` = *True*: By default document pydantic validators as class members. If *False*, hides it completely.\n\n### Models / Settings\n\n- `autodoc_pydantic_model_show_schema` = *True*: By default, adds collapsable section including formatted model json schema.\n- `autodoc_pydantic_model_show_config` = *True*: By default, adds model configuration settings to model doc string.\n- `autodoc_pydantic_model_show_validators` = *True*: By default, adds validator -> field mappings to model doc string.\n- `autodoc_pydantic_model_show_paramlist` = *False*: By default, hides overloaded and redundant parameter list from model signature.\n- `autodoc_pydantic_model_member_order` = *'groupwise'*: By default, sorts model members by type to group fields, validators and class config members.\n\n### Fields\n\n- `autodoc_pydantic_field_list_validators` = *True*: By default, lists all validators processing corresponding field.\n- `autodoc_pydantic_field_doc_policy` = *'both'*: By default, show doc string and and field description. If *'description'*, show field description only. If *'docstring'*, show doc string only.  \n- `autodoc_pydantic_field_show_constraints` = *True*: By default, show field constraints (e.g. minimum, maximum etc.).\n- `autodoc_pydantic_field_show_alias` = *True*: By default, show field alias in signature.\n\n### Validators\n\n- `autodoc_pydantic_validator_show_paramlist` = *False*: By default, hides meaningless parameter list from validators.\n- `autodoc_pydantic_validator_replace_retann` = *True*: By default, replaces validators' return annotation with references to processed fields.\n- `autodoc_pydantic_validator_list_fields` = *True*: By default, adds list of references to validators' doc string.\n",
    'author': 'mansenfranzen',
    'author_email': 'franz.woellert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mansenfranzen/autodoc_pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
