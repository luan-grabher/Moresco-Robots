# Moresco-Robots
Program to execute robots on enterprise Moresco

Features:
-------------
* CRUD to register 'fisical' robots with .jar .py .cmd and .bat by our paths
* Caller to call to an robot to run
* Executor to run robots in call list

Configuration
===============

Ini file:
----------
1 - Copy **moresco-robots.ini.example** and rename to **moresco-robots.ini**

2 - Configure database path, parameters path and parameters return path. The base path for all paths can be where this git repo folder is installed.

Emails:
----------
> Copy **email_config.ini.example** and rename to **email_config.ini**
> Configure with an **GMAIL** mail and password.

Schedule tasks Monthly and Dayly:
----------
> On **./Server** use .xml files to Schedule with Windows Tasks Scheduller
> **NOTE:** The folders of files to execute scheduled tasks maybe changed

Database:
---------
> If you **NOT HAVE** a database configured, copy **moresco-robots.backup.sqlite** and rename to **moresco-robots.sqlite**
