# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 03:31:09 2021

@author: Kenyon
"""
import CONFIG
from google_images_search import GoogleImagesSearch

    
def downloadImages(n, path='frames_in'):
    # you can provide API key and CX using arguments,
    # or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
    gis = GoogleImagesSearch(CONFIG.gis['api_key'], CONFIG.gis['project_id'])
    
    # define search params:
    _search_params = {
        'q': 'presentation meeting room',
        'num': n,
        'safe': 'active',
        'fileType': 'jpg|gif|png',
        'imgType': 'photo',
        'imgSize': 'MEDIUM',
        'imgDominantColor': 'imgDominantColorUndefined',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
    }
    
    # search first, then download and resize afterwards:
    gis.search(search_params=_search_params)
    for image in gis.results():
        try:
            image.download(path)
            image.resize(200, 200)
        except Exception as e:
            print(e)