```python
from contextlib import contextmanager
@contextmanager
def task(task='Task'):
    logger.info(f"{task} started")
    yield
    logger.info(f"{task} done")

@task()
def f():
    pass

f()
```