import urllib
import urllib2, cookielib
import re
import time
from multiprocessing import Pool

class Renren(object):
    def __init__(self, username, password):
        self.email = username
        self.password = password
        self.origURL = 'http://www.renren.com/Home.do'
        self.domain = 'renren.com'
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert('renren, cookie')
        except:
            None
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)
        
    def login(self):
        postdata = urllib.urlencode({
            'email' : self.email,
            'password' : self.password,
            'origURL' : self.origURL,
            'domain' : self.domain
            })
        req = urllib2.Request(
            url = 'http://www.renren.com/PLogin.do',
            data = postdata
            )
        try:
            urllib2.urlopen(req)
        except:
            print 'login failed'
        print 'successfully logined'

    def getFriendsList(self):
        req = 'http://friend.renren.com/myfriendlistx.do'
        try:
            r = self.opener.open(req)
            data = r.read()
        except:
            'can\'t get friends list'
        print 'successfully got friends list'
            
        f = re.search('friends=\[{.*?}\];', data)
        x = f.group()
        x = x[8:-1]

        x = x.replace('tr', 'Tr')
        x = x.replace('false', 'False')
        friends = eval(x)
        return friends

    def getTasksList(self):
        friends = self.getFriendsList()
        tasks = []
        for i in range(len(friends)):
            for key in friends[i].keys():
                if key == 'id':
                    req = "http://www.renren.com/profile.do?id="+str(friends[i][key])
                    tasks.append(req)
        print tasks
        return tasks
    
    def getFriendsImages(self):
        tasks = self.getTasksList()
        pool = Pool(processes = 4)      # five processes to increase the speed
        print pool.map(self.getAImage, tasks)


    def getAImage(self, req):
        r = self.opener.open(req)
        fri_name = eval("u'"+friends[i]['name']+"'").encode('utf-8')

        req = "http://photo.renren.com/getalbumprofile.do?owner=" + str(friends[i]['id'])
        try:
            r = urllib2.urlopen(req)
        except urllib2.URLError:
            print friends[i]['id'], " : ",  fri_name, "  Time out"
                    
        data = r.read()
        f = re.search('http://photo.renren.com/photo/\d*/photo-\d*\?curpage=0&t=?n?u?l?l?',data)
                    
        try:
            urlA = f.group()
        except AttributeError:
            print friends[i]['id'], " : ",  fri_name, "  Regexp Error"

        try:
            r = urllib2.urlopen(urlA)
            data = r.read()
        except (urllib2.URLError):
            print friends[i]['id'], " : ",  fri_name, "  Time out"

        f = re.search('http:\\\\/\\\\/hdn.xnimg.cn\\\\/photos\\\\/hdn\d*\\\\/.*?jpg',data)
        try:
            urlT = f.group()
        except AttributeError:
            print friends[i]['id'], " : ",  fri_name, "  Regexp Error"

        urlB = urlT.replace('\\','')

        try:
            r = urllib2.urlopen(urlB)
        except urllib2.URLError:
            print friends[i]['id'], " : ", fri_name, "  Time out"

        img = r.read()
        output = open(fri_name + '.jpg', 'wb')
        output.write(img)
        output.close()
        return friends[i]['id'], " : ", fri_name, " Got"
                    
