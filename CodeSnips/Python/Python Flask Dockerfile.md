---
title: Some title
author: Some person
tags:
  - tag 1
  - tag 2
date: 2014-12-25 00:00
summary: The article summary will be __parsed__ as markdown
---

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

# Copy just requirements first to create cached layer with deps
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Now copy the rest of the source
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

Notes:

- Creating a `.dockerignore` is recommended to prevent the `COPY . .` line from copying too much (e.g. if you have a `venv` in the working directory)
