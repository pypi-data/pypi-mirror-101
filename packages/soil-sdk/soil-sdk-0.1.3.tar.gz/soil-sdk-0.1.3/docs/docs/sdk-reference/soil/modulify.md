---
sidebar_label: modulify
title: soil.modulify
---

This module defines the @modulify decorator.

#### modulify

```python
modulify(_func: Optional[Callable[..., List[DataStructure]]] = None, *, output_types: Optional[Callable] = None, num_outputs: int = 1, _from_db: bool = False) -> Callable
```

Decorates a function to mark it as a soil module.

