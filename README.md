## Using [Docker Compose](https://docs.docker.com/compose/)

### to see config
```bash
docker compose --env-file=compose.env config
```

### tests
```bash
docker compose --env-file=compose.env --file=compose-tests.yaml down --remove-orphans && \
docker compose --env-file=compose.env --file=compose-tests.yaml build && \
docker compose --env-file=compose.env --file=compose-tests.yaml up
```

### to run
```bash
docker compose --env-file=compose.env down --remove-orphans && \
docker compose --env-file=compose.env build && \
docker compose --env-file=compose.env up
```

## Local config/unix-like

### Using [pyenv](https://github.com/pyenv/pyenv-installer)

```bash
$ cd src/
$ pyenv install 3.11.3
$ pyenv virtualenv 3.11.3 athena-env
$ pyenv local athena-env # optional/recommended (auto active env)
$ pyenv activate athena-env
$ pip install --upgrade pip
$ pip install -r requirements.txt -r requirements-dev.txt
```

### Creating database/user

*Obs: tested with PostgreSQL v12*

```bash
$ sudo su postgres
$ psql
> CREATE DATABASE <your_database_name>;
> CREATE USER <your_db_user> WITH PASSWORD '<your_db_password>';
> GRANT ALL ON SCHEMA public TO <your_db_user>;
> \q
$ exit
```

### Enviroment variables

* `DATABASE_CONN_STRING`=`<your_db_user>`:`<your_db_password>`@`<host:port>`/`<your_database_name>`
* `SECRET_KEY`=`<your_key>` - recommended generate a key with - `openssl rand -hex 32`
* `ALGORITHM`=HS256
* `PYTHONBREAKPOINT`=ipdb.set_trace # optional/recommended

### running alembic
```bash
$ cd src/
$ alembic upgrade head
```

## To run

```bash
cd src/athena

dotenv run uvicorn api.main:api --reload --port 8001
dotenv run uvicorn app.main:app --reload --port 8002
```

## Optionals

### Vscode Workspace
```
{
	"folders": [
		{
			"name": "athena",
			"path": "."
		},
		{
			"name": "apollo-devops",
			"path": "./apollo"
		},
		{
			"name": "ares-devops",
			"path": "./ares"
		},
		{
			"name": "apollo",
			"path": "./apollo/src",
		},	
		{
			"name": "ares",
			"path": "./ares/src"
		},
	],
	"settings": {
		"files.exclude": {
			"**/.git": true,
			"**/.svn": true,
			"**/.hg": true,
			"**/CVS": true,
			"**/.DS_Store": true,
			"**/Thumbs.db": true,
			"**/__pycache__": true,
			"src": true,
			"ares": true,
			"apollo": true,
		}		
	}
}
```