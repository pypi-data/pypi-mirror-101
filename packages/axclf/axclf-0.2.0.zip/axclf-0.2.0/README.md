# axclf

Save/restore Matplotlib axes limits during iterative and interactive
development.

## Background
This functionality becomes useful when using cell-mode functionality
in editors such as IdleX, Spyder, IEP, etc. During algorithm prototyping,
plots are generated. These helper routines allow for inspecting a
region of interest on a plot, and then running a change to see its effects
without needing to re-zoom/pan to the region of interest.

## Example

```
from pylab import *
from axclf import *
ion()

## interactive cell
figure(1)
axclf()  # save axes limits and clear figure

ex = 6  # adjust this number when re-running, (CTRL+Plus in IdleX)

x = linspace(0, 10, 1000)
y = sin(x) ** ex
plot(x, y)

axrestore()  # restore axes limits

```
