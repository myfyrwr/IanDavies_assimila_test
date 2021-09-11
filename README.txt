Contents:
------------------------------------
README.txt                    - this file
srs_transform.py              - class to perform coordinate transformations
test_srs_transform_nose.py    - test functions for  srs_transform.py
requirements.txt              - used to setup python environment.
------------------------------------
Unpack these files into a directory 
cd to that directory and create a python environment 
with a name of your choice, say 'envname' as follows: 

>conda create -n envname python=3.8.11 anaconda
>conda activate envname
>pip install -r requirements.txt --no-deps
>pip install nose

Note that I had to use --no-deps, as I had a problem with 
dependencies of a package called 'six'.

To run the tests using nose and generate the log file in the same directory:
>nosetests --nologcapture

Or to see the stdout
>nosetests --nologcapture -s 

There are other conversions to do (for instance lat/long <-> bng)
and other formats. 
Also other tests possible, but I concentrated on conversions to and from sinusoidal  
and tests thereof in in the time available.
