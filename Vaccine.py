#!/usr/bin/env python
# coding: utf-8

# In[1]:


import smtplib
import winsound
import requests
import time
import json
from datetime import datetime
from twilio.rest import Client 


# In[2]:


account_sid = 'your_twilio_account_id' 
auth_token = 'your_twilio_auth_token' 
client = Client(account_sid, auth_token) 


# In[3]:


date = input("Please enter desired slot date (dd-mm-yyyy) eg. 01-12-2020: ")
minAgeLimit = int(input("Please enter an age group (Either 18 or 45): "))
email=input("Please enter an email address if required to be notified through an email: ")
waitSeconds = int(input("Please enter the time to be refreshed(in seconds): "))
pincode=int(input("Enter your Pincode"))


# In[4]:


browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}


# In[ ]:


while True:

       currentTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
       uri="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}".format(pincode=pincode,date=date)
       #uri = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={districtId}&date={date}".format(districtId=districtId,date=date)
       webData = requests.request("GET", uri, headers=browser_header).json()
       dataCount = 0

       if(webData["sessions"] or len(webData["sessions"]) > 0):
           for session in ["sessions"]:
               if(("min_age_limit" not in session)  or session["min_age_limit"] <= minAgeLimit):
                   print("\nCenter ID: ",session["center_id"],"Block: ",session["block_name"],"Pin Code: ",session["pincode"],"Fees: ",session["fee_type"],"Minimum Age: ",session["min_age_limit"]) 
                   print("Available: ",session["available_capacity"],"Vaccine: ",session["vaccine"],"\n")
                   
                   dataCount += 1
                   
       if(dataCount == 0):
           message = client.messages.create( 
                             from_='whatsapp:+given_by_twilio',  
                             body='No Slot available Next scan in 1 hr',      
                             to='whatsapp:your_whatsapp_number' 
                         ) 
       
       else:
           #to Send message to your whatsapp number
           message = client.messages.create( 
                             from_='whatsapp:given_by_twilio',  
                             body='{TEXT}'.format( TEXT=json.dumps(webData["sessions"], indent = 3)),      
                             to='whatsapp:your_whatsapp_number' 
                         ) 
           #to send mail 
           winsound.Beep(3000, 500)
           if len(email)>0:
               senders_mail = 'sender_mail'
               receivers_mail=email
               message = 'Subject: {SUBJECT}\n\n{TEXT}'.format(SUBJECT='Cowin Center found', TEXT=json.dumps(webData["sessions"], indent = 3))
               mail = smtplib.SMTP('smtp.gmail.com',587)
               mail.ehlo()
               mail.starttls()
               mail.login('your_gmail_id','your_password')
               mail.sendmail(senders_mail,receivers_mail,message)
               mail.close()

       print("LastRefresh: {currentTime}, Age Group: {minAgeLimit} Years, Next Refresh In: {waitSeconds} Seconds".format(currentTime=currentTime,minAgeLimit=minAgeLimit,waitSeconds=waitSeconds))
       print("---------------------------------------------------------")
       
       time.sleep(waitSeconds)
       if flag!=2:
           break


# In[ ]:




