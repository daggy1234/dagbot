# dagbot
The official Repository for dagbot, the self proclaimmed n1 meme bot. https://dagbot-is.the-be.st 

### SQL Data

Dagbot needs 3 Tables in an SQL databse to function. You can use get the SQL from the migration.sql file and run em

Do note this is postgresql database

### configuration

#### configuration.yml
This is a file which stores all of dagbots data. You can view a sample in the repository

#### .env
**ONLY FOR DOCKER/k8s**
Customise the `dagbot.env`

If you do not want to use yaml you can set env vars and dagbot will autp generate the yml. This will only work whn using the container system.

### Dagbot Website

There is a task in a file named `statupload.py` this file just periodically uploads statistics to the dagbot-app api to display o the website.
You should remove this file.


### Running Normally

To Get Dagbot up and Running its as simple as runnig the script below.
Please note poetry is required.
**Configuration.yml** is required
```sh
poetry install
poetry run python -m dagbot
```

### Docker Build

`PLease note these docker configs are special to dagbot. For general purpose discord.py Dockerfiles please use these ones insteas.`
https://github.com/Gorialis/discord.py-docker/tree/master/dockerfiles

#### Cloningf Repo and Building Image locally

Build Image

```shell script
docker build -t dagbot .
```

Run with configuration.yml

```shell script
docker run -v ${PWD}/configuration.yml:/configuration.yml dagbot   
```

Run with `.env`

```shell script
docker run --env-file dagbot.env dagbot   
```

#### Using the dockerhub image

Run with configuration.yml

```shell script
docker run -v ${PWD}/configuration.yml:/configuration.yml daggy1234/dagbot:latest   
```

Run with `.env`

```shell script
docker run --env-file dagbot.env daggy1234/dagbot:latest
```

#### WIP

Currently uts docker however wil will soon move the kubernetes. WIll update ths readme when thats done.

### Server

Join the discord for help.

I recommend usingmy hosted version, but feel free to self host. Drop a star and read the license!

