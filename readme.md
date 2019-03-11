# pyTiler batch image cutter

pyTiler is a lightweight application designed to perform recursive image tiling tasks for use with Google's custom [StreetView API](https://developers.google.com/maps/documentation/javascript/examples/streetview-custom-tiles).
**Features:** pyTiler accepts a directory path and will process the images inside according to options specified at runtime.  Each image will be sized, cut, and saved into the tiles needed for an Ultra-HD Google StreetView sphere.

##  Dependencies

 - [Python](https://www.python.org/downloads/)  version 3.*

## Usage

 1. Run the program (compiled exe or .py)
 2. Select the folder with images to be batch processed.
 3. Select a processing option for the images:
	 - *1: Automatic*, pyTiler will use highest quality mode.
	 - *2: Prompt*, pyTiler will ask what to do for each image.
	 - *3: One Size*, pyTiler will scale all images to the same size before tiling, making sure all tiles are the same size for the entire batch job.
4. **Generate data?** Enter "y" (default) here to generate the JavaScript code needed to use the image tiles with Google StreetView.
5. Review and accept the prompts.

## Demo

Turn an image [like this](https://drive.google.com/file/d/10bd4Bf_hfCPMQbdFS16OalKWX799y3Hb/view?usp=sharing), into a whole bunch of [tiles like this](https://drive.google.com/open?id=1Nst5U2rec6DJElyofijUIoJw5eXp8pFg).  You can then use those tiles to create a [streetview sphere like this](https://tours.pqi.org/machineshop/#main3,158.8,-5.3,0.0).
