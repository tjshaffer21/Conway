Conway is an implementation of Conway's Game of Life.

### Requirements
+ Python 3.5
+ pygame 1.9.2
+ unittest

### Execution

In the main conway directory:

```python conway -w [w,h] -c [w,h]```

*-w* specifies the window size.

*-c* specifies the size of the conway system.

#### Controls

* *Enter* - A single iteration.
* *Space* - Loop start/stop
* *Esc*   - Quit

### Testing

``` python -m unittests tests\test_tilemap.py ```

``` python -m unittests discover -s tests ```