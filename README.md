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

### Add Search profile feature
* Import `filters` from rest_framework in `views.py`
* Edit `UserProfileViewSet` class

### Create Login API

* In `/profiles_api/views.py`:
  * Import `ObtainAuthToken` from rest_framework.authtoken.views
  * Import `api_settings` from rest_framework.settings
  * Define `UserLoginApiView` class
* In `/profiles_api/urls.py`:
  * Add a new path `path('login/', views.UserLoginApiView.as_view()),` in `urlpatterns`

#### Set token header using ModHeader Chrome extension (only for testing purposes)
1. "Login" using the Login API to obtain an authtoken
2. Open ModHeader and on the "Request Header" indicate "Authorization"
3. Type "Token " and paste the authtoken in the value field

With this, we can go to the profile i.e. `http://localhost:8000/api/profile/*` where `*` is the id of your authenticated profile.
We can now modify our own profile (previously blocked by the permissions tab) since we are authenticated.

### Create profile feed API

#### Create new Django model for storing user profile feed items
* Under `/profiles_api/models.py`:
  * Import `settings` from django.conf
  * Define a `ProfileFeedItem` class

#### Create and run model migration
* Connect to vagrant:
  * On terminal do:
    * `vagrant up` to start up virtual machine
    * `vagrant ssh` to connect to virtual machine
    * `cd /vagrant` to change directory to shared directory
    * `source ~/env/bin/activate` to activate virtual environment
* Then run `python manage.py makemigrations`
* Then the `ProfileFeedItem` model is created
  * Can be verified by looking under `/profiles_api/migrations` directory

#### Add profile feed model to admin
* Under `/profiles_api/admin.py`:
  * Add a line: `admin.site.register(models.ProfileFeedItem)`

#### Create profile feed item serializer
* Under `/profiles_api/serializers.py`:
  * Define a `ProfileFeedItemSerializer` class

#### Create ViewSet for profile feed item
* Under `/profiles_api/views.py`:
  * Define a `UserProfileFeedViewSet` class
* Under `/profiles_api/urls.py`:
  * Add a line: `router.register('feed', views.UserProfileFeedViewSet)`

#### Add permissions for feed API
* Under `/profiles_api/permissions.py`:
  * Define a `UpdateOwnStatus` class
* Under `/profiles_api/views.py`:
  * Import `IsAuthenticatedOrReadOnly` from rest_framework.permissions 
  * Edit `UserProfileFeedViewSet` class:
    * Add: ```permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )```

#### Restrict viewing status to authenticated users only
* Under `/profiles_api/views.py`:
  * Change import `IsAuthenticatedOrReadOnly` from rest_framework.permissions
  * To import `IsAuthenticated` from rest_framework.permissions
  * And adjust the `permissions_classes` in `UserProfileFeedViewSet` class accordingly

### Deploy app to AWS (Free tier)
* Note, these are the steps in the tutorial, some steps might not be necessary

#### Add key pair
* After signing in to the AWS console:
  * Click on `services` and then `Compute`
  * On the left bar, scroll down to `Network & Security` section
  * Click on `Key Pairs`
  * Click on `Actions` and then `Import key pair`
    * The key should be called `id_rsa.pub` in the home directory
    * Search up google on how to generate an rsa key-pair if it does not exist
  * On the directory with `id_rsa.pub`, do: `cat id_rsa.pub` and copy the key
  * Paste it on the AWS console at the "Import Key pair" page

#### Create an EC2 server instance
* On the AWS console, navigate to the EC2 Dashboard
* Click on `Launch Instance`
* Select `Ubuntu` and AMI to be `Ubuntu Server 18.04 LTS`
* Scroll down to the "Security Group" portion
  * Add a new rule to allow HTTP connection
* Launch instance

#### Add deployment scripts and config to project
* Created a `/deploy_v2/` directory containing:
  * `setup.sh`: Used for when we first set up our Server
    * Change the `PROJECT_GIT_URL` to our actual git clone url
    * The `PROJECT_BASE_PATH` is the location where we are going to store our project on the server
    * The subsequent lines are commandline commands to be executed on server
  * `update.sh`: Used to update the code on the server when we make changes
  * The other 2 files are config files

* Go to `/profiles_projects/settings.py` change `DEBUG` to False, or alternatively
* change the line to `DEBUG = bool(int(os.environ.get('DEBUG', 1)))`, which leaves it as 1 if not found (i.e. at development phase)
* Notice in the `/deploy_v2/supervisor_profiles_api.conf`, DEBUG is set to 0
* At the end of `settings.py` add line: `STATIC_ROOT = 'static/'` which is the location where django saves the static files

* **Note**: Before we actually deploy, the scripts need to have the permission to be executed:
  * On our working directory (terminal), do: `chmod +x deploy_v2/*.sh` to add executable rights to .sh files under `/deploy_v2/` directory

#### Deploy to server
* Go to AWS console > Services > Compute > EC2
  * Select `Running instances`
  * Hover over `Public DNS (IPv4)` and copy to clipboard
  * On our local terminal, use ssh:
    * `ssh ubuntu@<Paste whatever that was copied>` and press enter and "Yes" to connect to the server
  * On our GitHub page, navigate to the `/deploy_v2/` directory and click on `setup.sh`
    * Select "Raw" mode and **copy the url** on the browser
  * On our local terminal:
    * `curl -sL <Paste the copied link> | sudo bash -` used to retrieve contents from an url

* Once done, copy the `Public DNS (IPv4)` link again
* Go to `/profiles_project/settings.py` find `ALLOWED_HOSTS` list and add the copied link as a string
* Also add `'127.0.0.1'` to allow us to connect on localhost (?)
* Push all changes to GitHub and on the server, run the `update.sh` by:
  * Connect to server first (ssh ... command)
  * Change directory to the project directory: `cd /usr/local/apps/profiles-rest-api/`
  * Do: `sudo sh ./deploy_v2/update.sh`
* Now we can access the site by inputting `<Link copied from Public DNS (IPv4)>/api/` as the url
