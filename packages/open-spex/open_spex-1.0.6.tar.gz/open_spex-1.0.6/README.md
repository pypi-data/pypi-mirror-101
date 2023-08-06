openSpex - a basic analysis and display tool for radioxenon beta-gamma data on IMS-format.
Version 1.0.6 - April 13, 2021


Installation
------------

Create and activate a virtual environment:

$ python3 -m venv venv
$ source venv/bin/activate (on Windows: $ call venv\Source\\activate)

Install openSpex using pip:

(venv) pip install open-spex

Start application:

(venv) openSpex

See the help menu for further information. 

IMPORTANT NOTE: openSpex uses the Python module "pickle" to save analysed data as pkl-files. 
The pickle module is not secure. Only open pkl-files you trust.