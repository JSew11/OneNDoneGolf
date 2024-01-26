# One 'n Done Golf
Golf Pick'em site where users compete to select the best golfer on a tournament by tournament basis. Built using Django and PostgreSQL.

## Dev Environment Setup

### Installations
* Docker & Docker Compose (Included with [Docker Desktop](https://www.docker.com/products/docker-desktop/))
* Python Editor (I like [VSCode](https://code.visualstudio.com/download))
* [Git](https://git-scm.com/downloads)/Git UI (I like [GitKraken](https://www.gitkraken.com/))
* Database Management Client (I like [DBeaver](https://dbeaver.io/))
* API Client (I like [Postman](https://www.postman.com/downloads/))

### Project Setup
1. Clone the repo (https://github.com/JSew11/OneNDoneGolf) using the command:  
    `git clone https://github.com/JSew11/OneNDoneGolf`
1. Make sure you have a file named `.env` in your root directory with the following structure (you will most likely have to create one):  
```
DB_NAME=# this can be anything you want
DB_USERNAME=# this can be anything you want
DB_PASSWORD=# this can be anything you want
DB_HOST=db
DB_PORT=5432

SECRET_KEY=# this can be anything you want

API_BASE_URL="http://localhost:8000/api" # development api url

GOLF_DATA_API_BASE_URL="https://api.sportsdata.io/golf/v2" # sportsdataio golf api
GOLF_DATA_API_KEY=# get this from lead devs when setting up
```

### Running the App
1. Navigate to the project root
1. In your terminal, run the command `docker compose up -d` to start the app (to tear down, run `docker compose down`)  
1. If you have made local changes (outside of the Docker container) and wish to restart the app with them applied, run the command `docker compose restart`

### Viewing the App
* To view the local development app (after it has started) go to [http://localhost:3000](http://localhost:3000)