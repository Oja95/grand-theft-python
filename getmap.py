from PIL import Image
im = Image.open('map.tiff', 'r')
width, height = im.size
pixel_values = list(im.getdata())
newfile = open("maptxt.txt", "w")
for i in range(640*400):
    for j in range(3):
        newfile.write(str(pixel_values[i][j]))
        newfile.write(" ")
    newfile.write("\n")
