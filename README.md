<div id="top"></div>

<!-- Task Manager Django Project -->
## Task Manager Django Project

### Built With

* [Django](https://www.djangoproject.com/)

<!-- GETTING STARTED -->
## Getting Started

### Main python packages used

* django
* django-cloudinary-storage
* django-heroku
* gunicorn
* Pillow
* psycopg2
* python-dotenv
* whitenoise

### Installation

1. Make migrations
   ```sh
   python manage.py makemigrations
   ```
2. Migrate changes to the database
   ```sh
   python manage.py migrate
   ```
3. Make a superuser so you have access to the admin panel and rights to edit other registered users
   ```sh
   python manage.py createsuperuser
   ```
4. Run the web server
   ```sh
   python manage.py runserver
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Possible actions

- [x] Create account
- [x] Login to the platform
- [x] Create Tasks
- [x] Update Tasks
- [x] Edit Profile
- [x] Administer Users
- [ ] Search for Tasks (not implemented)
- [ ] Projects Board (not implemented)

## Additional Info

### Pre-created users for testing

- [x] User: admin - administrator privileges
- [x] User: manager - manager privileges
- [x] User: employee - employee privileges

#### Password for all users - Softuni2022

<p align="right">(<a href="#top">back to top</a>)</p>

