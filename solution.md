# Purple Cow Prototype

This is a prototype application designed for tracking "Items" via a RESTful API.

## System Requirements

* Ubuntu (or more generally Debian-flavored Linux)
* Storage Requirements: 1GB
* Docker (with ability to run as [non-root user](https://docs.docker.com/engine/install/linux-postinstall/))
* Client/Tool to hit API endpoints (e.g. Chrome, FireFox, Postman, Curl, etc.)

## Building/Running

Once the system requirements have been met, building and running should be as simple as performing the following command from the root of the project:

```
./startup.sh
```

While running the API should be accessible locally via `localhost`, `127.0.0.1`, and/or `[::1]` coupled with the web application's port (which can be [configured](#configuration)) with the path of `/item`, a la `http://localhost:3000/item`.

When the application is ready to be terminated, shutting it down is also as easy as running:

```
./shutdown.sh
```

No root permissions should be required assuming the above [guide](https://docs.docker.com/engine/install/linux-postinstall/) was followed; however, if it fails try the above commands with `sudo`. If it succeeds, feel free to open a new issue to resolve/clarify why non-root user permissions failed.

**WARNING:** This has only been tested for Ubuntu-environments. It is likely to work in other Debian-environments; however, it is unlikely to work "as-is" in a Linux distribution based around SELinux, e.g. CentOS, Fedora, RedHat. This is due to various security concerns that SELinux flags when using Docker.

## Configuration

At the moment, the only piece of configuration is the port that the web application is hosted on. This can be configured by modifying the `WEBAPP_PORT` property in the `.env` file in the root of the project that appears after running `startup.sh` for the first time.

**NOTE:** When changing this file, the application will need restarted with `restart.sh` from the root of the project. This can also be achieved by calling `shutdown.sh` and `startup.sh` in succession.

## Assumptions/Details

During this project a number of assumptions had to be made when interpreting the provided specification. They are listed below:

1. The specification requests that the API allow a user to "set" the items. This isn't clear whether this means we should support singular creation or bulk creation of items. At the moment, only the former is supported to simplify implementation. Updating this would not prove overly difficult.
   
2. The "item" object is requested to have only "id" and "name" but "created" and "updated" were also added, as these are fairly standard fields for models to track. They are not editable and are controlled completely internally to the application.
   
3. Items being persisted in memory followed later by storing them in a database didn't state that the database should completely replace this in-memory storage, so both were maintained. This prevents some code simplification, which could be easily remedied if the database became the sole source of item storage. Further, it wasn't stated if the contents of the database should be loaded in-memory, so this was added to prevent an inconsistency on application startup between the in-memory and database stores.

4. When starting the application with a single command it wasn't clear if it should perform both a build and a startup, as opposed to just starting, so doing both was chosen for user experience purposes. They could be readily separated into two steps, if need be.

5. The Dockerfile for the database container ended up solely comprised of a `FROM`. This was left to keep with the specification, but could be simplified by putting the name of the corresponding image in the `docker-compose.yml` file.

6. No authentication appeared necessary for this initial prototype, so it was omitted. With the selected technologies, it wouldn't be too difficult to add in various degrees of authentication and permission checking rather quickly.

7. To allow for rapid addition of additional models in a rather organized fashion, the "items" application was setup such that "models", "serializers", and "views" are packages that contain modules specific to a specific model and any future models that could support them. This is as opposed to throwing everything into a single monolithic `models.py`, `views.py`, and `serializers.py`.

8. Wasn't immediately clear that [README.md](README.md) was interchangeable with [solution.md](solution.md) so both were kept, with the README just pointing to this file.

9. The client didn't request for the Item's `name` to be `unique` so duplicates are permitted for the time being.

10. It wasn't specified whether the `id` should be an `int` or `uuid` so the latter was preferred in this case, as autoincrementing integers can pose a future security vulnerability by leaking information.

## Project Directory Structure

```
purple-cow  
│
└───.docker (Files for project containerization)
│   │
│   └───db (Files for database containerization)
│   └───webapp (Files for webapp containerization)
│   
└───app (Django Project directory)
    │
    └───items (Core Application)
    │   │
    │   └───migrations (Database migrations for 'items' application)
    │   └───models (Models for 'items' application Schema)
    │   └───serializers (Serializers for model de-/serialization and validation)
    │   └───views (Endpoints for REST API logic)
    │
    └───purplecow (Django-related configuration)
```

## Future Work

1. Add in Testing (Unit/Integration)
2. Add in Logging
3. Add in Authentication
4. Make startup, shutdown, and restart scripts more robust (i.e. able to run them from anywhere on the Host machine)
5. Split single web application docker container into Nginx and WSGI server (e.g. Gunicorn, uWSGI, etc.) containers
6. Create developer onboarding material

Anything more than that would be pushing beyond the realms of this proof of concept without additional guidance from the client.
