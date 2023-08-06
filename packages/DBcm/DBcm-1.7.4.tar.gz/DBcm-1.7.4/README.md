# DBcm
> The Database Context Manager from the 2nd Edition of Head First Python.


## Install

You can easily install DBcm into your local Python with this command:

`pip install DBcm`

Note: there is no `conda install` option at this time.

## How to use

The `UseDatabase` context manager for working with MySQL/MariaDB.

For more information, see Chapters 7, 8, 9, and 11 of the 2nd edition of
Head First Python.

Assumptions: you've installed either MySQL or MariaDB, created a database, granted a user full access to the database, and (optionally) created one of more tables within the database.

Begin by importing what you need from DBcm:

```python
from DBcm import UseDatabase, SQLError
```

Then create a dictionary which provides your DB credentials data (substituting the relevant values as required):

```python
config = { 'host': '127.0.0.1',
           'user': 'useridhere',
           'password': 'passwordhere',
           'database': 'dbnamehere',
         }
```

Use the `config` dictionary together with the `UseDatabase` context manager to interact with your database tables. Note: there's an assumption that you already know/understand some basic SQL here:

```python
with UseDatabase(config) as cursor:
    try:
        _SQL = "select * from log"
        cursor.execute(_SQL)
        data = cursor.fetchall()
    except SQLError as err:
        print('Your query broke:', str(err)
```

The result of the query is in the `data` variable. 

Enjoy, and have fun.  (Sorry: Python 3 only, due to type hints and new Exception syntax).
