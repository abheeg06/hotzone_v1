# COMP3297 GroupX HotZone

UI prototype: https://balsamiq.cloud/s976ssg/pwtzqt3  
Team Drive: https://drive.google.com/drive/folders/1SM24mntOmWvPcFDYgmVo8c5IKaX5165z?usp=sharing  

# How to run
First, clone the repo to your local directory with:
`git clone https://github.com/abheeg06/hotzone_v1.git`

In the directory, execute:
`cd hotzone_v1/hotzone_main`
`pip install pipenv`
`python -m pipenv install django~=3.1.2`
`python -m pipenv shell`
You should launched a shubshell in virtual environment

To run the server, execute the following commands in the subshell:
`cd project`
`python manage.py runserver`
The server should be started on http://127.0.0.1:8000/

Go to http://127.0.0.1:8000/cases to access the web app.

If you need to access the admin site, login at http://127.0.0.1:8000/admin with
username: groupx
password: groupx
