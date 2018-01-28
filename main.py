import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
from time import *

# BOITES

boites_modif = False
dict_boites = {}
with open('boites', 'rb') as monFichier:
    monDepickler = pickle.Unpickler(monFichier)
    try:
        dict_boites = monDepickler.load()
    except:
        pass

names_boites = ' - '.join(dict_boites)
answer = str()
while answer != 'o' and answer != 'n':
    answer = input('Voulez-vous utiliser une de ces boites mails ? [o/n]\n{}\n'.format(names_boites)).lower()
if answer == 'o':
    while answer not in dict_boites.keys():
        answer = input('Laquelle ? ')
    userlogin = dict_boites[answer][0]
    userpwd = dict_boites[answer][1]
else:
    userlogin = input("Login : ")
    userpwd = input("Password : ")

is_inside = False
for elt in list(dict_boites.items()):
    if elt[1][0] == userlogin:
        is_inside = True

answer = str()
if is_inside is False:
    while answer != 'o' and answer != 'n':
        answer = input('Voulez-vous ajouter cette boite mail ? [o/n]').lower()
    if answer == 'o':
        boites_modif = True
        new_boite = input('Nommez cette boite : ')
        dict_boites[new_boite] = userlogin, userpwd

if boites_modif is True:
    with open('boites', 'wb') as monFichier:
        monPickler = pickle.Pickler(monFichier)
        monPickler.dump(dict_boites)

# DESTINATAIRE

recipient_modif = False # Booléen pour savoir si les contacts ont été modifiés
dict_recipient = {}
with open('contacts', 'rb') as monFichier:
    monDepickler = pickle.Unpickler(monFichier)
    try:
        dict_recipient = monDepickler.load()
    except:
        pass

names_recipients = ' - '.join(dict_recipient)
answer = str()
recipient = str()
while answer != 'o' and answer != 'n':
    answer = input('Voulez-vous envoyer un mail à un de ces contacts ? [o/n]\n{}\n'.format(names_recipients)).lower() #VERFIER SI LE DICT EST VIDE
if answer == 'o':
    while answer not in dict_recipient.keys():
       answer = input('Lequel ? ')
    recipient = dict_recipient[answer]
else:
    recipient = input("Entrez l'adresse mail du destinataire : ")

answer = str()
if recipient not in dict_recipient.values():
    while answer != 'o' and answer != 'n':
        answer = input('Voulez vous ajouter ce contact ? [o/n] : ').lower()
    if answer == 'o':
        recipient_modif = True
        name = input('Nommez ce contact : ')
        dict_recipient[name] = recipient
else:
    for i in list(dict_recipient.items()):
        if i[1] is recipient:
            print('Vous contactez {}'.format(i[0]))

if recipient_modif is True:
    with open('contacts', 'wb') as monFichier:
        monPickler = pickle.Pickler(monFichier)
        monPickler.dump(dict_recipient)

# TEMPLATES

templates_modif = False
dict_templates = {}
with open('templates', 'rb') as monFichier:
    monDepickler = pickle.Unpickler(monFichier)
    try:
        dict_templates = monDepickler.load()
    except:
        pass

names_templates = ' - '.join(dict_templates)
answer = str()
is_inside = False
while answer != 'o' and answer != 'n':
    answer = input('Voulez-vous utiliser un de ces templates ? [o/n]\n{}\n'.format(names_templates)).lower()
if answer == 'o':
    while answer not in dict_templates.keys():
        answer = input('Lequel ? ')
    subject = dict_templates[answer][0]
    body = dict_templates[answer][1]
    is_inside = True
else:
    subject = input("Sujet : ")
    body = input("Contenu : ")

answer = str()
if is_inside is False:
    while answer != 'o' and answer != 'n':
        answer = input('Voulez-vous ajouter ce template ? [o/n] ').lower()
    if answer == 'o':
        templates_modif = True
        new_template = input('Nommez ce template : ')
        dict_templates[new_template] = subject, body

if templates_modif is True:
    with open('templates', 'wb') as monFichier:
        monPickler = pickle.Pickler(monFichier)
        monPickler.dump(dict_templates)

nb_mail = int(input('Combien de mail faut-il envoyer ? : '))

# ENVOI

msg = MIMEMultipart()
msg['From'] = userlogin
msg['To'] = recipient
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Connection au serveur
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(userlogin, userpwd)

mail = msg.as_string()

print('Envoi en cours...')
time_debut = time()

for i in range(nb_mail):
    server.sendmail(userlogin, recipient, mail)
    print('{}e mail envoyé !'.format(i+1))

time_fin = time()
print('Email(s) envoyé(s) !')
server.quit()

time_total = time_fin - time_debut
time_average = time_total / nb_mail
print('Action effectué en {} secondes\nTemps moyen par email : {}'.format(time_total, time_average))