Getting Started
===============

Installation
------------

Install fenn using pip:

.. code-block:: bash

   pip install fenn

Or using uv:

.. code-block:: bash

   uv pip install fenn

Quick Start
-----------

Initialize a project using the CLI:

.. code-block:: bash

   fenn list          # See available templates
   fenn pull empty    # Pull a template

Configure your project in ``fenn.yaml``:

.. code-block:: yaml

   project: my_project

   logger:
     dir: logger

   train:
     lr: 0.001

Run your entrypoint:

.. code-block:: bash

   python main.py