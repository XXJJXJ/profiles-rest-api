# Profiles REST API


### Vagrant Guides
* To Connect to vagrant server, on terminal do: `vagrant ssh`
  * Make sure the `Vagrantfile` is present in working directory
  * Make sure Vagrant and VirtualBox is downloaded
* To set up python virtual environment, on terminal do: `python -m venv ~/env`
* Change virtual machine directory to the `/vagrant` directory, do: `source ~/env/bin/activate` to activate virtual environment
* Set up the packages required by indicating them in the `requirements.txt` file (can be done locally since the documents are synced)
* In the virtual environment, do: `pip install -r requirements.txt` to install the packages in virtual environment

### Django Guides (Creating Django project and app)
* On the virtual environment, do: `django-admin.py startproject profiles_project .` to activate the python script, that takes in 3 arguments, `startproject` is the command, `profiles_project` is the project name and `.` indicates current directory
  * A file `manage.py` will be created in the current directory that will be used to create sub-apps
* Do `python manage.py startapp profiles_api`, this will create a new subfolder called `profiles_api`, a new django app within our project

#### How to enable a django app
* Go into the app's folder(`profiles_project`), in `settings.py`:
  * The variable `INSTALLED_APPS` contains a list of all the apps we need to use for our project
  * Add `'rest_framework', 'rest_framework.authtoken', 'profiles_api'` to `INSTALLED_APPS` list. (This step varies for each project)


### How to test
* On the virtual environment, do: `python manage.py runserver 0.0.0.0:8000`
* Then on our browser, type in `127.0.0.1:8000` to see the django web framework
  * Note `127.0.0.1` represents `localhost` and `8000` is the port number.


### Create our user database model & add user model manager

* Refer to `models.py` under `profiles_api` directory

### Set our custom user model

* Under `/profiles_project/settings.py` scroll to the bottom and add a line `AUTH_USER_MODEL = 'profiles_api.UserProfile'`

### Create migrations and sync DB

* cd to project directory `profile-rest-api`
  * On terminal do: `vagrant up` (if virtual machine not on)
  * Then `vagrant ssh` (if not connected to virtual environment)
  * On the virtual environment cd to `/vagrant/`
  * Do: `source ~/env/bin/activate` to switch to python venv
  * Do: `python manage.py makemigrations profiles_api`, "profiles_api" is the name of the app
    * With this, "UserProfile" written in the previous step is created
  * To run our migration, do: `python manage.py migrate`

### Create Superuser
* cd to project directory `profile-rest-api`
  * On terminal do: `vagrant up` (if virtual machine not on)
  * Then `vagrant ssh` (if not connected to virtual environment)
  * On the virtual environment cd to `/vagrant/`
  * Do: `source ~/env/bin/activate` to switch to python venv
  * Do: `python manage.py createsuperuser` and it will prompt us to key in our:
    * Email address (use your own)
    * Name
    * Password (twice, need to be strong)(!!!)
    * (If weak password is used, confirmation is required, y/N)

#### Enable Django admin
* On `/profiles_api/admin.py` import `models` ...
* Changes are made on the file...

#### Test Django admin
* On the virtual environment (through `source ~/env/bin/activate`)
* Run `python manage.py runserver 0.0.0.0:8000`
* Then go to your browser to visit `127.0.0.1:8000/admin` or `localhost:8000/admin`
* Log in to the superuser account created using your own credentials
  * On the page, we see apps in our Django project
  * Under `PROFILES_API`, the `User profiles` is named after our `UserProfile` model
  * Click `User profiles` and we see all the user profiles created
  * Click on the email to see the details (note: Password is hashed)

### Create APIViews
* Under `/profiles_api/` directory, open `views.py`
* Make the edits as shown in the new `views.py` file
  * `get` method
  * `post` method
  * `put` method
  * `patch` method
  * `delete` method

#### Configure view URL
* Under `/profiles_project/` directory, open `urls.py`
  * In `/profiles_project/urls.py` add an import for `include` and add the line `path('api/', include('profiles_api.urls'))` in `urlpatterns` variable
* Create another `urls.py` file under `/profiles_api/` directory
  * Make the change as per reflected in this file

#### Create a Serializer
* Under `/profiles_api` directory, create a file `serializers.py`
  * Edit it as per the file

### Create ViewSet
* Under `/profiles_api/` directory, open `views.py`
* Make the edits as shown in the new `views.py` file (a new class `HelloViewSet` under `HelloApiView` section)
  * `list` method
  * `create` method
  * `retrieve` method
  * ...

#### Add URL Router
* Changes made in `urls.py` under `/profiles_api/`

#### Testing ViewSet
* For the main screen at `http://localhost:8000/api/hello-viewset/`, we do not see methods from `retrieve` onwards (only have list and create)
* `http://localhost:8000/api/hello-viewset/1/` allow us to see the other methods.

### Create Profile API
* Define `UserProfileSerializer` in `/profiles_api/serializer.py`
* In `/profiles_api/views.py` define `UserProfileViewSet`

#### Register profile Viewset with the URL router
* In `/profiles_api/urls.py`, register profile ViewSet using the `router`

#### Test creating a profile
* Run the server as per above (using vagrant)
* On browser, go to `http://localhost:8000/api/profile/` and play around

#### Create permission class
* This is to avoid any users to modify other users
* Done using Django permission class
* Create a new file `permissions.py` under `/profiles_api/`
  * Define a class `UpdateOwnProfile`
    * Define a method `has_object_permission()`

#### Add authentication and permissions to ViewSet
* Changes in `/profiles_api/views.py`
  * Import `TokenAuthentication` from rest_framework.authentication
  * Import `permissions` from profiles_api
  * Update `UserProfileViewSet` class
