---
sidebar_label: api
title: soil.api
---

This package contains calls to the SOIL&#x27;s REST API

#### upload\_data

```python
upload_data(dtype: str, data: Any, metadata: Any) -> Result
```

Upload data to the cloud as a new dataset.

#### get\_result

```python
get_result(result_id: str) -> Dict[str, Any]
```

Get the result data

#### get\_result\_data

```python
get_result_data(result_id: str, query: Optional[Dict[str, str]] = None) -> Dict[str, Any]
```

Get the result data

#### upload\_module

```python
upload_module(module_name: str, code: str, is_package: bool) -> None
```

Uploads a module

#### get\_module

```python
get_module(full_name: str) -> GetModule
```

Downloads a module

#### set\_alias

```python
set_alias(alias: str, result_id: str, roles: Optional[List[str]] = None) -> None
```

Sets an alias for a result. Updates a previous one with the same name.

#### get\_alias

```python
get_alias(alias: str) -> Dict[str, Any]
```

Gets an alias

#### create\_experiment

```python
create_experiment(plan: Plan) -> Experiment
```

Runs an experiment in SOIL

#### get\_experiment

```python
get_experiment(experiment_id: str) -> Experiment
```

Runs an experiment from SOIL

#### get\_experiment\_logs

```python
get_experiment_logs(experiment_id: str, start_date: str) -> Any
```

Gets logs from a SOIL experiment

