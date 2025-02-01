# Swagger

## Dependencies

To install the virtual environment, run:

```console
python -m venv "$VIRTUAL_ENVIRONMENT"
source "$VIRTUAL_ENVIRONMENT/bin/activate"
pip3 install -r requirements.txt
```

## Usage

### Documentation

To launch the Swagger server, run:

```console
python3 -m swagger_server
```

Alternatively, to launch the docker container, run:

```connsole
docker build -t swagger_server .
docker run -p 8087:8087 swagger_server
```

To view the documentation, run:

```console
xdg-open localhost:8087/ui
```

### Tests

To launch the integration tests, run:

```console
tox
```
