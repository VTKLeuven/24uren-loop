# 24-hour run VTK

This is the repository of the 24-hour run app of VTK vzw. The app is based on a Django (Python) backend and a VueJS
 (Javascript) frontend. For development and deployment purposes, this app runs inside Docker. In production, the
  addition of an NGINX server, ASGI webserver (Daphne) and a Redis server is included. Finally, the database used in
   this project is Postgresql.
   
If you find a problem with or have additions to this guide, don't hesitate to open a ticket.
 
- [Features](#features)
  * [General information](#general-information)
  * [Views](#views)
  * [Admin](#admin)
- [Installation](#installation)
  * [Development](#development)
  * [Production](#production)
  * [Configuring HTTPS](#configuring-https)
  * [Database initialisation and migrations](#database-initialisation-and-migrations)
  * [Environment file](#environment-file)
  * [Build arguments](#build-arguments)
- [Permissions](#permissions)
- [Development](#development-1)
  * [Backend](#backend)
  * [Frontend](#frontend)
- [Useful commands](#useful-commands)
  * [Docker](#docker)
  * [Database](#database)
  * [Production](#production-1)
  * [Development](#development-2)

## Features
The front-end of the application consists of a couple of views (some of which are only visible when having the
 required permissions). On top of that there is also an admin page, only accessible for users within the staff group. 
 Keep in mind that all of the views (and even some parts of views) can be protected so that they are not visible to
 anyone without the required permissions. So can e.g. the queue be read-only for anyone, but can admins still edit
 and remove people from it.
 
### General information
This application allows tracking of runners during the 24 hour run. The core functionality provides a database backed
 queue and lap storage. At any time can these items be viewed from the admin page, later explained. On top of that, a
  point system for groups is provided. People (runners) can form groups and compete against other groups (or other
   people) for points. First of all, criteria determine an upper bound on their lap time. The lowest upper bound
    criterium will be selected for each lap and the corresponding amount of points will be rewarded to the runner. On
     top, groups can also have 'happy hours' which will provide a multiplier to the points, if completed within the
      happy hour. Finally, if using a more structured system, runners can be assigned to shifts. This system is
       purely informational and does not imply any other changes to the system.
 
### Views
This section will list the available views and their respective functionality:
- _Statistics_: This is the general index page consisting of several small lists and information cards. All of the
 following lists will contain up to three items:
  - _queue_: This will list the upcoming runners.
  - _top runners_: This will show the top three runners with their fastest lap. No runner will occur multiple times.
  - _top groups_: List the top groups according to their points.
  - _Most active runners_: The list shows the most active runners and their total amount of laps ran.
  
  On top of that, this page will also show the current runner with a timer, the two last laps with their time and a
   scatter plot consisting of the final 100 laps.
- _Full screen_: This view show the next, current and previous runner on a bigger scale. A good use of this is on a
 big screen for the audience to see. The current runner also has a live timer and the previous runner has his/her
  time displayed.
- _Queue_:  This page contains the full queue. By default, the queue is read-only to anyone. However, when logged in
 as an admin or someone with the correct permissions, this queue can be moved by dragging people or people can be
  removed by clicking the remove button. When pressing a card in the queue, information about that runner will be
   displayed in a form of "Quick information".
- _Queue up_: This view is by default only visible to the "competition" group, a group with a few more permissions
 than the anonymous user. This page is used to register people to the queue by making them scan their student id. If
  they do not exist in the system yet, a form will be displayed asking them to enter their personal information. Once
   successfully added to the queue, some quick information will be displayed on screen. This quick information is the
    same as in the queue.
- _Control_: This is maybe the most import view. It allows for advancement and reversal of laps. Once a runner
 finishes, the 'next lap' button should be pressed in order to finish this runners lap (and note the time) and start
  the next runners lap. If a mistake is made, pressing the reverse button will make sure the previous runner becomes
   'active' again and fixes it's time as if the advance button was never pressed.
- _Query_: This page contains some commonly requested queries on the database.
   
### Admin
The admin page contains the entire model. Any change necessary can be applied here (although, if possible, are best
 performed through the correct view). Only staff can and should have access to this page. The admin page also
  provides some other functionalities, not available in the views.
- _Runner_: In this section, runners can be pre-added in order to ensure a smooth registration during the event. On
 top of the regular registration, this method also provides a way to add a 'test time' and 'shifts' to a runner.
  The test time can be used when having pre-event tests and noting their time. It gives an indication of the
   performance of a runner. This time will be shown in the quick information when available. Finally, every runner
    can be edited here, also those signed up during the event. Using the search box above, you can search based on
     name and student id.
- _Lap_: This section contains the completed laps and their meta-data. After the event, all laps can also be
 downloaded as csv for future inspection. Please do not edit anything here during the event. If you do not know what
  you are doing, you will create inconsistencies and break the application. Using the search box above, you can
   search for specific names and student id's of users.
- _Queue tickets_: This is the database representation of the queue.
- _Universities_: When requiring multiple universities, add them here. By default, KU Leuven is already inserted.
- _Groups_: This section contains all the groups for which users can register. Groups have to be created through the
 admin, otherwise people cannot select them during sign up.
- _Happy hours_: Contains a list of all the possible happy hours a group can be registered to.
- _Criteria_: Contains a list of all the criteria, with their points.
- _Shifts_: A list of all the shifts for which runners can be signed up. Keep in mind, runners cannot sign themselves
 up for shifts, only admin can do this.
 
- _Users_: This can be used to add new users (not runners) to the application. Check the is_staff and is_admin box
 for full permissions, only put them in the 'competition' group for restricted permissions (i.e. the group required
  to access the queue up). 
 
## Installation
Both installation guides start from a server (host) with Docker installed. Next this git repository is pulled. The
 `app_home` variable will be used throughout the guide to indicate the home folder of the git repository (the one
  with manage.py file).
```bash
git clone <git url>
cd <app_home>
```
**Attention**: if running both development and production build on the same machine. They will use a shared database.

### Development
The first step is to build the development images. The building process might take a while. This step only when the
 node_modules changed or new packages are installed (using `npm install`, `pip install` or through a `git pull`).
```
sudo docker-compose -f docker-compose.dev.yml build
```
Afterwards, to boot up the development server, run the following command. This will run the Docker containers in a
 separate process.
```
sudo docker-compose -f docker-compose.dev.yml up -d
```
Again, the development boot up for the frontend takes a while. This progress can be monitored by typing one of the
 following commands. The latter will open up a continuous logger and can be closed using `CTRL+C`. Once the frontend
  indicates 100%, the build should be completed.
```
sudo docker-compose -f docker-compose.dev.yml logs
sudo docker-compose -f docker-compose.dev.yml logs -f
```
The development server is now up and running. To access the Docker containers, refer to [Docker commands](#docker).

If this is the first time, you might want to set up the database correctly and add (dummy) data. See [Database
 initialisation](#database-initialisation-and-migrations)

Make sure to check all the environment variables. `SERVER_*` variables should be adjusted to your local IP and ports
 for the development server. See [Environment variables](#environment-file)

You are now able to access your server from outside. Admin pages can be reached through port 8000 (where the django
 backend is running) and all frontend pages can be reached through port 8080 (where the VueJS development server is
  running). The development server has hot reload, which means that file edits should be directly reflected in the
   server. Monitoring these updates (e.g. for errors) can be done by opening up the Docker logs.
  
To gracefully shut down the docker containers, run
```
sudo docker-compose -f docker-compose.dev.yml down
```  

### Production
The production build will set run the application through an ASGI webserver (Daphne) behind a NGINX server for
 serving static assets. In addition to this, the SSE events also make use of a Redis server.
In order to run a production build, run the following command:
```
sudo docker-compose -f docker-compose.prod.yml build
```
Afterwards, the server can be booted up through. The parameter _<num_worker>_ is the amount of django workers.
```
sudo docker-compose -f docker-compose.prod.yml up -d --scale worker=<num_worker>
```
Finally, the nginx docker (together with certbot) also has to be booted:
```
cd nginx
sudo docker-compose up -d --build
```

**ATTENTION**: The following fields should be edited in the environment files ([Environment variables](#environment-file)):
- _.env.prod_: `SECRET_KEY` `DJANGO_ALLOWED_HOSTS` `SQL_PASSWORD`
- _.env.db.prod_: `POSTGRES_PASSWORD`

**ATTENTION**: The production build is not yet configured for HTTPS. This still has to be done ([here](#configuring-https)).

Before using the server, the database initialisation should be performed.
 In addition to this, all the static files must also be collected for NGINX to provide them:
```
sudo docker exec <docker_web_container_name> python manage.py collectstatic --noinput
```

To initialise the database, follow the first steps from the database setup ([Database initialisation](#database-initialisation-and-migrations)).
 To create an admin account (with secure password), run the following command in the web Docker container:
```
sudo docker exec -it <docker_web_container_name> python manage.py createsuperuser
```

Make sure to check all the environment variables. See ([Environment variables](#environment-file)).

Finally, before use, make sure to reset the queue ticket sequence in the database and make sure the queue is empty.
 This allows the new queue to begin from scratch (although it should never overflow, better safe than sorry).
```
sudo docker exec <docker_db_container_name> psql -U <username> -d <db_name> -c "alter sequence competition_queueticket_id_seq RESTART WITH 1"
``` 

The production build is now up and running. The default port opening up from the container is 1337. This can be
 edited inside the `docker-compose.prod.yml` file. Simply change the _1337_ to the desired port under the nginx
  configuration.


### Configuring HTTPS
The following external [guide](https://www.cloudbooklet.com/how-to-install-nginx-and-lets-encrypt-with-docker-ubuntu-20-04/).
If this is the first time booting up with certbot, you have to disable the ssl server. Afterwards you run the container 
(with the app container running in order to have the volumes created). Finally after certbot successfully generated the 
ssl certificated you can enable the ssl server again and reboot the container. HTTPS should now be up and running.

### Database initialisation and migrations
To initialise, run the following command in the backend docker container (in development the one marked `web-backend
`, in production the normal `web` container). Running commands in a Docker container is explained in [Docker commands
](#docker). Hint: opening a terminal can be useful.
```
python manage.py migrate
```
To initialise some common app data (like a default university, base scores and multipliers, ...), run the following.
```
python manage.py competition_init
```

**DO NOT RUN THE FOLLOWING IN A PRODUCTION BUILD!**
To create an admin user with default credentials (username: admin, password: admin), run
```
python manage.py init_users
```
To create dummy data for the app, run the following. This will create a user (username: competition, password
: competition) which will be in the _competition_ group. More on permissions in [Permissions](#permissions).
```
python manage.py competition_create_dummy_data
```

### Environment file
The following section will explain all environment variables:
- _DEBUG_: Can take the value of 0 or 1. Used to indicate if the Django server is run in Debug mode or not
- _SECRET_KEY_: The secret key used by Django for cryptographic purposes. **Should be edited in production.**
- _DJANGO_ALLOWED_HOSTS_: The allowed hosts on which the Django server will accept connections. This is the url and
/or ip of your server. Multiple addresses may be provided as a space delimited array. **Adjust in production**
- _DJANGO_TEMPLATE_PATHS_: A space delimited array of paths (inside the container) where Django can find templates
- _DJANGO_STATIC_PATHS_: A space delimited array of paths (inside the container) where Django can find static assets.
- _DJANGO_TIMEZONE_: The default timezone used by Django for it's display and conversions.
- _DATABASE_: Variable used to check which database backend is being used (only postgres is supported)
- _SQL_ENGINE_: The SQL engine used by Django (only _django.db.backends.postgresql_ supported).
- _SQL_DATABASE_: The name of the sql database. Most likely the same as `.env.db.* -- POSTGRES_DB`.
- _SQL_USER_: The user for logging in to the sql database. Most likely the same as `.env.db.* -- POSTGRES_USER`
- _SQL_PASSWORD_: The password for the user in the sql database. Most likely the same as `.env.db.* -- POSTGRES_PASSWORD`. **Edit this in production**
- _SQL_HOST_: The host url for the database.
- _SQL_PORT_: The port for the database connections.
- _REDIS_URL_: Only used in production. The url of the redis server.
- _REDIS_PORT_: Only used in production. The port of the redis server.

### Build arguments
- _SERVER_URL_: The url of the backend server. **Adjust in production**
- _SERVER_PORT_: The port of the backend server. **Adjust in production, can be left empty**
- _HTTPS_: A boolean indicating whether to reroute the events through https. **Adjust in production to 1**
- _TITLE_: The default title of the app.

## Permissions
The app uses three different groups with each their own permissions:
- _anonymous_: These are users who are not logged in.
- _competition_: This is a group (accessed through the admin) to which users can be added. This group is meant for
 opening up pages that should only be visible to some users or inside your organisation stand. Extra privileges
  include signing up users.
- _admin_: These are users with staff status. These people can access everything and as such also control the lap
 timings, rearrange the queue, remove people from the queue, ...

To edit permissions, they have to be adjusted in two different places: the frontend and the backend.
- _Frontend_: The frontend opens up two getters through the _Vuex store_: `is_group` and `is_admin`. Furthermore
, entire views can be guarded in the router.
- _Backend_: Permissions can be updated in the `permissions.py` file. Each view has a corresponding _open_ variable
. If more permission have to be opened, they can be added to the `OPEN_PERMISSIONS` set. Editing permissions for the
 `competition` group can be done in the admin. This does not include opening up specific views, but rather access to
  specific actions.

Each REST API link on the backend has a permission bound to it. The code names have the following syntax: 
`rest_<action>_<model_name>`. Adding the `rest_` prefix in the permissions.py variables is not required.

## Development

### Backend
As told above, the backend in written using Django. For a general tutorial, look in the official Django documentation
(this is highly recommended if you've never worked with Django before). In addition, the following useful packages are
 installed:
- _rest_framework_: Django REST API
- _django_eventstream_: An SSE package for Django
- _django_filters_: A package for filtering requests (used in combination with REST).

Normally you shouldn't edit anything in the it24u folder.

All code for the backend is inside the `competition` folder. Next follows an explanation of the files:
- _admin.py_: When you have models you want to be editable in the admin, add them in this file. More information can
 be found in the Django documentation.
- _app.py_: This file shouldn't be edited. More information in Django documentation.
- _filters.py_: This file contains extra custom filters used for the REST API.
- _models.py_:  Contains all the database models. Make sure to create REST permissions in the Meta subclass. More
 information can be found in the Django documentation. Complex operations should be added to _services.py_.
- _permissions.py_: This file contains helper classes and constant variables for easy edit. 
- _routing.py_: This file shouldn't be edited. More information in Django Channels package documentation.
- _serializers.py_: This file contains serializers in order to convert Django models to JSON format. More information
 in Django REST framework package. A more custom base class is used in this project to allow the addition of extra
  fields when necessary during conversion. Best is to extend from this class instead of ModelSerializer.
- _services.py_: This file contains more complex database operations. Complex database operations **should not** be
 added directly in models.py, but rather here to maintain cleaner overview. 
- _signals.py_: This file contains signal methods, e.g. when a record in the database is edited, this can send SSE
 events to it's subscribers. More information on signals can be found in the Django documentation.
- _test.py_: Should contain tests... but doesn't.
- _urls.py_: Contains all the url patterns. When adding a new model, a REST url can be created following the `router
.register()` commands. The other urls most likely don't require any edit. More information can be found in both the
 original Django documentation and the Django REST framework documentation.
- _views.py_: Contains extra (non-Vue related) views or specific (non-model related) REST views. More information can
 be found in both the original Django documentation and the Django REST framework documentation.
- _viewsets.py_: Contains all REST API endpoints and actions. For more information, look in the Django REST
 documentation.
 
Incoming requests can be divided into three categories: `/admin` `/api` `/` and will be handled by different handlers.
- `/admin`: This will be handled by the normal Django admin handler.
- `/api`: This will be handled by the REST handler.
- `/`: This will be forwarded to the index.html from VueJS and will further be handled by the VueJS router in the
 frontend.
 
Some basics on the REST handler. Viewset urls are found in _urls.py_ in the router registrations. Every viewset has
 the following "actions" by default:
- _list_: The is called when a GET request is performed to the viewset.
- _retrieve_: Called when a GET request is performed, with an added `/<id>`.
- _create_: Called when a POST request is made with the corresponding data.
- _update_: Called when a POST request is made with an added `/<id>` and corresponding data.
- _destroy_: Called when a DELETE request is made with an added `/<id>`.
Any extra actions are registered through the `@action` decorator. When adding new actions, make sure to also create
 permissions for them in the _models.py_ file with the corresponding model (and corresponding naming scheme). When
  creating a new viewset, always add the `get_permissions` method corresponding to the other examples. Finally
   more (general) information on viewsets can be found in the Django REST framework documentation.
   
Making edits in the _models.py_ file requires database migrations. Make sure to run `python manage.py makemigrations`
 and `python manage.py migrate` in the Docker backend container to reflect these changes. These are not automatic
 with the hot reload.
 
### Frontend
The frontend is written using the VueJS framework. For a general tutorial, look at the official documentation (highly
 recommended if you've never worked with Vue before). Also make sure to refresh your memory on Vue reactivity caveats.
 The source folder for the Vue project is `/competition/vue-app/src` with the following structure:
- _/components_: This folder contains some reusable components for the views. These components already have most (if
 not all) server interaction for their respective data. More on these later.
- _/filters_: Contains global Vue filters.
- _/plugins_: Most likely not edited.
- _/router_: Contains all the routings available. More on this later.
- _/store_: Contains the Vuex Store. More is explained later.
- _/utils_: Contains some Javascript utility functions.
- _/views_: Contains all the views of the app.
- _App.vue_: The main container of the entire app. Contains e.g. the sidebar navigation system.

**The views**. These are the highest level views you can display to the consumers. They should ideally not
 contain any server requests and be kept as simple as possible. Extract most items into logical, reusable components.
  Ideally, they are self explanatory.
  
**The Vue router**. The router is just as explained in the Vue-router documentation with one added element. Every
 view should contain a `hasPermission` function inside the meta field. This function should return a boolean stating
  whether or not the user has permission to view this page. If the result is false, the user will automatically be
   redirected to the login page.
 
**The Vuex store**. Used as explained in the official documentation. The store contains all urls and best practice is
 to always refer to these urls if required in the components. **NEVER HARDCODE URLS**. Furthermore is offers some
  getters for user information such as `isAuthenticated` `is_group` ... The update SSE and Auth function should never
   be used outside of the vuex file. They are used internally for the actions. Most likely you will never touch
    authentication or SSE setup. Finally. The store contains simple actions like `login` and `subscribe_sse`.
- Using `(un)subscribe_sse`: When you want to receive SSE updates from the server, these actions can be called
 (official Vuex documentation shows how to call actions). They need an 'event' parameter (e.g. lap_update) and a
  handler (a function that is called when an update is received). These actions are usually called in `mounted` and
   `beforeDestroy`. **Do unsubscribe your events in beforeDestroy**.
   
**Components**. Most properties, events and slots can be identified by looking at the code. Simply do a search for
 `slot` in the file to identify all slot possibilities. Some components support `#full` slot, this can be used to
  only take over the server functionality and completely rewrite the look of the component.


## Useful commands

### Docker
- List all running Docker containers: `sudo docker ps`
- Run a single command in a Docker container: `sudo docker exec <docker_container_name> <command>`
- Open an interactive terminal in a Docker container: `sudo docker exec -it <docker_container_name> sh`
- Build a Docker composition: `sudo docker-compose -f <docker-compose_filename> build`
- Start a Docker composition (in detached mode): `sudo docker-compose -f <docker-compose_filename> up -d`
- Shut down a Docker composition: `sudo docker-compose -f <docker-compose_filename> down`
- Open the Docker logs: `sudo docker-compose -f <docker-compose_filename> logs`
- Open the Docker logs (continuous mode): `sudo docker-compose -f <docker-compose_filename> logs -f`

### Database
These commands are run from a container which runs the server backend.
- Flush the database: `python manage.py flush --noinput`
- Migrate the database: `python manage.py migrate`

### Production
These commands are run from the web container.
- Collect static resources: `python manage.py collectstatic --noinput`

### Development
These commands are run in either the frontend or backend container.
- Make migrations (after a Model update): (backend) `python manage.py makemigrations`
- Install a new package (python): (backend) `pip install <package_name>`
- Export pip installation: (backend) `pip freeze > requirements.txt`
- Install a new package (npm): (frontend) `npm install <package_name>`
