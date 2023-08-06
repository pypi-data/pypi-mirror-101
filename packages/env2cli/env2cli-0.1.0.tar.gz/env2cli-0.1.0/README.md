# Env2Cli

## Desription

Instead of maintain ugly and long entrypoint scripts to call your module with environment variables as arguments from your dockerfile, just add this elegant converting framework from environment variables to cli command line arguments.

## Installation

```bash
pip install env2cli
```

## Usage

Assume your old dockerfile looked like this

```Dockerfile
...
ENV POSITIONAL_ARG val
ENV SOME_PARAM value
ENV OTHER_PARAM valy

...

ENTRYPOINT python main.py ${POSITIONAL_ARG} -p ${SOME_PARAM} --other ${OTHER_PARAM} ...
```

Add new file, for example, `entrypoint.py` like this:

```python
from main import main
from env2cli import * 

argv = bulk_apply([
    Argument('POSITIONAL_ARG'),
    Argument('SOME_PARAM', '-p'),
    Argument('OTHER_PARAM', '--other')
])

main(argv)
```
And the new dockerfile should be looking like this:

```Dockerfile
ENV POSITIONAL_ARG val
ENV SOME_PARAM value
ENV OTHER_PARAM valy

...

ENTRYPOINT python entrypoint.py
```

Or even if your program isn't python!

```Dockerfile
ENV POSITIONAL_ARG val
ENV SOME_PARAM value
ENV OTHER_PARAM valy

...

ENTRYPOINT ./myprog $(env2cli.py)
# instead ENTRYPOINT ./myprogram ${POSITIONAL_ARG} -p ${SOME_PARAM} --other ${OTHER_PARAM}
```