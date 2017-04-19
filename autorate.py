import requests
import re
import time
import random
 
 
'''
嗯~
这个脚本

仅以此创造更多无聊的时间
 
此工具用于课程自动随机评价
 等级限于A B
 下方配置用户账号
'''
 
#config###############
UID="6316040*****"   # your ID
stime=5              # waiting how long
badprob=0.3          # the probability of bad
######################
 
def aob():
    '''
    ****************
    30% get B
    ****************
    '''
    if random.random()<badprob:
        return 'B'
    else:
        return 'A'
 
#based head
bh={
    "Accept-Language": "zh-CN,zh;q=0.8", 
    "Accept-Encoding": "gzip, deflate, sdch", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
    "User-Agent": "Mozilla/5.0 (Cendows 1.0 x128)", 
    "Upgrade-Insecure-Requests": "1"   
    }
 
#get sessionid
h1=bh
h1.update({
        "Host": "10.1.90.3", 
        "Connection": "keep-alive", 
        "Cache-Control": "max-age=0", 
        })
url = "http://10.1.90.3/pg/"
#APP=BCC
r = requests.get(url,headers=h1)
SID = r.headers['Set-Cookie'].split('; ')[0]
 
#login
data={
    "T1":UID,     #username
    "T2":'pass',      #password
    "R1":"S",     #student
    #"B1":"%B5%C7%C2%BD" #unknown
}
url="http://10.1.90.3/pg/shengfen.asp"
h2=bh
h2.update({ 
        "Origin": "http://10.1.90.3", 
        "Referer": "http://10.1.90.3/pg/", 
        "Cache-Control": "max-age=0", 
        "Cookie": SID, 
        "Content-Type": "application/x-www-form-urlencoded"
        })
requests.post(url,headers=h2,data=data) #submite userdata and login
 
#get course list
h3=bh
h3.update({
        "Referer": "http://10.1.90.3/pg/shengfen.asp", 
        "Cookie": "U%5Fatt=S; U%5Fname={}; {}".format(UID,SID), 
        })
url="http://10.1.90.3/pg/S_Lesson.asp"
r = requests.get(url,headers=h3)
 
r.encoding='GBK'
page = r.text
#get course list
courses = dict(re.findall('id=([0-9]{2,5})">(.*?)<',page))
 
#show the list
print("ID   Name")
for k,v in courses.items():
    print("%s %s"%(k,v))
print("Total: %d"%len(courses))
 
#judge
for CID in courses.keys():
    print("\n::[%5s] %s\n"%(CID,courses[CID]))
    #get one course
    url="http://10.1.90.3/pg/Lesson.asp?L_id=%s"%CID
    #just animation
    #this is question list
    clist = requests.get(url,headers=h3).content.decode('GBK')
    #course atter id
    att = re.findall(r'L_att" value=([0-9])',clist,flags=16)[0]
    #now we have got the page and start to fill it
    h4=bh
    h4.update({
                "Origin": "http://10.1.90.3", 
                "Referer": "http://10.1.90.3/pg/Lesson.asp?L_id=%s"%CID, 
                "Cache-Control": "max-age=0", 
                "Cookie": "U%5Fatt=S; U%5Fname={}; {}".format(UID,SID), 
                "Content-Type": "application/x-www-form-urlencoded"
                })
 
    url2="http://10.1.90.3/pg/result.asp"
 
    myjudge={
             'L_att': att,
             'L_id': CID,
             'R1': aob(),
             'R2': aob(),
             'R3': aob(),
             'R4': aob(),
             'R5': aob(),
             'R6': aob(),
            }
    check=''
    for i in range(1,7):
            check += myjudge['R%s'%i]
    #too nice
    if 'B' not in check:
        myjudge['R3'] = 'B'
    #too bad
    if 'A' not in check:
        myjudge['R3'] = 'A'
 
    #like a man
    print('waiting')
    time.sleep(stime)
    print('go on')
    requests.post(url2,headers=h4,data=myjudge)
    #sure?
    Total=0
    myensure={'L_id': CID}
    for i in range(1,7):
        if myjudge['R%s'%i]=='A':
            myensure['R_%s'%i]=16
            Total+=16
        else:
            myensure['R_%s'%i]=13
            Total+=13
    #for ensure
    #refresh
    myensure['Total']=Total
    for k,v in myensure.items():
        print(k,v)
 
    #submite now!
    url3='http://10.1.90.3/pg/results.asp'
    h4['Referer']="http://10.1.90.3/pg/result.asp"
    r = requests.post(url3,headers=h4,data=myensure)
    #result
    ret=r.content.decode('gbk')
    print(ret[15:26],'\n')
