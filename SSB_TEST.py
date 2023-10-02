import telegram

import pdb
from statistics import mode
import time
import glob
import math
import pdb
import re
import os
import sys
import pdb
import random
import operator
import numpy as np
from PIL import Image
import cv2
import pickle
import numpy.ma as ma
import itertools
import pandas as pd

import traceback
  


#import CT_CFG as CFG
#import CT_FAO
#import CT_PP
#import CT_VIS
#import CT_UTIL
#import CT_ML
#import CT_IMP

def telegram_bot(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        # Reply with the same message
        bot.sendMessage(chat_id=chat_id, text=update.message.text)
    return "okay"

#StickerSlickerBot:
#telegram_bot_token = "1943780316:AAEtF-qz5buAAuGj-SxQwwCUwalH5HBEaCs"
#https://api.telegram.org/bot1943780316:AAEtF-qz5buAAuGj-SxQwwCUwalH5HBEaCs/getMe

#StickerRefacerBot:
#telegram_bot_token = "2010641439:AAEJxTMXN74F_mjr1DsJncb52vmp9xMIpzU"

#StickerReAnimatorBot:
#telegram_bot_token = "1980494163:AAFMzZKMCerEXPEL5Dd_pL_O7fQCBeS159E"
def process_dir(request=None, target_dir=''):
    
    pdb.set_trace()
    
    dir_name = r'.\src\\'
    # Get list of all files only in the given directory
    list_of_files = filter( os.path.isfile,
                            glob.glob(dir_name + '*') )
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted( list_of_files,
                            key = os.path.getmtime)
    # Iterate over sorted list of files and print file path 
    # along with last modification time of file 
    for file_path in list_of_files:
        print(file_path)
        
        try:
            extract_faces(None, '1', file_path)
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError as err:
            print("ValueError: {0}".format(err))
        except AttributeError as err:
            print("AttributeError: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()
        #raise
def extract_faces(request=None, jid='1', target_dir=''):
        
    #pdb.set_trace()
    
    supported_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.gif']
    
    if(not target_dir):
        target_dir = r'.\src\{}.jpg'.format(jid)
    path, file_name = os.path.split(target_dir)
    _, ext = os.path.splitext(target_dir)
    
    frame=None
    if(ext in supported_extensions):
        frame = cv2.imread(target_dir)
        cv2.imwrite(r'frames_in\{}'.format(file_name), frame)
    elif(ext in supported_extensions):
        vidcap = cv2.VideoCapture(target_dir)
        success,frame = vidcap.read()
        cv2.imwrite(r'frames_in\{}'.format(file_name), frame)
        
    height, width, channels = frame.shape
    
    maxSize = (np.min((height, width)), np.min((height,width)))
    minSize = tuple(np.divide(maxSize,10).astype(int))
    scale_factor = 1.1
    min_neighbors = range(3, 15, 2)
    flags = 0
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    ''' Our classifier returns the ROI of the detected face as a tuple, 
    It stores the top left coordinate and the bottom right coordiantes'''
    score = []
    for mn in min_neighbors:
        objects, rejectLevels, levelWeights = face_classifier.detectMultiScale3(gray, scale_factor, mn, flags, minSize, maxSize, True)
        #if (objects.shape[0] == score):
        #    print(score)
        #    break
        #else:
        #    score = objects.shape[0]
        #    print(score)
        score.append(len(objects))
        
    print(score)
    if(mode(score)==0):
        raise ValueError
    mn = min_neighbors[score.index(mode(score))]
    objects, rejectLevels, levelWeights = face_classifier.detectMultiScale3(gray, scale_factor, mn, flags, minSize, maxSize, True)
    
    '''When no faces detected, face_classifier returns and empty tuple'''


    if(objects is None):
        print("No faces found")
    '''We iterate through our faces array and draw a rectangle over each face in faces'''
    frame_detect = np.copy(frame)
    for o,lw in zip(objects,levelWeights):
        lw = str(int(lw))
        x,y,w,h = tuple(o)
        cv2.rectangle(frame_detect, (x,y), (x+w,y+h), (0,0,255), 2)
        
        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (int(x+(w/2)), int(y+(h/2)))
        # fontScale
        fontScale = 1
        # Blue color in BGR
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        # Using cv2.putText() method
        frame_detect = cv2.putText(frame_detect, lw, org, font, 
                           fontScale, color, thickness, cv2.LINE_AA)
        
    cv2.imwrite(r'frames_detect\{}'.format(file_name), frame_detect)
        
        
    #objects = np.hstack((objects, np.sum(objects[:,2:4], axis=1).reshape(-1,1)))
    objects = objects[objects[:,3].argsort()]
    frame_out = np.copy(frame)
    
    sticker = cv2.imread(r'.\stickers\{}.webp'.format(jid), cv2.IMREAD_UNCHANGED)
    
    #if(True):
    if(np.all(sticker[:,:,3] == sticker[0,0,3])):
        for (x,y,w,h) in objects:
            resize = cv2.resize(sticker, (w,h))
            frame_out[y:y+h,x:x+w] = resize[:,:,:3]
    else:
        for (x,y,w,h) in objects:
            resize = cv2.resize(sticker, (w,h))
            
            for i in range(resize.shape[0]):
                for j in range(resize.shape[1]):
                    pixel = resize[i,j,:]
                    trans = pixel[3]
                    trans = trans/255.0
                    if(trans > 0):
                        #frame[y+i,x+j] = (1.0-trans)*frame[y+i,x+j] + trans*resize[i,j,:3]
                        frame_out[y+i,x+j] = trans*resize[i,j,:3]
    
                    
            #frame[y:y+h,x:x+w] = cv2.resize(sticker, (w,h))
            #cv2.imshow('Face Detection', resized)
            #cv2.waitKey(0)
            
    cv2.imwrite(r'frames_out\{}'.format(file_name), frame_out)
        
    #cv2.destroyAllWindows()
    
    