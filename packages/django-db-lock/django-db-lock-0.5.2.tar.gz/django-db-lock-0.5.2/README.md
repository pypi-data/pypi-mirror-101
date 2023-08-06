# django-db-lock

Lock something and keep status in database. A simple distributed lock system.

## Install

```shell
pip install django-db-lock
```

## Usage With django_db_lock app in project

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_db_lock',
    'django.contrib.humanize',
    ...
]

DJANGO_DB_LOCK_AUTO_REGISTER_MODEL = True
DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN = True
DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES = True
DJANGO_DB_LOCK_APP_LABEL = "django_db_lock"
```

- Required.
- Insert `django_db_lock` into INSTALLED_APPS.
- Insert `django.contrib.humanize` into INSTALLED_APPS to enable the i18n translation.
- DJANGO_DB_LOCK_AUTO_REGISTER_MODEL default to True, so that the Lock model is auto registerd.
- DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN default to True, so that the Lock model's admin site is auto registered.
- DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES default to True, so that the Lock Services is auto registered in django_db_lock.urls.
- DJANGO_DB_LOCK_APP_LABEL default to django_db_lock, so that the Lock model is registered under django_db_lock. You can change it to any exists app.

**pro/urls.py**

```
...
from django.urls import path
from django.urls import include

urlpatterns = [
    ...
    path('dblock/', include("django_db_lock.urls")),
    ...
]
```

- Optional.
- Export db-lock services only if you have client app to use the service.

**app/views.py**

```
import uuid
from django_db_lock.client import get_default_lock_server
from django_db_lock.client import DjangoDbLock

def view01(request):
    lock_server = get_default_lock_server()
    lock_name = "view01lock"
    worker_name = "view01worker"
    timeout = 10
    with DjangoDbLock(lock_server, lock_name, worker_name, timeout) as locked:
        if locked:
            do_something...
    ...
```

##  Usage Without django_db_lock app in project 

**pro/settings.py**

```
DJANGO_DB_LOCK_AUTO_REGISTER_MODEL = False
DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN = False
DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES = False
DJANGO_DB_LOCK_API_SERVER = **You api server**
DJANGO_DB_LOCK_ACQUIRE_LOCK_PATH = "acquireLock"
DJANGO_DB_LOCK_RELEASE_LOCK_PATH = "releaseLock"

```

- You must set DJANGO_DB_LOCK_AUTO_REGISTER_MODEL to False, so that you will not get django_db_model's Lock model auto registered.
- You must set DJANGO_DB_LOCK_API_SERVER in your settings.py
- DJANGO_DB_LOCK_ACQUIRE_LOCK_PATH default to "acquireLock". Only if your server have changed the url, you have to change it to match the server.
- DJANGO_DB_LOCK_RELEASE_LOCK_PATH default to "releaseLock". Only if your server have changed the url, you have to change it to match the server.

**app/views.py**

```
import uuid
from django_db_lock.client import get_default_lock_server
from django_db_lock.client import DjangoDbLock

def view01(request):
    lock_server = get_default_lock_server()
    lock_name = "view01lock"
    worker_name = str(uuid.uuid4()) # unique worker name
    timeout = 10 # the lock will be released by force after `timeout` seconds.
    with DjangoDbLock(lock_server, lock_name, worker_name=worker_name, timeout=timeout) as locked:
        if locked:
            do_something...
    ...
```


## Releases


| Version | Released Time | Content                                                    | Notice |
| ------ | ---------- | ---------------------------------------------------------------- | ---- |
| v0.1.0 | 2018/05/10 | 1. First release. | |
| v0.1.1 | 2018/05/11 | 2. Fix. | |
| v0.2.0 | 2020/08/29 | 3. Reconstituted.<br />4. Allow register the Lock model into another app, use setting DJANGO_DB_LOCK_APP_LABEL.<br />5. Use django-apiview to provides restful API.<br />6. Use camelStyle parameter format.<br />7. Add i18n for zh-hans. | Incompatible with old releases. |
| v0.2.1 | 2020/08/29 | 8. Fix setup description. | |
| v0.3.0 | 2020/09/01 | 9. Add django_db_lock.client.DjangoDbLock. | |
| v0.3.1 | 2020/09/01 | 10. Rename zh_hans to zh_Hans.<br />11. Fix setup descriptions. | |
| v0.4.0 | 2020/09/08 | 12. Add abstract LockBase model.<br />13. Add django_db_lock.client module.<br />14. Put services in one class, so that you may create many lock server instance. | |
| v0.4.1 | 2020/10/21 | 15. Add setup requires library. | |
| v0.5.1 | 2021/03/24 | 16. Use redis lock before db lock. | |
| v0.5.2 | 2020/04/09 | 17. Release redis lock if lock in redis success but lock in database fail.<br />18. Fix problems, and unit tests passed. | |
