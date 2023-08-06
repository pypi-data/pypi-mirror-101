# VGS CLI
[![CircleCI](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master.svg?style=svg&circle-token=dff66120c964e4fbf51dcf059b03746910d0449d)](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master)

Command Line Tool for programmatic configurations on VGS.

[Official Documentation](https://www.verygoodsecurity.com/docs/vgs-cli/getting-started)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [PyPI](#pypi)
- [Run](#run)
- [Running in Docker](#running-in-docker)
- [Commands](#commands)
    
## Requirements
[Python 3](https://www.python.org/downloads/) or [Docker](https://docs.docker.com/get-docker/).

## Installation

### PyPI
Install the latest version from [PyPI](https://pypi.org/project/vgs-cli/):
```
pip install vgs-cli
```

## Run

Verify your installation by running:
```
vgs --version
```

## Running in Docker

In order to run in Docker we recommend declaring the following `docker-compose.yaml`:
```yaml
version: '3'
services:

  cli:
    image: quay.io/verygoodsecurity/vgs-cli:${VERSION:-latest}
    stdin_open: true # docker run -i
    tty: true        # docker run -t
    env_file:
      - .env
    command: bash
    ports:
      - "7745:7745"
      - "8390:8390"
      - "9056:9056"
```
First, you start the lightweight cli container in detached mode by executing:
```bash
docker-compose up -d cli
```
Then proceeding with login:
```
docker-compose exec cli vgs login
```
And now you are ready to execute any vgs cli command:
```
docker-compose exec cli vgs logs access -V tntmiph5i0n
```

To use auto login option you can declare the following `.env` file:
```
VGS_CLIENT_ID=<YOUR-CLIENT-ID>
VGS_CLIENT_SECRET=<YOUR-CLIENT-SECRET>
``` 
Alternatively, you can set the environment variables right in the `docker-compose.yaml`:
```yaml
version: '3'
services:

  cli:
    image: quay.io/verygoodsecurity/vgs-cli:${VERSION:-latest}
    stdin_open: true # docker run -i
    tty: true        # docker run -t
    environment:
      VGS_CLIENT_ID: <YOUR-CLIENT-ID>
      VGS_CLIENT_SECRET: <YOUR-CLIENT-SECRET>
    command: bash
    ports:
      - "7745:7745"
      - "8390:8390"
      - "9056:9056"
```

Run a specific version:
```bash
VERSION=[VERSION] docker-compose up -d
``` 

You can turn on debugging by appending `-d` or `--debug` right after `vgs`:
```
docker-compose exec cli vgs --debug logs access -V tntmiph5i0n
```
## Commands

- [`help`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#exploring-the-cli)
- [`login`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#login) and [auto login](https://www.verygoodsecurity.com/docs/vgs-cli/commands#auto-login)  
- [`logout`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#logout)
- [`routes get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)
- [`routes apply`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#apply)
- [`logs access`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#access)

## Sphinx Documentation

In order to generate [Sphinx](https://www.sphinx-doc.org/en/master/index.html) documentation:
```
pip install -r dev-requirements.txt
cd docs
make html
```
Check the generated docs:
```
open build/html/index.html
```

## Plugins Development

See [Click - Developing Plugins](https://github.com/click-contrib/click-plugins#developing-plugins).

In order to develop a plugin you need to register your commands to an entrypoint in `setup.py`.

Supported entrypoints:

- `vgs.plugins` - for extending `vgs` with sub-commands
- `vgs.get.plugins` - for extending `vgs get` with sub-commands
- `vgs.apply.plugins` - for extending `vgs apply` with sub-commands
- `vgs.logs.plugins` - for extending `vgs logs` with sub-commands

Example:
```python
entry_points='''
    [vgs.plugins]
    activate=vgscliplugin.myplugin:new_command
    
    [vgs.get.plugins]
    preferences=vgscliplugin.myplugin:new_get_command
'''
```
