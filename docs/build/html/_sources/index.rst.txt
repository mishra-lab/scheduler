.. Clinician Scheduler documentation master file, created by
   sphinx-quickstart on Thu Jan 10 13:28:57 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Clinician Scheduler
===================

.. contents:: Table of Contents
   :local:
   :backlinks: none

The clinician scheduler allows you to automatically generate and publish 
schedules that satisfy common constraints in an on-call system, while taking
into account the preferences of clinicians.

Setup
-----

Generating Google API credentials
"""""""""""""""""""""""""""""""""

.. note::
   This process should only be done the very first time you are running
   the program. If you have previously generated a credential file using
   this process you should be able to re-use it. Just make sure that the
   credential file is placed in the same folder as the executable (``scheduler.exe``).

The application uses Google calendar for retrieving clinician 
time-off requests and long weekend information, as well as uploading the 
generated schedule to the calendar. These operations require the use
of Google API credentials, which can be generated as follows.

1. Sign into https://console.developers.google.com.
2. Click on the project selector at the top left of the page.

.. figure:: _static/images/google_credentials/step2_select_a_project.png
   :class: with-border
   :target: _static/images/google_credentials/step2_select_a_project.png

3. Click on `New Project`.

.. figure:: _static/images/google_credentials/step3_new_project.png
   :class: with-border
   :target: _static/images/google_credentials/step3_new_project.png

4. Enter "Clinician Scheduler" as the `Project Name` and click `Create`.

.. figure:: _static/images/google_credentials/step4_create_project.png
   :class: with-border
   :target: _static/images/google_credentials/step4_create_project.png

5. Now you should see the dashboard for the Clinician Scheduler project. 
   You will need to enable the Google calendar API. Click on `Enable APIs and Services`.

.. figure:: _static/images/google_credentials/step5_enable_apis_and_services.png
   :class: with-border
   :target: _static/images/google_credentials/step5_enable_apis_and_services.png

6. Search for "Google calendar API" using the search bar, and select it.

.. figure:: _static/images/google_credentials/step6_search_calendar_api.png
   :class: with-border
   :target: _static/images/google_credentials/step6_search_calendar_api.png

7. Click `Enable`.

.. figure:: _static/images/google_credentials/step7_enable_calendar_api.png
   :class: with-border
   :target: _static/images/google_credentials/step7_enable_calendar_api.png

8. Now you should see the overview page for the Google calendar API. 
   To generate the credentials, click `Create credentials`.

.. figure:: _static/images/google_credentials/step8_create_credentials.png
   :class: with-border
   :target: _static/images/google_credentials/step8_create_credentials.png

9. On the credentials form, choose "Google Calendar API" for `Which API are you using?`,
   then "Other UI (e.g. Windows, CLI tool)" for `Where will you be calling the API from?`
   and "User data" for `What data will you be accessing?`. Then click on `What credentials do I need?`.

.. figure:: _static/images/google_credentials/step9_credentials_form.png
   :class: with-border
   :target: _static/images/google_credentials/step9_credentials_form.png

10. Enter "Client" for `Name` and click on `Create OAuth client ID`.

.. figure:: _static/images/google_credentials/step10_oauth_client_id.png
   :class: with-border
   :target: _static/images/google_credentials/step10_oauth_client_id.png

11. Choose the email address associated to your account for `Email address`
    and enter "Clinician Scheduler" for `Product name shown to users`, then 
    click `Continue`.

.. figure:: _static/images/google_credentials/step11_oauth_consent_screen.png
   :class: with-border
   :target: _static/images/google_credentials/step11_oauth_consent_screen.png

12. Your credentials are now generated! Make sure to download and save 
    them in the same location that you unzipped the application, so that
    the credential file and the executable file (``scheduler.exe``) are in the same folder.

.. figure:: _static/images/google_credentials/step12_download_credentials.png
   :class: with-border
   :target: _static/images/google_credentials/step12_download_credentials.png

.. attention::
   Make sure the credential file is saved as ``credentials.json`` (rename it, if necessary), 
   or otherwise the application will not be able to recognize it!

Google Calendar Configuration
"""""""""""""""""""""""""""""

Creating a calendar
~~~~~~~~~~~~~~~~~~~

1. Navigate to https://calendar.google.com and sign in to the appropriate account.

2. Click on the settings icon next on the left side, and select `New Calendar`.

.. figure:: _static/images/google_calendar/create_calendar/step2_new_calendar.png
   :class: with-border
   :target: _static/images/google_calendar/create_calendar/step2_new_calendar.png

3. Enter a name for your calendar and click `Create calendar`.

.. figure:: _static/images/google_calendar/create_calendar/step3_create.png
   :class: with-border
   :target: _static/images/google_calendar/create_calendar/step3_create.png

Adding holiday events
~~~~~~~~~~~~~~~~~~~~~

.. note::
   It is recommended to create full-day events for holidays and clinician requests.

Create an event by clicking on any cell in the calendar. Make sure that 
the name of the event you create starts with "**[holiday]**", so that the
scheduler can recognize the event correctly. Click `Save` once you are done.

.. figure:: _static/images/google_calendar/create_holiday.png
   :class: with-border
   :target: _static/images/google_calendar/create_holiday.png

.. _adding-clinician-requests:

Adding clinician requests
~~~~~~~~~~~~~~~~~~~~~~~~~

Create an event by clicking on any cell in the calendar. Make sure that 
the name of the event you create has the format: "**[request] Name**", so that the
scheduler can recognize the event correctly. Click `Save` once you are done.

.. figure:: _static/images/google_calendar/create_request.png
   :class: with-border
   :target: _static/images/google_calendar/create_request.png

.. Warning::
   It is important that the name you use in the event name matches the name in 
   the clinician configuration you create in :ref:`clinician-configuration`.

Usage
-----

.. _authentication:

Authentication
""""""""""""""
When the scheduler first makes a connection to Google calendar, it needs
to create an authentication token, which will be used to simplify future 
connections.

This requires you to allow the scheduler application to access a calendar 
that you specified. You may encounter this when using any functionality that
interacts with Google calendar, for example in :ref:`generating-a-schedule`
or in :ref:`publishing-a-schedule-to-google-calendar`.

1. The scheduler should have automatically opened the access request page
   in a browser window, in which case you can skip to step 2. **Otherwise**, 
   locate the command prompt for the scheduler. You should see instructions 
   to open the access request printed on the command prompt. Follow these instructions
   in order to open the access request page manually.

.. figure:: _static/images/authentication/open_in_browser.png
   :class: with-border
   :target: _static/images/authentication/open_in_browser.png

2. Follow the instructions on the access request page in order to allow
   the scheduler application to read/write from/to the calendar you specified.

.. figure:: _static/images/authentication/access_request.png
   :class: with-border
   :target: _static/images/authentication/access_request.png

   **(Optional)** If you opened the access request manually in step 1, you will
   receive an authentication code which needs to be pasted into the command prompt

.. figure:: _static/images/authentication/access_request_auth_code.png
   :class: with-border
   :target: _static/images/authentication/access_request_auth_code.png

3. Once you have completed the authentication process, the scheduler will
   automatically resume its functionality.

.. _clinician-configuration:

Clinician Configuration
"""""""""""""""""""""""

Before we can generate a schedule, we need to create a configuration file
that specifies which clinicians are available, and how many weeks each 
clinician should fulfill.


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
   `New Config`.

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
click on `Open Config`, navigate to the location of the configuration file,
and select it.

.. figure:: _static/images/configuration/load_config.png
   :class: with-border
   :target: _static/images/configuration/load_config.png

.. _adding-a-new-clinician:

Adding a new clinician
~~~~~~~~~~~~~~~~~~~~~~

1. From the configuration tab, click `New Clinician`. You should see a
form for supplying details.

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

Scheduling
""""""""""

.. _generating-a-schedule:

Generating a schedule
~~~~~~~~~~~~~~~~~~~~~
Once you have created a configuration file, you can switch over to the 
`Scheduler` tab of the application in order to generate a schedule.

1. From the scheduling tab, click on `Load` and select the configuration
   file that you generated in :ref:`clinician-configuration` 

.. figure:: _static/images/scheduling/generate_schedule/step1_load_config.png
   :class: with-border
   :target: _static/images/scheduling/generate_schedule/step1_load_config.png

2. Enter the calendar year for the schedule that you want to generate.

.. figure:: _static/images/scheduling/generate_schedule/step2_calendar_year.png
   :class: with-border
   :target: _static/images/scheduling/generate_schedule/step2_calendar_year.png

3. **(Optional)** In order to retrieve the time-off requests that were populated
   in Google calendar in :ref:`adding-clinician-requests`, we need to specify the
   calendar ID. Open the calendar in your browser, and navigate to the 
   `Settings and sharing` page.
   On the setting page, navigate to the `Integrate calendar` section, and copy
   the value under `Calendar ID` to your clipboard. 
   Paste this value into the `Google Calendar ID` textbox on the `Scheduler`
   tab.

.. figure:: _static/images/scheduling/generate_schedule/step3_calendar_id.png
   :class: with-border
   :target: _static/images/scheduling/generate_schedule/step3_calendar_id.png

4. **(Optional)** If you supplied a calendar ID in step 3, you can configure 
   the options `Retrieve Time-off Requests` and `Retrieve Long Weekends` as necessary.
   Enabling `Retrieve Time-off Requests` will read the time-off calendar events
   from the calendar specified in `Calendar ID`, while enabling 
   `Retrieve Long Weekends` will read the holiday events from that calendar.

.. figure:: _static/images/scheduling/generate_schedule/step4_retrieve_events.png
   :class: with-border
   :target: _static/images/scheduling/generate_schedule/step4_retrieve_events.png

5. **(Optional)** In the case that you only need to generate a schedule for
   a subset of the calendar year, you can select the amount of blocks you need 
   to generate by specifying a value in `Number of Blocks`. By default, the 
   scheduler will generate a full schedule, corresponding to 26 blocks.

.. figure:: _static/images/scheduling/generate_schedule/step5_number_of_blocks.png
   :class: with-border
   :target: _static/images/scheduling/generate_schedule/step5_number_of_blocks.png

6. Click on `Generate`, and after a few moments you should see a preview of
   the generated schedule in the table.

   **(Optional)** See :ref:`authentication` in case you encounter problems
   with Google calendar at this stage.

.. figure:: _static/images/scheduling/generate_schedule/step6_generate_schedule.png
   :class: with-border
   :target: _static/images/scheduling/generate_schedule/step6_generate_schedule.png

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

.. _publishing-a-schedule-to-google-calendar:

Publishing a schedule to Google Calendar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are satisfied with the generated schedule, you can publish it
to Google calendar, by clicking on `Publish`.

.. figure:: _static/images/scheduling/publish_schedule/publish_schedule.png
   :class: with-border
   :target: _static/images/scheduling/publish_schedule/publish_schedule.png

.. warning::
   This process might take some time, especially if the number of events
   to be published is quite large.

Clearing a published schedule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to remove all the published events created by the application,
simply click on `Clear`.

.. figure:: _static/images/scheduling/publish_schedule/clear_schedule.png
   :class: with-border
   :target: _static/images/scheduling/publish_schedule/clear_schedule.png

.. warning::
   This process might take some time, especially if the number of published
   events is quite large.