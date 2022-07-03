# URL-Shortner


 ## Setup
 
 
 To setup this project in your local machine:
 
  1. Create a directory in your local machine (Name of your choice):  <br> ```$ mkdir Shortner```

  2. Change present working directory into `Office`: <br> ```$ cd Shortner```

  3. Create a Virtual Environment: <br> ```$ python3 -m venv venv```

  4. Activate Virtual Environment: <br> ```$ source venv/bin/activate```

  5. Clone the Staging branch of this repository: <br> ```$ git clone https://github.com/DrAnonymousNet/URL-Shortner.git```

  6. Intall Dependencies in the requirements.txt: <br> ```$ pip install -r requirements.txt``` <br> 

  7. Change into the `url_shortner` directory and create a `.env` file

  ```
  11. Make migrations: <br> ```$ python manage.py migrate```
  12. Run the development server: <br> ```$ python manage.py runserver```
  
  ## File Tree
  


```

url_shortner/

├── api
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
└── url_shortner
    ├── .env
    ├── asgi.py
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   └── settings.cpython-38.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

  
  ```


