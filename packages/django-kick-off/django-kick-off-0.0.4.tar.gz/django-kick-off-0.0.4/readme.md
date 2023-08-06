# Kick-Off-Django

The idea of this package is to avoid the repetitive task of configuring a Django project and virtual environment.  


## Installation

```python
pip install django-kick-off
```

## Usage

```python
python3 -m kick_off <project_name> <venv_name>
```
OUTPUT:
- requirements.txt
- virtual environment
- Django project with an app.

## Example #1 (Generic Naming)

```python
python3 -m kick_off
```

OUTPUT:
```bash
|--requirements.txt
|--venvMySite/
    |--bin/
    |--include/
    |--lib/
    |--pyvenv.cfg
|--mysite/
    |--home/
    |--mysite/
    |--manage.py
    |--db.sqlite3
```

## Example #2 (Only Project Naming)

```python
python3 -m kick_off test_web
```

OUTPUT:
```bash
|--requirements.txt
|--venvTestWeb/
    |--bin/
    |--include/
    |--lib/
    |--pyvenv.cfg
|--test_web/
    |--home/
    |--test_web/
    |--manage.py
    |--db.sqlite3
```

## Example #3 (Project and Venv Naming)

```python
python3 -m kick_off test_web Example
```

OUTPUT:
```bash
|--requirements.txt
|--venvExample/
    |--bin/
    |--include/
    |--lib/
    |--pyvenv.cfg
|--test_web/
    |--home/
    |--test_web/
    |--manage.py
    |--db.sqlite3
```