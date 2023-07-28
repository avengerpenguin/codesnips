---
tags: direnv, python
---

## Prerequisites

- `direnv` is installed

## Snippet

Create `.envrc` in project root:

```bash
# Using direnv built-in to create venv
layout python3  
# Create venv as alias to latest
# Useful for configuring ./venv as a fix dir in Pycharm etc.
ln -sfn .direnv/$(basename $VIRTUAL_ENV)/ venv  

# Optionally look for a 2nd file containing passwords
# e.g. export API_KEY=xxx
if file .envrc.secret ; then  
  source_env .envrc.secret  
fi
```
