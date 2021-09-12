# Module to convert spatial coordinates between reference systems.
# Can convert between sinusoidal, lat-long, and bng.
import logging
import numpy as np
import inspect # needed to get current function for logging
# Get calling function - for logging
def callingFunc():
	return inspect.getouterframes( inspect.currentframe() )[1]

LOG_FORMAT = '%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s %(message)s'
logging.basicConfig(filename=__file__+'.log',  level = logging.INFO,format = LOG_FORMAT)

logging.info("loading:" + __file__)
import osr
class SRS_Transform:
	"""
	 SRS_Transform performs a selection of transformations from one Spatial Reference System (SRS) 
	 to another. The SRSs must be define from their PROJ4 or WKT strings  
	 Currently suppoerted SRS are:
	 1 sinusoidal
	 2 BNG (British National Grid)
	 3 Latitude/Longitude.
	"""

	# Sinusoidal definition
	# from https://spatialreference.org/ref/sr-org/6842/
	# It fully match with the metadata in the MODIS products
	#sinusoidal_srs = (f'+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 '
	#				  f'+b=6371007.181 +units=m +no_defs ')
	R=6371007.181 # extract this value from the string to use for parameter error checking
	sinusoidal_srs = (f'+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a={R} '
					  f'+b={R} +units=m +no_defs ')

	# British National Grid (BNG) definition
	# from https://spatialreference.org/ref/epsg/osgb-1936-british-national-grid/
	# User should pass those parameters?
	bng_srs = (f' +proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 '
			   f' +x_0=400000 +y_0=-100000 +ellps=airy +datum=OSGB36 '
			   f' +units=m +no_defs ')

	# Sinusoidal  spatial reference system
	sin_SRS = osr.SpatialReference()
	sin_SRS.ImportFromProj4(sinusoidal_srs)

	# BNG spatial reference system.
	bng_SRS = osr.SpatialReference()
	bng_SRS.ImportFromProj4(bng_srs)
	# Lat,Long spatial reference system.
	LatLong_SRS = osr.SpatialReference()
	LatLong_SRS.ImportFromEPSG(4326) # should this ID be programmable?

	transform_sin2bng = osr.CoordinateTransformation(sin_SRS,bng_SRS)
	transform_bng2sin = osr.CoordinateTransformation(bng_SRS,sin_SRS)

	transform_sin2LatLong = osr.CoordinateTransformation(sin_SRS,LatLong_SRS)
	transform_LatLong2sin = osr.CoordinateTransformation(LatLong_SRS,sin_SRS)

	# sin<->bng transform methods
	@classmethod
	def sin2bng(cls,sin_point):
		"""Transform from sunusoidal reference to BNG (British National Grid).

		Parameters:
		This is a class method, so the first argument is the class name.
		The second argument is an array of two floating point numbers 
		representing coordinate in sinusoidal reference system.
		Returns:
		An array of 3 floating point numbers containing the corresponding BNG 
		coordinates.
		"""
		logging.info(callingFunc()[3] + f'( {sin_point[0]}, {sin_point[1]} )')
		if (abs(sin_point[0]) > np.pi *cls.R or abs(sin_point[1]) > np.pi *cls.R/2.0):
			logging.error(callingFunc()[3] + \
				f":parameter out of range:({sin_point[0]},{sin_point[1]})")
			return (float('inf'), float('inf'), float('inf')) # or 'NaN' better?
		return cls.transform_sin2bng.TransformPoint(sin_point[0], sin_point[1])

	@classmethod
	def bng2sin(cls,bng_point):
		"""Transform from BNG (British National Grid) to sinusoidal reference.

		Parameters:
		This is a class method, so the first argument is the class name.
		The second argument is an array of two floating point numbers 
		representing coordinate in BNG reference system.
		Returns:
		An array of 3 floating point numbers containing the corresponding sinusoidal 
		coordinates.
		"""
		logging.info(callingFunc()[3] + f'( {bng_point[0]} {bng_point[1]} )' )
		return cls.transform_bng2sin.TransformPoint(bng_point[0], bng_point[1])

	# sin<->LatLong transform methods
	@classmethod
	def sin2LatLong(cls,sin_point):
		"""Transform from sunusoidal reference to Lat Long.

		This is a class method, so the first argument is the class name.
		The second argument is an array of two floating point numbers 
		representing coordinate in sinusoidal reference system.
		Returns 
		An array of 3 floating point numbers containing the corresponding lat, long and height.
		"""
		logging.info(callingFunc()[3] + f'( {sin_point[0]}, {sin_point[1]} )')
		if (abs(sin_point[0]) > np.pi *cls.R or abs(sin_point[1]) > np.pi *cls.R/2.0):
			logging.error(callingFunc()[3] + \
				f":parameter out of range:({sin_point[0]},{sin_point[1]})")
			return (float('inf'), float('inf'), float('inf')) # or should it be 'NaN' ?
		return cls.transform_sin2LatLong.TransformPoint(sin_point[0], sin_point[1])
	
	@classmethod
	def LatLong2sin(cls,latLong_point):
		"""Transform from Lat Long to sinusoidal.

		This is a class method, so the first argument is the class name.
		The second argument is an array of two floating point numbers 
		representing coordinate in lat long reference system.
		Returns 
		An array of 3 floating point numbers containing the corresponding sinusoidal coords
		"""
		logging.info(callingFunc()[3] + f'( {latLong_point[0]} {latLong_point[1]} )')
		return cls.transform_LatLong2sin.TransformPoint(latLong_point[0], latLong_point[1])
	
