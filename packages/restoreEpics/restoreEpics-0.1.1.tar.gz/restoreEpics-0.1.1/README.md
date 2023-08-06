# restoreEpics

A simple package that gives wrapped caput and writeMatrix functions for writing EPICS channels which save previous values and a restoreEpics function can be used later to restore all values in case of error, interrupt, or as a final restore.

## Usage

### Restoring channels

```
from restoreEpics import restoreEpics, backUpVals, restoreMethods, caput, caget

try:
    # do some work that uses caget or caput as usual
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```

### Writing to matrices with form basename_ii_jj_suffix

```
from restoreEpics import restoreEpics, backUpVals, restoreMethods, writeMatrix

try:
    writeMatrix(basename, mat, suffix=suffix, tramp=10)
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```

### Make your own restoring methods

```
from restoreEpics import restoreEpics, backUpVals, restoreMethods
from awg import Sine

def exciteSine(ch, freq, ampl, duration=10, ramptime=1):
    exc = Sine(ch, freq, ampl, duration=duration)
    exc.start(ramptime=ramptime)
    if all([ele['name'] != ch for ele in bak]):
        backUpVals += [{'type': 'excSine', 'name': 'ch', 'exc': exc}]  # Store the exc object wth a type defined.


def restoreExc(exc):
    exc.stop()  # Restoring method for excitation.

# Add the restoring method to restoreMethods dictionary with type defined above as key
restoreMethods['excSine'] = restoreExc

try:
    exciteSine('blah', 0.5, 10)
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```
