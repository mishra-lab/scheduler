.. Clinician Scheduler documentation master file, created by
   sphinx-quickstart on Thu Jan 10 13:28:57 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

User Manual
===========

.. contents:: Table of Contents
   :local:
   :backlinks: none

.. _clinician-configuration:

Clinician Configuration
"""""""""""""""""""""""

The clinician configuration specifies which clinicians are available,
which divisions they are covering, and how many weeks they should cover
in each of their divisions.


Creating a new configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, you will get a blank configuration file when you launch
the program. If you would like to discard the changes you have made and 
start a configuration file from scratch, simply click on `New Config`.

.. figure:: _static/images/configuration/new_config.png
   :class: with-border
   :target: _static/images/configuration/new_config.png

.. warning::
   Unsaved changes to a configuration file will be discarded upon clicking
   on `New Config`.

Saving the configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are ready to save the configuration you created, click on 
`Save Config` and choose a place to save your file. Make note of the name
and directory of the file so you could load it in future runs.

.. figure:: _static/images/configuration/save_config.png
   :class: with-border
   :target: _static/images/configuration/save_config.png

Loading a configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you would like to open a previously created configuration file, simply
click on `Open Config`, navigate to the location of the file,
and select it.

.. figure:: _static/images/configuration/load_config.png
   :class: with-border
   :target: _static/images/configuration/load_config.png

.. _adding-a-new-clinician:

Adding a new clinician
~~~~~~~~~~~~~~~~~~~~~~

1. From the configuration tab, click `New Clinician`. You should see a
form for supplying clinician details.

.. figure:: _static/images/configuration/add_clinician/step1_new_clinician.png
   :class: with-border
   :target: _static/images/configuration/add_clinician/step1_new_clinician.png

2. Fill out the name, email (optional), and divisions that the clinician
   will be covering. To add a division you can click on `Add` and a new row 
   will be added to the table which you can fill out. You can set the minimum
   and maximum number of blocks that a clinician can work in a given division. 

.. note::
    A single block corresponds to two weeks.

.. figure:: _static/images/configuration/add_clinician/step2_add_division.png
   :class: with-border
   :target: _static/images/configuration/add_clinician/step2_add_division.png

3. To delete a row from the table, select the row and then click `Remove`.

.. figure:: _static/images/configuration/add_clinician/step3_remove_division.png
   :class: with-border
   :target: _static/images/configuration/add_clinician/step3_remove_division.png

4. When you are finished entering the data for the clinician, click `Ok`.
   You should now see a new entry in the main table for that clinician.

.. figure:: _static/images/configuration/add_clinician/step4_add_clinician.png
   :class: with-border
   :target: _static/images/configuration/add_clinician/step4_add_clinician.png

Deleting an existing clinician
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To delete an existing clinician, simply select a row corresponding
to the clinician in the table and click on `Delete Clinician`.

.. figure:: _static/images/configuration/delete_clinician.png
   :class: with-border
   :target: _static/images/configuration/delete_clinician.png


Editing an existing clinician
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To edit the information of a clinician, select a row corresponding
to the clinician in the table and click on `Edit Clinician`. You should
see a dialog window where you can change the information. For more 
details on how to enter data in the edit dialog, see :ref:`adding-a-new-clinician`.

.. figure:: _static/images/configuration/edit_clinician.png
   :class: with-border
   :target: _static/images/configuration/edit_clinician.png

Requests & Holiday Weekends
"""""""""""""""""""""""""""

TODO....

Scheduling
""""""""""

.. _generating-a-schedule:

Generating a schedule
~~~~~~~~~~~~~~~~~~~~~
Once you have created a configuration file, you can switch over to the 
`Scheduler` tab of the application in order to generate a schedule.

TODO....

.. note::
   It is possible that the scheduler will not be able to come up with a 
   schedule that satisfies your constraints. You can try adjusting 
   some constraints by changing the minimum and maximum number of blocks of
   clinicians in the configuration file. See :ref:`clinician-configuration`
   for more information on changing the configuration file.

Exporting a schedule
~~~~~~~~~~~~~~~~~~~~

If you are satisfied with the generated schedule, you can choose to export
it as an Excel file. There are two format options: `Yearly Export` and 
`Monthly Export`. 

Selecting the `Yearly Export` option will generate an excel file with a single
sheet, displaying the clinicians that are covering a particular division
for a given week or weekend. It is very similar to the table output in
the application itself.

.. figure:: _static/images/scheduling/export_schedule/export_yearly.png
   :class: with-border
   :target: _static/images/scheduling/export_schedule/export_yearly.png

Selecting the `Monthly Export` option will generate a more detailed breakdown
of the schedule, with a separate sheet for every month, detailing which
clinician covers which division on which day.

.. figure:: _static/images/scheduling/export_schedule/export_monthly.png
   :class: with-border
   :target: _static/images/scheduling/export_schedule/export_monthly.png

Sample Output
"""""""""""""

Application Output
~~~~~~~~~~~~~~~~~~

TODO...

Yearly Excel Format
~~~~~~~~~~~~~~~~~~~

.. figure:: _static/images/scheduling/sample_yearly.png
   :class: with-border
   :target: _static/images/scheduling/sample_yearly.png

Monthly Excel Format
~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/images/scheduling/sample_monthly.png
   :class: with-border
   :target: _static/images/scheduling/sample_monthly.png