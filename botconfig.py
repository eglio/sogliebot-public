#login area clienti 3
# -*- coding: utf-8 -*-

#credenziali singolr - inutili
user1gb="NUM_TEL1" # sostituire con numero di telefono senza +39
password1gb="PASSWORD1" #sostituire con password

password7gb="Sicaca00" #password area clienti 3
user7gb="3913943100" #sostutuire con num di telefono

utentiList=["0123456789","9876543210"] #num telefono senza +39
passwordList=["password1","password2"] #plaintext password, oAuth non supportato

#token oauth Pushbullet
pb_token="token" #inutile, sostituito con pushpad 
pushpad_token = "token_pushpad" # sostiture con token oAuth pushpad

#sezione - altro
#percentuali rimanenti sotto quale avvisare
soglia1=15 
soglia2=8 
soglia3=3 

frequenza=15 #in minuti, indica la frequenza di controllo delle soglie, consigliata 10+
