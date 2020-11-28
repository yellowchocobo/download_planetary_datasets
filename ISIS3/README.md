# ISIS3 commands
Documentation from https://isis.astrogeology.usgs.gov/
 
### lronac2isis
This program takes an image from the Lunar Reconnaissance Orbiter Narrow Angle Camera and produces an Isis cube containing the image data.
- Converts EDR to ISIS 3 cube file with attached label

### spiceinit
This program searches the ISIS data areas in order to discern the SPICE kernels required for the camera cube. Cubes which have supported 
camera models in the ISIS system require spacecraft position, pointing, body shape and orientation, sun position, and other information 
in order to compute ground positions (latitude/longitude) and photometric viewing angles. This information is stored in SPICE kernels.
- Update labels with camera pointing information using “spiceinit” and the system defaults
- Uses the default lunar shape model or DEM
- Level 0

### lronaccal
lronaccal performs radiometric corrections to images acquired by the Narrow Angle Camera aboard the Lunar Reconnaissance Orbiter spacecraft. 
The LRO NAC camera will make observations simulteously with the HiRise camera.

The LRO NAC detector has a total of 5064 pixels, divided among an A channel and a B channel. The pixels alternate between the two channels: 
ABABABAB, etc. Images from LROC NAC may or may not include all pixels in the acquired image. There are special summing modes that are 
utilized on-board the spacecraft to average detector pixels to combine them into a single output pixel value. The value of the ISIS label 
keyword, SpatialSumming, indicates the number of samples that were summed and averaged to result in the pixel values stored in the file. 
Note that this will reduce the number of samples in the output image by a factor of at most the SpatialSumming mode value.
- Calibrate image to convert to I/F values using “lronaccal”

### lronacecho
lronacecho implements a correction designed to remove an echo effect from LROC NAC images. In the summer of 2011, an echo effect was 
discovered in the NAC detectors. The signal in each pixel is replicated to a smaller extent in the pixel on the same line 2 columns over, 
1 collumn in summed NACs. MSSS was consulted and it was confirmed this is a detector effect related to the high speed (>3000 lines/second) 
of the NAC detectors. The even and odd columns of the detector have separate signal processing chains, so when one pixel is read out, the 
next pixel with the same signal processing chain is two columns over. There is no measurable effect 4 columns over; the echo has no echo.
- Remove artifacts using “lronacecho”
- A correction designed to remove an observed brightness “echo” across adjacent pixels in NAC frames
- Level 1 (calibrated data record, CDR)

### cam2map
This program projects an ISIS level0 or level1 cube to a map (ISIS level2 cube). The input cube requires SPICE data and therefore spiceinit 
should be executed prior to running cam2map. The map projection is defined using a PVL file which is specified in cam2map in the MAP 
parameter. Note: the system defaults to the Sinusoidal projection (ISIS projection based templates are located in 
$ISISROOT/appdata/templates/maps). To learn more about using map projections in ISIS, refer to the ISIS Workshop "Learning About Map Projections".
- Map-project image using “cam2map”
- There are interpolation options
- Level 2 (Reduced data record, RDR)

### stretch
This program stretchs or remaps pixels values in a cube. Note that the same stretch is applied to all bands within the cube. 
- Re-stretch the image (not sure if I should use this option, as it oftens results in the blooming of a large number of images).

### cubeatt
Copies the input cube to the output cube using the specified attributes.
I think it converts the image it a lower byte format (to limit the size of the image)
