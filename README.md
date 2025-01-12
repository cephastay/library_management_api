# Library Management System API
   __Overview__  
```
The Library Management System API provides a set of RESTful endpoints 
    
It supports functionalities like browsing books, borrowing and
returning books, writing reviews, and other database CRUD actions on b
```
__Requirements__    

    The required software/tool and libraries you will need for the  
    API to function properly are listed below. The bullets are  
    hyperlinked to the respective tool website.

- [Python 3.10+](https://www.python.org/downloads/release/python-3100/)
- [Django 5.0+](https://www.djangoproject.com/download/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SQLite 3(for development)](https://www.sqlite.org/download.html) or [MySQL 8 (for production)](https://dev.mysql.com/downloads/installer/)

#
__Installation__    

The instructions outlined here should be followed through   
in your command line terminal. These are done with `bash` shell.

_*Clone the repository from github:*_ 
```bash
$ git clone https://github.com/cephstay/library_management_api.git
```

_*Move into the automatically created directory: `library_management_api
```bash
$ cd library_management_api
```

_*Create and activate the virtual environment `library_venv`*_
```bash
$ source library_venv/bin/activate
```

_*Install the library packages in the `requirements.txt` file*_
```bash
$ pip install -r requirements.txt
```

_*Set up your database connection settings in the `.env` file*_

- [Instructions in env_setup.md file]()

_*Migrate the database*_
```bash
$ python manage.py migrate
```

_*Create a SuperUser (Optional)*_
```bash
$ python manage.py createsuperuser --username --email --password
```

_*Start the Development Server*_
```bash
$ python manage.py runserver
```

The API should now be running at `https://127.0.0.1:8000`
