# code to concatenate before and after images for input into the neural net
import csv
import glob
import os
from numpy import genfromtxt
import csv
import math
import cv2
from PIL import Image
import skimage
import skimage.io
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import string
import matplotlib.cm as cm
import ntpath
import random

#filename and associated label will be written to this CSV file:
newfile = 'alginate_autogenerated_annotations_.csv'
f = open(newfile, 'wb')
fw = csv.writer(f)
fw.writerow(['Image File Name', 'Label'])

#new images will be deposited in this folder:
foldername = "alginate_image_folder"
os.mkdir(foldername)

#annotations will be read from the following CSV files (to create one list of labels)
labels = []
csv_read_files =['alginate_manual_crop_annotations.csv']
for readFile in csv_read_files:
    lines = csv.reader(open(readFile, "rU"))
    lines = list(lines)
    for x in range(1, len(lines)): #skip titles row at index 0
        labels.append(lines[x][1])
    

for x in range(1,14):    #for each whole transfer image
    count_init = (x-1)*10
    print "\nnew set"
    BeforeName = 'alginate_pictures/' + str(z) +'A.bmp'
    AfterName = 'alginate_pictures/' + str(z) +'B.bmp'
    
    BefIm = cv2.imread(BeforeName, 0)
    AfIm = cv2.imread(AfterName, 0)
    
    [h, w] = BefIm.shape
    BefIm= BefIm[0:h-600, 400:w-200]
    AfIm = AfIm[0:h-600, 400:w-200]
#    cv2.imshow('Image', (cv2.resize(BefIm,(int(.4*(w-600)/2), int(.4*(h-600)/2)))))
#    cv2.waitKey()
#    cv2.imshow('Image', (cv2.resize(AfIm,(int(.4*(w-600)/2), int(.4*(h-600)/2)))))
#    cv2.waitKey()

    [h, w] = BefIm.shape
    #fourths
    BefIm_cut_1 = BefIm[0:int(h/2), 0:int(w/2)]
    BefIm_cut_2 = BefIm[0:int(h/2), int(w/2):w]
    BefIm_cut_3 = BefIm[int(h/2):h, 0:int(w/2)]
    BefIm_cut_4 = BefIm[int(h/2):h, int(w/2):w]
    #sixths
    BefIm_cut_5 = BefIm[0:int(h/2), 0:int(w/3)]
    BefIm_cut_6 = BefIm[0:int(h/2), int(w/3):int(2*w/3)]
    BefIm_cut_7 = BefIm[0:int(h/2), int(2*w/3):w]
    BefIm_cut_8 = BefIm[int(h/2):h, 0:int(w/3)]
    BefIm_cut_9 = BefIm[int(h/2):h, int(w/3):int(2*w/3)]
    BefIm_cut_10 = BefIm[int(h/2):h, int(2*w/3):w]
    
    before = [BefIm, BefIm_cut_1, BefIm_cut_2,BefIm_cut_3, BefIm_cut_4, BefIm_cut_5, BefIm_cut_6, BefIm_cut_7, BefIm_cut_8, BefIm_cut_9, BefIm_cut_10]
    #fourths
    AfIm_cut_1 = AfIm[0:int(h/2), 0:int(w/2)]
    AfIm_cut_2 = AfIm[0:int(h/2), int(w/2):w]
    AfIm_cut_3 = AfIm[int(h/2):h, 0:int(w/2)]
    AfIm_cut_4 = AfIm[int(h/2):h, int(w/2):w]
    #sixths
    AfIm_cut_5 = AfIm[0:int(h/2), 0:int(w/3)]
    AfIm_cut_6 = AfIm[0:int(h/2), int(w/3):int(2*w/3)]
    AfIm_cut_7 = AfIm[0:int(h/2), int(2*w/3):w]
    AfIm_cut_8 = AfIm[int(h/2):h, 0:int(w/3)]
    AfIm_cut_9 = AfIm[int(h/2):h, int(w/3):int(2*w/3)]
    AfIm_cut_10 = AfIm[int(h/2):h, int(2*w/3):w]
    after = [AfIm, AfIm_cut_1, AfIm_cut_2, AfIm_cut_3, AfIm_cut_4, AfIm_cut_5, AfIm_cut_6, AfIm_cut_7, AfIm_cut_8, AfIm_cut_9, AfIm_cut_10]
    

    count = count_init  #label = labels[count]
    label = labels[count]
    
    #pairs = [before picture, after picture, filename]
    pairs = [[before[0], after[0], "transfer_" + str(x)+ "positive_whole"]]
    
    print "normalizing all but the first (whole) image"
    for cut_num in range(1,len(before)):
        cut = before[cut_num]
        normalized_cut_b = (cut - float(cut.min())) * 255/float(cut.ptp())
        normalized_cut_b = np.uint8(normalized_cut_b)
        cut = after[cut_num]
        normalized_cut_a = (cut - float(cut.min())) * 255/float(cut.ptp())
        normalized_cut_a = np.uint8(normalized_cut_a)
        #name = positive/negative + transfer# + _normalizedcut + which cut it is
        pairs.append([normalized_cut_b,normalized_cut_a, labels[count] +"_normalizedcut"+str(cut_num)])
        count +=1
    count = count_init

    print "rotating images"
    for image_set in range(0,len(pairs)): #for every image (whole, fourths and sixths = 11 total)
        image_set = pairs[image_set]
        rotlables = ["90", "180", "270"]
        degrees = [90.0, 180.0, 270.0]
        for rotation in range(0,3): #0 = 90, 1 = 180, 2 = 270 (0 degrees is already in the list)
            name = image_set[2]+"_rot"+rotlables[rotation]
            bef_cut = np.rot90(np.asarray(image_set[0]),degrees[rotation])
            af_cut = np.rot90(np.asarray(image_set[1]),degrees[rotation])
            pairs.append([bef_cut, af_cut, name])
        count+=1
    print "mirroring images"
    for image_set in range(0,len(pairs)): #for every image (whole, fourths and sixths = 11 total)
        image_set = pairs[image_set]
        fliplabels = ["vertmirror", "horizmirror"]
        for flip_val in range(1,3): #1 = vertical flip; 2= horizontal flip
            name = image_set[2]+fliplabels[flip_val-1]
            pairs.append([cv2.flip(image_set[0],flip_val), cv2.flip(image_set[1],flip_val), name])
            
    #pairs = [whole, normalized fourths, normalized sixths,
    print "combining and saving images"
    for image_set in pairs:
        combined = np.hstack((image_set[0], image_set[1]))
        name = "transfer_"+ str(x) + "_" + image_set[2] + '_combined' + '.jpg'
        if "positive" in image_set[2]:
            cv2.imwrite(os.path.join(foldername, name), combined)
            fw.writerow([name, "positive"])
        else:
            cv2.imwrite(os.path.join(foldername, name), combined)            
            fw.writerow([name, "negative"])
        

f.close()