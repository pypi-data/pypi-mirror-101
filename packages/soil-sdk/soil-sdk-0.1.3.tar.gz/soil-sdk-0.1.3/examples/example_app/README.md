# README

This is an example SOIL application using the iris dataset.

## Install

```sh
python -m venv .venv
```

**Run this line everytime you work with this project.**
```sh
source .venv/bin/activate
```

```sh
pip install -r requirements.txt
```

```sh
pip install -r requirements_remote.txt
```

Only if you are creating a new repo.
```sh
git init
```

You are going to love and hate this (not in this order).
```
pre-commit install
```

## Scripts

### Reset indexes
```sh
soil run setup reset-dbs
```


### Upload new data

```sh
soil run data new-data data/iris.csv
```

### Train model


```sh
soil run schedules train
```


### Do predictions

```sh
soil run schedules predict
```
