########################################################################
########################################################################
import ch
import random
import sys
import re
import json
import time
import datetime
import os
import urllib
from urllib.parse import quote
from xml.etree import cElementTree as ET
if sys.version_info[0] > 2:
  import urllib.request as urlreq
else:
  import urllib2 as urlreq

botname = 'setzFK' ##Login
password = 'setz123A!' ##Senha

########################################################################
#ROOMS NICKS
########################################################################

def sntonick(username):
    user = username.lower()
    if user in nicks:
        nick = json.loads(nicks[user])
        return nick
    else:
        return user

########################################################################
#GETUPTIME / REBOOT
########################################################################

def getUptime():
    # do return startTime if you just want the process start time
    return time.time() - startTime

def reboot():
    output = ("rebooting server . . .")
    os.popen("sudo -S reboot")
    return output
  
########################################################################
#UPTIME
########################################################################

def uptime():
 
     total_seconds = float(getUptime())
 
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
 
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
 
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
     return string;

########################################################################
#DEFINITIONS
########################################################################

dictionary = dict() 
f = open("definitions.txt", "r")
for line in f.readlines():
  try:
    if len(line.strip())>0:
      word, definition, name = json.loads(line.strip())
      dictionary[word] = json.dumps([definition, name])
  except:
    print("[ERROR]Cant load definition: %s" % line)
f.close()
##nicks
nicks=dict()#empty list
f=open ("nicks.txt","r")#r=read w=right
for line in f.readlines():#loop through eachlinimporte and read each line
    try:#try code
        if len(line.strip())>0:#strip the whitespace checkgreater than 0
            user , nick = json.loads(line.strip())
            nicks[user] = json.dumps(nick)
    except:
        print("[Error]Can't load nick %s" % line)
f.close()
##Rooms
rooms = []
f = open("rooms.txt", "r") 
for name in f.readlines():
  if len(name.strip())>0: rooms.append(name.strip())
f.close()
##owners
owners = []
try:
    file = open("owners.txt", "r")
    for name in file.readlines():
        if len(name.strip()) > 0:
            owners.append(name.strip())
    print("[INFO]Owners loaded...")
    file.close()
except:
    print("[ERROR]no file named owners")
    print("2 second to read the error")
    time.sleep(2)
    exit()
time.sleep(1)

###admin
admin = []
try:
    file = open("admin.txt", "r")
    for name in file.readlines():
        if len(name.strip()) > 0:
            admin.append(name.strip())
    print("[INFO]Admin loaded...")
    file.close()
except:
    print("[ERROR]no file named admin")
    print("2 second to read the error")
    time.sleep(2)
    exit()
time.sleep(1)

##Dlist
dlist = []
f = open("dlist.txt", "r") 
for name in f.readlines():
  if len(name.strip())>0: dlist.append(name.strip())
f.close()
##SN TRY
sn = dict()
try:
  f = open('note.txt','r')
  sn = eval(f.read())
  f.close()
except:pass
##Send Notes
sasaran = dict()
f = open ("notes.txt", "r") 
for line in f.readlines():
  try:
    if len(line.strip())>0:
      to, body, sender = json.loads(line.strip())
      sasaran[to] = json.dumps([body, sender])
  except:
    print("[Error] Notes load fails : %s" % line)
f.close()
##SN Notifs
notif = []
f = open("notif.txt", "r")
for name in f.readlines():
  if len(name.strip())>0: notif.append(name.strip())
f.close


########################################################################
#TEXTO ARCO-ÍRIS
########################################################################

def rainbow(word):
    length = len(word)
    #set rgb values
    r = 255 #rgb value set to red by default
    g = 0
    b = 0
    sub = int(765/length)
    counter = 0
    string = ""
    for x in range(0, length):
        letter = word[counter]
        s = "<f x12%02X%02X%02X='0'>%s" % (r, g, b, letter)
        string = string+s
        counter+=1
        if (r == 255) and (g >= 0) and (b == 0): #if all red
            g = g+sub
            if g > 255: g = 255
        if (r > 0) and (g == 255) and (b == 0): #if some red and all green
            r = r-sub #reduce red to fade from yellow to green
            if r<0: r = 0 #if red gets lower than 0, set it back to 0
        if (r == 0) and (g == 255) and (b >= 0):
            b = b+sub
            if b>255:
                b = 255
                trans = True
        if (r == 0) and (g > 0) and (b == 255):
            g = g-sub
            if g<0: g = 0
        if (r >= 0) and (g == 0) and (b == 255):
            r = r+sub
            if r>255: r = 255
    return string

########################################################################
#BGTIME
########################################################################
  
def bgtime(x):
        try:
                x = user if len(x) == 0 else x
                html = urlreq.urlopen("http://st.chatango.com/profileimg/%s/%s/%s/mod1.xml" % (x.lower()[0], x.lower()[1], x.lower())).read().decode()
                inter = re.compile(r'<d>(.*?)</d>', re.IGNORECASE).search(html).group(1)
                if int(inter) < time.time():
                        lbgtime = getSTime(int(inter))
                        return "O BG desse usuário acabou %s atrás" % lbgtime
                else: return "O tempo de bg de <b>%s</b>: %s" % (x.lower(), getBGTime(int(inter)))
        except: return 'Esse usuário não tem bg.'

def getBGTime(x):
                    total_seconds = float(x - time.time())
                    MIN     = 60
                    HOUR    = MIN * 60
                    DAY     = HOUR * 24
                    YEAR    = DAY * 365.25
                    years   = int( total_seconds / YEAR )      
                    days    = int( (total_seconds % YEAR ) / DAY  )
                    hrs     = int( ( total_seconds % DAY ) / HOUR )
                    min = int( ( total_seconds  % HOUR ) / MIN )
                    secs = int( total_seconds % MIN )
                    string = ""
                    if years > 0: string += "<font color='#00ffff'>" + str(years) + "</font> " + (years == 1 and "ano" or "anos" ) + ", "
                    if len(string) > 0 or days > 0: string += "<font color='#00ffff'>" + str(days) + "</font> " + (days == 1 and "dia" or "dias" ) + ", "
                    if len(string) > 0 or hrs > 0: string += "<font color='#00ffff'>" + str(hrs) + "</font> " + (hrs == 1 and "hora" or "horas" ) + ", "
                    if len(string) > 0 or min > 0: string += "<font color='#00ffff'>" + str(min) + "</font> " + (min == 1 and "minuto" or "minutos" ) + " e "
                    string += "<font color='#00ffff'>" +  str(secs) + "</font> " + (secs == 1 and "segundo" or "segundos" )
                    return string;

########################################################################
#YOUTUBE
########################################################################

def tube(args):
  """
  #In case you don't know how to use this function
  #type this in the python console:
  >>> tube("pokemon dash")
  #and this function would return this thing:
  {'title': 'TAS (DS) Pokémon Dash - Regular Grand Prix', 'descriptions': '1st round Grand Prix but few mistake a first time. Next Hard Grand Prix will know way and few change different Pokémon are more faster and same course Cup.', 'uploader': 'EddieERL', 'link': 'http://www.youtube.com/watch?v=QdvnBmBQiGQ', 'videoid': 'QdvnBmBQiGQ', 'viewcount': '2014-11-04T15:43:15.000Z'}
  """
  search = args.split()
  url = urlreq.urlopen("https://www.googleapis.com/youtube/v3/search?q=%s&part=snippet&key=AIzaSyBSnh-sIjd97_FmQVzlyGbcaYXuSt_oh84" % "+".join(search))
  udict = url.read().decode('utf-8')
  data = json.loads(udict)
  rest = []
  for f in data["items"]:
    rest.append(f)
  
  d = random.choice(rest)
  link = "http://www.youtube.com/watch?v=" + d["id"]["videoId"]
  videoid = d["id"]["videoId"]
  title = d["snippet"]["title"]
  uploader = d["snippet"]["channelTitle"]
  descript = d["snippet"]['description']
  count    = d["snippet"]["publishedAt"]
  return "Result: %s <br/><br/><br/><br/><br/><br/><br/><br/><font color='#ffcc00'><b>%s</b></font><br/><font color='#ff0000'><b>Uploader</b></font>:<b> %s</b><br/><font color='#ff0000'><b>Uploaded on</b></font>: %s<br/><font color='#ff0000'><b>Descriptions</b></font>:<i> %s ...</i><br/> " % (link, title, uploader, count, descript[:200])

########################################################################
#GS / GOOGLE SEARCH
########################################################################

def gs(args):
  args = args.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('<br/>[%s] %s : http://%s' % (q, title.capitalize(), link))
      q += 1
  return "<br/><br/>".join(setter[0:4])

########################################################################
#GIS
########################################################################

def gis(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Resultado da pesquisa por <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:1])
def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Resultado da pesquisa por <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])


def jis(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Resultado da pesquisa por <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:3])
def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Resultado da pesquisa por <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

##Random number game
def numbergame():
    randomnumber=random.choice(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"])
    answer=randomnumber
    return answer    
########################################################################
#SAVERANK
########################################################################

def saveRank():
    f = open("owners.txt","w")
    f.write("\n".join(owners))
    f.close()
    f = open("admin.txt","w")
    f.write("\n".join(admin))
    f.close()
    
def googleSearch(search):
  try:
    encoded = urllib.parse.quote(search)
    rawData = urllib.request.urlopen("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+encoded).read().decode("utf-8")
    jsonData = json.loads(rawData)
    searchResults = jsonData["responseData"]["results"]
    full = []
    val = 1
    for data in searchResults:
      if "youtube" in data["url"]:
        data["url"] = "http://www.youtube.com/watch?v="+data["url"][35:]
      full.append("<br/>"+"(<b>%s</b> %s -> %s" % (val, data["title"], data['url']))
      val = val + 1
    return '<br/>'.join(full).replace('https://','http://')
  except Exception as e:
    return str(e)

########################################################################
#TLI / TRADUTOR
########################################################################

def tli(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=PT|ID", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tip(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=ID|PT", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tle(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=PT|EN", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tlp(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=EN|PT", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tjp(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=JA|PT", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break


def tlj(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=PT|JA", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break


def dtl(args):
  url = "http://ws.detectlanguage.com/0.2/detect?q="+"+".join(quote(args).split())+"&key=demo"
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request(url, headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('  ','').replace(' Subtitle Indonesia','').replace('-subtitle-indonesia','')
  res = re.findall('"language":"(.*?)"', resp)
  newset = list()
  num = 1
  return "".join(res).upper()

def dtg(args):
  url = "http://ws.detectlanguage.com/0.2/detect?q="+"+".join(quote(args).split())+"&key=demo"
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request(url, headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('  ','').replace(' Subtitle English','').replace('-subtitle-english','')
  res = re.findall('"language":"(.*?)"', resp)
  newset = list()
  num = 1
  return "".join(res).upper()

########################################################################
#CORES DE FONTE
########################################################################

class TestBot(ch.RoomManager):
  
  def onInit(self):
    self.setNameColor("ffffff") #cor do nick do bot
    self.setFontColor("000000")# cor da font do bot
    self.setFontFace("1")
    self.setFontSize(10)
    self.enableBg()
    self.enableRecording()

########################################################################
#CONEXÃO
########################################################################

  def onConnect(self, room):
    print("Connected")
  
  def onReconnect(self, room):
    print("Reconnected")
  
  def onDisconnect(self, room):
    print("Disconnected")

########################################################################
#OBTER ACESSO
########################################################################

  def getAccess(self, user):
    if user.name in owners: return 4 # Owners
    elif user.name in admin: return 3 # Admins
    else: return 0

#SN Notif
    if user.name in notif and user.name in sasaran:
      room.message(user.name+", you got a note left unread. Do +readnote to read it")
      notif.remove(user.name)
      
########################################################################
#ON MENSAGEM / PERSONALIDADE DO BOT E PREFIX
########################################################################
  
  def onMessage(self, room, user, message):
   try:
    msgdata = message.body.split(" ",1)
    if len(msgdata) > 1:
      cmd, args = msgdata[0], msgdata[1]
    else:
      cmd, args = msgdata[0],""
      cmd=cmd.lower() 
    global lockdown
    global newnum
    print(user.name+" - "+message.body)
    if user.name in notif:
        notif.remove(user.name)
    if user == self.user: return

    if "Wafy" == message.body.lower() or "@wafy " == message.body.lower() or "wafy" == message.body.lower():
      if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist:
       room.message (random.choice(["O que foi?", "O que quer? ","Como posso ser útil? ", "Oi, Olá docinho ^_^", "Qui é?", "Fala xD ","Diga!! *waves* ", "Diga me ^o^", "Chora zz", "Vai embora >_> ","Tuts tuts *waves* ", "Fala amore >3", "Me beija :x", "Oi more xD ","Belezinha? *waves* ", "*Abraço você " +user.name.title()+ "* Olá ^_^ ","Ei você ♪","Oi...", "Olá ","Oi *waves* ", "Oe ^_^", "Oi! ^_^", "Olá ^^ ","Olááá *waves* ", "Oe ^o^", "Pois não? xD", "Oeee ","Oiêêê *waves* ", "Oi tudo bem? ^_^", "Oi! ^-^", "Olá ^u^ ","Firmeza? *waves* ", "Oe ^o^","Oi " +user.name.title()+ " (: "," Olá " +user.name.title()+ ". *waves* ", "Oe " +user.name.title()+ ". *waves* ", "Ei você " +user.name.title()+ " :x", "Oiê " +user.name.title()+ ". *waves*","Opa "+sntonick(user.name)+"! x3"," Oe blz " +user.name.title()+ " "," O que foi " +user.name.title()+ "?", "Ki é " +user.name.title()+ "?", "Hm " +user.name.title()+ "?","Eai " +user.name.title()+ "! XD ","Pois não " +user.name.title()+ "?", "Fala " +user.name.title()+ "!", "Sim " +user.name.title()+ "?", "Oie " +user.name.title()+"-Senpai.","O que " +user.name.title()+ "? ","Olá " +user.name.title()+ "-San! ", "Você de novo " +user.name.title()+ "?", "Em que eu posso ajudar " +user.name.title()+ "?", " Senpai?","Oiiiiiii " +user.name.title()+ "-san "," yo " +user.name.title()+ ".", "Como posso ajudar " +user.name.title()+ "?", " Brinca comigo " +user.name.title()+ "?", " Ei você " +user.name.title()+"-sama."]),True)

    if "bot" == message.body.lower() or "Bot" == message.body.lower() or "Bot." == message.body.lower():
      if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist:
       room.message (random.choice(["O que foi?", "O que quer? ","Como posso ser útil? ", "Oi, Olá docinho ^_^", "Qui é?", "Fala xD ","Diga!! *waves* ", "Diga me ^o^", "Chora zz", "Vai embora >_> ","Tuts tuts *waves* ", "Fala amore >3", "Me beija :x", "Oi more xD ","Belezinha? *waves* ", "*Abraço você " +user.name.title()+ "* Olá ^_^ ","Ei você ♪","Oi...", "Olá ","Oi *waves* ", "Oe ^_^", "Oi! ^_^", "Olá ^^ ","Olááá *waves* ", "Oe ^o^", "Pois não? xD", "Oeee ","Oiêêê *waves* ", "Oi tudo bem? ^_^", "Oi! ^-^", "Olá ^u^ ","Firmeza? *waves* ", "Oe ^o^","Oi " +user.name.title()+ " (: "," Olá " +user.name.title()+ ". *waves* ", "Oe " +user.name.title()+ ". *waves* ", "Ei você " +user.name.title()+ " :x", "Oiê " +user.name.title()+ ". *waves*","Opa "+sntonick(user.name)+"! x3"," Oe blz " +user.name.title()+ " "," O que foi " +user.name.title()+ "?", "Ki é " +user.name.title()+ "?", "Hm " +user.name.title()+ "?","Eai " +user.name.title()+ "! XD ","Pois não " +user.name.title()+ "?", "Fala " +user.name.title()+ "!", "Sim " +user.name.title()+ "?", "Oie " +user.name.title()+"-Senpai.","O que " +user.name.title()+ "? ","Olá " +user.name.title()+ "-San! ", "Você de novo " +user.name.title()+ "?", "Em que eu posso ajudar " +user.name.title()+ "?", " Senpai?","Oiiiiiii " +user.name.title()+ "-san "," yo " +user.name.title()+ ".", "Como posso ajudar " +user.name.title()+ "?", " Brinca comigo " +user.name.title()+ "?", " Ei você " +user.name.title()+"-sama."]),True)
     
    if "oi" == message.body.lower() or "Oi" == message.body.lower() or "Oi." == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Oi, como vai você " +user.name.title()+ "? "," Como vão as coisas " +user.name.title()+ "?", "Quanto tempo " +user.name.title()+ "!", "Tudo em cima " +user.name.title()+ "?","Quais são as novas " +user.name.title()+ "?","Beleza " +user.name.title()+ "?","Oe " +user.name.title()+ "...","Olá, " +user.name.title()+ "~","Oiê, " +user.name.title()+ "!","Olá *waves*", "Oe *waves*"," Hola (: ","Olá ^^ ", "Oi ^_^"]),True)

    if "hola" == message.body.lower() or "Hola" == message.body.lower() or "Hola." == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Hola *waves*", "Hola ^_^"," Hola (: ","Hola ^^ ", "Hola xD"]),True)

    if "hello" == message.body.lower() or "Hello" == message.body.lower() or "Hello." == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Hello *waves*", "Hello ^_^"," Hello (: ","Hello *hugs* ^^ ", "Hello xD"]),True)

    if "hi" == message.body.lower() or "Hi" == message.body.lower() or "Hi." == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Hi *waves*", "Hi *hugs* ^_^"," Hi (: ","Hi ^^ ", "Hi xD"]),True)

    if "bom dia" == message.body.lower() or "Bom dia" == message.body.lower() or "dia" == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Buenos días. " +user.name.title()+ ". ;) ","Bom dia " +user.name.title()+ "!", "Oh, bom dia " +user.name.title()+ ". :o ", "E o que tem de bom " +user.name.title()+ "?", "Bom dia " +user.name.title()+". <3","Bom dia,Jão~"]),True)

    if "boa tarde" == message.body.lower() or "boa tarde" == message.body.lower() or "tarde" == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Boa tarde " +user.name.title()+ "! ","Boa, " +user.name.title()+ "!", "Buenas tardes " +user.name.title()+ ". ;) "]),True)

    if "boa noite" == message.body.lower() or "Boa noite" == message.body.lower() or "noite" == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Boa noite zé! :C ","Boa noite " +user.name.title()+ ". :P ", "Noite " +user.name.title()+ "~", "Buenas noches. " +user.name.title()+ "! ;) "]),True)    

    if "tchau" == message.body.lower() or "Tchau" == message.body.lower() or "xau" == message.body.lower():
     if self.getAccess(user) >= 0 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Adios papito " +user.name.title()+ "! *waves* ","  Até breve " +user.name.title()+ "~", "A gente se vê " +user.name.title()+ ".", "A gente se topa por ai " +user.name.title()+ "?","Até logo, " +user.name.title()+ "...","Falou " +user.name.title()+ "~","Até mais " +user.name.title()+ ". <3","Vaza, " +user.name.title()+ " </3","Volte logo " +user.name.title()+ "!","Tchau " +user.name.title()+ "!","Xau " +user.name.title()+ "~","*Abraço* tchau tchau more xD","Rala </3", "tchau </3"," Bye! </3 ","Até logo ♥ ", "tchau ^^"," Até mais ","xô xô ", "tchau ^^"," Bye! ","Vaza! ", "Adiós ^^"," Até + ","Falow ", "Hasta luego","*me sento em seu colo " +user.name.title()+ "* Não vai LOL "," *Abraço " +user.name.title()+ "* volte logo :x ","A gente se topa por ai  " +user.name.title()+ " n.n"," Adios papito  n.n", "Falou  " +user.name.title()+ "  >3", "Até qualquer hora" +user.name.title()+ ". ", "Volte logo n.n"   ]),True)
   
    if message.body == "": return  
    if message.body[0] == ">" or message.body[0] == "*" or message.body[0] == ">": 
      data = message.body[1:].split(" ", 1)
      if len(data) > 1:
        cmd, args = data[0], data[1]
      else:
        cmd, args = data[0], ""

########################################################################
#VERIFICAR ACESSO
########################################################################
        
      if self.getAccess(user) == 1: return 
      def pars(args):
        args=args.lower()
        for name in room.usernames:
          if args in name:return name    
      def roompars(args):
        args = args.lower()
        for name in self.roomnames:
          if args in name:return name
      def roomUsers():
          usrs = []
          gay = []
          prop = 0
          prop = prop + len(room._userlist) - 1
          for i in room._userlist:
            i = str(i)
            usrs.append(i)
          while prop >= 0:
            j = usrs[prop].replace("<User: ", "")
            i = j.replace(">", "")
            gay.append(i)
            prop = prop - 1
          return gay
      
      def getParticipant(arg):
          rname = self.getRoom(arg)
          usrs = []
          gay = []
          finale = []
          prop = 0
          prop = prop + len(rname._userlist) - 1
          for i in rname._userlist:
            i = str(i)
            usrs.append(i)
          while prop >= 0:
            j = usrs[prop].replace("<User: ", "")
            i = j.replace(">", "")
            gay.append(i)
            prop = prop - 1
          for j in gay:
            if j not in finale:
              finale.append(j)
          return finale


########################################################################
##COMANDOS ENGRAÇADOS 1
########################################################################
        
##comer
      if cmd == "comer":
        die1=random.randint(1,10)
        if args:
            room.message("*Ah não "+user.name.title()+" come "+args+"* "+str(die1)+" vezes ao dia")
        else:
          room.message("*Oh não "+random.choice(room.usernames)+" come "+random.choice(room.usernames)+"* "+str(die1)+" vezes ao dia")


##tea
      if cmd == "chá":
        die1=random.randint(1,10)
        if args:
            room.message("*Te sirvo chá com "+str(die1)+" cubos de açucar "+args+"*")
        else:
          room.message("*Te sirvo chá com "+str(die1)+" colheres com açucar "+random.choice(room.usernames)+"*")



##cookies
      if cmd == "bisco":
        die1=random.randint(2,10)
        if args:
            room.message("*Dou pra você "+str(die1)+" biscoitos "+args+"*")
        else:
          room.message("*Dou pra você "+str(die1)+" biscoitos "+random.choice(room.usernames)+"*")



##pedrinhas
      if cmd == "pedra":
        die1=random.randint(2,20)
        if args:
            room.message("*Taco em ti "+str(die1)+" pedrinhas "+args+"*")
        else:
          room.message("*Taco em ti "+str(die1)+" pedrinhas "+random.choice(room.usernames)+"*")

          
##poke
      if cmd == "poke":
          die1=random.randint(1,2000)
          die2=random.randint(1,2000)
          die3=random.randint(1,2000)
          room.message(random.choice(["Oi "+sntonick(user.name)+" Você achou um pokémon com "+str(die1)+" de ataque "+str(die2)+" defesa com "+str(die3)+"% de energia. ^_^"]))


#pet
      if cmd == "animal":
          die1=random.randint(1,1000)
          die2=random.randint(1,1000)
          die3=random.randint(1,500)
          room.message(random.choice(["Alô "+sntonick(user.name)+" Você achou um animal de estimação com "+str(die1)+" de ataque "+str(die2)+" defesa com "+str(die3)+"% de fraquesa."]))


##dados
      if cmd == "dados":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message("Rolando os dados caiu um "+str(die1)+" e um "+str(die2))


##Palavra da sorte
      if cmd.lower() == "pls":
          if self.getAccess(user) >= 0:
              room.message(random.choice(["Sua palavra da sorte é: Amigas","Sua palavra da sorte é: Amigos","Sua palavra da sorte é: Chupeta","Sua palavra da sorte é: leite","Sua palavra da sorte é: Feijoada","Sua palavra da sorte é: Cachoeira","Sua palavra da sorte é: Arco-Iris","Sua palavra da sorte é: Céu","Sua palavra da sorte é: Furry","Sua palavra da sorte é: Segredo","Sua palavra da sorte é: Silêncio","Sua palavra da sorte é: Vida","Sua palavra da sorte é: voyeur","Sua palavra da sorte é: Oral","Sua palavra da sorte é: Pitada","Sua palavra da sorte é: Bomdade","Sua palavra da sorte é: Alegria","Sua palavra da sorte é: Bruxaria","Sua palavra da sorte é: Encanto","Sua palavra da sorte é: Enfeite","Sua palavra da sorte é: Pistola","Sua palavra da sorte é: Grande","Sua palavra da sorte é: Pequeno","Sua palavra da sorte é: Lábios","Sua palavra da sorte é: Safado","Sua palavra da sorte é: Safada","Sua palavra da sorte é: Pudim","Sua palavra da sorte é: Bolo","Sua palavra da sorte é: Sexo","Sua palavra da sorte é: Trepar","Sua palavra da sorte é: Amor","Sua palavra da sorte é: Paixão","Sua palavra da sorte é: Vizinha","Sua palavra da sorte é: Namoro","Sua palavra da sorte é: Namorada","Sua palavra da sorte é: Amante","Sua palavra da sorte é: Senpai","Sua palavra da sorte é: Irmã","Sua palavra da sorte é: Mãe","Sua palavra da sorte é: Sonho","Sua palavra da sorte é: Cuidado","Sua palavra da sorte é: Serpente","Sua palavra da sorte é: Aranha","Sua palavra da sorte é: Barata","Sua palavra da sorte é: Anime ","Sua palavra da sorte é: Penis","Sua palavra da sorte é: Perereca","Sua palavra da sorte é: Piriquita","Sua palavra da sorte é: Trouxa","Sua palavra da sorte é: Limão","Sua palavra da sorte é: Felicidade","Sua palavra da sorte é: Vampiro","Sua palavra da sorte é: Orgias","Sua palavra da sorte é: Incesto","Sua palavra da sorte é: Açucar","Sua palavra da sorte é: Pimenta","Sua palavra da sorte é: Ovo","Sua palavra da sorte é: Idiota","Sua palavra da sorte é: Gato","Sua palavra da sorte é: Cachorro","Sua palavra da sorte é: Cadela","Sua palavra da sorte é: Rosa","Sua palavra da sorte é: Morango","Sua palavra da sorte é: Vaca","Sua palavra da sorte é: Mingau","Sua palavra da sorte é: Pizza","Sua palavra da sorte é: Amizade"]))              


##sua waifu
      if cmd == "waifu":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(""+user.name.title()+" sua waifu vai ser "+random.choice(room.usernames)+" vocês vão se beijar "+str(die1)+" vezes ao dia, vai levar "+str(die1)+" fora em um mês e tem "+str(die2)+"% de chance de ficar com essa pessoa ^_^")
      

##hug
      if cmd == "abraço":
          if args:
            room.message("*Abraçando " + args+"*")
          else:
            room.message("*Abraço "+random.choice(room.usernames)+"*")


##kiss
      if cmd == "beijo":
          if args:
            room.message("*Beijando " + args+"*")
          else:
            room.message("*Beijo "+random.choice(room.usernames)+"*")


##Porcentagem
      if cmd == "8b":
          die1=random.randint(0,100)
          if args:
            room.message(random.choice([" "+str(die1)+"% de chance de ser verdade." , " "+str(die1)+"% de chance de ser mentira"]))
          else:
            room.message("Digite >% mais uma pergunta exemplo ( >% você é idiota?) Eu acho que é "+str(die1)+"% idiota, haha.")
            
##slove
      if cmd == "amor":
          die1=random.randint(0,100)
          if args:
            room.message("Seu nível de amor por " + args+ " é "+str(die1)+"%")
          else:
            room.message("Seu nível de amor por "+random.choice(room.usernames)+" é  "+str(die1)+"% ")


##amor da sua vida
      if cmd == "amor2":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(""+user.name.title()+" o amor da sua vida é "+random.choice(room.usernames)+" vocês vão se beijar "+str(die1)+" veze's ao dia e tem "+str(die2)+"% de chance de ficar com essa pessoa ^^")
          
            
##kill           
      if cmd == "matar":
        die1=random.randint(2,20)
        if args:
            room.message(random.choice(["*Fuzilando " + args +" com  "+str(die1)+" tiros* ","*Dando "+str(die1)+" Machadadas em " + args + "* ","*Dou "+str(die1)+" tiros em " + args + "* ","*Cravando "+str(die1)+" facas nos olhos de " + args + "* *lol*","*Matando " + args + " com sexo* o.O", "*Tiros em você, " + args + "*", "*Eu jogo gasolina em, " + args + ", e coloco fogo, queimaaaaaa! *lol*"]))
        else:
            room.message("Oooh, Não!!! "+random.choice(room.usernames)+" acaba de morrer. ")

##beijar           
      if cmd == "bj":
        die1=random.randint(2,20)
        if args:
            room.message(random.choice(["*Beijando " + args +" enquanto chupa sua lingua "+str(die1)+" vezes n///n ","*Dando "+str(die1)+" beijocas em " + args + "* ","*Dou "+str(die1)+" mordidas nos labios de "+ args + "* nada de beijos >//>"]))
        else:
            room.message("*Beijando "+random.choice(room.usernames)+"*")

            
##Numero da sorte
      if cmd.lower() == "nst":
          if self.getAccess(user) >= 0:
              room.message(random.choice(["Numero da sorte: 1","Número da sorte: 2","Número da sorte: 3","Número da sorte: 4","Número da sorte: 5","Número da sorte: 6","Número da sorte: 7","Número da sorte: 8","Número da sorte: 9","Número da sorte: 10","Número da sorte: 11","Número da sorte: 12","Número da sorte: 13","Número da sorte: 14","Número da sorte: 15","Número da sorte: 16","Número da sorte: 17","Número da sorte: 18","Número da sorte: 19","Número da sorte: 20","Número da sorte: 21","Número da sorte: 22","Número da sorte: 23","Número da sorte: 24","Número da sorte: 25","Número da sorte: 26","Número da sorte: 27","Número da sorte: 28","Número da sorte: 29","Número da sorte: 30","Número da sorte: 31","Número da sorte: 32","Número da sorte: 33","Número da sorte: 34","Número da sorte: 35","Número da sorte: 36","Número da sorte: 37","Número da sorte: 38","Número da sorte: 39","Número da sorte: 40","Número da sorte: 41","Número da sorte: 42","Número da sorte: 43","Número da sorte: 44","Número da sorte: 45","Número da sorte: 46","Número da sorte: 47","Número da sorte: 48","Número da sorte: 49","Número da sorte: 50","Número da sorte: 51","Número da sorte: 52","Número da sorte: 53","Número da sorte: 54","Número da sorte: 55","Número da sorte: 56","Número da sorte: 57","Número da sorte: 58","Número da sorte: 59","Número da sorte: 60","Número da sorte: 61","Número da sorte: 62","Número da sorte: 63","Número da sorte: 64","Número da sorte: 65","Número da sorte: 66","Número da sorte: 67","Número da sorte: 68","Número da sorte: 69","Número da sorte: 70","Número da sorte: 71","Número da sorte: 72","Número da sorte: 73","Número da sorte: 74","Número da sorte: 75","Número da sorte: 76","Número da sorte: 77","Número da sorte: 78","Número da sorte: 79","Número da sorte: 80","Número da sorte: 81","Número da sorte: 82","83","Número da sorte: 84","Número da sorte: 85","Número da sorte: 86","Número da sorte: 87","Número da sorte: 88","Número da sorte: 89","Número da sorte: 90","Número da sorte: 91","Número da sorte: 92","Número da sorte: 93","Número da sorte: 94","Número da sorte: 95","Número da sorte: 96","Número da sorte: 97","Número da sorte: 98","Número da sorte: 99","Número da sorte: 100"]))


#Frases de anime
      if cmd.lower() == "frase":
          if self.getAccess(user) >= 0:
              room.message(random.choice(["Tudo o que um sonho precisa para ser realizado é alguém que acredite que ele possa ser realizado.","Imagine uma nova história para sua vida e acredite nela.","Não espere por uma crise para descobrir o que é importante em sua vida.","Ser feliz sem motivo é a mais autêntica forma de felicidade.","Não existe um caminho para a felicidade. A felicidade é o caminho.","Saber encontrar a alegria na alegria dos outros, é o segredo da felicidade.","A alegria de fazer o bem é a única felicidade verdadeira.","Pedras no caminho? Eu guardo todas. Um dia vou construir um castelo.","Acredite em si próprio e chegará um dia em que os outros não terão outra escolha senão acreditar com você.","Não permito que nenhuma reflexão filosófica me tire a alegria das coisas simples da vida.","Somente quando encontramos o amor, é que descobrimos o que nos faltava na vida.","Pessimismo leva à fraqueza, otimismo ao poder.","Se você sabe conviver com pessoas intempestivas, emotivas, vulneráveis, amáveis, que explodem na emoção: acolha-me.","De levado, emo e louco todo mundo tem um pouco.","Lembrarei dos dias ruins, pois eles trazem a inspiração, o que antes era só dor, hoje move minha emoção.","Nem sempre somos coerentes com o nosso ponto de vista. Pois às vezes enxergamos com os olhos da emoção","A noite é mais sombria um pouco antes do amanhecer.","Depois de uma longa tempestade, aguarde por um dia de sol. É na noite mais escura e sombria que somos capazes de enxergar as estrelas.","Foi numa noite sombria, que olhei pro céu, percebi a decepção, abri meus olhos e fechei meu coração.","Parti para terra sombria, lugar onde os sonhos não brotam e o resto do mundo esquecia.","Não gosto de interpretar silêncios. Minha mente pode se tornar mais sombria do que a realidade.","Sombria não é aquela noite escura e aterradora, mas aquela pessoa que carrega o ódio no coração.","A persistência é o caminho do êxito.","A vida é maravilhosa se não se tem medo dela.","Creio no riso e nas lágrimas como antídotos contra o ódio e o terror.","Num filme o que importa não é a realidade, mas o que dela possa extrair a imaginação.","Você nunca achará o arco-íris, se você estiver olhando para baixo.","Cada segundo é tempo para mudar tudo para sempre.","A única coisa tão inevitável quanto a morte é a vida.","O som aniquila a grande beleza do silêncio.","Falar sem aspas, amar sem interrogação, sonhar com reticências, viver sem ponto final.","Nunca me senti só. Gosto de estar comigo mesmo. Sou a melhor forma de entretenimento que posso encontrar.","Não, eu não odeio as pessoas. Só prefiro quando elas não estão por perto.","Não tenho tempo pra mais nada, ser feliz me consome muito.","A única verdade é que vivo. Sinceramente, eu vivo. Quem sou? Bem, isso já é demais.","O que importa afinal, viver ou saber que se está vivendo?","Quando estamos sozinhos, só pensamos em morrer. Mas quando temos alguém, só pensamos em sobreviver.  Naruto ","É difícil esconder a tristeza atrás de risos o tempo todo.  Naruto ","Eu sempre quis te ver de novo. Te pedir desculpas. Dizer que te amava.  Ano Hana ","Me odeie como quiser, mas minha dor ainda será maior que a sua!  Naruto ","Sou um cachorro que late para a lua sem ter coragem de pegá-la.  Bleach ","Ao por sua cabeça no meu peito, seu corpo reconheceu os batimentos do seu coração.  Angel Beats! ","Amor e perdão não são sentimentos que compramos com palavras bonitas.  Naruto ","O desejo egoísta de querer manter a paz provoca guerras e o ódio nasce para proteger o amor.  Naruto ","Não importa quem vença, a justiça sempre prevalecerá. Isso porque é o vencedor quem define o que é justiça.  One Piece ","Meu compromisso é sempre vencer.  Dragon Ball Z ","Pesadelos não duram para sempre. Um dia você acorda e eles se foram.  Dragon Ball Z ","Você me mostrou que o poder não é nada se não for guiado pelo amor.  Dragon Ball Z ","É bonito quando um planeta desaparece, não importa qual seja. Dragon Ball Z ","Você quer que eu diga a verdade ou continuamos amigos?  Dragon Ball Z ","Como você pode falar de coração e sentimentos, quando suas entranhas estão podres.  Os Cavaleiros do Zodíaco ","Não é que sou solitário. Conheço a estupidez humana e não quero me contagiar.  Death Note ","Viva firme. Fique velho e careca, e morra depois de mim. E se der, morra sorrindo.  Bleach ","Vou colocar o nome do meu cachorro de Seiya. Assim, quando eu for treiná-lo eu irei falar: Sente Seiya!","Não importa o corpo, nem a aparência, e sim a alma.  Soul Eater","As pessoas não temem morrer, as pessoas temem imaginar a morte.  Soul Eater ","A derrota de hoje é a semente para a vitória de amanhã!  Fairy Tail ","A única coisa que me agarra a esse mundo são meus amigos.  Fairy Tail ","Se você pudesse escolher entre Pokémons existirem de verdade ou a paz mundial, qual Pokémon você escolheria?","É tolice temer o desconhecido.  Naruto ","Você é apenas um idiota que nasceu com uma genética boa.  Naruto ","Não fique forte para matar alguém que odeia, mas para proteger alguém que ama.  Fullmetal Alchemist ","Eu sou a escuridão, você é a luz. Não andamos pelo mesmo caminho.  O Mordomo Negro ","Neste mundo há pessoas que não conseguem sobreviver por causa da cruel relidade. Eu vendo sonhos para estas pessoas.  O Mordomo Negro ","Não importa quanto tempo passe, o destino dos anjos e demônios é empatar.  O Mordomo Negro ","A justiça deve ser analisada individualmente.  Death Note ","Não importa o quanto tente, você sozinho não pode mudar o mundo. Mas este é o lado bonito do mundo.  Death Note ","Esse mundo está podre, e quem apodreceu junto com ele deve morrer!  Death Note ","Se existe alguém que pode machucar você, existe alguém que pode curar suas feridas. Hatori Souma - Fruits Basket","Conhecendo tanto a derrota quanto a vitória, andando por ai derramando lágrimas, é assim que você se torna um verdadeiro homem. Shanks - One Piece","Você é lento até para cair... Kuchiki Byakuya - Bleach","Eu fechei meus olhos a muito tempo, meus objetivos estão na escuridão. Sasuke Uchiha","Você não pode morrer por alguém que ama. Precisa estar vivo para protege-la, sempre. D.N. Angel","No final estamos todos sozinhos. É absolutamente impossível fazer alguém pertencer a você.Yasu"]))


            
########################################################################
#SITES DE IMAGENS
########################################################################
            
      if cmd == "psit":
         room.message("Ooi "+user.name+" <br/> http://i.ntere.st <br/>http://giphy.com<br/>http://huaban.com<br/>http://weheartit.com<br/>https://anime-pictures.net<br/>http://www.zerochan.net<br/>http://www.4chan.org<br/>https://br.pinterest.com<br/>http://bakarenders.com<br/>http://www.renders-graphiques.fr <br/>",True)

      if cmd == "psit2":
         room.message("Ooi "+user.name+" <br/> https://prcm.jp<br/>http://e-shuushuu.net<br/>http://www.minitokyo.net<br/>https://wall.alphacoders.com<br/>http://konachan.net<br/>https://yande.re<br/>http://www.gelbooru.com<br/>http://danbooru.donmai.us<br/>http://www.v3wall.com<br/>http://www.theanimegallery.com<br/> ",True)  

      if cmd == "icons":
         room.message("Ooi "+user.name+"  <br/> http://kawaiis-icons.tumblr.com<br/>http://yumis-icons.tumblr.com<br/>http://anime-icon-plaza.tumblr.com<br/>http://r-h-kawai-icons.tumblr.com<br/>http://sillica.tumblr.com<br/>http://anime--icons.tumblr.com<br/>http://2hundrdpx.tumblr.com<br/>http://fuckyeahanimangaicons.tumblr.com<br/>",True)   

      if cmd == "p18":
         room.message("Ooi "+user.name+"  <br/> https://luscious.net<br/>http://www.kawaiihentai.com<br/>http://hentai-image.com<br/>http://mutimutigazou.com<br/>http://www.mg-renders.net<br/>http://g.e-hentai.org<br/>http://www.moe.familyrenders.com<br/>http://ors-renders-ero.animemeeting.com<br/>",True)   

########################################################################
##LISTA DE COMANDOS
########################################################################

      if cmd == "cmds":
          room.message("Os comandos disponíveis (yt(+ pesquisa), gs(+ pesquisa), amor(+ nickname), amor2(previsão amor), mods, chingar, comer(+ nickname), poke, pedra(+ nickname), bisco(+ nickname), chá(+ nickname), bot/8b(+ Perguntas), waifu(previsão waifu), matar(+ nickname), gis(+ pesquisa), jis(+ pesquisa), prof(+ nickname), mini(+ nickname), bg(+ nickname), pic(+ nickname), bgtime(+ nickname), pls(Palavra da sorte), frase, nst(Número da sorte), animal, num/guess(Adivinhar números), bater(+ nickname), abs(+ nickname), falar(+ palavras/frases), rfalar(+ palavras/frases), achar(+ nickname), ir(+ nome de chat), sair(+ nome de chat), chats, en(+ nickname + mensagem), ln(ler notas), cde(caixa de entrada), pvt(+ nickname + mensagem), wiki(+ pesquisa), cor/cor2(+ palavras), dados, abraço(+ nickname), beijo(+ nickname), beijo(+ nickname), ping, cso(+ nickname), meuip, user(+ nome de chat), emod)",True)
          
########################################################################
#SETRANK
########################################################################
              
##Setrank
      if cmd == "setrank": 
        if self.getAccess(user) < 0:return
        try:
          if len(args) >= 3:
            name = args
            if pars(name) == None:
                name = name
            elif pars(name) != None:
                name = pars(name)
            name, rank = args.lower().split(" ", 1)
            if rank == "4":
              owners.append(name)
              f = open("owners.txt", "w")
              f.write("\n".join(owners))
              f.close()
              room.message("Sukses")
              if name in admin:
                admin.remove(name)
                f = open("admin.txt", "w")
                f.write("\n".join(admin))
                f.close()
            if rank == "3":
              admin.append(name)
              f = open("admin.txt", "w")
              f.write("\n".join(admin))
              f.close()
              room.message("Sukses")
              if name in owners:
                owners.remove(name)
                f = open("owners.txt", "w")
                f.write("\n".join(owners))
                f.close()
            if rank == "2":
               room.message("Sukses")
               if name in owners:
                 owners.remove(name)
                 f = open("owners.txt", "w")
                 f.write("\n".join(owners))
                 f.close()
               if name in admin:
                 admin.remove(name)
                 f = open("admin.txt", "w")
                 f.write("\n".join(admin))
                 f.close()
            if name in owners:
                  owners.remove(name)
                  f = open("owners.txt", "w")
                  f.write("\n".join(owners))
                  f.close()
            if name in admin:
                  admin.remove(name)
                  f = open("admin.txt", "w")
                  f.write("\n".join(admin))
                  f.close()       
        except:
              room.message("something wrong")
            
#######################################################################
#COMANDOS CHAT 1
########################################################################

##delete chat  
      elif (cmd == "delete" or cmd == "dl" or cmd == "del"):
          if room.getLevel(self.user) > 0:
            if self.getAccess(user) >= 0 or room.getLevel(user) > 0:
              name = args.split()[0].lower()
              room.clearUser(ch.User(name))
            else:room.message("Você não pode fazer isso :|")
          else:
            room.message("Eu não sou mod aqui :|")

##Créditos
      if cmd == "crd":
        room.message("Olá "+user.name.title()+" Meu <f x12000000='0'><b>dono</b></f> é %s<br/><f x12000000='0'><b>Créditos:</b></f> %s" % (", ".join(owners), ", ".join(admin)),True)
  
##banlist            
      elif cmd == "banlist":
          if self.getAccess(user) >= 0 or room.getLevel(user) > 0:
            room.message("A lista de proibição é: "+str(room.banlist))
 
##Find
      if cmd == "achar" and len(args) > 0:
        name = args.split()[0].lower()
        if not ch.User(name).roomnames:
          room.message("Não encontrei esse ser talvez esteja no quarto se é que me entende ( ͡° ͜ʖ ͡°)")
        else:
          room.message("Pode achar %s em %s" % (args, ", ".join(ch.User(name).roomnames)),True)

########################################################################
#EVAL / SEI LÁ MAIS DEVE SER IMPORTANTE ESSE LANCE
########################################################################
                
      if cmd == "ev" or cmd == "eval" or cmd == "e":
        if self.getAccess(user) == 0:
          ret = eval(args)
          if ret == None:
            room.message("Done.")
            return
          room.message(str(ret))

########################################################################
#COMANDOS ENGRAÇADOS 2
########################################################################

##8ball
      elif cmd == "bot":
          if len(args)>0:
            obv = ["O que você quer?","O que deseja?"]
            insult = ["Foda se você","Foda se","Que porra","Eu te odeio","Beija minha bunda ^_^"]
            jelas = ["O que foi?","O que você quer?"]
            if args in obv:
              room.message(random.choice(["Eu quero a sua namorada ^^"," Quero você ^_^ "," Eu preciso de você "," Sea meu amante >3"," Seu amor! "," Dê-me seu dinheiro !!! :@"]))
            if args in jelas:
              room.message(random.choice(["Não é óbvio?!","Eu preciso de afeto vem ni mim  <3","Eu quero amor *h*"]))
            if args in insult:
              room.message(random.choice(["Muito bem, foda se você ^_^","Oh merda >_>","Que coisa, fale com minha mão."]))
            else:
              if args in obv or args in insult or args in jelas: return
              room.message(random.choice(["lol","lel","Fiquei sabendo que peixes podem voar...","Eu não li isso .u.","Gosta de pizza? (:","Vai dormi :@","zzz","Perde tempo não ^^","Vem pra minha cama >3","Não ^^","Oh NÃO :C","Talvez :o","Sim porra >_>","Sim amor *o*","Muito bem, foda se você ^_^","Oh merda >_>","Que coisa, fale com minha mão.","Não é óbvio?!","Eu preciso de afeto vem ni mim  <3","Eu quero amor *h*","Eu quero a sua namorada ^^"," Quero você ^_^ "," Eu preciso de você "," Sea meu amante >3"," Seu amor! "," Dê-me seu dinheiro !!! :@","Foda se você","Foda se","Que porra","Eu te odeio","Beija minha bunda ^_^","Não mesmo *lol*","Pode apostar que sim! ^^ ","Sem chance .-.","Totalmente positivo capitão... o.ô"," Sai fora -.-","Omg, sério isso? >.>"," Claro que não :@ "," Eu adoraria isso! <3","O simples não... ^o^ ","Ah, talvez. :s "," Nunca... :v","Respondo se mandar nudes. *blush*","A resposta seria cabeluda ô.o", "Sim. *-*","Sinto muito, mas… T.T"," Eu respondo se me pagar um sorvete :c"," É provavel que sim ^.^ ","As Perspectivas são boas C: "," Depende do ponto de vista...","Fale seriamente pourra :@", "Como se atreve :@", "Isso vai acontecer em breve (: ", "Isso vai acontecer hoje (: ", "Não vai acontecer nunca n.n", "Cala-te idiota zz","Shh beije-me agora. ","A resposta não é importante "," Esqueça :@"," Eu já disse que te amo? u///u"," Por favor, pare de perguntar coisas estúpidas >.>"," Vou te dizer se você me der uma pizza "," Não vai acontecer nem se você usar mágia ","Vamos fazer sexo? go go"," Faça silêncio pervertido zz "," Você me da nojo, como ousa :@ "," Você é kawaii, lógico que sim, agora me ame n.n "," OMG Casar comigo? "," Pare de ser tão fofis"," Eu não sei o que vou fazer para você n.n"," Continuará com isso? n.n"," Foda-se zz"," Tudo vai ficar bem Shh shh <3 "," *beijo você * silêncio baby "," NÃO !: @ "," YES! :@ "," Definitivamente ^^"," Claro ^~^ "," Eu adoraria isso! >.> ","Sim", "Claro (:", "Sim n.n", "Não de jeito nenhum >.>" "Claro que não '-'", "Certamente não </3", "Não nem em um milhão de anos zz", "Nopes XD", "Não", "Nem", "De jeito nenhum ç.ç" , "Não agora :@", "Não desta vez n.n", "ninguém se importa *bored* ", "não é possível *bored* ", "shh vai comer o seu amigo zz", "shhh me come agora :@", "Noooooooooo", "Yeeeeeeeeesssssssss", " Não me incomode zz "," Que pergunta estúpida zz"]))
          else:
            room.message("No comando 8ball você deve fazer uma pergunta para o bot responder  (EXEMPLO: >bot eu vou me casar?) ^_^")

##smack
      elif cmd =="chingar":
          if args:
            room.message("*Dou na sua cara @"+args+"* Quem é seu papai cadela? :@",True)
            self.setTimeout(int(4),room.message,"Diga meu nome cadela!! Diga a porra do meu nome!!")             
            self.setTimeout(int(8),room.message,"Diga :@+99")
          else:
            room.message("*Dou na sua cara @"+random.choice(room.usernames)+"* Quem é seu papai cadela?")
            self.setTimeout(int(4),room.message,"Fale meu nome cadela!! Fale a porra do meu nome!!")
            self.setTimeout(int(8),room.message,"Fale :@+99")
            
##Say
      if cmd == "falar":
        room.message(args)

##rsay
      if cmd == "reverse" or cmd == "rfalar":
          if args:
            room.message(args[::-1])
          else:
            room.message("Fook off"[::-1])

##Rainbow
      elif cmd == "cor":
            if args == "":
              rain = rainbow('Rainbow!')
              room.message(rain,True)
            else: 
               rain = rainbow(args)
               room.message(rain,True)

##Rainbow
      elif cmd == "cor2":
          if args == "":
            rain = rainbow('Rainbow!')
            room.message(rain)
          else: 
              rain = rainbow(args)
              room.message(rain)

          
########################################################################
#COMANDOS GIS / GOOGLE IMAGENS
########################################################################

      elif cmd == "jis":
        if args:
          room.message(jis(args),True)

      elif cmd == "gis":
        if args:
          room.message(gis(args),True)

########################################################################
#COMANDOS ALEATÓRIOS
########################################################################
          
      if cmd == "gs": 
        room.message(gs(args),True)    

      elif cmd == "youtube" or cmd == "yt":
        if args:
          room.message(tube(args),True)

      elif cmd == "bgtime":
        if args:
          room.message(bgtime(args),True)

###New number###
      elif (cmd == "num"):
          newnum = numbergame()
          room.message("Escolhe um numero de 1 a 100 exemplo (>guess 69)")
          print("[INFO] NEW NUMBER : "+newnum)
          return newnum          

###Guess number##
      elif (cmd == "guess") and len(args) > 0:
            if(args==newnum):
              room.message("*star* *star* DING DING DIIING *star* *star* ^_^ "+sntonick(user.name)+" , acertou com o número: "+args)
            elif(args!=newnum and newnum > args ):
              room.message("É um numero mais alto. ^^")
            elif(args!=newnum and newnum < args ):
              room.message("É um numero mais baixo. ^^")
            else:
              room.message("error x_x")

########################################################################
#TLI / TRADUTOR 2
########################################################################
          
      if cmd == "tli":
        args = quote(args)
        room.message(tli(args, dtl(args)))

      if cmd == "tip":
        args = quote(args)
        room.message(tip(args, dtl(args)))

      if cmd == "tle":
        args = quote(args)
        room.message(tle(args, dtg(args)))

      if cmd == "tlp":
        args = quote(args)
        room.message(tlp(args, dtg(args)))

      if cmd == "tpj":
        args = quote(args)
        room.message(tlj(args, dtg(args)))

      if cmd == "tjp":
        args = quote(args)
        room.message(tjp(args, dtg(args)))
        
          
########################################################################
#COMANDOS CHAT 2
########################################################################
          
##Random User
      if cmd == "randomuser":
        room.message(random.choice(room.usernames))
          
##ismod
      elif cmd == "emod":
        user = ch.User(args)
        if room.getLevel(user) > 0:
          room.message("Sim")
        else:
          room.message("Não")

##Define            
      elif cmd == "define" or cmd == "df" and len(args) > 0:
          try:
            try:
              word, definition = args.split(" as ",1)
              word = word.lower()
            except:
              word = args
              definition = ""
            if len(word.split()) > 4:
              room.message("Fail")
              return
            elif len(definition) > 0:
              if word in dictionary:
                room.message("%s defined already" % user.name.capitalize())
              else:
                dictionary[word] = json.dumps([definition, user.name])
                f =open("definitions.txt", "w")
                for word in dictionary:
                  definition, name = json.loads(dictionary[word])
                  f.write(json.dumps([word, definition, name])+"\n")
                f.close
                room.message("Definition Saved")
            else:
              if word in dictionary:
                definition, name = json.loads(dictionary[word])
                room.message("<br/>ID : %s<br/>Keyword : %s<br/>Definition:<br/>%s" % (name, word, definition),True)
              else:
                room.message(args+" is not defined")
          except:
            room.message("something wrong")
            
##uwl
      if cmd == "uwl" and self.getAccess(user) >= 3:
        try:
          if args in owners:
            owners.remove(args)
            f = open("owners.txt","w")
            f.write("\n".join(owners))
            f.close()
            room.message("Sukses")
          if args in admin:
            admin.remove(args)
            f = open("admin.txt","w")
            f.write("\n".join(admin))
            f.close()
            room.message("Sukses")  
        except:
          room.message("Gagal")

##sbg        
      if cmd== "sbg":
            if self.getAccess(user) >= 3:
              if len(args) > 0:
                  if args == "on":
                    room.setBgMode(1)
                    room.message("Background On")
                    return
                  if args == "off":
                    room.setBgMode(0)
                    room.message("Background Off")

##udf
      if cmd == "udf" and len(args) > 0:
          try:
            word = args
            if word in dictionary:
              definition, name = json.loads(dictionary[word])
              if name == user.name or self.getAccess(user) >= 3:
                del dictionary[word]
                f =open("definitions.txt", "w")
                for word in dictionary:
                  definition, name = json.loads(dictionary[word])
                  f.write(json.dumps([word, definition, name])+"\n")
                f.close
                room.message(args+" has been removed from Definition database")
                return
              else:
                room.message("<b>%s</b> you can not remove this define only masters or the person who defined the word may remove definitions" % user.name, True)
                return
            else:
               room.message("<b>%s</b> is not yet defined you can define it by typing <b>define %s: meaning</b>" % args, True)
          except:
            room.message("Gagal")
            return

            
########################################################################
#COMANDOS ENGRAÇADOS 3
########################################################################

##fap
      elif cmd == "bater":
          if room.name == "ecchi-us":
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" Está batendo uma pensando em "+room.name+", que vergonha n.n",user.name+" Batendo uma enquanto pensanva em "+herp+" gozando escondido né? haha",user.name+" pfff pare de chupar "+herp+" ele nem esta vendo :@ ",user.name+" se masturbando com a calcinha da sua mãe, PUTO!!! :@",user.name+" Batendo uma e gozando na foto de "+herp+" que porra é essa? *lol*"]), True)
          else:
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" chupando "+room.name+" enquanto dorme sem noção n.n",user.name+" chupando a irmã de "+herp+" deveria ser envergonhar n.n",user.name+" que isso jove? comendo "+herp+" no meio da rua? ",user.name+" se masturbando com a cueca de "+herp+" B-BAKAAAAAA!!! :@",user.name+" Batendo uma e gozando na foto de "+herp+" *lol*",user.name+" Está batendo uma pensando em "+room.name+", que vergonha n.n",user.name+" Batendo uma enquanto pensanva em "+herp+" gozando escondido né? haha",user.name+" pfff pare de chupar "+herp+" ele nem esta vendo :@ ",user.name+" se masturbando com a calcinha da sua mãe, PUTO!!! :@",user.name+" Batendo uma e gozando na foto de "+herp+" que porra é essa? *lol*"]), True)    

##abs
      elif cmd == "abs":
          if room.name == "ecchi-us":
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" abraça  "+room.name+" com carinho* ti fofis x3",user.name+" abraçando "+herp+" por trás* querendo tirar uma casquinha né? haha",user.name+" abraçando "+herp+"* ",user.name+" está abraçando "+herp+" enquanto pega em sua bunda* wut o:"]), True)
          else:
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" abraça  "+room.name+" com carinho* ti fofis x3",user.name+" abraçando "+herp+" por trás* querendo tirar uma casquinha né? haha",user.name+" abraçando "+herp+"* ",user.name+" está abraçando "+herp+" enquanto pega em sua bunda* wut o:",user.name+" abraça "+room.name+" com amor* <3",user.name+" senta no colo de "+herp+" e abraça* onwww *o*",user.name+" abraçando "+herp+" enquanto rouba um beijo* oh oh :o ",user.name+" abraça "+herp+" com a mão dentro da* B-BAKAAAAAA!!! :@",user.name+" abraçando "+herp+" e rouba sua carteira* pqp *lol*",user.name+" abraça "+room.name+"* e vai bater pensando nisso* sem noção n.n",user.name+" abraçando "+herp+"* e fica LOkA LOkA XDDD",user.name+" abraçando "+herp+"* onww ti fofis </3 ",user.name+" abraçando e chupando pescoço de "+herp+"* what o.O"]), True)    


########################################################################
#COMANDOS PERFIL DO CHATANGO
########################################################################
            
##prof            
      elif cmd=="prof":
        try:
          args=args.lower()
          stuff=str(urlreq.urlopen("http://"+args+".chatango.com").read().decode("utf-8"))
          crap, age = stuff.split('<span class="profile_text"><strong>Age:</strong></span></td><td><span class="profile_text">', 1)
          age, crap = age.split('<br /></span>', 1)
          crap, gender = stuff.split('<span class="profile_text"><strong>Gender:</strong></span></td><td><span class="profile_text">', 1)
          gender, crap = gender.split(' <br /></span>', 1)
          if gender == 'M':
              gender = 'Male'
          elif gender == 'F':
              gender = 'Female'
          else:
              gender = '?'
          crap, location = stuff.split('<span class="profile_text"><strong>Location:</strong></span></td><td><span class="profile_text">', 1)
          location, crap = location.split(' <br /></span>', 1)
          crap,mini=stuff.split("<span class=\"profile_text\"><!-- google_ad_section_start -->",1)
          mini,crap=mini.split("<!-- google_ad_section_end --></span>",1)
          mini=mini.replace("<img","<!")
          picture = '<a href="http://fp.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/full.jpg" style="z-index:59" target="_blank">http://fp.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/full.jpg</a>'
          prodata = '<br/> <a href="http://chatango.com/fullpix?' + args + '" target="_blank">' + picture + '<br/><br/> Age: '+ age + ' <br/> Gender: ' + gender +  ' <br/> Location: ' +  location + '' '<br/> <a href="http://' + args + '.chatango.com" target="_blank"><u>Chat With User</u></a> ' "<br/><br/> "+ mini 
          room.message(prodata,True)
        except:
          room.message(" Tem certeza que "+args+" existe? O.O ")
      elif cmd=="mini":
        try:
          args=args.lower()
          stuff=str(urlreq.urlopen("http://"+args+".chatango.com").read().decode("utf-8"))
          crap,mini=stuff.split("<span class=\"profile_text\"><!-- google_ad_section_start -->",1)
          mini,crap=mini.split("<!-- google_ad_section_end --></span>",1)
          mini=mini.replace("<img","<!")
          prodata = '<br/>'+mini
          room.message(prodata,True)
        except:
          room.message("Acha mesmo que "+args+" existe?  o.O ")

##bg
      if cmd == "bg":
        try:
          args=args.lower()
          picture = '<a href="http://st.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/msgbg.jpg" style="z-index:59" target="_blank">http://fp.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/msgbg.jpg</a>'
          prodata = ''+picture
          room.message(""+prodata,True)
        except:
          room.message("Eu penso que "+args+" não existe n.n")

##pic
      if cmd == "pic":
                link = "http://fp.chatango.com/profileimg/%s/%s/%s/full.jpg" % (args[0], args[1], args)
                room.message(""+link,True)    

########################################################################
#COMANDOS ALEATÓRIOS
########################################################################

##Sentnote
      elif cmd == "cde":
          if user.name in sn:
            mesg = len(sn[user.name])
            room.message(" ["+str(mesg)+"] mensagen's.")

##send notes
      elif cmd == "en" or cmd == "sendnote":
          args.lower()
          untuk, pesan = args.split(" ", 1)
          if untuk[0] == "+":
                  untuk = untuk[1:]
          else:
                  if pars(untuk) == None:
                    room.message("Quem é "+untuk+" ?")
                    return
                  untuk = pars(untuk)
          if untuk in sn:
            sn[untuk].append([user.name, pesan, time.time()])
            if untuk not in notif:
              notif.append(untuk)
            else:pass
          else:
            sn.update({untuk:[]})
            sn[untuk].append([user.name, pesan, time.time()])
            if untuk not in notif:
              notif.append(untuk)
            else:pass
          room.message('Enviado para %s'% (untuk)+". ^^" , True)
				
##Read Notes
      elif cmd =="ln" or cmd =="readnote":
          if user.name not in sn:
            sn.update({user.name:[]})
          user=user.name.lower()
          if len(sn[user]) > 0:
            messg = sn[user][0]
            dari, pesen, timey = messg
            timey = time.time() - int(timey)
            minute = 60
            hour = minute * 60
            day = hour * 24
            days =  int(timey / day)
            hours = int((timey % day) / hour)
            minutes = int((timey % hour) / minute)
            seconds = int(timey % minute)
            string = ""
            if days > 0:
              string += str(days) + " " + (days == 1 and "dia" or "dias" ) + ", "
            if len(string) > 0 or hours > 0:
              string += str(hours) + " " + (hours == 1 and "hora" or "horas" ) + ", "
            if len(string) > 0 or minutes > 0:
              string += str(minutes) + " " + (minutes == 1 and "minuto" or "minutos" ) + ", "
            string += str(seconds) + " " + (seconds == 1 and "segundo" or "segundos" )
            room.message("[<font color='#6699CC'><b>Mensagem </b></font>] enviada por - "+sntonick(dari)+" : "+pesen+"  (<font color='#9999FF'>"+string+" atrás </font>)", True)
            try:
              del sn[user][0]
              notif.remove(user)
            except:pass
          else:room.message("Você não tem mensagens "'%s'%(user)+" n.n" , True)

          
##myip
      elif cmd =="meuip":
          if self.getAccess(user) < 0: return
          try:
            room.message("O seu I.P. o endereço é : "+message.ip)
          except:
            room.message("Houve um erro, eu não sou mod nesse chat. ^_^")

##cso
      if cmd=="cso":
          offline = None
          url = urlreq.urlopen("http://"+args+".chatango.com").read().decode()
          if not "buyer" in url:
            room.message(args+" não existe mais okay")
          else:
            url2 = urlreq.urlopen("http://"+args+".chatango.com").readlines()
            for line in url2:
              line = line.decode('utf-8')
              if "leave a message for" in line.lower():
                print(line)
                offline = True
            if offline:
              room.message(args+" está <f x12FF0000='1'>Offline</f>",True)
            if not offline:
              room.message(args+" está <f x1233FF33='1'>Online</f>",True)

      elif cmd == "wiki":
          if args == "":
            room.message("Digite algo para pesquisar ^_^")
          else:
            room.message("http://en.wikipedia.org/wiki/"+args)
            
########################################################################
#COMANDOS 2
########################################################################
          
##Private Messages
      elif cmd=="pvt":
        data = args.split(" ", 1)
        if len(data) > 1:
          name , args = data[0], data[1]
          self.pm.message(ch.User(name), "Mensagem enviada por - "+user.name+" : "+args+" ")
          room.message("Enviado para "+name+"")

##ping
      if cmd == "ping":
           if args == "":
            usrs = []
            gay = []
            finale = []
            prop = 0
            prop = prop + len(room._userlist) - 1
            for i in room._userlist:
              i = str(i)
              usrs.append(i)
            while prop >= 0:
              j = usrs[prop].replace("<User: ", "")
              i = j.replace(">", "")
              gay.append(i)
              prop = prop - 1
            for i in gay:
              if i not in finale:
                finale.append(i)
            if len(finale) > 40:
              room.message("@%s"% (" @".join(finale[:41])), True)
              self.getRoom("reitiatest").message("<br/><br/><b>Nama</b>: %s <br/><b>Rooms</b>: %s  <br/><b>Commmand</b>: %s  <br/><b>IP</b>: %s" % (user.name, room.name, cmd, message.ip), True)     
            if len(finale) <=40 :
              room.message("@%s"% (" @".join(finale)), True)
              self.getRoom("reitiatest").message("<br/><br/><b>Nama</b>: %s <br/><b>Rooms</b>: %s  <br/><b>Commmand</b>: %s  <br/><b>IP</b>: %s" % (user.name, room.name, cmd, message.ip), True)     
           if args != "":
             if args not in self.roomnames:
               room.message("I'm not there.")
               self.getRoom("reitiatest").message("<br/><br/><b>Nama</b>: %s <br/><b>Rooms</b>: %s  <br/><b>Commmand</b>: %s <br/><b>IP</b>: %s" % (user.name, room.name, cmd, message.ip), True)     
               return
 
##leave
      elif cmd == "sair"  and self.getAccess(user) >=4:
        if not args:args=room.name
        self.leaveRoom(args)
        room.message("*saindo de "+args+"* ^^")
        print("[SAVE] SAVING Rooms...")
        f = open("rooms.txt", "w")
        f.write("\n".join(self.roomnames))
        f.close()

##join

      if cmd == "ir" and len(args) > 1:
          if self.getAccess (user) >= 0:
              if args not in self.roomnames:
                room.message("*Partiu para "+args+"* ^^")
                self.joinRoom(args)
              else:
                room.message("Eu já estou lá :o")
              print("[SAVE] SAVING Rooms...")
              f = open("rooms.txt", "w")
              f.write("\n".join(self.roomnames))
              f.close()
      elif cmd == "user":
         if args == "":
          usrs = []
          gay = []
          finale = []
          prop = 0
          prop = prop + len(room._userlist) - 1
          for i in room._userlist:
            i = str(i)
            usrs.append(i)
          while prop >= 0:
            j = usrs[prop].replace("<User: ", "")
            i = j.replace(">", "")
            gay.append(i)
            prop = prop - 1
          for i in gay:
            if i not in finale:
              finale.append(i)
          if len(finale) > 40:
            room.message("<font color='#9999FF'><b>40</b></font> de <b>%s</b> Usuários atuais em %s"% (len(finale), ", ".join(finale[:41])), True)
          if len(finale) <=40 :
            room.message("No momento tem [<b>%s</b>] Usuário's nesse chat's || %s"% (len(finale),", ".join(finale)), True)
         if args != "":
           if args not in self.roomnames:
             room.message("Eu não estou lá "+sntonick(user.name)+".")
             return
           users = getParticipant(str(args))
           if len(users) > 40:
             room.message("<font color='#9999FF'><b>40</b></font> de <b>%s</b> Usuários atuais em <b>%s</b>: %s"% (len(users), args.title(), ", ".join(users[:41])), True)
           if len(users) <=40:
             room.message("No momento tem [<b>%s</b>] Usuário's nesse chat's || <b>%s</b>: %s"% (len(users), args.title(), ", ".join(users)), True) 
##bot rooms
      elif cmd == "chats" : 
        j = [] 
        for i in self.roomnames: 
          j.append(i+'[%s]' % str(self.getRoom(i).usercount)) 
          j.sort() 
        room.message("Eu estou online em "+"[%s] chat's || "%(len(self.roomnames))+", ".join(j))
##Mods
      elif cmd == "mods":
          args = args.lower()
          if args == "":
            room.message("<font color='#ffffff'><b>Room</b>: "+room.name+" <br/><b>Owner</b>: <u>"+ (room.ownername) +"</u> <br/><b>Mods</b>: "+", ".join(room.modnames), True)
            return
          if args in self.roomnames:
              modask = self.getRoom(args).modnames
              owner = self.getRoom(args).ownername
              room.message("<font color='#ffffff'><b>Room</b>: "+args+" <br/><b>Owner</b>: <u>"+ (owner) +"</u> <br/><b>Mods</b>: "+", ".join(modask), True)
              

   except Exception as e:
      try:
        et, ev, tb = sys.exc_info()
        lineno = tb.tb_lineno
        fn = tb.tb_frame.f_code.co_filename
        #room.message("[Expectation Failed] %s Line %i - %s"% (fn, lineno, str(e)))
        return
      except:
        #room.message("Undescribeable error detected !!")
        return


  ##Other Crap here, Dont worry about it
  
  def onFloodWarning(self, room):
    room.reconnect()
  
  def onJoin(self, room, user):
   print(user.name + " joined the chat!")
  
  def onLeave(self, room, user):
   print(user.name + " left the chat!")
  
  def onUserCountChange(self, room):
    print("users: " + str(room.usercount))

  def onPMMessage(self, pm, user, body):
    print("PM - "+user.name+": "+body)
    pm.message(user, "Olá eu sou um bot, fale com meu dono em vez disso. ^_^")


if __name__ == "__main__":
  TestBot.easy_start(rooms, botname, password)

##################################################################################################################  
##=============================================== End ==========================================================##
##################################################################################################################
