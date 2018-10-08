# **************************************************************
#
#	Python image tiler for creating Google Street View tiles.
#	written Caelan Borowiec 2013
#	Caelan.Borowiec@gmail.com
#
# **************************************************************


import os
from PIL import Image
import ntpath
import math

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

dir = input("Enter the relative path to the image directory: ")

iTileWidth = 256
iTileHeight = 128

googleCrop = input("Tiles for Google Streetview will be created from images in the current directory.\n\
Defaults:\n\
	Zoom levels 0-4.\n\
	Tile size "+str(iTileWidth)+"x"+str(iTileHeight)+"px.\n\
	Confirm? Y/n  ")
if "n" in googleCrop:
	iTileWidth = int(input("Enter a width for each tile: "))
	iTileHeight = int(input("Enter a height for each tile (suggested: "+str(int(iTileWidth/2))+"px): "))


ensure_dir(dir+"/tiles/")
#for x in range(0, 5):
#	ensure_dir(dir+"/tiles/zoom"+str(x)+"/")

input("\nPress any key to begin slicing all images in " + dir)

for fileName in os.listdir(dir):
	currentFile = dir + "\\" + fileName
	
	if os.path.isfile(currentFile):
		print("Opening:	", fileName)
		
		#temp = path_leaf(currentFile)
		fName, fExt= os.path.splitext(fileName)

		try:
			im=Image.open(currentFile)
			print("Opened:		", currentFile)
			print("Details:	", im.format, im.size, im.mode, "\n\n")
			
			#	Each zoom level requires four times the tiles of the previous zoom level.
			#	zoom 0 = 1 image
			#	zoom 1 = 4 images
			#	zoom 2 = 16 images
			#	etc
			
			#	The base panorama needs to be resized so that it can be cropped to fit the exact number of tiles required:
			for Zoom in range(0, 5):
				rowsCols = int(math.pow(2, Zoom))
				
				iBaseWidth = rowsCols * iTileWidth
				iBaseHeight = rowsCols * iTileHeight
				tiles = rowsCols*rowsCols
					
				print("Resizing image to "+str(iBaseWidth)+"x" + str(iBaseHeight) + " to fit " + str(tiles) + " tiles")
				
				sizedImage = im.copy()
				
				# Resize the image
				sizedImage.thumbnail((iBaseWidth,iBaseHeight), Image.ANTIALIAS)
				# This is a proportional resize, so we should check to make sure the height is correct:
				
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
				
				ensure_dir(dir+"/tiles/"+str(fileName)+"/zoom"+str(Zoom)+"/")
				while currentRow < totalRows:
					while currentColumn < totalColumns:
						#print("Exporting tile from", (currentColumn*iTileWidth), "to", ((currentColumn*iTileWidth)+iTileWidth), "(width) and", (currentRow*iTileHeight), "to", ((currentRow*iTileHeight)+iTileHeight), "(height)")
						
						box = (int(currentColumn*iTileWidth), int(currentRow*iTileHeight), int((currentColumn*iTileWidth)+iTileWidth), int((currentRow*iTileHeight)+iTileHeight))
						#print(box, "\n----\n")

						#tile = sizedImage.crop(box)
						tileFile = dir +  "/tiles/" + str(fileName)+"/zoom"+str(Zoom)+"/tile_"+str(currentRow)+"_"+str(currentColumn)+"."+im.format
						#print ("Saving to:", tileFile)
						
						sizedImage.crop(box).save(tileFile) #Crop the image
						
						currentColumn += 1
					currentRow += 1
					currentColumn = 0

			
		except IOError as e:
			print("IOError: [",e.errno,"] ", e)
			input()
