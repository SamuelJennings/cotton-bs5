Cotton BS5 Documentation
========================

Bootstrap 5 components for Django Cotton - A comprehensive library of reusable, modular components.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cotton_components/index
..    cotton_components/layouts/index

Getting Started
---------------

Cotton BS5 provides a collection of Bootstrap 5 components that work seamlessly with Django Cotton.

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install cotton-bs5

Add ``cotton_bs5`` to your ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

   INSTALLED_APPS = [
       ...
       "django_cotton",
       "cotton_bs5",
       ...
   ]

Quick Example
~~~~~~~~~~~~~

.. code-block:: html

   <c-bs5.grid cols="2" gap="3">
     <c-bs5.grid.col cols="6">
       Content for 6 columns
     </c-bs5.grid.col>
     <c-bs5.grid.col cols="6">
       Content for 6 columns
     </c-bs5.grid.col>
   </c-bs5.grid>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
