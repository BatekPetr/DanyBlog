# Dany Blog
## Overview
This project implements a family web blog. It is a secure and private blog, where users and viewers are required to register
and be accepted in order to view and add content.

Hosted at [PythonAnywhere](https://petrb.eu.pythonanywhere.com/login?next=%2F).

## Used technologies
### Front end
* HTML, Jinja2 templating
* CSS, Bootstrap ([Clean Blog](https://startbootstrap.com/theme/clean-blog) theme)
* a little of Javascript for dynamic rendering in [users.html](src/templates/accounts/users.html)

### Back end
* Python Flask - blueprints, logging, routing, WTForms
* SQLAlchemy for database access and management
* Google OAuth authentication

### Development
* Pycharm, Mozilla Firefox, Google chrome
* Python [venv](https://docs.python.org/3/library/venv.html) environment
* CHatGPT for initial templates generation

## Ideas for improvement (ToDo)
* The blog was inteded for family members, therefore it is partially in Czech and partially in English 
(due to conflict of development habits and targeting of family). Make the App Multilingual with Flask Babel.
* Add possibility to comment and like posts.
* Add error HTML templates