# Getting started with Fast API, Docker and Firebase <!-- omit from toc -->

## Contents <!-- omit from toc -->

- [Introduction](#introduction)
- [FastAPI Introduction](#fastapi-introduction)
- [FastAPI Examples](#fastapi-examples)
  - [Documentation](#documentation)
  - [Path Parameters](#path-parameters)
  - [Query Parameters](#query-parameters)
  - [Post (put) model with Pydantic](#post-put-model-with-pydantic)
  - [Response (get) Model with Pydantic](#response-get-model-with-pydantic)
  - [Authentication](#authentication)
  - [Test](#test)
- [Intro to Docker](#intro-to-docker)
- [Dockerize with Local Deployment](#dockerize-with-local-deployment)
- [Cloud Deployment](#cloud-deployment)
  - [Setup Google Cloud Run](#setup-google-cloud-run)
  - [Deploy Docker Image to Artifact Registry](#deploy-docker-image-to-artifact-registry)
- [Authentication with Firebase](#authentication-with-firebase)
  - [Firebase Setup](#firebase-setup)
- [Avoiding CORS issues](#avoiding-cors-issues)
  - [CORS](#cors)
  - [The Complete Main.py](#the-complete-mainpy)
- [Userid Route](#userid-route)
- [Next Steps](#next-steps)

# Introduction

The objective for this repo is to illustrate how to create a realistic bakend API ("application") that serves a UI frontend. To that end, we introduce fastAPI, Docker and Firebase Authenticaiton. Included are deplopyment examples to local dev, to GCP Cloud Run, and authentication with Firebase.

Additionally, the [Jupyter Notebook Examples](<[./notebook/fast_api_requests.ipynb](https://github.com/Aljgutier/fastapi_docker/tree/main/notebooks)>) illustrate how to make `http` requests to the deployed API and dockerized fastAPI application.

A React-Firebse frontend application that uses this backend is demonstrated [here](https://github.com/Aljgutier/react_firebase?tab=readme-ov-file#reset-password). The frontend application sends an authorization bearer token to this backend. As a simple usage example, the backend will get the associated userid from Firebase and send it back to the frontend.

Together a React-Firebase frontend with the fastAPI backend form a modern and effective technology stack for building applications such as analytics platforms, data tools, and scientific applications where Python is preferred on the backend.

All the Python packages (and versions) needed to deploy the API are contained in the `requiremts.txt` file. Additional packages to test your applciaton (not requred for the deployed app) are contained in the `requirements_local.txt` file.

# FastAPI Introduction

FastAPI is a concise modern freamwork for building APIs, for example, to serve as a backend API for a front end React applicaton.

An excellent overview of FastAPI and Docker is found in the following reference and summarized below - [Intro to FastAPI and Docker](https://medium.com/@alidu143/containerizing-fastapi-app-with-docker-a-comprehensive-guide-416521b2457c)

1. Fast: FastAPI is built on top of Starlette, an asynchronous web framework, which allows it to handle high loads with incredible speed and efficiency. It is really really fast.
2. Type Annotations: FastAPI utilizes Python’s type hinting system to provide automatic request/response validation, resulting in enhanced reliability and fewer bugs.
3. API Documentation: FastAPI generates interactive documentation with Swagger UI and ReDoc, making it effortless to explore and understand API endpoints.
4. Security: FastAPI supports various authentication methods, including OAuth2, API key validation, and JWT tokens, enabling secure API development.
5. Asynchronous Support: FastAPI is designed to take advantage of Python’s async and await syntax, enabling efficient handling of I/O-bound operations.

# FastAPI Examples

The examples in this repo are adapted from the following two references - [FastAPI Introduction](https://medium.com/coderhack-com/introduction-to-fastapi-c31f67f5a13), [FastAPI getting started](https://dorian599.medium.com/fastapi-getting-started-3294efe823a0).

In this repo, several improvements are made including addition of missing details, setup in a realistic and wholistic setting, authenthication, coding best practice enhancements, deployment to Cloud Runner and all together forming a minimal requirements realistic backend API.

The folder structure in these examples is as follows.

```text
   backend
       +- app
          +- __init__.py
          +- main.py
          +- routes.py
```

For our purposes the top level project directory is "backend". The `app` folder contains the `main.py` and `routes.py` modules where we will define the routes and `__init__.py` , an empty file, specifies to Python that this folder is a Python package which is helpful for organizing your code into sepearte modules, especially as your application grows.

```sh
$ cd backend
```

With your preferred virtual env manger, create virtual environment. For example, below a virtual env is setup with `pyenv` - your Python version and virtual environment, of course, will differ.

```sh
$ pyenv virtualenv 3.12.7 venv_fapidckr
$ pyenv local venv_fapidckr
$ pip install fastapi uvicorn
```

In you favorite coding editor (`VSCode` recommended) create the main.py application with the following contents. Here we start the app `app = FastAPI()` and include the routes defined in app.routes. Notice also, following coding best practeces, we have included a docstring at the top of the module. This will add useful documentation and avoid Pylint warnings.

```Python
# main.py
"""
FastAPI Hello World, Getting Started application, main.py
"""

from fastapi import FastAPI
from app.routes import router

# initialize app
app = FastAPI()

app.include_router(router)
```

Next, create the routes.py file inside the app folder. We will define all our routes in this file.

We begin with the "/" route and respond with a dictionary `{"Hello","World"}

```Python
# routes.py
"""
API route definitions
"""

from fastapi import APIRouter
from fastapi import Header
from pydantic import BaseModel

router = APIRouter()

# get hello world
@router.get("/")
def read_root():
    """
    Get root, and respond with ` {"Hello": "World"}`
    """
    return {"Hello": "World"}
```

While in the backend directory, launch the API (i.e., "app" ) with uvicorn. The app will reload if any of its files changes. This is convenient as we are developing and changing the app.

```sh
$ uvicorn app.main:app --reload
```

In the Browser go to http://localhost:8000

You will receive

```json
{ "Hello": "World" }
```

## Documentation

To access the interactive API documentation, go to http://127.0.0.1:8000/docs. FastAPI automatically generates this documentation using Swagger UI.

You can also access alternative API documentation at http://127.0.0.1:8000/redoc, which uses ReDoc.

## Path Parameters

Now lets get back to defining some additional routes. Path parameters are parameters in the path of a URL and they are defined using braces {}. For example, an API with a path parameter for a person's name works as follows.

```Python
# get with Path Parameters
@router.get("/greet/{name}")
def greet(name: str):
    """Get Items

    Args:
        name (str): url path parameter

    Returns:
        json: key:"hello", value: "world"
    """
    return f"Hello {name}"
```

Try the followng in your browser
http://localhost:8000/greet/John

You will then receive the following response in the browser.

```text
"Hello John"
```

## Query Parameters

Query parameters are key-value pairs in the query string of a URL. For example:

/items?category=clothes&brand=Zara

```Python
# get with Query Parameters
@router.get("/items/")
def read_parameters(category: str, brand: str):
    """read query paraemters, key=value pairs in the url string

    Args:
        category (str): category query parameter
        brand (str): brand query paraemter

    Returns:
        dict: keys category and brand
    """
    return {"category": category, "brand": brand}
```

Try the foolowing URL address in your web browser
http://localhost:8000/items?category=clothes&brand=Zara

You will receive the following response.

```json
{ "category": "clothes", "brand": "Zara" }
```

## Post (put) model with Pydantic

In the following examples we will define an http `body` and define its structure with the Pydantic BaseModel. If the HTTP request body does not conform to the model it will be rejected.

```Python
# Post with Pydantic Body/Data Model
class ItemPost(BaseModel):
    """Post Body/Data Model

    Args:
        BaseModel (BaeModel): Pydantic Base Model
    """

    name: str
    description: str = None
    price: float
    tax: float = None


@router.post("/items_post/")
def create_item(item: ItemPost):
    """Create item from post
    Args:
        item (ItemPost): item following the ItemPost model

    Returns:
        ItemPost: returns the item
    """
    return item
```

You can test the HTTP put using the ./notebooks/fast_api_requests.ipynb notebook.

```Python
# Sample url and data/body

url = "http://localhost:8000/items_post"

data = {
    "name": "Foo",
    "description": "A new item",
    "price": 45.2
}

response= requests.post(url, json=data)
response.status_code

print()
print(f'respone.status_code = {response.status_code}')

if response.status_code == 200:
    print()
    print(f'response.json() = {response.json()}')
```

Produces the following response.

```text
respone.status_code = 200

response.json() = {'name': 'Foo', 'description': 'A new item', 'price': 45.2, 'tax': None}
```

## Response (get) Model with Pydantic

Similar to the previous example, in this case we will define a model for the HTTP body using the Pydantic BaseModel.

```python

# Get with Pydantic Return Model
class ItemGet(BaseModel):
    """Get Model

    Args:
        BaseModel (BaseModel): PyDantic Base Model
    """

    name: str
    description: str
    price: float


@router.get("/items_get/")
def read_items():
    """get items

    Returns:
        itemGet: itemGet type
    """
    items = [
        ItemGet(name="Foo", description="A new item", price=45.2),
        ItemGet(name="Bar", description="Another item", price=10.5),
    ]
    return items
```

In the path operation, we use that model to validate and serialize the request body. When you call /items/ with a request body like:

```json
{
  "name": "Foo",
  "description": "A new item",
  "price": 45.2
}
```

Use the Jupyter notebook fast_api_requests.ipynb to make the requests call for this example.

```Python
url = "http://localhost:8000/items"

response= requests.post(url, json=data)

response.json
```

The response is

```Python
{  'name': 'Foo',
   'description': 'A new item',
   'price': 45.2,
   'tax': None
}
```

## Authentication

```python
@router.get("/protected")
# def protected(authorization: str):
def protected(authorization: str = Header()):  # ✅ Works with Pylance ... properly grabs the header fromm authorization otherwise expects header as path parameter
    # def protected(password: str, required_password: str = "secret"):
    """return success with valid token

    Args:
        authorization (str): authorization token

    Returns:
        str: "success" if token is valid, otherwise returns "invalid token"
    """
    if authorization == "token12345":
        # if password == required_password:
        return "Success!"
    return "invalid token"
```

Test the authentication with the Jupyter notebook request

```Python

url = "http://localhost:8000/protected"
headers = {'Authorization':"token12345"}

response= requests.get(url, headers=headers)

print()
print(f'respone.status_code = {response.status_code}')

if response.status_code == 200:
    print()
    print(f'response.json() = {response.json()}')
```

You should receive the following response

```txt
respone.status_code = 200

response.json() = Success!
```

## Test

FastAPI has test client functionality built-in thanks to Starlette. You can test your API as follows:

Tests are setup in the notebook - ./notebooks/fast_api_requests.ipynb

```python
import sys
sys.path.append("..")
from fastapi.testclient import TestClient
from hello_world_app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

test_read_root()
```

Refer to additional test examples in the Ipython notebook

# Intro to Docker

The previously mentioned reference also provides an excellent overview of Docker [Intro to FastAPI and Docker](https://medium.com/@alidu143/containerizing-fastapi-app-with-docker-a-comprehensive-guide-416521b2457c).

- **Docker Daemon**: The Docker Daemon is a background service that runs on the host machine and manages the lifecycle of containers. It listens to the Docker API requests and handles container operations such as starting, stopping, and monitoring containers.
- **Containerd**: Containerd is a lightweight container runtime that manages the low-level container operations, including image handling, container execution, and storage.
  Docker CLI: The Docker Command Line Interface (CLI) is a command-line tool used to interact with Docker. It provides a set of commands to manage Docker images, containers, networks, volumes, and other Docker resources.
- **Docker Images**: A Docker image is a read-only template that contains all the dependencies, configuration, and code required to run a Docker container. Images are built using a Dockerfile, which defines the instructions to create the image. Images are stored in a registry, such as Docker Hub or a private registry, and can be pulled and run on any Docker-compatible system.
- **Docker Containers**: A Docker container is a running instance of a Docker image. Containers are isolated environments that encapsulate the application and its dependencies, ensuring consistent behavior across different environments. Each container runs as an isolated process and has its own filesystem, networking, and process space.
- **Docker Registry**: A Docker registry is a repository that stores Docker images. The most commonly used registry is Docker Hub, which is a public registry that hosts a vast collection of Docker images. You can also set up private registries to store your custom Docker images securely.

Additionally, the following Docker primer [Docker Primer](https://github.com/Aljgutier/docker) is useful for quick reference to Docker commands and an overview of Docker.

On a Mac, installation is advisable with the Homebrew package manager.

```sh
$ brew install docker
$ # or
$ brew upgrade docker
```

On a PC, refer to the [Docker install page](https://www.docker.com/products/docker-desktop/).

You can manage containers and images (deploy, run, and rm old images and containers) with the Docker UI or on the command line. Below we will illustrate command line examples.

# Dockerize with Local Deployment

In the project directory, create the Dockerfile.

```sh

FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

```

Make sure the Docker daemon is running - launch Docker Desktop and it will start the Docker daamon.

Create the docker image with the docker build command

```sh
$ docker build -t fastapi_hello_app .

----
[+] Building 21.3s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                                                              0.0s
 => => transferring dockerfile: 527B                                                                                                              0.0s
 => [internal] load .dockerignore                                                                                                                 0.0s
 => => transferring context: 2B                                                                                                                   0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim                                                                                8.1s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                     0.0s
 => [internal] load build context                                                                                                                 0.1s
 => => transferring context: 91.36kB
```

list the docker images on your machine

```sh
 docker images
 ----
REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
fastapi_hello_app   latest    c0ab9fecf062   11 seconds ago   150MB
```

-t tags the immage with `fastapi_hello_app`
'.' specifies the current working directory

Run the Docker image with the Docker run command.

```sh
$ docker run -p 8000:8080 fastapi_hello_app
```

Now type http:0.0.0:8000 into the browser. Your address http:0.0.0:8000 maps port 8080 (Docker) to your port 8000 (Web URL)

```text
{"Hello":"World"}
```

# Cloud Deployment

You have numerous options for deploying/hosting your Docker containers including

- web solutions, such as AWS (Amazon), GCP (Google), Azure (Microsoft)
- or even your own local computer.

There are many tradeoffs and reasons that will drive your decision for hosting service including ease of use, cost, and compatability with your technology stack and providers. For example, some services offer free initial hosting but are expensive to scale. Hosting locally is good for intial development but brings significant responsibilities for security, privacy and scale in a production setting.

In my case, the fastAPI backend serves a front-end (UI) service hosted on yet a different platform. GCP hosting on Cloud Run makes sense since the data storage is in the Big Query Data Warehouse (on GCP) and the Cloud Run hosting service and infrastructure is among the most cost effective (serverless pricing), scalable (auto-scaling) and offers additional services like Firebase app authentication services, IP addresses and HTTPS security.

As a side note, I prefer to build my Docker images locally rather than building remotely. This allows better visibility for debug, testing, and cost control.

## Setup Google Cloud Run

Here are listed a set of simplified step by step setup instructions for deploying to the Google Artifact Registry and subsequently deploying to the Google Cloud Run (serverless) service.

- Step 0: Pre-requisite
  As a pre-requisite GCP CLI and a GCP Project ID are required.
- Step 1: login to GCP with the GCP CLI
  `$ google auth login `
- step 2: Enable the artifact registry with the CLI
  `$ gcloud services enable artifactregistry.googleapis.com`
- step 3: create an artifact repository
  `$ gcloud artifacts repositories create "repo name" --repository-format=docker --location="REGION"--description="description ..."`
- step 4: list your repositories
  `$ gcloud artifacts repositories list`
- step 5: Configure Docker to use the GCP CLI to authenticate requests to the Artifact Registry
  ` $ gcloud auth configure-docker [REGION]-docker.pkg.dev`

Detailed instructions are found in the following references:

- Pushing Artifacts to Artifact Registry: A Step-by-Step Guide, https://medium.com/@abhinav.90444/title-pushing-artifacts-to-artifact-registry-a-step-by-step-guide-97f825242cfc

- Google Cloud, Artifact Registry, https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images#gcloud

## Deploy Docker Image to Artifact Registry

As a reminder of your available local images, first list your local Docker images

```text
$ docker images
-----
REPOSITORY          TAG       IMAGE ID       CREATED              SIZE
fastapi_hello_app   latest    e414682a267c   About a minute ago   150MB

```

**Tag the image**

```sh
$ docker tag [IMAGE_NAME] \
/[PROJECT_ID]/[REPO_NAME]/[IMAGE_NAME]:[TAG]
```

Below, for example, `fastapi_hello_app`, and TAG `v-0-0` replace the IMAGE and TAG fields. You will still need to add your REGION and GCP PROJECT-ID. The choice of tag (on the Registry) is completely up to you.

```sh
docker tag fastapi_hello_app [REGION]-docker.pkg.dev/[PROJECT ID]/[REPOSITORY]/fastapi_hello_app:v0-0-0

```

**Push to Artifact Registry**

Now we are ready to push this image to the Artifact Registry.

```sh
$ docker push [REGION]-docker.pkg.dev/[PROJECT ID]/[repo-name]/<[IMAGE]:[TAG]>
------
ea680fbff095: Pushed
v0-0-0: digest: sha256:2bf42bbeb22437ee3172a0e551cef87d3198c1be59caf43c1db4aed578e89622 size: 1993
```

You can check the GCP Artifact Registry on the Web Console to confirm the image is there.

After issuing the above command notice the shaw digest from the command output. It will be useful for the next section. It is also available on your GCP Artifact Registry console.

**Deploy to Cloud Run**

Here is the pattern for deploying the image to Cloud Run

```sh
$ gcloud run deploy <service-name> --image <image-registry-url>
```

The service-name is restricted to alphanumeric characters and dashes (not underscore)

```sh
$ gcloud run deploy [SERVICE_NAME] --image [REGION]-docker.pkg.dev/[PROJECT ID]/[REPO]/[IMAGE]@sha256:[DIGEST]
```

For example, the service-name and image-registry-url will take on the following form. You can always copy the URL string from the GCP Artifact Registry Console.

```sh
$ gcloud run deploy fast-api-hello --image [REGION]-docker.pkg.dev/[PROJECT ID]/[REPO]/[IMAGE]@sha256:2bf42bbeb22437ee3172a0e551cef87d3198c1be59caf43c1db4aed578e89622
------

Service [fast-api-hello] revision [fast-api-hello-00002-fhr] has been deployed and is serving 100 percent of traffic.
Service URL: https://fast-api-hello-aa55f576yq-uc.a.run.app

```

When issuing the command you will be asked to allow un-authenticated access. Say yes for now and later we will add authenticaion credentials. Make sure to delete the deployment (cloud run console) when concluding this exercise.

Your service is now deployed.

In your browser, go to the service URL listed in the command output above. You should receive the Hello World response

```json
{ "Hello": "World" }
```

# Authentication with Firebase

Amongst other thiings, Firebase is an excellent service for supporting OAuth authorization and managing the user's login and passwords.

In some cases a simple application without authorizaion is preferred. However, if Authorization if required, then first setup the following steps and then do the Cloud Run deployment as above.

## Firebase Setup

We follow the steps in this [article](https://medium.com/@gabriel.cournelle/firebase-authentication-in-the-backend-with-fastapi-4ff3d5db55ca) for setting up firebase authentication. As before, we make several enhancements.

Start by setting up firebase or use an existing Firebase Project

- If you don't already have a Firebase project, then in the Google console create a firebase project and give it a nmae of your choosing (e.g. "fast_api_users")
- Next within firebase project, go to Project Settings then Service accounts and click Generate new private key
- Save the file in your backend directory in the file `service-account.json`
- Create the `.env` file in the backend directory with the following content.

```text
# .env
ENV=dev
GOOGLE_APPLICATION_CREDENTIALS="./service-account.json"
FRONTEND_URL=http://localhost:3000
```

- We will need the FRONTEND_URL variable to avoid CORS issues, see below. The FRONTEND_URL corresponds to the default port number for a React application on the localhost. This will be replaced with a deployed URL in a production setting.

- For security purposes, make sure both of these files (`.env` and `service-account.json`) are listed in your `.gitignore` so that they do not get saved/uploaded to your repository.

- You do not need to include `service-account.json` in the repo as the account key (environment variable) is automatically set for you when you deploy to Cloud Run container.

We will add all the config settings to config.py file in the app directory. Our directory and files will look like the following.

```text
  backend
     +- app
         +-- __init__.py
         +-- routes.py
         +-- config.py
     main.py
     .env
     service-account.json
     .gitignore
```

Below is listing of the config.py file. The Python `BaseSettings` method imports environment variables and makes them available to other modules (e.g., see main.py, below)

THe `get_firebase_user_from_token` method calls the Firebase service to get the `userid` from the Authorizaton header. This is employed by the `/userid` route, discussed below.

```Python
# config.py
"""
configuration settings

- google credentials
- fast api settings
- get firebase user from token

"""

from pathlib import Path
from functools import lru_cache

from typing import Annotated, Optional
from pydantic_settings import BaseSettings

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token


class Settings(BaseSettings):
    """Main settings"""

    app_name: str = "demofirebase"
    env: str = "development"
    frontend_url: str = "NA"
    google_application_credentials: str

    class Config:
        """
        .env
        """

        env_file = str(Path(__file__).resolve().parent.parent / ".env")


@lru_cache
def get_settings() -> Settings:
    """Settings

    Returns:
        Settings: list of settings
    """

    try:
        settings = Settings()
    except Exception as e:
        print("Failed to load settings:", e)
        raise
    return settings


# use of a simple bearer scheme as auth is handled by firebase and not fastapi
# we set auto_error to False because fastapi incorrectly returns a 403 intead
# of a 401
# see: https://github.com/tiangolo/fastapi/pull/2120
bearer_scheme = HTTPBearer(auto_error=False)

def get_firebase_user_from_token(
    token: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> Optional[dict]:
    """Uses bearer token to identify firebase user id

    Args:
        token : the bearer token. Can be None as we set auto_error to False

    Returns:
        dict: the firebase user on success
    Raises:
        HTTPException 401 if user does not exist or token is invalid
    """

    try:
        if not token:
            # raise and catch to return 401, only needed because fastapi returns 403
            # by default instead of 401 so we set auto_error to False
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        return user

    # lots of possible exceptions, see firebase_admin.auth, but most of the time it is a credentials issue
    except Exception as exc:
        # see https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

```

# Avoiding CORS issues

## CORS

CORS - Cross Origin Resource Sharing is a browser security feature that restricts web pages from requesting resources from a different domain than the one that served the page. In other words, it prevents one website/service from directly accessing resources from another website.

Therefore, depending on how you deploy your frontend and your backend, you may encounter CORS issues. In fastAPI, CORS issues are easy to deal with.

We add the following to main.py

```Python
from fastapi.middleware.cors import CORSMiddleware
import os
...
origins = [os.getenv("FRONTEND_URL", "")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## The Complete Main.py

The complete main.py file listing follows. Environment variables are imported from `config.py` (`get_settings`)

```Python
# main.py
"""
FastAPI Hello World, Getting Started application, main.py

"""

# Firevase
import firebase_admin
from firebase_admin import credentials

# Corrs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

# importing config will also call load_dotenv to get GOOGLE_APPLICATION_CREDENTIALS
from app.config import get_settings

# initialize app and routes
app = FastAPI()
app.include_router(router)

settings = get_settings()
origins = [settings.frontend_url]

# Fireebase
cred = credentials.Certificate(settings.google_application_credentials)

firebase_admin.initialize_app(cred)
# Debug ... Google FIrebase Check
print("Current App Name:", firebase_admin.get_app().project_id)

# Corrs
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

```

# Userid Route

Next, we add a route, `/userid`, to get the `userid` from the token, `get_firebase_user_from_token` method in `config.py`.

```Python
@router.get("/userid")
async def get_userid(user: Annotated[dict, Depends(get_firebase_user_from_token)]):
    """gets the firebase connected user"""
    return {"id": user["uid"]}
```

# Next Steps

An examplar frontend React Application is described [here](https://github.com/Aljgutier/react_firebase). The frontend application illustrates how to send the Autorization header with Firebase token and subsequently displays the returned`userid`.
