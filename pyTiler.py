# **************************************************************
#
#	v 1.2.0
#	Python image tiler for creating Google Street View tiles.
#
# **************************************************************


import os
import sys
from PIL import Image
import ntpath
import math
import tkinter as tk
from tkinter import filedialog

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#
#	Main thread starts here
#
root = tk.Tk()
root.withdraw()

while True:
	print("Please select the folder with images to be processed...")
	dir = filedialog.askdirectory(title="Please select the folder with images to be processed:")
	if len(dir) > 0:
		print("\nYou selected '%s'\n" %dir)
	#dir = input("Enter the relative path to the image directory: ")
	#dir = os.path.abspath(dir)
	if not os.path.exists(dir):
		if len(dir) > 0:
			print("	Path '%s' does not exist or is not accessible" %dir)
		else:
			print("	You did not select a path")
		retry = input("		Retry? Y/n  ")
		if retry == 'n' or retry == 'N':
			sys.exit()
	else:
		break

while True:
	mode = int(input("Please select how to run the tiler:\n\
	1. Full automatic (recommended):\n\
		Tiler will process each image for maximum quality and give output at the end\n\
	2. Prompt:\n\
		Image tiler will ask for settings confirmation for each image\n\
	3. One size:\n\
		Specify one setting to use for all images\n\n\
Enter 1, 2, or 3 now: "))
	if mode > 0 or mode < 4:
		break

if mode == 3:
	iTileWidth = int(input("Enter a width for each tile: "))
	iTileHeight = int(input("Enter a height for each tile (suggested: "+str(int(iTileWidth/2))+"px): "))
	
code = input("Generate data for processed images? Y/n\n")
if code == 'n' or code == 'N':
	bCode = False
else:
	bCode = True
	
ensure_dir(dir+"/tiles/")
	
if bCode:
	input("\nFor code generation to work, images to be processed should be given short, descriptive, lowercase, space-free names.\n\
	Example: 'meeting_room-1.jpg' or 'main_lobby.jpg'\n\n\
If your source image files are named, press enter to continue. Otherwise, please name them now.")
	
	htmlCode = 'This JavaScript function is used to return the correct image tile to Google Maps JavaScript API.  See their documentation for more details.\n\n\
	// Return a pano image given the panoID.\n\
	function getCustomPanoramaTileUrl(pano,zoom,tileX,tileY)\n\
	{\n\
		var path = "path/to/tiles/"+pano+"/zoom"+zoom+"/tile_"+tileY+_"+tileX+".JPEG";\n\
		console.log(path);\n\
		return path;\n\
	}\n\n\n'
	
	htmlCode += "The following code should be placed inside your getCustomPanorama(pano,zoom,tileX,tileY) { switch(pano) {  } } block:\n"

input("\nPress enter to begin processing all images in\n	" + dir + "\n")



for fileName in os.listdir(dir):
	currentFile = dir + "/" + fileName
	
	if os.path.isfile(currentFile):
		print("Opening:	", fileName)
	
		sName, sExt= os.path.splitext(fileName)

		try:
			im=Image.open(currentFile)
			print("Opened:		", currentFile)
			print("Details:	", im.format, im.size, im.mode, "\n\n")
			
			if not mode == 3:
				iTileWidth = math.floor(im.size[0] / 16) #Get 1/16th of the image pixel width rounded down (eg; 1047.59 = 1047.0)
				#print("iTileWidth = " + str(iTileWidth))
				iTempImageWidth = iTileWidth * 16 #Find a compatible image size: 1047*16 = 16752.0
				#print("iTempImageWidth = " + str(iTempImageWidth))
				
				percentWidth = (iTempImageWidth / float(im.size[0]))
				iTempImageHeight = int((float(im.size[1]) * float(percentWidth)))
				
				#im = im.resize((iTempImageWidth, iTempImageHeight), PIL.Image.ANTIALIAS)
				#im.save('resized_image.jpg')

				iTileHeight = iTempImageHeight // 16
				
				if mode == 2:
					sizeConfirm = input("Best tile size dimensions detected as: " + str(iTileWidth) + "x" + str(iTileHeight) + "px.  Confirm? Y/n")
					if sizeConfirm == "n" or sizeConfirm == "N":
						iTileWidth = int(input("Enter a width for each tile: "))
						iTileHeight = int(input("Enter a height for each tile (suggested: "+str(int(iTileWidth/2))+"px): "))
			
			if bCode:
				htmlCode += '\n\
case "{0}":\n\
	return {{\n\
		location:\n\
		{{\n\
			pano: "{0}",\n\
			//description: "description",\n\
			//latLng: new google.maps.LatLng(0, 0)\n\
		}},\n\
		// The text for the copyright control.\n\
		//copyright: "Imagery (c) Yourself",\n\
		// The definition of the tiles for this panorama.\n\
		tiles:\n\
		{{\n\
			tileSize: new google.maps.Size({1!s}, {2!s}),\n\
			worldSize: new google.maps.Size({3!s}, {4!s}),\n\
			// The heading at the origin of the panorama tile set.\n\
			centerHeading: 0, //adjust this\n\
			getTileUrl: getCustomPanoramaTileUrl\n\
		}}\n\
	}};\n\
break;\n\n'.format( sName, iTileWidth, iTileHeight, iTileWidth*16, iTileHeight*16 )
			
			#	Each zoom level requires four times the tiles of the previous zoom level.
			#	zoom 0 = 1 image
			#	zoom 1 = 4 images
			#	zoom 2 = 16 images
			#	etc
			
			#	The base panorama needs to be resized so that it can be cropped to fit the exact number of tiles required:
			for Zoom in range(0, 5):			
				rowsCols = int(math.pow(2, Zoom)) #The number of rows (and columns)
				
				iBaseWidth = rowsCols * iTileWidth
				iBaseHeight = rowsCols * iTileHeight
				tiles = rowsCols*rowsCols
					
				print("Resizing image to "+str(iBaseWidth)+"x" + str(iBaseHeight) + " to fit " + str(tiles) + " tiles")
				
				sizedImage = im.copy()
				
				# Resize the image
				sizedImage = sizedImage.resize((iBaseWidth,iBaseHeight), Image.ANTIALIAS)
				#sizedImage.thumbnail((iBaseWidth,iBaseHeight), Image.ANTIALIAS)
				# This is a proportional resize, so we should check to make sure the height is correct:
				
				#testfile = dir +"/"+ str(sName)+str(Zoom)+"."+im.format
				#sizedImage.save(testfile)
				
				iSizedHeight,iSizedWidth = sizedImage.size
				if iSizedWidth/2 != iSizedHeight:
					# The image needs to be padded, so we'll add black pixels to the bottom of the image:
					print("Padding image...")
					sizedImage = sizedImage.crop((0, 0, iBaseWidth, iBaseHeight))
					
				ImageWidth,ImageHeight = sizedImage.size
				print("Image sized to:	"+str(int(ImageWidth))+"x"+str(int(ImageHeight))+"px")
				
				totalColumns = rowsCols
				totalRows = rowsCols
				
				print("Cutting image into", totalRows, "rows,", totalColumns, "columns.", "\n	", int(totalRows*totalColumns), "Tiles @", iTileWidth, "px", "by", iTileHeight, "px", "\n")
				currentRow = 0
				currentColumn = 0
				
				ensure_dir(dir+"/tiles/"+str(sName)+"/zoom"+str(Zoom)+"/")
				while currentRow < totalRows:
					while currentColumn < totalColumns:
						#print("Exporting tile from", (currentColumn*iTileWidth), "to", ((currentColumn*iTileWidth)+iTileWidth), "(width) and", (currentRow*iTileHeight), "to", ((currentRow*iTileHeight)+iTileHeight), "(height)")
						
						box = (int(currentColumn*iTileWidth), int(currentRow*iTileHeight), int((currentColumn*iTileWidth)+iTileWidth), int((currentRow*iTileHeight)+iTileHeight))
						#print(box, "\n----\n")

						#tile = sizedImage.crop(box)
						tileFile = dir +  "/tiles/" + str(sName)+"/zoom"+str(Zoom)+"/tile_"+str(currentRow)+"_"+str(currentColumn)+"."+im.format
						#print ("Saving to:", tileFile)
						
						sizedImage.crop(box).save(tileFile) #Crop the image
						
						currentColumn += 1
					currentRow += 1
					currentColumn = 0
			
			
			
		except IOError as e:
			print("IOError: [",e.errno,"] ", e)
			input()
			
if bCode:
	if os.path.isfile(dir+"/tiles/"+"code.js"):
		os.remove(dir+"/tiles/"+"code.js") #Delete file if it exists
	htmlFile = open(dir+"/tiles/"+"code.js", "a")
	htmlFile.write(htmlCode)
	htmlFile.close()
