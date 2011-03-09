import re
import time
import urllib
import urllib2, cookielib
from multiprocessing import Pool

email = 'renws1990@sina.com'
password = 'gogogo54188'
origURL = 'http://www.renren.com/Home.do'
domain = 'renren.com'
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def login(username, password, origURL, domain):
    postdata = urllib.urlencode({
        'email'    : email,
        'password' : password,
        'origURL'  : origURL,
        'domain'   : domain
        })
    req = urllib2.Request(
        url = 'http://www.renren.com/PLogin.do',
        data = postdata
        )
    try:
        urllib2.urlopen(req)
    except:
        print 'Can\'t login'
    print 'Logan on successfully!'

def friendsList(opener):
    req = 'http://friend.renren.com/myfriendlistx.do'
    r = opener.open(req)
    data = r.read()
    f = re.search('friends=\[{.*?}\];', data)
    tmp = f.group()
    tmp = tmp[8:-1]

    tmp = tmp.replace('tr', 'Tr')
    tmp = tmp.replace('false', 'False')
    friendsList = eval(tmp)
    return friendsList

def tasksList(opener):

    friends = []
    try:
        friends = friendsList(opener)
    except:
        print 'can\'t get friends list'

    tasksList = []
    for i in range(len(friends)):
        for key in friends[i].keys():
            if key == 'id':
                req = "http://photo.renren.com/getalbumprofile.do?owner=" + str(friends[i]['id'])
                # req = "http://www.renren.com/profile.do?id="+str(friends[i][key])
                tasksList.append(req)

    return tasksList
                    
def getPotrait(req):

    # r = opener.open(req)
    try:
        r = urllib2.urlopen(req)
    except:
        print 'error'
        return
        # continue
    try:
        data = r.read()
        f = re.search('http://photo.renren.com/photo/\d*/photo-\d*\?curpage=0&t=?n?u?l?l?',data)
    except:
        print 'error'
        return

    try:
        urlA = f.group()
    except AttributeError:
        print 'error'
        return
        # print friends[i]['id'], " : ",  fri_name, "  Regexp Error"
        # continue

    try:
        r = urllib2.urlopen(urlA)
        data = r.read()
        f = re.search('http:\\\\/\\\\/hdn.xnimg.cn\\\\/photos\\\\/hdn\d*\\\\/.*?jpg', data)
    except (urllib2.URLError):
        print 'error'
        return
        # print friends[i]['id'], " : ",  fri_name, "  Time out"
        # continue

    # f = re.search('http:\\\\/\\\\/hdn.xnimg.cn\\\\/photos\\\\/hdn\d*\\\\/.*?jpg', data)
    try:
        urlT = f.group()
        urlB = urlT.replace('\\','')
    except AttributeError:
        print 'error'
        return
        # print friends[i]['id'], " : ",  fri_name, "  Regexp Error"
        # continue

    # urlB = urlT.replace('\\','')

    try:
        r = urllib2.urlopen(urlB)
        tmp = re.search('large_[\d\D]*.jpg', urlB)
        image_name = tmp.group()
        img = r.read()

    except:
        print 'Can\'t get potrait'
        return

    # tmp = re.search('large_[\d\D]*.jpg', urlB)
    # image_name = tmp.group()

    # img = r.read()
    output = open('./pics/'+image_name, 'wb')
    output.write(img)
    output.close()
    print image_name + ' is done.'

def getPotraits(email, password, origURL, domain, opener):
    # download Potraits of friends with multi processes
    login(email, password, origURL, domain)
    tasks = tasksList(opener)
    pool = Pool(processes = 10)
    pool.map(getPotrait, tasks)

beginTime = time.time()                 # to know how long it takes
getPotraits(email, password, origURL, domain, opener)
endTime = time.time()
timeUsed = endTime - beginTime
print 'It takes' + str(timeUsed)

