'''
########################################################
# Name Project: Attendance List                        #
# Developer Name: Mario Wessen                         #
# Contact: mrfwn@cin.ufpe.br                           #
# Date last Modify:  24/06/2019                        #
# Description File:This is Class for manipuled         #
# Contacts. Methods for automation the system          #
########################################################
'''
import os
import qrcode
#from qrcode.image.pure import PymagingImage
#from PIL import Image, ImageFont, ImageDraw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
import glob
import bitly_api

class Contact:
    BASE_FOLDER = "./app/qrfolder/"
    def urlFormat(self,listURL,fromEmail,password,check):
        urlDatalist = []
        API_USER = "#####"
        API_KEY = "#####"
        for url in listURL:
            value = url['url']
            value = value[value.index('2'):]
            value = value[:value.index('.')]
            value = value.split('/')
            urlDatalist.append(
                 {'url': url['url'],
                 'title':value[3],
                 'date': value[2]+ '_' + value[1]+ '_' + value[0]})
        id = 1         
        if check == 'rec':
            toEmail = 'email1' 
        elif check == 'sp':
            toEmail = 'email2'
        elif check == 'rj':
            toEmail = 'email3'

        for url in urlDatalist:
            subject = 'QRCODE ' + url['title'] +  ' #g1'
            msg = MIMEMultipart()
            msg['From'] = fromEmail
            msg['To'] = toEmail
            msg['Subject'] = subject
            try:
                bitlyInstance = bitly_api.Connection(API_USER, API_KEY)
                urlShorte = bitlyInstance.shorten(uri = url['url'])
                message = 'Link_Real: '+url['url'] + '\n' + 'Link_Encurtado: ' + urlShorte['url']
                qrcodeImg = qrcode.make(urlShorte['url'])
                nameImage = self.BASE_FOLDER+'qrg1_'+url['date']+'_mat_'+ str(id) +'.png'
                qrcodeImg.save(nameImage)
                msg.attach(MIMEImage(open(nameImage, 'rb').read(), name=os.path.basename(nameImage)))
                msg.attach(MIMEText(message.encode('utf-8'), 'plain', 'utf-8'))
                server = smtplib.SMTP("smtp.office365.com", 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(fromEmail, password)
                server.sendmail(fromEmail, toEmail, msg.as_string())
                server.close()
                id +=1
            except:
                return False
        files = glob.glob(self.BASE_FOLDER+'*')
        for f in files:
            os.remove(f)
        return True
