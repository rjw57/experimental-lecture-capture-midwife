# Prototype agent health check endpoint

This repository implements a prototype healthcheck endpoint for lecture capture
agents. It is designed to be quick to hack on and would not be suitable for
production use.

## Running

```bash
$ docker build -t uisautomation/lecture-capture-midwife .
$ docker run --rm -p 8080:80 uisautomation/lecture-capture-midwife
```

## Use

Run birthscream pointing at the ingest URL:

```bash
$ birthscream -q --post-url=http://localhost:8080/cry
```

You can see received payloads at http://localhost:8080/payloads.

A health-check endpoint is available at http://localhost:8090/healthz.
