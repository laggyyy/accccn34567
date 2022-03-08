from time import time as timestamp
import json
import secmail
from time import timezone, sleep
import hmac
import base64
from hashlib import sha1
from uuid import uuid4
import requests
import amino
import os
import json
import threading
import requests
import wget
import heroku3
client=amino.Client()
def sigg(data):
        key='fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2'
        mac = hmac.new(bytes.fromhex(key), data.encode("utf-8"), sha1)
        digest = bytes.fromhex("32") + mac.digest()
        return base64.b64encode(digest).decode("utf-8")
def gen():
  mail = secmail.SecMail()
  email = mail.generate_email()
  return email

def gen1(email,dev):
  data = {
            "identity": email,
            "type": 1,
            "deviceID": dev
        }
  data=json.dumps(data)
  headers = {
            "NDCDEVICEID": dev,
            "NDC-MSG-SIG": sigg(data),
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)",
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
  
  response = requests.post(f"https://service.narvii.com/api/v1/g/s/auth/request-security-validation", headers=headers, data=data)
  return response

def gen2(email,dev):
        headers = {
            "NDCDEVICEID": dev,
            #"NDC-MSG-SIG": dev.device_id_sig,
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)",
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        data = json.dumps({
            "secret": f"0 456789",
            "deviceID": dev,
            "email": email,
            "clientType": 100,
            "nickname": "sdfghj",
            "latitude": 0,
            "longitude": 0,
            "address": None,
            "clientCallbackURL": "narviiapp://relogin",
            #"validationContext": {
                #"data": {
                    #"code": verificationCode
                #},
                #"type": 1,
                #"identity": email
            #},
            "type": 1,
            "identity": email,
            "timestamp": int(timestamp() * 1000)
        })
        headers["NDC-MSG-SIG"]=sigg(data)
        response = requests.post(f"https://service.narvii.com/api/v1/g/s/auth/register", data=data, headers=headers)
        #print(response.text)
        return response.json()

def devv():
  while True:
    dev=client.devicee()
    email=gen()
    gen1(email,dev)
    co=gen2(email,dev)
    print(co)
    if co["api:statuscode"]==270:
      
      url=co["url"]
      device=url.split("deviceid=")[1].split("'")[0]
      break
  return device

key="7ad5b9cf-7c8c-4ff5-a016-6186e636d3b7"
nickname="light"
app_name="accj567890"
url="https://save.thehybridklaus.repl.co"
password="Charlie123"
def restart():
    heroku_conn = heroku3.from_key(key)
    botapp= heroku_conn.apps()[app_name]
    botapp.restart()
def send(data):
    requests.post(f"{url}/save",data=data)
client=amino.Client("17925AEBB52F0AB6309A4D963914DD5ABBA536CE2ACC53643300942EF82983B504AF220835D92B95DB")

def codee(link):
	d={"data":link}
	p=requests.post("http://192.46.210.24:5000/captcha",data=d)
	return p.json()["dick"]

#password=custompwd

for i in range(3):
  dev=devv()
  #dev=client.device_id
  email=client.gen_email()
  print(email)
  client.request_verify_code(email = email,dev=dev)
  link=client.get_message(email)
  try: code=codee(link)
  except: pass
  
  
  try:
    client.register(email = email,password = password,nickname =nickname, verificationCode = code,deviceId=dev)
    #sub.send_message(chatId=chatId,message="Criada")
    d={}
    d["email"]=str(email)
    d["password"]=str(password)
    d["device"]=str(dev)
    t=json.dumps(d)
    data={"data":t}
    send(data)
  except Exception as l:
    print(l)
    pass


restart()
