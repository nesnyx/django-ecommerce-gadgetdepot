
# Ecommerce Gadget Depot Django Project




![App Screenshot](https://download.logo.wine/logo/Django_(web_framework)/Django_(web_framework)-Logo.wine.png)

I am building an application project with Django and Python, where I also use Bootstrap for its appearance and styling.

Briefly, this application is an e-commerce web application that specifically sells mobile phones. The application is also integrated with a payment gateway such as Paypal.

django : https://www.djangoproject.com/

Paypal Developer : https://developer.paypal.com/

bootstrap : https://getbootstrap.com/ 


## Installation
You can clone this project use 

```git clone https://github.com/nesnyx/django-ecommerce-gadgetdepot.git```


Install this project with pip

- You need make your own virtual environment
```bash
  python -m venv venv
  source venv/Scripts/activate
```
- Install packages needed, i included in this repo
```
  pip install -r requirements.txt
```

- Migrate the database, you can use anything database do you want like postgresql,mysql, in this case i just use SQLite

```
  python manage.py makemigrations
  python manage.py migrate
```

- Run this project just typing like this

```
  python manage.py runserver
```


## Environment Variables

To run this project, you will need to edit the following environment variables to your .env file

`SECRET_KEY`

`DEBUG`

`EMAIL_HOST`

`EMAIL_PORT`

`EMAIL_HOST_USER`

`EMAIL_HOST_PASSWORD`

`EMAIL_USE_TLS`

based about EMAIL the following want to know more please read documention https://docs.djangoproject.com/en/5.0/topics/email/


## Feedback

If you have any feedback, please reach out to us at baraaris64@gmail.com


## Support

For support, email baraaris64@gmail.com

