## Using [pyenv](https://github.com/pyenv/pyenv-installer)

```bash
$ pyenv install 3.11.0
$ pyenv virtualenv 3.11.0 atena-env
$ pyenv local atena-env # optional/recommended (auto active env)
$ pyenv activate atena-env
$ pip install --upgrade pip
$ pip install -r requirements.txt -r requirements-dev.txt
```

## Enviroment variables


* `DB_USER`=`<your_db_user>`
* `DB_PASSWORD`=`<your_db_password>`
* `DB_HOST`=`<your_db_host>`
* `DB_DATABASE`=`<your_database_name>`
* `SECRET_KEY`=`<your_key>` - recommended generate a key with - `openssl rand -hex 32`
* `ALGORITHM`=HS256
* `PYTHONBREAKPOINT`=ipdb.set_trace # optional/recommended

## Creating user/database

```bash
$ sudo su postgres
$ psql
> CREATE DATABASE <your_database_name>;
> CREATE USER <your_db_user> WITH PASSWORD '<your_db_password>';
> GRANT ALL ON SCHEMA public TO <your_db_user>;
> \q
$ exit

# running alembic
cd source/
alembic upgrade head
```