# Webster

Autonomous, highly configurable web crawling platform

![](doc/Comp-diag.jfif)

## Installation

Clone the repository locally:
```bash
git clone git@github.com:Bogdanfl935/Webster.git
```

## Deployment

Using [Docker](https://www.docker.com/), run the following from within the `source` directory:

> **Prerequisite**
> 
> Environment variables must be configured in a common file `<path/to/your/env/file>`

```bash
docker-compose --env-file <path/to/your/env/file> -f docker-compose-independent.yml -p independent up --build --remove-orphans 
```
```bash
docker-compose --env-file <path/to/your/env/file> -f docker-compose-dependent.yml -p dependent up --build --remove-orphans
```

## Usage

If running on default configuration, the client may be accessed at `http://localhost:50009/`

Upon authentication, the crawler may be used as such:

1. Going to `Activity` tab, the crawler can be started and stopped accordingly. To start the crawler, provide a starting URL from which the crawling activity shall proceed.

1. Going to `Configuration` tab, both the crawler and parser may be adjusted. By default, the parser takes into account only `<a>` tags. Additional tags may be introduced in order to target additional content.

1. Parsed content may be accessed in the `Archive` tab. Content is indexed by source URL and may be downloaded into a `.zip` file.

1. Memory usage and statistics are displayed on the home page. Several metrics include: memory usage, anchors parsed, tag yield by source.

## Authors

The Webster crawling platform has been developed with the support of:
+ **Bogdan-Flavius Budihala**
+ **Mihai Damian**


