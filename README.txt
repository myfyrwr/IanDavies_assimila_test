Contents:
------------------------------------
README.txt                    - this file
srs_transform.py              - class to perform coordinate transformations
test_srs_transform_nose.py    - test functions for  srs_transform.py
requirements.txt              - used to setup python environment.

------------------------------------
Installation and running.
------------------------------------
Unpack these files into a directory 
>git clone https://github.com/myfyrwr/IanDavies_assimula_test
cd to that directory 

If anaconda is not initialized in your environment,
find the full path to the conda executable, and  type this:
replacing bash with whatever shell you use.
eval "$(/full/path/to/your/anaconda3/bin/conda shell.bash hook)"

create a python environment 
with a name of your choice, say 'envname' as follows: 

>conda create -n envname python=3.8.11 anaconda
say y when at the prompt.
>conda activate envname
>pip install -r requirements.txt --no-deps
>pip install nose

Note that I had to use --no-deps. You may not need to, 
but I had a problem with dependencies due to  a package called 'six'.

To run the tests using nose and generate the log file in the same directory:
>nosetests --nologcapture

Or to see the stdout
>nosetests --nologcapture -s 

------------------------------------
to do.
------------------------------------
There are other conversions to do (for instance lat/long <-> bng)
and other formats to consider. 
Also other tests possible, but I concentrated on conversions to and from 
sinusoidal  and tests thereof in the time available.

Might need to perform better error checking - particularly
where sinusoidal values are out of range in 'corner regions' 
