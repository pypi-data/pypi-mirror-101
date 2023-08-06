===============
pySerialSensors
===============

.. image:: https://img.shields.io/pypi/v/pyserialsensors.svg
        :target: https://pypi.python.org/pypi/pyserialsensors

.. image:: https://img.shields.io/travis/Egenskaber/pyserialsensors.svg
        :target: https://travis-ci.com/Egenskaber/pyserialsensors

.. image:: https://readthedocs.org/projects/pyserialsensors/badge/?version=latest
        :target: https://pyserialsensors.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Egenskaber/pyserialsensors/shield.svg
     :target: https://pyup.io/repos/github/Egenskaber/pyserialsensors/
     :alt: Updates



Serial communication with sensors via I2C, SPI and UART using FTDI USB bridges

Make sure your current user is member of the `dialout` group.


* Free software: MIT license
* Documentation: https://pyserialsensors.readthedocs.io.


Features
--------

Supported Sensors
* SHT85
* SFM3000
* SDP810
* SPS30
* BME280
* SCD30
* ADS1015
* MAX31865
* SMGAir2

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
### Rename FTDI
Use tools/renamy.py

Check the result using 
```lsusb -d 0403: -v```

### Known Issues

- After a reconnect the measurement frequency drops due to hard coded frequency in the reconnection code.
