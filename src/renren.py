import re
import urllib
import urllib2
import cookielib
from multiprocessing import Pool

origURL = 'http://www.renren.com/Home.do'
domain = 'renren.com'
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


def login(email, password, origURL, domain):
    # login renren.com
    postdata = urllib.urlencode({
        'email': email,
        'password': password,
        'origURL': origURL,
        'domain': domain
        })
    req = urllib2.Request(
        url='http://www.renren.com/PLogin.do',
        data=postdata
        )
    try:
        urllib2.urlopen(req)
    except:
        print 'Can\'t login'
    print 'Log on successfully!'


def friendsList(opener):
    # get the friends list
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
    # make a list of friends' portrait albums
    friends = []
    try:
        friends = friendsList(opener)
    except:
        print 'can\'t get friends list'

    tasksList = []
    for i in range(len(friends)):
        for key in friends[i].keys():
            if key == 'id':
                req = "http://photo.renren.com/getalbumprofile.do?owner=" \
                    + str(friends[i]['id'])
                tasksList.append(req)

    return tasksList


def getPotrait(req):
    # download and save a friend's portrait
    try:
        r = urllib2.urlopen(req)
    except:
        print 'error open'
        return

    try:
        data = r.read()
        f = re.search(
                      'http://photo.renren.com/photo/\d*/photo-\d*\?curpage=0&t=?n?u?l?l?',
                      data
                      )
    except:
        print 'error read'
        return

    try:
        urlA = f.group()
    except AttributeError:
        print 'error parse URL'
        return

    try:
        r = urllib2.urlopen(urlA)
        data = r.read()
        f = re.search(
                      'http:\\\\/\\\\/hdn.xnimg.cn\\\\/photos\\\\/hdn\d*\\\\/.*?jpg',
                      data)

    except (urllib2.URLError):
        print 'error search'
        return

    try:
        urlT = f.group()
        urlB = urlT.replace('\\', '')

    except AttributeError:
        print 'error parse image url'
        return

    try:
        r = urllib2.urlopen(urlB)
        tmp = re.search('large_[\d\D]*.jpg', urlB)
        image_name = tmp.group()
        img = r.read()

    except:
        print 'Can\'t get portrait'
        return

    output = open('./pics/' + image_name, 'wb')
    output.write(img)
    output.close()
    print image_name + ' is done.'


def visitFriend(req):
    try:
        urllib2.urlopen(req)
    except:
        print 'error'
        return


def visitAll(email, password):
    login(email, password, origURL, domain)
    tasks = tasksList(opener)
    pool = Pool(processes=30)
    pool.map(visitFriend, tasks)


def getPotraits(email, password):
    # download portraits of friends with multiple processes
    login(email, password, origURL, domain)
    tasks = tasksList(opener)
    pool = Pool(processes=20)
    pool.map(getPotrait, tasks)
