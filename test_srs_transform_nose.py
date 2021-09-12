# test functions for SRS_Transform class.
from srs_transform import SRS_Transform
import numpy as np

# Tolerance values needed for some tests
# where values are expected to match, but can be
# a bit off due small errors introduced by  floating point arithmetic
TOL9 = 1e-9
TOL8 = 1e-8

# 'average' Radius of the earth (assumed spherical?) 
# this value was taken from the sinusoidal srs. 
R=6371007.181 

# Next two tests use the initial values supplied by Ian.
def test_sin2bng_1():
	coords = SRS_Transform.sin2bng((-317759.094, 6162636.771))
	assert coords[0] ==  207930.32884220436
	assert coords[1] ==  618409.8383623955
	assert coords[2] == 0.0

def test_sin2LatLong_1():
	coords = SRS_Transform.sin2LatLong((-317759.094, 6162636.771))
	assert coords[0] ==  55.42186150777619
	assert coords[1] ==  -5.035284162360862
	assert coords[2] == 0.0

# do a round trip  sin -> bng -> sin, should get back where we started.
def test_sin2bng2sin():
	sincoords = (-200000,3000000)# pick any valid values
	bngcoords =      SRS_Transform.sin2bng(sincoords)
	sincoords_back = SRS_Transform.bng2sin(bngcoords)
	assert abs(sincoords[0] - sincoords_back[0] ) <= TOL9
	assert abs(sincoords[1] - sincoords_back[1] ) <= TOL9
	
# do a round trip  sin -> latLong -> sin
def test_sin2LatLong2sin():
	sincoords = (-200000,3000000) # pick any valid values
	latLongcoords  =      SRS_Transform.sin2LatLong(sincoords)
	sincoords_back =      SRS_Transform.LatLong2sin(latLongcoords)
	assert abs(sincoords[0] - sincoords_back[0] ) <= TOL9
	assert abs(sincoords[1] - sincoords_back[1] ) <= TOL9
	
# print the sinusoidal coords of some extreme lat long values
def test_BigLatLong2sin():
	ll3 = (0,0)
	sinu =      SRS_Transform.LatLong2sin(ll3)
	print (f'lat long ({ll3[0]},{ll3[1]}) is sinusoidal ({sinu[0]},{sinu[1]})')
	ll4 = (90,0)
	sinu =      SRS_Transform.LatLong2sin(ll4)
	print (f'lat long ({ll4[0]},{ll4[1]}) is sinusoidal ({sinu[0]},{sinu[1]})')
	ll5 = (0,180)
	sinu =      SRS_Transform.LatLong2sin(ll5)
	print (f'lat long ({ll5[0]},{ll5[1]}) is sinusoidal ({sinu[0]},{sinu[1]})')
	ll1 = (90,-180)
	sinu =      SRS_Transform.LatLong2sin(ll1)
	print (f'lat long ({ll1[0]},{ll1[1]}) is sinusoidal ({sinu[0]},{sinu[1]})')
	ll2 = (-90,180)
	sinu =      SRS_Transform.LatLong2sin(ll2)
	print (f'lat long ({ll2[0]},{ll2[1]}) is sinusoidal ({sinu[0]},{sinu[1]})')

def test_sin2LastLongExtreme():
	ll = (0,180)
	# Check the conversion is doing what it's supposed to for an extreme value.
	# sinu[0] should be close to pi*R == half the circumference of the earth.
	sinu = SRS_Transform.LatLong2sin(ll)
	assert abs(sinu[0] -np.pi *R ) <= TOL9
	assert abs(sinu[1]) <= TOL9

def test_too_big_sin2LatLong():
	# these are expected to fail - because of the increment added/subtracted 
	# to/from the lat/longs,which are already at the limit of the domain.
	# Each fail should put an ERROR messages in the log file
	increment = 0.0001
	coords = SRS_Transform.sin2LatLong( (np.pi *R +increment, 0))
	print (coords)
	assert coords[0] == float('inf') 
	assert coords[1] == float('inf') 
	assert coords[2] == float('inf') 
	coords = SRS_Transform.sin2LatLong( (-np.pi *R -increment, 0))
	print (coords)
	assert coords[0] == float('inf') 
	assert coords[1] == float('inf') 
	assert coords[2] == float('inf') 
	coords = SRS_Transform.sin2LatLong( (0, np.pi*R /2.0 +increment))
	print (coords)
	assert coords[0] == float('inf') 
	assert coords[1] == float('inf') 
	assert coords[2] == float('inf') 
	coords = SRS_Transform.sin2LatLong( (0, -np.pi*R /2.0 -increment))
	print (coords)
	assert coords[0] == float('inf') 
	assert coords[1] == float('inf') 
	assert coords[2] == float('inf') 
	# now do sin2lanlong with a coordinate that is not in the range of LatLong2sin
	# - in one of the corner regions
	sinu= (np.pi *R -1 ,np.pi *R /2.0 -1 )
	coords = SRS_Transform.sin2LatLong( sinu)
	print (coords)
	# Seems to be returning a valid lat long pair. 
	# isn't this wrong? If so, converter should maybe check param values,
	# log an error, return infs.
	
def test_sin2LastLongExact():
	# Check the sinu conversion is doing what it's supposed to for some general values.
	for longit in range(-180, 180, 10):
		for lat in range(-90,90,10):
			sinu = SRS_Transform.LatLong2sin((lat,longit))
			expected_value_x = np.cos (lat * np.pi / 180) * np.pi * R * longit / 180 
			expected_value_y = lat *  np.pi * R / 180 # just a linear scaling on y axis
			expected_value_z = 0.0
			#print (sinu[0], expected_value_x)
			#print (sinu[1], expected_value_y)
			assert abs(sinu[0] -expected_value_x ) <= TOL8
			assert abs(sinu[1] -expected_value_y ) <= TOL8
			assert abs(sinu[2] -expected_value_z ) <= TOL8

