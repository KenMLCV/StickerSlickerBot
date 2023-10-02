
import pdb
from statistics import mode, StatisticsError
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
import copy
import traceback
  


#import CT_CFG as CFG
#import CT_FAO
#import CT_PP
#import CT_VIS
#import CT_UTIL
#import CT_ML
#import CT_IMP

#def telegram_bot(request):
#    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
#    if request.method == "POST":
#        update = telegram.Update.de_json(request.get_json(force=True), bot)
#        chat_id = update.message.chat.id
#        # Reply with the same message
#        bot.sendMessage(chat_id=chat_id, text=update.message.text)
#    return "okay"

#StickerSlickerBot:
#telegram_bot_token = "1943780316:AAEtF-qz5buAAuGj-SxQwwCUwalH5HBEaCs"
#https://api.telegram.org/bot1943780316:AAEtF-qz5buAAuGj-SxQwwCUwalH5HBEaCs/getMe

#StickerRefacerBot:
#telegram_bot_token = "2010641439:AAEJxTMXN74F_mjr1DsJncb52vmp9xMIpzU"
#https://api.telegram.org/bot2010641439:AAEJxTMXN74F_mjr1DsJncb52vmp9xMIpzU/getMe

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
            pass
            #extract_faces(None, '1', file_path)
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
def get_detect_preview(src_path=r'upload/file_28.jpg'):
        
    supported_image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    supported_video_extensions = ['.webp', '.mp4', '.gif']
    
    path, file_name = os.path.split(src_path)
    _, ext = os.path.splitext(src_path)
    
    frame=None
    if(ext in supported_image_extensions):
        frame = cv2.imread(src_path)
        cv2.imwrite(r'detect\{}'.format(file_name), frame)
    elif(ext in supported_video_extensions):
        vidcap = cv2.VideoCapture(src_path)
        success,frame = vidcap.read()
        cv2.imwrite(r'detect\{}'.format(file_name), frame)
        
    height, width, channels = frame.shape
    
    maxSize = (np.min((height, width)), np.min((height,width)))
    minSize = tuple(np.divide(maxSize,10).astype(int))
    scale_factor = 1.1
    #min_neighbors = range(3, 25, 2)
    flags = 0
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #face_classifier = cv2.CascadeClassifier(os.path.abspath(r'C:/Users/kjone/anaconda3/envs/py36/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml'))
    ''' Our classifier returns the ROI of the detected face as a tuple, 
    It stores the top left coordinate and the bottom right coordiantes'''
    roi_l_l = []
    min_neighbors = 3
    while(True):
        objects, rejectLevels, levelWeights = face_classifier.detectMultiScale3(gray, scale_factor, min_neighbors, flags, minSize, maxSize, True)
        if(len(objects) == 0):
            break
        roi_l_l.append(objects.tolist())
        min_neighbors = min_neighbors + 2
        #if (objects.shape[0] == score):
        #    print(score)
        #    break
        #else:
        #    score = objects.shape[0]
        #    print(score)
        
    #print(score)
    #if(mode(score)==0):
    #    return [], ''
    scores=[]
    roi_min=-1
    roi_max=-1
    roi_mode=-1
    for roi_idx, roi_l in enumerate(roi_l_l):
        scores.append(len(roi_l))
    roi_max = scores.index(max(scores))
    roi_min = scores.index(min(scores))
    try:
        roi_mode = scores.index(mode(scores))
    except:
        roi_mode = int(math.ceil((len(scores)/2.0)))
    roi_d = {}
    #roi_d['MAX'] = len(roi_l_l[roi_max]) > 10 ? roi_l_l[roi_max] : roi_l_l[roi_max]
    #roi_d['MODE'] = len(roi_l_l[roi_mode]) > 10 ? roi_l_l[roi_mode][:9] : roi_l_l[roi_mode]
    #roi_d['MIN'] = len(roi_l_l[roi_min]) > 10 ? roi_l_l[roi_min][:9] : roi_l_l[roi_min]
   
    roi_d['MAX'] = roi_l_l[roi_max]
    roi_d['MODE'] = roi_l_l[roi_mode]
    roi_d['MIN'] = roi_l_l[roi_min]
    
    if(len(roi_d['MAX']) > 10):
       roi_d['MAX'] = roi_l_l[roi_max][:11]
    if(len(roi_d['MODE']) > 10):
       roi_d['MODE'] = roi_l_l[roi_mode][:11]
    if(len(roi_d['MIN']) > 10):
       roi_d['MIN'] = roi_l_l[roi_min][:11]
       
    #roi_l, rejectLevels, levelWeights = face_classifier.detectMultiScale3(gray, scale_factor, mn, flags, minSize, maxSize, True)
    
    '''When no faces detected, face_classifier returns and empty tuple'''


    #if(objects is None):
    #    print("No faces found")
    '''We iterate through our faces array and draw a rectangle over each face in faces'''
    frame_detect_preview = np.copy(frame)
    roi_iterable = copy.deepcopy(roi_d['MAX'])
    for roi_idx, roi in enumerate(roi_iterable):
        x,y,w,h = tuple(roi)
        if(roi in roi_d['MAX']):
            cv2.rectangle(frame_detect_preview, (x,y), (x+w,y+h), (0,0,255), 10)
            i = roi_d['MAX'].index(roi)
            roi_d['MAX'][i].append(roi_idx)
            #i = np.where((roi_d['MAX'] == roi).all(axis=1))[0][0]
            #roi_d['MAX'][i] = np.append(roi_d['MAX'][i], roi_idx)
        if(roi in roi_d['MODE']):
            cv2.rectangle(frame_detect_preview, (x+10,y+10), (x+w,y+h), (0,255,0), 10)
            i = roi_d['MODE'].index(roi)
            roi_d['MODE'][i].append(roi_idx)
            #i = np.where((roi_d['MODE'] == roi).all(axis=1))[0][0]
            #np.append(roi_d['MODE'][i], roi_idx)
        if(roi in roi_d['MIN']):
            cv2.rectangle(frame_detect_preview, (x+20,y+20), (x+w,y+h), (255,0,0), 10)
            i = roi_d['MIN'].index(roi)
            roi_d['MIN'][i].append(roi_idx)
            #i = np.where((roi_d['MIN'] == roi).all(axis=1))[0][0]
            #np.append(roi_d['MIN'][i], roi_idx)
        
        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        #org = (int(max(x-10, 0)), int(max(y-10, 0)))
        #org = (int(x+w/2), int(y+h/2))
        org = (int(x+10), int(y+h-10))
        # fontScale
        fontScale = 2
        # Blue color in BGR
        #color = (255, 255, 255)
        # Line thickness of 2 px
        #thickness = 4
        # Using cv2.putText() method
        frame_detect_preview = cv2.putText(frame_detect_preview, str(roi_idx), org, font, 
                           fontScale, (255,255,255), 10, cv2.LINE_AA)
        frame_detect_preview = cv2.putText(frame_detect_preview, str(roi_idx), org, font, 
                           fontScale, (0,0,0), 5, cv2.LINE_AA)
    frame_detect_preview_path = 'detect/{}'.format(file_name)
    cv2.imwrite(frame_detect_preview_path, frame_detect_preview)
    return frame_detect_preview_path, roi_d
def get_modify_preview(src_path, roi_l, f_s_kwargs_d):
    
    supported_image_extensions = ['.jpg', '.jpeg', '.png']
    supported_video_extensions = ['.webp', '.mp4', '.gif']
    
    path, file_name = os.path.split(src_path)
    _, ext = os.path.splitext(src_path)
    
    frame = cv2.imread(src_path)
        
    height, width, channels = frame.shape
    
    #if(objects is None):
    #    print("No faces found")
    '''We iterate through our faces array and draw a rectangle over each face in faces'''
    modify_preview_frame = np.copy(frame)
    
    #data['face_idx_to_sticker_kwargs'][f_idx] = {'gcp_path':dst_name, 'local_path':local_path, 'scale':1.5, 'flip':False, 'rotation':0} 
    
    for roi in roi_l:
        if(roi[-1] in f_s_kwargs_d.keys()):
            
            x,y,w,h,roi_idx = copy.deepcopy(roi)
            f_s_kwargs = f_s_kwargs_d[roi_idx]
            x, y, w, h = scale_roi((x,y,w,h), f_s_kwargs['scale'])
            sticker = cv2.imread(f_s_kwargs['local_path'], cv2.IMREAD_UNCHANGED)
            if(f_s_kwargs['flip']):
                sticker = cv2.flip(sticker, 1)
            modify_preview_frame = overlay_sticker(modify_preview_frame, sticker, (x,y,w,h))
            
            
            for s in [1.0, 1.25, 1.5, 1.75, 2.0]:
                x,y,w,h,roi_idx = copy.deepcopy(roi)
                x, y, w, h = scale_roi((x,y,w,h), s)
                x, y, w, h = truncate_roi((x,y,w,h), modify_preview_frame.shape[:2])
                cv2.rectangle(modify_preview_frame, (x,y), (x+w,y+h), (0,0,255), 2)
            
            x,y,w,h,roi_idx = copy.deepcopy(roi)
            x, y, w, h = scale_roi((x,y,w,h), f_s_kwargs['scale'])
            x, y, w, h = truncate_roi((x,y,w,h), modify_preview_frame.shape[:2])
            cv2.rectangle(modify_preview_frame, (x,y), (x+w,y+h), (0,255,0), 2)
            
            x,y,w,h,roi_idx = copy.deepcopy(roi)
            # font
            font = cv2.FONT_HERSHEY_SIMPLEX
            # org
            org = (int(x+10), int(y+h-10))
            # fontScale
            fontScale = 2
            # Blue color in BGR
            #color = (255, 255, 255)
            # Line thickness of 2 px
            #thickness = 4
            # Using cv2.putText() method
            modify_preview_frame = cv2.putText(modify_preview_frame, str(roi_idx), org, font, 
                               fontScale, (255,255,255), 10, cv2.LINE_AA)
            modify_preview_frame = cv2.putText(modify_preview_frame, str(roi_idx), org, font, 
                               fontScale, (0,0,0), 5, cv2.LINE_AA)
            
    modify_preview_frame_path = 'modify/{}'.format(file_name)
    cv2.imwrite(modify_preview_frame_path, modify_preview_frame)
    return modify_preview_frame_path
def get_finalize_preview(src_path, roi_l, f_s_kwargs_d):
    
    supported_image_extensions = ['.jpg', '.jpeg', '.png']
    supported_video_extensions = ['.webp', '.mp4', '.gif']
    
    path, file_name = os.path.split(src_path)
    _, ext = os.path.splitext(src_path)
    
    frame = cv2.imread(src_path)
        
    height, width, channels = frame.shape
    
    #if(objects is None):
    #    print("No faces found")
    '''We iterate through our faces array and draw a rectangle over each face in faces'''
    modify_preview_frame = np.copy(frame)
    
    #data['face_idx_to_sticker_kwargs'][f_idx] = {'gcp_path':dst_name, 'local_path':local_path, 'scale':1.5, 'flip':False, 'rotation':0} 
    
    for roi in roi_l:
        if(roi[-1] in f_s_kwargs_d.keys()):
            
            x,y,w,h,roi_idx = copy.deepcopy(roi)
            f_s_kwargs = f_s_kwargs_d[roi_idx]
            x, y, w, h = scale_roi((x,y,w,h), f_s_kwargs['scale'])
            sticker = cv2.imread(f_s_kwargs['local_path'], cv2.IMREAD_UNCHANGED)
            if(f_s_kwargs['flip']):
                sticker = cv2.flip(sticker, 1)
            modify_preview_frame = overlay_sticker(modify_preview_frame, sticker, (x,y,w,h))
            
    modify_preview_frame_path = 'finalize/{}'.format(file_name)
    cv2.imwrite(modify_preview_frame_path, modify_preview_frame)
    return modify_preview_frame_path
def scale_roi(roi, scale):
    x, y, w, h = roi
    x_offset = (w*scale)-w
    y_offset = (h*scale)-h
    x = x-int(x_offset/2.0)
    y = y-int(y_offset/2.0)
    w = w*scale
    h = h*scale
    roi = [x,y,w,h]
    roi = [math.floor(i) for i in roi]
    return roi
def truncate_roi(roi, frame_shape):
    x, y, w, h = roi
    
    if(x<0):
        w = w + x
        x = 0
        
    if(y<0):
        h = h + y
        y = 0
    
    if(x+w > frame_shape[1]):
        w=frame_shape[1]-x
        
    if(y+h > frame_shape[0]):
        h=frame_shape[0]-y
        
    return [x,y,w,h]
    
def overlay_sticker(frame, sticker, roi):
    f_h, f_w = frame.shape[:2]
    r_x,r_y,r_w,r_h = roi[:4]
    
    
    if(sticker.shape[1] < sticker.shape[0]):
        sticker2roi_scale = float(r_w)/float(sticker.shape[1])
        s_w = r_w
        s_h = math.floor((sticker.shape[0]*sticker2roi_scale))
        s_x = r_x
        s_y = r_y - math.floor(((s_h-r_h)/2.0))
    else:
        sticker2roi_scale = float(r_h)/float(sticker.shape[0])
        s_h = r_h
        s_w = math.floor((sticker.shape[1]*sticker2roi_scale))
        s_y = r_y
        s_x = r_x - math.floor(((s_w-r_w)/2.0))
    
    resize = cv2.resize(sticker, (s_w,s_h), interpolation = cv2.INTER_AREA)
    
    #s_y, s_x = sticker.shape*sticker2roi_scale
        
    for o_x in range(resize.shape[0]):
        if(s_x+o_x > 0 and s_x+o_x < f_w):
            for o_y in range(resize.shape[1]):
                if(s_y+o_y > 0 and s_y+o_y < f_h):
                    try:
                        pixel = resize[o_y,o_x,:]
                        trans = pixel[3]
                        if(trans > 0):
                            trans = trans/255.0
                            #frame[y+i,x+j] = (1.0-trans)*frame[y+i,x+j] + trans*resize[i,j,:3]
                            frame[s_y+o_y,s_x+o_x] = trans*resize[o_y,o_x,:3]
                    except:
                        print("Sticker Overlay Error:", sys.exc_info()[0])
                        traceback.print_exc()
                        continue
    return frame
    #sticker2roi_scale = min(sticker.shape)/roi
    #if(np.all(sticker[:,:,3] == sticker[0,0,3])):
    #    for (x,y,w,h) in objects:
    #        resize = cv2.resize(sticker, (w,h))
    #        frame_out[y:y+h,x:x+w] = resize[:,:,:3]
    #else:
    #    for (x,y,w,h) in objects:
    #        resize = cv2.resize(sticker, (w,h))
            
    
                    
            #frame[y:y+h,x:x+w] = cv2.resize(sticker, (w,h))
            #cv2.imshow('Face Detection', resized)
            #cv2.waitKey(0)
            
    #cv2.imwrite(r'frames_out\{}'.format(file_name), frame_out)
        
    #cv2.destroyAllWindows()
    
"""
def get_detect_preview_2():
        
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
"""