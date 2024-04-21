# Kumquat API

## QUick Start

### Install packages.

```bash
pip isntall -r requirements.txt
```

### Make migrations. 

```bash
python manage.py makemigrations kmqtAuth program equipment 
python manage.py migrate
```

### Creat superuser.

```bash
python .\manage.py createsuperuser --username test --email test@test.text
```

### Start server

```bash
python3 manage.py runserver
```

#### *Launch with settings for development if you need*

```shell
python manage.py runserver --settings=path.to.setting.py
```

You have to replace `/` or `\ ` with `.`! Just like this:

```shell
python manage.py runserver --settings kumquatAPI.settings_dev
```
