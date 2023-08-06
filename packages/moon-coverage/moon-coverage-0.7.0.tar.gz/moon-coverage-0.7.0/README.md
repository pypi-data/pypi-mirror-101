ESA Moon Coverage Toolbox
=========================

<img src="https://moon-coverage.readthedocs.io/en/stable/_static/moon-coverage.png" align="right" hspace="50" vspace="25" height="200">

[
    ![CI/CD](https://juigitlab.esac.esa.int/datalab/moon-coverage/badges/main/pipeline.svg)
    ![Coverage](https://juigitlab.esac.esa.int/datalab/moon-coverage/badges/main/coverage.svg)
](https://juigitlab.esac.esa.int/datalab/moon-coverage/pipelines/main/latest)
[
    ![Documentation Status](https://readthedocs.org/projects/moon-coverage/badge/?version=stable)
](https://readthedocs.org/projects/moon-coverage/builds/)

[
    ![Version](https://img.shields.io/pypi/v/moon-coverage.svg?label=Lastest%20release&color=lightgrey)
](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/tags)
[
    ![License](https://img.shields.io/pypi/l/moon-coverage.svg?color=lightgrey&label=License)
](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/blob/main/LICENSE.md)
[
    ![PyPI](https://img.shields.io/badge/PyPI-moon--coverage-blue?logo=Python&logoColor=white)
    ![Python](https://img.shields.io/pypi/pyversions/moon-coverage.svg?label=Python&logo=Python&logoColor=white)
](https://pypi.org/project/moon-coverage/)

[
    ![Docs](https://img.shields.io/badge/Docs-moon--coverage.readthedocs.io-blue?&color=orange&logo=Read%20The%20Docs&logoColor=white)
](https://moon-coverage.readthedocs.io)
[
    ![DataLab](https://img.shields.io/badge/Datalab-datalabs.esa.int-blue?&color=orange&logo=Jupyter&logoColor=white)
](https://datalabs.esa.int)

---

The [moon-coverage](https://juigitlab.esac.esa.int/datalab/moon-coverage)
python package is a toolbox to perform
surface coverage analysis based on orbital trajectory configuration.
Its main intent is to provide an easy way to compute observation
opportunities of specific region of interest above the Galilean
satellites for the ESA-JUICE mission but could be extended in the
future to other space mission.

It is actively developed by
the [Laboratory of Planetology and Geodynamics](https://lpg-umr6112.fr/)
(CNRS-UMR 6112) at the University of Nantes (France), under
[ESA-JUICE](https://sci.esa.int/web/juice) founding support.

<p align="center">
  <img src="https://moon-coverage.readthedocs.io/en/stable/_images/lpg-esa.png" alt="LPG / ESA logos"/>
</p>

Installation
------------

The package is available on [pypi](https://pypi.org/project/moon-coverage/)
and can be install directly with `pip`:

```bash
pip install moon-coverage
```

If you already installed `moon-coverage` and you want to upgrade it to the latest version,
you need to add a `--upgrade` flag in the `pip` command above.


Documentation
-------------

The module documentation can be found on [ReadTheDocs](https://moon-coverage.readthedocs.io).
You can look into the `notebooks/` folder for additional examples.

Local development and testing
-----------------------------

Setup:
```bash
git clone https://juigitlab.esac.esa.int/datalab/moon-coverage
cd moon-coverage

pip install -e .
pip install -r tests/requirements.txt -r docs/requirements.txt
```

Linter:
```bash
flake8 moon_coverage/ tests/ setup.py docs/conf.py
pylint --rcfile=setup.cfg moon_coverage/ tests/*/*.py setup.py
```

Unit tests (with `pytest`):
```bash
pytest --cov moon_coverage tests/
```

Build the docs (with `sphinx`):
```bash
sphinx-build docs docs/_build --color -W -bhtml
```

Deploy on a JupyterLab Docker instance
--------------------------------------

A `Dockerfile` configuration setup is provided in the `docker/` folder.

```bash
cd docker/
```

To build the Docker image:

```bash
docker-compose build
```

Start the JupyterLab instance:

```bash
docker-compose run --service-ports jupyter-lab
```

Then click on the link in the console: `http://127.0.0.1:8000/lab?token=xxxxxxxxx`

You can check that the instance is correctly configured:

```bash
docker-compose run jupyter-lab-tests
```
