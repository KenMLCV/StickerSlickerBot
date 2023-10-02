from telebot import TeleBot, types
import os
import storage
import urllib
import pickle
from functools import partial
import json
from pprint import pprint
from pprint import PrettyPrinter

#import asyncio
#import nest_asyncio
#nest_asyncio.apply()
#__import__('IPython').embed()

import SSB_STO, SSB_CV, CONFIG
from enum import Enum


import pdb
pdb.set_trace()

class States(Enum):
    BUSY = -1
    START = 0
    UPLOAD = 1
    DETECT = 2
    MATCH = 3
    MODIFY = 4
    FINALIZE = 5
    

SAVE_STATE = {States.BUSY:False, States.START:True, States.UPLOAD:True, States.DETECT:True, States.MATCH:True, States.MODIFY:True, States.FINALIZE:True}
bot = TeleBot(CONFIG.telegram['token'], skip_pending=True)
gcp_storage = SSB_STO.SSB_GCP_STO()

#INITIALIZE=True
USER_DATA = {}
supported_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.gif']
emoji_to_value_d = {'0⃣':0, '1⃣':1, '2⃣':2, '3⃣':3, '4⃣':4,' 5⃣':5, '6⃣':6, '7⃣':7, '8⃣':8, '9⃣':9,
                    '🟥':'MAX','🟩':'MODE','🟦':'MIN',
                    '⏫':'SCALE+','⏬':'SCALE-','↔':'FLIP'}
emoji_number_box_l = ['0⃣','1⃣','2⃣','3⃣','4⃣',' 5⃣', 
                      '6⃣','7⃣','8⃣','9⃣']
#def initialize():
#    pdb.set_trace()
#    updates = bot.get_updates()
#    uid_l = []
#    for update in updates:
#        uid = update.message.from_user.id
#        if(uid not in uid_l):
#            bot.send_message(chat_id=uid, text="re-initializing")
#            uid_l.append(uid)

def initialize(msg):
    #print('INIT')
    #msg = args
    user_id = msg.from_user.id
    if(not user_id in USER_DATA):
        USER_DATA[user_id] = {}
        data = USER_DATA[msg.from_user.id]
        data['user_id'] = msg.from_user.id
        data['chat_id'] = msg.chat.id
        data['file_id'] = False
        data['file_path'] = False
        data['gcp_src_path'] = False
        data['original_msg'] = False
        data['detect_msg'] = False
        data['preview_msg'] = False
        data['detect_faces'] = False
        data['match_faces'] = False
        data['message'] = False
        data['reply_message'] = False
        data['reply_preview'] = False
        data['save_states'] = SAVE_STATE
        data['sticker_file_id_to_path']={}
        data['face_idx_to_sticker_kwargs'] = {}
        data['state'] = States.START
        #print(USER_DATA.keys())
        #markup = types.ReplyKeyboardMarkup()
        #markup.add(types.KeyboardButton(text='share phone'))
        # ask for phone number
        #bot.send_message(chat_id=msg.from_user.id, text='share your phone number', reply_markup=markup)
        #removeKeyboard = {'remove_keyboard':True}
        #removeKeyboardEncoded = json.dumps(removeKeyboard)
        #urllib.request.urlopen("https://api.telegram.org/{}/sendmessage?chat_id={}&text={}&reply_markup=\"remove_keybaord\":true".format(CONFIG.telegram['token'], data['chat_id'], 'INITIALIZING')).read()
        #bot.sendMessage(msg.chat.id, 'Initializing.', { replyMarkup: 'hide' });
        markup = types.ReplyKeyboardHide(selective=False)
        types.ReplyKeyboardHide()
        bot.send_message(msg.chat.id, 'Ready.', reply_markup=markup)
def save_state(msg):
    #print('SAVE')
    user_id = msg.from_user.id
    data = USER_DATA[user_id]
    #print(USER_DATA[user_id])
    data['message'] = msg
    state_enum = USER_DATA[user_id]['state']
    if(data['save_states'][state_enum]):
        data['save_states'][state_enum] = False
        with open('state/{}_{}_{}.pickle'.format(user_id, state_enum.name, state_enum.value), 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
    
def load_state(state_file_name):
    with open('state/{}'.format(state_file_name), "rb") as file:
        data = pickle.load(file)
    #USER_DATA[data['user_id']]=data
    return data
def replay(state_file_name):
    #pdb.set_trace()
    state_path, file_name = os.path.split(state_file_name)
    file_name, ext = os.path.splitext(file_name)
    user_id, state_name, state_value = file_name.split("_", 3)
    data = load_state(state_file_name)
    msg = data['message']
    user_id = data['user_id']
    USER_DATA[user_id] = data
    
    markup = types.ReplyKeyboardHide(selective=False)
    types.ReplyKeyboardHide()
    bot.send_message(msg.chat.id, 'REPLAY - {}'.format(state_name), reply_markup=markup)
    
    pipeline_functions = [partial(start, msg), partial(upload, msg), partial(detect, msg),
              partial(match, msg), partial(modify, msg), partial(finalize, msg)]
    pipeline_functions[int(state_value)]()
    
"""
def update_reply_message():
    pass
def update_reply_preview():
    pass
def update_reply_keyboard(buttons, row_width, state):
    USER_DATA[user_id] = {}
    data = USER_DATA[user_id]
    data['state'] = state
    #if(state == States.DETECT)
    markup = types.ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True, row_width=row_width)
    #bot.send_message(data['user_id'], text=text, reply_markup=markup)
"""

#@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.START)
@bot.message_handler(commands=['reface'])
#@bot.message_handler(func=save_state)
#@bot.message_handler(func=initialize)
#@save_state
#@initialize
#@bot.message_handler(func=initialize)
def start(msg):
    pprint('START')
    pprint(vars(msg))
    initialize(msg)
    save_state(msg)
    pprint(USER_DATA[msg.from_user.id])
    # clear user reservation data
    #pdb.set_trace()
    # ask for date
    #data = USER_DATA[user_id]
    #data['user_id'] = user_id
    reply_msg = bot.reply_to(msg, text='Upload a PNG/JIF/GIF/MP4 . . . ')
    # new line
    USER_DATA[msg.from_user.id]['state'] = States.UPLOAD

#@bot.message_handler(content_types=['document', 'photo']) 
@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.UPLOAD, content_types=['document', 'photo'])
def upload(msg):
    pprint('UPLOAD')
    pprint(vars(msg))
    #pdb.set_trace()
    save_state(msg)
    #print("UPLOAD {}".format(msg.from_user.id))
    # get user data
    data = USER_DATA[msg.from_user.id]
    if(msg.content_type == 'photo'):
        data['file_id'] = msg.photo[-1].file_id
        #CHECK IF FILE TS_TRK.pkl EXISTS IN STORAGE
        #ba = bot.download_as_bytearray()
        d = bot.get_file(data['file_id'])
        data['file_path'] = d.file_path
    elif(msg.content_type == 'document'):
        data['file_id'] = msg.document.file_id
        #CHECK IF FILE TS_TRK.pkl EXISTS IN STORAGE
        #ba = bot.download_as_bytearray()
        d = bot.get_file(msg.document.file_id)
        data['file_path'] = d.file_path
    file_path, file_name = os.path.split(data['file_path'])
    _, ext = os.path.splitext(data['file_path'])
    
    #if supported store in GCP bucket.
    if(ext in supported_extensions):
        bot.reply_to(msg, text='🖼...⏳')
        download_link = CONFIG.telegram['download_link'].format(CONFIG.telegram["token"], file_path)
        download_link = "{}/{}".format(download_link, file_name)
        local_path = "upload/{}".format(file_name)
        data['local_file_path'] = local_path
        urllib.request.urlretrieve(download_link, local_path)
        #bot.download(download_link)
        dst_name = r'{}{}'.format(data['file_id'],ext)
        uploaded = gcp_storage.upload_blob(local_path, dst_name)
        if(uploaded):
            data['gcp_src_path'] = dst_name
            #detect(msg)
            #bot.edit_message_text('🖼...✔', reply_msg.chat.id, reply_msg.message_id)
            bot.reply_to(msg, text='⌛...✔')
            USER_DATA[msg.from_user.id]['state'] = States.DETECT
            msg.text = 'DETECT'
            msg.content_type='text'
            detect(msg)
            #markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            #markup.add(types.KeyboardButton(text='DETECT'))
            #bot.send_message(chat_id = data['user_id'], text='Continue . . . ?', reply_markup=markup)
            #print(USER_DATA[msg.from_user.id])
            #detect(msg)
        else:
            bot.reply_to(msg, text='⌛...❌')
    else:
        bot.reply_to(msg, text='🖼...❌')
    #https://api.telegram.org/file/bot1234:abcd/photos/file_name.jpg
    #if msg.document.mime_type == "video/mp4":
    #   bot.get_file(file_id).download(path)
    # file = update.message.photo[0].file_id
    # obj = context.bot.get_file(file)
    # obj.download()
    
    #data['visual'] = msg.text
    # update storage
    #USER_DATA[msg.from_user.id] = data
    # ask about persons count
    #bot.reply_to(msg, text='how manytype persons?')
    # new line
    #storage.set_user_state(msg.from_user.id, States.WAIT_PERSONS_COUNT)
    
#@bot.message_handler(content_types=['text']) 
@bot.message_handler(func=lambda msg: msg.text in ['DETECT','🟥','🟩','🟦'] and USER_DATA[msg.from_user.id]['state'] == States.DETECT)
#@bot.message_handler(func=save_state)
#@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.DETECT)
def detect(msg):
    pprint('DETECT')
    pprint(vars(msg))
    #pdb.set_trace()
    data = USER_DATA[msg.from_user.id]
    if(msg.text in ['DETECT']):
        save_state(msg)
        data['detect_type'] = 'MODE'
        bot.reply_to(msg, text='😉...⏳')
        #pdb.set_trace()
        #if(msg.text == 'NEXT'):
        local_path = data['local_file_path']
        #success = gcp_storage.download_blob(data['gcp_src_path'], dst_name)
        preview_path, faces = SSB_CV.get_detect_preview(local_path)
        #detect_preview_msg = bot.send_photo(msg.from_user.id, SSB_STO.get_file_link(preview_path))
       
        #update = bot.send_photo(msg.from_user.id, SSB_STO.get_file_link(data))
        #data['detect_preview_msg'] = detect_preview_msg
        #data['match_preview_msg'] = False
        #data['match_faces'] = faces
        
        if(len(faces['MAX']) > 0):
            bot.reply_to(msg, text='⌛...✔')
            data['faces'] = faces
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
            markup.add('🟥','🟩','🟦')
            #for e in ['🟥','🟩','🟦']:
            #    markup.add(types.KeyboardButton(text=e))
            data['reply_message'] = bot.send_photo(msg.from_user.id, photo=open(preview_path, 'rb'), caption='SELECT FACES BY BOX COLOR (R, G, B)', reply_markup=markup)
            
            #markup.add(types.KeyboardButton(text='MAX'))
            #markup.add(types.KeyboardButton(text='MODE'))
            #markup.add(types.KeyboardButton(text='MIN'))
            #USER_DATA[msg.from_user.id]['state'] = States.MATCH
            """
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='ONE2ALL'))
            markup.add(types.InlineKeyboardButton(text='ONE2ONE'))
            markup.add(types.InlineKeyboardButton(text='RANDOM'))
            bot.send_message(chat_id=msg.from_user.id, text="Select Match Mode.", reply_markup=markup)
            USER_DATA[msg.from_user.id]['state'] = States.MATCH
            """
        else:
            bot.send_message(chat_id=msg.from_user.id, text="⌛...❌", reply_markup=markup)

    if(msg.text in ['🟥','🟩','🟦']):
            data['detect_type'] = emoji_to_value_d[msg.text]
            USER_DATA[msg.from_user.id]['state'] = States.MATCH
            #markup = types.ReplyKeyboardMarkup(['MATCH'], resize_keyboard=True, one_time_keyboard=True, row_width=1)
            #bot.send_message(data['user_id'], reply_markup=markup)
            msg.text = 'MATCH'
            msg.content_type='text'
            match(msg)
        
    #for s_idx, s in enumerate(scores):
    #    markup.add(types.InlineKeyboardButton(text=str(s)))
    #bot.send_message(chat_id=msg.from_user.id, text="Choose the option which includes all the faces you'd like to stickerize.", reply_markup=markup)
    #storage.set_user_state(msg.from_user.id, States.MATCH_STICKERS)

@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.MATCH, content_types=['text', 'sticker'])
#@bot.message_handler(func=save_state)
#@bot.message_handler(content_types=['text', 'sticker']) 
#@bot.message_handler(msg.text in ) 
#@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.MATCH and msg.content_type in ['text', 'sticker'])
#@bot.message_handler(func=lambda msg: (USER_DATA[msg.from_user.id]['state'] == States.MATCH and (msg.content_type=='text' and msg.text == 'MATCH' or msg.text in [emoji_to_value_d[msg.text] in USER_DATA[msg.from_user.id]['faces'].keys()]) or msg.content_type=='sticker'))
def match(msg):
    pprint('MATCH')
    pprint(vars(msg))
    pprint((USER_DATA[msg.from_user.id]['state']))
    #print(msg.content_type, msg.text)
    #pdb.set_trace()
    data = USER_DATA[msg.from_user.id]
    
    if(msg.content_type == 'text' and msg.text == 'MATCH'):
        save_state(msg)
        data['cur_faces'] = data['faces'][data['detect_type']]
        data = USER_DATA[msg.from_user.id]
        
        bot.send_message(data['user_id'], text='Please upload a sticker.')
        
    if(msg.content_type=='sticker'):
        data['sticker_id'] = msg.sticker.file_id
        data['sticker_msg'] = msg
        bot.reply_to(msg, text='🆒...⏳')
        d = bot.get_file(msg.sticker.file_id)
        file_path, file_name = os.path.split(d.file_path)
        #bot.reply_to(msg, text='Uploading . . .')
        download_link = CONFIG.telegram['download_link'].format(CONFIG.telegram["token"], file_path)
        download_link = "{}/{}".format(download_link, file_name)
        local_path = "upload/{}".format(file_name)
        data['sticker_local_path'] = local_path
        #data['local_file_path'] = local_path
        urllib.request.urlretrieve(download_link, local_path)
        #bot.download(download_link)
        dst_name = file_name
        uploaded = gcp_storage.upload_blob(local_path, dst_name)
        if(uploaded):
            bot.reply_to(msg, text='⌛...✔')
            data['sticker_gcp_path'] = dst_name
            #f_idx = data['cur_face']
            #data['face_idx_to_sticker_kwargs'][f_idx] = {'gcp_path':dst_name, 'local_path':local_path, 'scale':1.5, 'flip':False, 'rotation':0} 
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=len(data['cur_faces']))
            buttons = []
            for f in data['cur_faces']:
                buttons.append(types.KeyboardButton(text=emoji_number_box_l[f[-1]]))
            markup.add(*buttons)
            #markup.add('NEXT', 'CANCEL')
            #markup.add(types.KeyboardButton(text='CANCEL'))
            bot.reply_to(data['sticker_msg'], text="Select faces to match or upload a new sticker.", reply_markup=markup)
    
    if (msg.content_type=='text' and msg.text in emoji_number_box_l ): #emoji_to_value_d[msg.text] in USER_DATA[msg.from_user.id]['cur_faces'].keys()
            data['face_idx_to_sticker_kwargs'][emoji_to_value_d[msg.text]] = {'gcp_path':data['sticker_gcp_path'], 'local_path':data['sticker_local_path'], 'scale':1.5, 'flip':False, 'rotation':0} 
            bot.reply_to(data['sticker_msg'], text='{}...✔'.format(emoji_number_box_l[emoji_to_value_d[msg.text]]))
            #pprint(vars(data['face_idx_to_sticker_kwargs']))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=len(data['cur_faces']))
            buttons = []
            for f in data['cur_faces']:
                buttons.append(types.KeyboardButton(text=emoji_number_box_l[f[-1]]))
            buttons.append(types.KeyboardButton(text='DONE'))
            markup.add(*buttons)
            #markup.add(types.KeyboardButton(text='CANCEL'))
            bot.reply_to(data['sticker_msg'], text="Select faces to match or upload a new sticker.", reply_markup=markup)
        #data['cur_face'] = int(msg.text)
        #bot.send_message(msg.from_user.id, text='Upload a sticker for face #{}'.format(msg.text))
        #return
        #preview = data['detect_preview_msg']
    
    if(msg.text=='DONE'):
        USER_DATA[msg.from_user.id]['state'] = States.MODIFY
        msg.text='MODIFY'
        modify(msg)
        #markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        #markup.add('MODIFY')
    
#@bot.message_handler(func=save_state)
#@bot.message_handler(content_types=['text']) 
@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.MODIFY, content_types=['text'])
def modify(msg):
    #pdb.set_trace()
    pprint('MODIFY')
    #pprint( USER_DATA[msg.from_user.id])
    pprint(vars(msg))
    #pprint(msg.text[-1] in ['⏫','⏬','↔'])
    data = USER_DATA[msg.from_user.id]
    #def fetch(msg):
    #    faces = data['cur_faces']
    #    local_path = data['local_file_path']
    #    success = gcp_storage.download_blob(data['gcp_src_path'], data['local_file_path'])
    def preview(msg, data):
        f_s_kwargs_d = data['face_idx_to_sticker_kwargs']
        preview_path = SSB_CV.get_modify_preview(data['local_file_path'], data['cur_faces'], data['face_idx_to_sticker_kwargs'])
        bot.send_photo(msg.from_user.id, photo=open(preview_path, 'rb'))
        """
        if(data['reply_preview']):
            #file_path = bot.get_file(data['reply_message'].photo.file_id)
            #bot.send_message(msg.chat.id, 'Hello World')
            #bot.delete_message(msg.chat.id, msg.message_id)
            #bot.edit_message_media(chat_id=data['reply_message'].chat.id, message_id=data['reply_message'].message_id, media=types.InputMediaPhoto(data['reply_message'].photo.file_id))
            data['reply_preview']=bot.send_photo(msg.from_user.id, photo=open(preview_path, 'rb'))
        else:
            data['reply_preview']=bot.send_photo(msg.from_user.id, photo=open(preview_path, 'rb'))
       """
    def reply(msg, data):
        if(not data['reply_message']):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            for key in data['face_idx_to_sticker_kwargs']:
                buttons=[]
                #print(key)
                buttons.append(types.KeyboardButton(text='{}...⏫'.format(emoji_number_box_l[key])))
                buttons.append(types.KeyboardButton(text='{}...⏬'.format(emoji_number_box_l[key])))
                buttons.append(types.KeyboardButton(text='{}...↔'.format(emoji_number_box_l[key])))
                markup.add(*buttons)
                
            buttons=[]
            buttons.append(types.KeyboardButton(text='PREVIEW'))
            buttons.append(types.KeyboardButton(text='DONE'))
            buttons.append(types.KeyboardButton(text='CANCEL'))
            markup.add(*buttons)
            bot.send_message(msg.from_user.id, 'Modify sticker placement or click DONE.', reply_markup=markup)
            data['reply_message'] = bot.send_message(msg.from_user.id, PrettyPrinter().pformat(data['face_idx_to_sticker_kwargs']))
        else:
            data['reply_message'] = bot.edit_message_text(PrettyPrinter().pformat(data['face_idx_to_sticker_kwargs']), data['reply_message'].chat.id, data['reply_message'].message_id)
    #pdb.set_trace()
    if(msg.text == 'MODIFY'):
        data['reply_message'] = False
        save_state(msg)
        #fetch(msg)
        preview(msg, data)
        reply(msg, data)
    elif(msg.text[-1] in ['⏫','⏬','↔']):
        f_idx = int(msg.text[0])
        f_s_kwargs = data['face_idx_to_sticker_kwargs'][f_idx]
        
        if(msg.text[-1]=='⏫'):
            f_s_kwargs['scale'] = f_s_kwargs['scale']+0.25
        elif(msg.text[-1]=='⏬'):
            f_s_kwargs['scale'] = f_s_kwargs['scale']-0.25
        elif(msg.text[-1]=='↔'):
            f_s_kwargs['flip'] = not f_s_kwargs['flip']
        reply(msg, data)
    elif(msg.text in ['PREVIEW']):
        preview(msg,data)
    elif(msg.text in ['DONE']):
        USER_DATA[msg.from_user.id]['state'] = States.FINALIZE
        finalize(msg)
        
        
#@bot.message_handler(content_types=['text']) 
#@bot.message_handler(func=save_state)
#@bot.message_handler(func=lambda msg: USER_DATA[msg.from_user.id]['state'] == States.FINALIZE)
def finalize(msg):
    
    pprint('FINALIZE')
    pprint(vars(msg))
    data = USER_DATA[msg.from_user.id]
    f_s_kwargs_d = data['face_idx_to_sticker_kwargs']
    preview_path = SSB_CV.get_finalize_preview(data['local_file_path'], data['cur_faces'], data['face_idx_to_sticker_kwargs'])
    bot.send_photo(msg.from_user.id, photo=open(preview_path, 'rb'))
    
    markup = types.ReplyKeyboardHide(selective=False)
    types.ReplyKeyboardHide()
    bot.send_message(msg.chat.id, 'ReFace Complete.', reply_markup=markup)
    del USER_DATA[msg.from_user.id]
        

#replay("1082583031_MODIFY_4.pickle")
bot.polling(none_stop=True)
