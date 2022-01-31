# Webster

Autonomous, highly configurable web crawling platform

![](doc/Comp-diag.jfif)

## Installation

Clone the repository locally:
```bash
git clone git@github.com:Bogdanfl935/Webster.git
```

## Usage

Using [Docker](https://www.docker.com/), run the following from within the `source` directory:

> **Prerequisite**
> 
> Environment variables must be configured in a common file `<path/to/your/env/file>`

```bash
docker-compose --env-file <path/to/your/env/file> -f docker-compose-independent.yml -p independent up --build --remove-orphans 
```

