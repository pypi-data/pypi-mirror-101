# Confboy

[![codecov](https://codecov.io/gh/Euromance/confboy/branch/master/graph/badge.svg?token=O5LFEZO8WM)](https://codecov.io/gh/Euromance/confboy)

Better configs with TOML support.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install confboy.

```bash
pip install confboy
```

## Usage

```python
import confboy


base_config = {
    'nested': {
        'one': 1,
        'two': 2,
    },
    'three': 3,
}

config = confboy.Config(base_config)

config.nested.one  # Returns `1`
config.three       # Returns `3`
```

Although it is advised not to change the config
during runtime, it is also possible:

```python
config.nested.one = 10
config.nested.one  # Returns `10`

config.new_nested = {'one': 1}
config.new_nested.one  # Returns `10`
```

Confboy also supports dynamic values
that can use other values from the same config.
You can use it to build connection URLs or whatever.
Shines with changing config during runtime:
change `config.postgres.user` and `config.postgres.url`
will be rebuilt on every query if it's a callable.

```python
def add(a, b):
    return a + b

config = confboy.Config(
    base_config={
        'a': {'a': 1},
        'b': 2,
        'a_plus_b': 'callable:add',  # Tell confboy to call `add` from provided callables
    },
    callables={
        'add': {
            'func': add,
            'kwargs': {              # Define kwargs and value paths for them
                'a': 'a.a',
                'b': 'b',
            },
        },
    }
)

config.a_plus_b  # Returns 3
```

Confboy can take values from TOML files as well.
Provided config will be merged over base config.

```toml
# config.toml

[nested]
one = 1
two = 2

not = "nested"
```

```python
config = confboy.Config(toml_config_path='config.toml')
config.nested.one  # Returns 1
config.not         # Returns 'nested'
```

Confboy's merges are __soft__: if the value
is present in the config but not in patch,
it won't be deleted from the config.
It supports value deletion and everything.
Just try it out or check the source code!
