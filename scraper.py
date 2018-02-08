import botconfig as cfg
import time
import sys
#from pushbullet import Pushbullet
from selenium import webdriver
import datetime
import pushpad
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

toggleswitch=0  #switcha numeri di telefono, 0=1gb 1=7gb

def login(id):
	drivers[id].get('https://areaclienti3.tre.it/133/controllo-costi.jsp')
	time.sleep(5)
	drivers[id].execute_script("document.getElementById('username1').value = '"+ cfg.utentiList[id] +"';")
	drivers[id].execute_script("document.getElementById('password1').value = '"+ cfg.passwordList[id] +"';")
	drivers[id].execute_script("sendForm();")
	time.sleep(2)
	
#if cfg.user is None or cfg.password is None  or cfg.pb_token is None or cfg.frequenza<1: #username e password da botconfig.py
#	print ("File di configurazione non valido!") #TODO: Wizard
#	sys.exit() #telegram handling


#preparo webdriver
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
drivers = [webdriver.PhantomJS(), webdriver.PhantomJS()] #TODO da PATH
drivers[0].set_window_size(1200,800)
drivers[1].set_window_size(1200,800)

login(0)
login(1)

#preparo pushpad
notificatore=pushpad.Pushpad(auth_token= cfg.pushpad_token, project_id=4128)


#matrice flag di soglia raggiunta: colonne=flag, righe=id cubo   [rig][col]
numeri = 2
numflag = 3

flags = [[False for j in range(numflag)] for i in range(numeri)]

last_push=[datetime.datetime.now(), datetime.datetime.now()]

while True:
	toggleswitch=0  #switcha numeri di telefono, 0=1gb 1=7gb
	today=datetime.datetime.now()
	if (last_push[toggleswitch] < today):
		flags[toggleswitch][0]= True
		flags[toggleswitch][1]= True
		flags[toggleswitch][2]= True
	
	drivers[toggleswitch].get('https://areaclienti3.tre.it/133/controllo-costi.jsp')
	time.sleep(5)
	try:
		rimanente = drivers[toggleswitch].find_element_by_css_selector("#color0 > div:nth-child(1)")
		value = rimanente.get_attribute('innerHTML')
		value = value[:-1]	
		value = value.replace(',', '.')
		print (value) #return?
		if ((float(value) < cfg.soglia3) and flags[toggleswitch][3]==false): 
			avvisa(value, toggleswitch)
			flags[toggleswitch][3]=true
			last_push[toggleswitch]=datetime.datetime.now()
		else:
			if ((float(value) < cfg.soglia2) and flags[toggleswitch][2] ==false): 
				avvisa(value, toggleswitch)
				flags[toggleswitch][2]=true
				last_push[toggleswitch]=datetime.datetime.now()
			else:
				if ((float(value) < cfg.soglia1) and flags[toggleswitch][1] ==false): 
					avvisa(value, toggleswitch)
					flags[toggleswitch][1]=true
					last_push[toggleswitch]=datetime.datetime.now()

	except:
		drivers[toggleswitch].save_screenshot('screen.png')
		with open("my_cool_picture.jpg", "rb") as pic:
			file_data = pb.upload_file(pic, "screen.png")
		#push = pb.push_file(**file_data)
		login(toggleswitch) # i cookie non erano validi, ripeto login
	
	toggleswitch = 1

	today=datetime.datetime.now()
	if (last_push[toggleswitch] < today):
		flags[toggleswitch][0]= True
		flags[toggleswitch][1]= True
		flags[toggleswitch][2]= True
	
	drivers[toggleswitch].get('https://areaclienti3.tre.it/133/controllo-costi.jsp')
	time.sleep(5)
	try:
		rimanente = drivers[toggleswitch].find_element_by_css_selector("#color0 > div:nth-child(1)")
		value = rimanente.get_attribute('innerHTML')
		value = value[:-1]	
		value = value.replace(',', '.')
		print (value) #return?
		if ((float(value) < cfg.soglia3) and flags[toggleswitch][3]==false): 
			avvisa(value, toggleswitch)
			flags[toggleswitch][3]=true
			last_push[toggleswitch]=datetime.datetime.now()
		else:
			if ((float(value) < cfg.soglia2) and flags[toggleswitch][2] ==false): 
				avvisa(value, toggleswitch)
				flags[toggleswitch][2]=true
				last_push[toggleswitch]=datetime.datetime.now()
			else:
				if ((float(value) < cfg.soglia1) and flags[toggleswitch][1] ==false): 
					avvisa(value, toggleswitch)
					flags[toggleswitch][1]=true
					last_push[toggleswitch]=datetime.datetime.now()

	except:
		drivers[toggleswitch].save_screenshot('screen.png')
		#with open("screen.png", "rb") as pic:
			#file_data = pb.upload_file(pic, "screen.png")
		#push = pb.push_file(**file_data)
		notificationerror = pushpad.Notification(
				notificatore,
				body="Errore! controlla lo screenshot", # max 120 characters
				title="AVVISO SOGLIE 3", # optional, defaults to your project name, max 30 characters
				#target_url="http://example.com",  # optional, defaults to your project website
				icon_url="http://www.freeiconspng.com/uploads/error-icon-32.png", # optional, defaults to the project icon
				#ttl=604800, # optional, drop the notification after this number of seconds if a device is offline
				require_interaction=True, # optional, prevent Chrome on desktop from automatically closing the notification after a few seconds
				image_url="screen.png", # optional, an image to display in the notification content
				starred=True # optional, bookmark the notification in the Pushpad dashboard (e.g. to highlight manual notifications
			)
		notificationerror.broadcast()
		login(toggleswitch) # i cookie non erano validi, ripeto login
	time.sleep(cfg.frequenza*60)

def avvisa(val, cubo):
			#pb = Pushbullet(cfg.pb_token)
			frase=["% al cubo da 1gb (rete 6052)", "% al cubo da 1gb (rete 43EE)"]
			#push = pb.push_note("SOGLIE TRE", "Attenzione! resta solo il "+val+frase[cubo])
			notification = pushpad.Notification(
				notificatore,
				body="Attenzione! resta solo il "+val+frase[cubo], # max 120 characters
				#title="Website Name", # optional, defaults to your project name, max 30 characters
				#target_url="http://example.com",  # optional, defaults to your project website
				#icon_url="http://example.com/assets/icon.png", # optional, defaults to the project icon
				#ttl=604800, # optional, drop the notification after this number of seconds if a device is offline
				require_interaction=True, # optional, prevent Chrome on desktop from automatically closing the notification after a few seconds
				#image_url="http://example.com/assets/image.png", # optional, an image to display in the notification content
				starred=False # optional, bookmark the notification in the Pushpad dashboard (e.g. to highlight manual notifications
			)
notification.broadcast()
