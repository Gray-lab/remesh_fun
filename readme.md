# Software Engineer - Take Home Project
#### Martin Grym - April 10th, 2022
---

## Requirements
Local environment requirements are included in the requirements.txt file. 

```
asgiref==3.6.0
backports.zoneinfo==0.2.1
Django==4.2
sqlparse==0.4.3pyth
django-nose==1.4.7
coverage==7.2.3
```
---
## Recommended setup for local server
For running a local instance of the project, the following steps are recommended. A unix based operating system is assumed. The project was completed on, and the commands were tested on, an Ubuntu 20.04 instance running in WSL. 

Strictly speaking, it is not required that a virtual environment be used - but it is good practice.

1. Download the repository and navigate to the top directory: *add command!*
2. Ensure that python version 3.8.10 (or higher) is installed: 
```
$ python --version
Python 3.8.10
```
3. Create a virtual environment 
```
$ python -m venv ./path/to/virtual_env
```
4. Activate the virtual env: 
```
$ source ./path/to/virtual_env/bin/activate
```
5. Install requirements
```
$ pip install -r requirements.txt
```
6. *move to some directory?*
7. Run the Django development server
```
$ python manage.py runsever
```
8. Navigate to localhost (128:0:0:1) to see the web app!

Note: This server should not be used in production!

## To run tests
django-nose and coverage libraries were used to help with testing. If libraries were installed from the requirements.txt, these should already be installed. To run the tests:
```
$ python manage.py test
```
100% coverage was obtained in views and forms. Models.py also has good coverage, but the coverage library only detects the return and branch statement testing, thus incorrectly marking imports, etc as untested.

An html document showing the coverage of various modules can be found in the /remesh/cover directory after tests have been run.
This document is automatically created by coverage after the first time tests are run.


## Other notes
An admin page has been created for ease of editing the models
username = admin
password = testadmin

Note: I would never include login info in a readme for a production project! This is just for ease of use.
Another note: That includes things like secret keys, which would typically be kept in a .env file that is not tracked on git, and would be specified as environment variables in a hosting environment like Heroku.


