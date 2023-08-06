# cstream
### C++ Style Colorful output stream for Python with debug level capabilities.

<br>
<br>

## Install (_all systems_)
```bash
$ pip install cstream
```

## Introduction
Default `stderr`, `stdwar` and `stdlog` instances are directed to standard error output. `stdout` is also available. `devnull` is not a `Stream`. It's a context manager.

## Examples
```python
from cstream import Stream, stderr, stdout, stdlog, stdwar, devnull

# Set debug level
Stream.set_lvl(1)

# Will be printed
stderr[0] << "Error: You are wrong."

# Gets printed also
stdwar[1] << "Warning: Just a warning... in yellow."

# Bypassed
stdlog[2] << "DEBUG: Some blue text printed to stderr"

# Suppress output written to stdout and stderr
with devnull:
    print("Bye World?")
```

## Next steps:
- Complete `logging` integration.