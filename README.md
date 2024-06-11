# Food Planner REST API

This RESTful API enables users to save recipes, add them to collections and plan them with calendar entries. It is still a work in progress but could eventually be consumed by a frontend such as this [Food Planner](https://github.com/willelson/food-planner) app.

Created with Python [Fast API](https://fastapi.tiangolo.com/).

## Installation

Create your virtual environment.

```
python3 -m venv env
```

Activate the virtual environment.

```
source env/bin/activate
```

Install the requirements.

```
pip install -r requirements.txt
```

To set up environment variables create a `.env` file in the root directory, and add your secret key.

```
SECRET_KEY=<your secret key>
```

## Run the project

Start the dev server.

```
uvicorn main:app --reload
```

Navigate to `http://localhost:8000/docs` to view the swagger docs and interact with the API.
