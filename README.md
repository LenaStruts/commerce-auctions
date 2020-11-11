# Auctions
> In this project I worked on creating an auction website using Django framework. 

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
The purpose of this project is to design an eBay-like e-commerce auction site using Django framework. 

## Screenshots
![Screenshot1](https://user-images.githubusercontent.com/61382735/98832278-eb584380-243c-11eb-9cbb-4404d268d8fb.png)
![Screenshot2](https://user-images.githubusercontent.com/61382735/96607975-2e6d3e00-12f9-11eb-920a-319115ca85e3.png)

## Technologies
* Python - version 3.6
* Django - version 3.1
* Gunicorn - version 20.0
* Postgres - version 12.4
* Bootstrap4

## Setup
```
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```

Create .env file such as: 
```
POSTGRES_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_NAME=<your_postgres_name>
POSTGRES_USER=<your_postgres_username>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_HOST=<your_postgres_url>
POSTGRES_PORT=<your_postgres_port>
DJANGO_SECRET_KEY=<your_django_secret_key>
```

```
python manage.py makemigrations auctions
python manage.py migrate
python manage.py runserver

```
See your website at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Features
* View active listings, add or remove them from the watchlist, look at the comments and previous bids
* Create your own listings and close the auction, when you get the desired bid
* Bid and comment on listings you like, and win the auction with the highest bid

To-do list:
* improve design 
* improve responsiveness, in particular for mobile devices

## Status
Project is paused, because it fullfills the requirements of the course, but some changes to be done to improve functionality and design.

## Inspiration
This project is part of the Harvard course I am taking, in particular CS50’s Web Programming with Python and JavaScript, project 2 - commerce

## Contact
Created by [Lena Struts](https://www.linkedin.com/in/lena-yeliena-struts-5aa96292/) - feel free to contact me!
