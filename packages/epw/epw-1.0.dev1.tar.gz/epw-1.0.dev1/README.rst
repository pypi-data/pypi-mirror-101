=================
EnergyPlusWrapper
=================

Copyright (c) 2019 Jérémie DECOCK (www.jdhp.org)

* Web site: http://www.jdhp.org/software_en.html#epw
* Online documentation: https://jdhp.gitlab.io/epw
* Examples: https://jdhp.gitlab.io/epw/gallery/

* Notebooks: https://gitlab.com/jdhp/eplus-python-wrapper-notebooks
* Source code: https://gitlab.com/jdhp/eplus-python-wrapper
* Issue tracker: https://gitlab.com/jdhp/eplus-python-wrapper/issues
* EnergyPlusWrapper on PyPI: https://pypi.org/project/epw
* EnergyPlusWrapper on Anaconda Cloud: https://anaconda.org/jdhp/epw


Description
===========

EnergyPlus wrapper for Python

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

*  Python >= 3.0

.. _install:

Installation
============

Gnu/Linux
---------

You can install, upgrade, uninstall EnergyPlusWrapper with these commands (in a
terminal)::

    pip install --pre epw
    pip install --upgrade epw
    pip uninstall epw

Or, if you have downloaded the EnergyPlusWrapper source code::

    python3 setup.py install

.. There's also a package for Debian/Ubuntu::
.. 
..     sudo apt-get install epw

Windows
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.4 under Windows 7.
..     It should also work with recent Windows systems.

You can install, upgrade, uninstall EnergyPlusWrapper with these commands (in a
`command prompt`_)::

    py -m pip install --pre epw
    py -m pip install --upgrade epw
    py -m pip uninstall epw

Or, if you have downloaded the EnergyPlusWrapper source code::

    py setup.py install

MacOSX
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.5 under MacOSX 10.9 (*Mavericks*).
..     It should also work with recent MacOSX systems.

You can install, upgrade, uninstall EnergyPlusWrapper with these commands (in a
terminal)::

    pip install --pre epw
    pip install --upgrade epw
    pip uninstall epw

Or, if you have downloaded the EnergyPlusWrapper source code::

    python3 setup.py install


Documentation
=============

* Online documentation: https://jdhp.gitlab.io/epw
* API documentation: https://jdhp.gitlab.io/epw/api.html


Example usage
=============

::

    import epw
    import matplotlib.pyplot as plt

    sub_dict = {("Material", "BETON 20CM", "Conductivity"): 9.99}

    df = epw.core.sub_run(epw.data.idf_cube_path(),
                          weather_file_path=epw.data.weather_san_francisco_tmy_path(),
                          sub_dict=sub_dict)

    df.plot()
    plt.show()


Bug reports
===========

To search for bugs or report them, please use the EnergyPlusWrapper Bug Tracker at:

    https://gitlab.com/jdhp/eplus-python-wrapper/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
