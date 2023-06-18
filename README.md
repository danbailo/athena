## Using [Docker Compose](https://docs.docker.com/compose/)

### to see config
```bash
docker compose --env-file=compose-local.env config
```

### tests
```bash
docker compose --env-file=compose-local.env --file=compose-tests.yaml down --remove-orphans && \
docker compose --env-file=compose-local.env --file=compose-tests.yaml build && \
docker compose --env-file=compose-local.env --file=compose-tests.yaml up
```

### to run
```bash
docker compose --env-file=compose-local.env --file=compose-local.yaml down --remove-orphans && \
docker compose --env-file=compose-local.env --file=compose-local.yaml build && \
docker compose --env-file=compose-local.env --file=compose-local.yaml up
```

## Local config/Debian-based

### Using [pyenv](https://github.com/pyenv/pyenv-installer)

```bash
cd src/
pyenv install 3.11.3
pyenv virtualenv 3.11.3 athena-env
pyenv local athena-env # optional/recommended (auto active env)
pyenv activate athena-env
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

### Creating database/user

*Obs: tested with PostgreSQL v12/15*

*(Optional) Install lib to generate password:*
```bash
sudo apt install apache2-utils
```

Generating passwords
```bash
htpasswd -nb my_user my_password
```

```bash
sudo su postgres
psql
CREATE DATABASE <your_database_name>;
CREATE USER <your_db_user> WITH PASSWORD '<your_db_password>';
GRANT ALL ON SCHEMA public TO <your_db_user>;
\q
exit
```

### Enviroment variables

* `DATABASE_CONN_STRING`=`<your_db_user>`:`<your_db_password>`@`<host:port>`/`<your_database_name>`
* `SECRET_KEY`=`<your_key>` # recommended generate a key with - `openssl rand -hex 32`
* `ALGORITHM`=HS256 # tested
* `ATHENA_ARES_BASE_URL`=http://localhost:<port> # `8000` for example
* `ATHENA_APOLLO_BASE_URL`=http://localhost:<port> # `8001` for example
* `PYTHONBREAKPOINT`=ipdb.set_trace # optional/recommended

### running Ares(backend)
```bash
cd ares/
alembic upgrade head
cd src/
dotenv run uvicorn main:app --reload --port 8000
```

### running Apollo(frontend)

```bash
cd apollo/src
dotenv run uvicorn main:app --reload --port 8001
```


## Optionals

### AWS EC2 Deployment

Works on free tier!

Required files:
* `compose-prod.yaml`

The variables that you need to set is the same as `compose-local.yaml`, but we will add this values in GitHub Actions Secrets, because this file contains sensitive credentials.

After we add the secrets on GitHub Actions enviroment(in this project as configured as `ATHENA_PROJECT_SECRETS`), the `deploy.yaml` will automatic generate the file `compose-prod.yaml`.

Basically, what you need to do is create the file `compose-prod.yaml` locally and create the secret in GitHub Actions from your repository with the name `ATHENA_PROJECT_SECRETS` and add the content generated by this command:
```bash
base64 -w 0 compose-prod.env
```
[How to get project secrets using GitHub Actions](https://stackoverflow.com/questions/67964110/how-to-access-secrets-when-using-flutter-web-with-github-actions/67998780#67998780)

Required options:
* VM Image: **Amazon Linux**

Add this config in advanced tab to init the instances with this config(or run after).

```bash
#!/bin/bash
yum install -y docker
systemctl start docker
systemctl enable docker
```

After run above commands, run the commands bellow.
```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

sudo usermod -aG docker ${USER}
sudo reboot
```

---

### Traefik configuration

*(Optional) Install lib to generate password:*
```bash
sudo apt install apache2-utils
```

Generating passwords
```bash
htpasswd -nb my_user my_password
```

Utils links:
* https://doc.traefik.io/traefik/routing/providers/docker/
* https://doc.traefik.io/traefik/reference/dynamic-configuration/docker/
* https://doc.traefik.io/traefik/user-guides/docker-compose/acme-tls/

---

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