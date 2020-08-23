# Employee Management

    CRUD operation with Flask(Python)
        LogIn
        LogOut
        Create User Account
        Create, Read, Update, Delete employee record
        Control access
        Authentication

## Skills used

    Flask(Python), HTML, CSS

    Front-End
        HTML
        CSS

    Back-End
        Python
        Bcrypt
        JWT

    Database
        PostgreSQL

    Deploy
        Heroku

<img src="https://img.icons8.com/color/48/000000/python.png"/><img src="https://img.icons8.com/color/48/000000/html-5.png"/><img src="https://img.icons8.com/color/48/000000/css3.png"/><img src="https://img.icons8.com/color/48/000000/postgreesql.png"/><img src="https://img.icons8.com/color/48/000000/heroku.png"/><img src="https://img.icons8.com/color/48/000000/sass.png"/>
        
#### Setup Info

    pip install pipenv

    pipenv shell

    pipenv install flask

    pipenv install psycopg2
    pipenv install psycopg2-binary

    pipenv install flask-sqlalchemy (Tool to access SQL database like PostgreSQL)

    pipenv install gunicorn (Python Web Server to deploy to heroku)

    Shift + Ctrl + p  => choose the correct python interpreter

    Connect DB(PostgreSQL)
        from flask_sqlalchemy import SQLAlchemy

        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:port_number/database_name'
        app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

        db = SQLAlchemy(app)

    Create Data model into PostgreSQL
        python
        from app import db
        db.create_all()

    python-dotenv
        pipenv install python-dotenv

        app.py
            from dotenv import load_dotenv
            import os
            load_dotenv()
            os.getenv('NAME')

    JWT
        pipenv install flask-jwt-extended

        from flask_jwt_extended import (
            JWTManager, jwt_required, jwt_optional, create_access_token,
            get_jwt_identity, get_raw_jwt, set_access_cookies, unset_jwt_cookies
        )

    bcrypt
        pipenv install Flask-Bcrypt

        from flask_bcrypt import Bcrypt

        bcrypt = Bcrypt(app)

    Error handling: SQLAlchemy (Optional)
        pipenv install flake8

        Python: Select Linter
        flake8



<a href="https://icons8.com/icon/13441/python">Python icon by Icons8</a>

<a href="https://icons8.com/icon/20909/html-5">Html 5 icon by Icons8</a>

<a href="https://icons8.com/icon/21278/css3">CSS3 icon by Icons8</a>

<a href="https://icons8.com/icon/38561/postgresql">PostgreSQL icon by Icons8</a>

<a href="https://icons8.com/icon/31085/heroku">Heroku icon by Icons8</a>

<a href="https://icons8.com/icon/QBqFNfPPB2Kx/sass">Sass icon by Icons8</a>
