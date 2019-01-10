.. Clinician Scheduler documentation master file, created by
   sphinx-quickstart on Thu Jan 10 13:28:57 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Clinician Scheduler
===================

.. toctree::
   :maxdepth: 2

The clinician scheduler allows you to automatically generate and publish 
schedules that satisfy common constraints in an on-call system, while taking
into account the preferences of clinicians.

Setup
-----
Download and unzip the compressed file to an appropriate folder.

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

.. image:: images/gapi/step2_select_a_project.png

3. Click on `New Project`.

.. image:: images/gapi/step3_new_project.png

4. Enter "Clinician Scheduler" as the `Project Name` and click `Create`.

.. image:: images/gapi/step4_create_project.png

5. Now you should see the dashboard for the Clinician Scheduler project. 
You will need to enable the Google calendar API. Click on `Enable APIs and Services`.

.. image:: images/gapi/step5_enable_apis_and_services.png

6. Search for "Google calendar API" using the search bar, and select it.

.. image:: images/gapi/step6_search_calendar_api.png

7. Click `Enable`.

.. image:: images/gapi/step7_enable_calendar_api.png

8. Now you should see the overview page for the Google calendar API. 
To generate the credentials, click `Create credentials`.

.. image:: images/gapi/step8_create_credentials.png

9. On the credentials form, choose "Google Calendar API" for `Which API are you using?`,
then "Other UI (e.g. Windows, CLI tool)" for `Where will you be calling the API from?`
and "User data" for `What data will you be accessing?`. Then click on `What credentials do I need?`.

.. image:: images/gapi/step9_credentials_form.png

10. Enter "Client" for `Name` and click on `Create OAuth client ID`.

.. image:: images/gapi/step10_oauth_client_id.png

11. Choose the email address associated to your account for `Email address`
and enter "Clinician Scheduler" for `Product name shown to users`, then 
click `Continue`.

.. image:: images/gapi/step11_oauth_consent_screen.png

12. Your credentials are now generated! Make sure to download and save them 
in the same location that you unzipped the application, so that the 
credential file and the executable file (``scheduler.exe``) are in the same folder.

.. image:: images/gapi/step12_download_credentials.png

.. attention::
   Make sure the credential file is saved as ``credentials.json`` (rename it, if necessary), 
   or otherwise the application will not be able to recognize it!

Usage
-----
