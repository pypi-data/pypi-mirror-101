# django-safe-settings

Django application let you write your database password settings in an encrypted way.


## Install

```
pip install django-safe-settings
```


## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_safe_settings',
    ...
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "NAME": "project_database_name",
        "USER": "project_database_username",
        "PASSWORD": "e7293477f3fa2a72935913624eecdeb5",
        "OPTIONS": {
            "init_command": """SET sql_mode="STRICT_TRANS_TABLES" """,
        },
    },
}

...

## ##################################################################
## this must be at the bottom of settings.py
## ##################################################################
from django_safe_settings.patch import patch_all
patch_all()


```

- Set sensitive configuration items to encrypted values, e.g. `PASSWORD=e7293477f3fa2a72935913624eecdeb5`, the real plain value is `passwordfortest`.
- Use `python manage.py django_safe_settings_encrypt PLAIN_DATA` to get the encrypted value, e.g.
    ```
    C:\git\django-safe-settings>python manage.py django_safe_settings_encrypt passwordfortest
        plain value = passwordfortest
    encrypted value = e7293477f3fa2a72935913624eecdeb5
    ```
- We use fastutils.cipherutils.AesCipher for encryption, and the password is related to Django's SECRET_KEY, so when the SECRET_KEY's value changes, the encrypted value must be regenerated.
- You can use encrypt values anywhere in Django's settings.

## Releases

| Release | Time | Changes                                                     | Notice |
| ------ | ---------- | ---------------------------------------------------------------- | ---- |
| v0.1.0 | 2020/03/01 | 1. First release. | |
| v0.1.1 | 2020/03/01 | 2. Remove unused imports. | |
| v0.1.2 | 2020/04/12 | 3. Test in django 3.2 and the unit test passed. | |
