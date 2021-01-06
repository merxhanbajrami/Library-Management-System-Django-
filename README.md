# Library Management System
An automated system to manage a public library. Every member of the library club, can interact with the system by borrowing books online, also has its own dashboard where he can see his activity, return dates, deadlines etc. Also an administrator panel for librarians to control and manage the system easily through an interactive interface, where he can manage all books and users, also add new features to the system.

Development
The backend of the system is developed using Django. The frontend is developed with HTML,CSS + Bootstrap.

Setup
To use this template to start your own project:

Existing virtualenv
If your project is already in an existing python3 virtualenv first install django by running
$ pip install django
And then run the django-admin.py command to start the new project:

$ python3 -m django startproject \


First clone the repository from Github and switch to the new directory:

$ git clone git@github.com/merxhan/Library-Management-System-Django-.git

$ cd Library-Management-System-Django-

Activate the virtualenv for your project.

Install project dependencies:


$ pip install -r requirements.txt
Then simply apply the migrations:


$ python manage.py migrate
You can now run the development server:

$ python manage.py runserver
