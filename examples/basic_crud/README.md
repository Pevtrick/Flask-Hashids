# Basic CRUD example application

A simple CRUD application demonstrating how to use the Flask-Hashids extension.

## Configuration and startup

- Setup a virtual environment within the basic_crud directory: `python3 -m venv venv`
- Activate the newly created virtual environment: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Start the app: `python app.py`

## Usage

Test out the curl commands below to see examples on how the hashid works for various CRUD operations.

### Create a user

```bash
curl \
  -d '{"name": "John Doe"}' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -i \
  -X POST \
  localhost:5000/users
```

```
HTTP/1.1 201 CREATED
Server: ...
Date: ...
Content-Type: application/json
Content-Length: 48
Connection: close

{"id":"Wb","name":"John Doe","url":"/users/Wb"}
```

### Get all users

```bash
curl \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -i \
  localhost:5000/users
```

```
HTTP/1.1 200 OK
Server: ...
Date: ...
Content-Type: application/json
Content-Length: 50
Connection: close

[{"id":"G8","name":"John Doe","url":"/users/G8"}]
```

### Get a single user

```bash
curl \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -i \
  localhost:5000/users/G8
```

```
HTTP/1.1 200 OK
Server: ...
Date: ...
Content-Type: application/json
Content-Length: 48
Connection: close

{"id":"G8","name":"John Doe","url":"/users/G8"}
```

### Update a user

```bash
curl \
  -d '{"name": "Jane Doe"}' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -i \
  -X PUT \
  localhost:5000/users/G8
```

```
HTTP/1.1 204 NO CONTENT
Server: ...
Date: ...
Content-Location: /users/G8
Content-Type: application/json
Connection: close
```

### Delete a user

```bash
curl \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -i \
  -X DELETE \
  localhost:5000/users/G8
```

```
HTTP/1.1 204 NO CONTENT
Server: ...
Date: ...
Content-Type: application/json
Connection: close
```
