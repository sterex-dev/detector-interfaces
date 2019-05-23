# detector_interfaces

A set of classes to programatically interface with detectors.

# Summary

The current list of supported detectors includes:

- Basler 2040-35gm

# Configuration

To communicate with Basler cameras, the Pylon software/drivers (https://www.baslerweb.com/en/sales-support/downloads/software-downloads/) and pypylon package (https://github.com/basler/pypylon) need to be installed.

# Usage

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

camera.disconnect()
```

