# detector_interfaces

A set of classes to interface with detectors.

# Summary

These classes provide a way to programmatically interface with supported detectors. The current list of supported equipment includes:

- Basler 2040-35gm

# Configuration

To communicate with Basler cameras, the Pylon software/drivers (https://www.baslerweb.com/en/sales-support/downloads/software-downloads/) and pypylon package (https://github.com/basler/pypylon) need to be installed.

# Usage

Import the necessary class, 

```Python

import numpy as np
import pylab as plt

from detector_interfaces import Basler_2040_35gm

camera = Basler_2040_35gm()
camera.connect()

camera.expose(1)
res, code = camera.readNImagesFromBuffer(1)

plt.imshow(res[0])
plt.show()

camera.disconnect()```
