jupyterlab-yq-kfidentity
===============================

A Custom Jupyter Widget Library

Installation
------------

To install use pip:

    $ pip install jupyterlab_yq_kfidentity

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/credo/jupyterlab-yq-kfidentity.git
    $ cd jupyterlab-yq-kfidentity
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix jupyterlab_yq_kfidentity
    $ jupyter nbextension enable --py --sys-prefix jupyterlab_yq_kfidentity

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite jupyterlab_yq_kfidentity

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
