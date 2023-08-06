# Python Package Boilerplate

This is an minimal example of how to publish a python package.

You can follow along with the [guide](https://nrempel.com/how-to-publish-a-python-package-to-pypi).


### WARNING: do not run apply_custom_naming.py from another directory. It will delete things (potentially).
### INFO: If no script name is entered, it will delete both the scripts directory and scripts line from setup.py
To apply a custom name to your package, run:

python3 apply_custom_naming.py


In order for the automated publishing workflow to work on release, you must first add these secrets, as they are not automatically imported from the template:
    
    PYPI_USERNAME
    PYPI_PASSWORD
