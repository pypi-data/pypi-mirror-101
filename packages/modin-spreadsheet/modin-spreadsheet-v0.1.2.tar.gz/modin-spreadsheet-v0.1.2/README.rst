.. image:: https://github.com/modin-project/modin/blob/3d6368edf311995ad231ec5342a51cd9e4e3dc20/docs/img/MODIN_ver2_hrz.png?raw=true
    :target: https://modin.readthedocs.io
    :width: 77%
    :align: center
    :alt: Modin

=================
Modin-spreadsheet
=================
Modin-spreadsheet is the underlying package for the `Modin <https://modin.readthedocs.io>`_ Spreadsheet API. It renders
DataFrames within a Jupyter notebook as a spreadsheet and makes it easy to explore with intuitive scrolling, sorting,
and filtering controls. The spreadsheet allows click editing, adding/removing rows, etc. and can also be controlled
using the API. Modin-spreadsheet also records the history of changes made so that you can share or reproduce your
results.

Modin-spreadsheet builds on top of `SlickGrid <https://github.com/mleibman/SlickGrid>`_ and Modin to provide a highly
responsive experience even on DataFrames with 100,000 rows.

Modin-spreadsheet is forked from `Qgrid <https://github.com/quantopian/qgrid>`_, which was developed by Quantopian.
Some documentation will reference Qgrid documentation as we continue to build out our own documentation. To learn more
about Qgrid, here is an `introduction on YouTube <https://www.youtube.com/watch?v=AsJJpgwIX0Q>`_.

Here is an example of the Modin-spreadsheet widget in action.

.. figure:: docs/images/overview_demo.gif
    :align: left
    :target: docs/images/overview_demo.gif
    :width: 200px

    A brief demo showing the common use cases for Modin-spreadsheet: filtering, editing, sorting, generating
    reproducible code, and exporting the changed dataframe

API Documentation
-----------------
Full documentation for Modin-spreadsheet is still in progress. Most features are documented on Qgrid's readthedocs: `https://qgrid.readthedocs.io/ <http://qgrid.readthedocs.io/en/latest/>`_.

Installation
------------
Modin-spreadsheet is intended be used through the `Modin Spreadsheet API <https://modin.readthedocs.io>`_ (Docs in progress...). Please install Modin and Modin-spreadsheet by running the following: ::

    pip install modin
    pip install modin[spreadsheet]

To enable the Modin-spreadsheet widget, you may need to also run::

  jupyter nbextension enable --py --sys-prefix modin_spreadsheet

  # only required if you have not enabled the ipywidgets nbextension yet
  jupyter nbextension enable --py --sys-prefix widgetsnbextension

If needed, Modin-spreadsheet can be installed through PyPi. ::

  pip install modin-spreadsheet

Features
----------
**Column-specific options**:
The feature enables the ability to set options on a per column basis.  This allows you to do things like explicitly
specify which column should be sortable, editable, etc.  For example, if you wanted to prevent editing on all columns
except for a column named `'A'`, you could do the following::

    col_opts = { 'editable': False }
    col_defs = { 'A': { 'editable': True } }
    modin_spreadsheet.show_grid(df, column_options=col_opts, column_definitions=col_defs)

See the `show_grid <https://qgrid.readthedocs.io/en/v1.1.0/#qgrid.show_grid>`_ documentation for more information.

**Disable editing on a per-row basis**:
This feature allows a user to specify whether or not a particular row should be editable. For example, to make it so
only rows in the grid where the `'status'` column is set to `'active'` are editable, you might use the following code::

    def can_edit_row(row):
        return row['status'] == 'active'

    modin_spreadsheet.show_grid(df, row_edit_callback=can_edit_row)

**Dynamically update an existing spreadsheet widget**:
These API allow users to programmatically update the state of an existing spreadsheet widget:

    - `edit_cell <https://qgrid.readthedocs.io/en/latest/#qgrid.QgridWidget.edit_cell>`_
    - `change_selection <https://qgrid.readthedocs.io/en/latest/#qgrid.QgridWidget.change_selection>`_
    - `toggle_editable <https://qgrid.readthedocs.io/en/latest/#qgrid.QgridWidget.toggle_editable>`_
    - `change_grid_option <https://qgrid.readthedocs.io/en/latest/#qgrid.QgridWidget.change_grid_option>`_ (experimental)

**MultiIndex Support**:
Modin-spreadsheet displays multi-indexed DataFrames with some of the index cells merged for readability, as is normally
done when viewing DataFrames as a static html table.  The following image shows Modin-spreadsheet displaying a
multi-indexed DataFrame:

.. figure:: https://s3.amazonaws.com/quantopian-forums/pipeline_with_qgrid.png
    :align: left
    :target: https://s3.amazonaws.com/quantopian-forums/pipeline_with_qgrid.png
    :width: 100px

    Disclaimer: This is from the Qgrid documentation.

**Events API**:
The Events API provides ``on`` and ``off`` methods which can be used to attach/detach event handlers. They're available
on both the ``modin_spreadsheet`` module (see `qgrid.on <https://qgrid.readthedocs.io/en/latest/#qgrid.on>`_), and on
individual SpreadsheetWidget instances (see `qgrid.QgridWidget.on <https://qgrid.readthedocs.io/en/latest/#qgrid.QgridWidget.on>`_).

Having the ability to attach event handlers allows us to do some interesting things in terms of using Modin-spreadsheet
in conjunction with other widgets/visualizations. One example is using Modin-spreadsheet to filter a DataFrame that's
also being displayed by another visualization.

Here's how you would use the ``on`` method to print the DataFrame every time there's a change made::

    def handle_json_updated(event, spreadsheet_widget):
        # exclude 'viewport_changed' events since that doesn't change the DataFrame
        if (event['triggered_by'] != 'viewport_changed'):
            print(spreadsheet_widget.get_changed_df())

    spreadsheet_widget.on('json_updated', handle_json_updated)

Here are some examples of how the Events API can be applied.

This shows how you can use Modin-spreadsheet to filter the data that's being shown by a matplotlib scatter plot:

.. figure:: docs/images/linked_to_scatter.gif
    :align: left
    :target: docs/images/linked_to_scatter.gif
    :width: 600px

    Disclaimer: This is from the Qgrid documentation.

This shows how events are recorded in real-time. The demo is recorded on JupyterLab, which is not yet supported, but
the functionality is the same on Jupyter Notebook.

.. figure:: docs/images/events_api.gif
    :align: left
    :target: docs/images/events_api.gif
    :width: 600px

    Disclaimer: This is from the Qgrid documentation.

Running from source & testing your changes
------------------------------------------

If you'd like to contribute to Modin-spreadsheet, or just want to be able to modify the source code for your own purposes, you'll
want to clone this repository and run Modin-spreadsheet from your local copy of the repository.  The following steps explain how
to do this.

#. Clone the repository from GitHub and ``cd`` into the top-level directory::

    git clone https://github.com/modin-project/modin-spreadsheet.git
    cd modin-spreadsheet

#. Install the current project in `editable <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_
   mode::

    pip install -e .

#. Install the node packages that Modin-spreadsheet depends on and build Modin-spreadsheet's javascript using webpack::

    cd js && npm install .

#. Install and enable Modin-spreadsheet's javascript in your local jupyter notebook environment::

    jupyter nbextension install --py --symlink --sys-prefix modin_spreadsheet && jupyter nbextension enable --py --sys-prefix modin_spreadsheet

#. Run the notebook as you normally would with the following command::

    jupyter notebook

Manually testing server-side changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the code you need to change is in Modin-spreadsheet's python code, then restart the kernel of the notebook you're in and
rerun any Modin-spreadsheet cells to see your changes take effect.

Manually testing client-side changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the code you need to change is in Modin-spreadsheet's javascript or css code, repeat step 3 to rebuild Modin-spreadsheet's npm package,
then refresh the browser tab where you're viewing your notebook to see your changes take effect.

Running automated tests
^^^^^^^^^^^^^^^^^^^^^^^
There is a small python test suite which can be run locally by running the command ``pytest`` in the root folder
of the repository.

Contributing
------------
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. See the
`Running from source & testing your changes`_ section above for more details on local Modin-spreadsheet development.

If you are looking to start working with the Modin-spreadsheet codebase, navigate to the GitHub issues tab and start looking
through interesting issues.

Feel free to ask questions by submitting an issue with your question.
