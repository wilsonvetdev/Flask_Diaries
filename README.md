# Flask_Diaries

### Dependencies and Requirements:
* Python 3.9.1
* pip
* flask
* python-dotenv
* flask-wtf
* flask-sqlalchemy
* flask-migrate
* flask-login
* flask-moment

### Setup

1. Git clone this repository onto local environment
2. cd into the repo
  * Run below command to ensure Python 3 environment and download requirements for this application, and not the Python that comes installed with your local machine.
  * $ python3 -m venv env
  * $ source env/bin/activate
  * $ pip install -r requirements.txt
3. run in CLI - flask run <br><b>Note: ENV variables defined in .flaskenv file already if you want to take a look.</b>
4. visit http://127.0.0.1:5000/ on your browser

### Functionalities

1. User is able to register a new account.
2. Existing user/blogger is able to create/edit/delete posts.
3. Posts are ordered by timestamp in descending order on a user's home page.
4. Updated posts will appear on the top of all posts.
