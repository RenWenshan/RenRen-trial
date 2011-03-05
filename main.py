from renren import Renren

# get username and password for RenRen.com
username = raw_input('Email: ')
password = raw_input('Password: ')
print

# # get the path to save images
# path = raw_input('Save to?(eg. /home/vincent/Pictures/RenRen/)  :')
# if not path:
#     path = '/home/vincent/Pictures/RenRen/'
# if path[-1] != '/':
#     path = path + '/'


# main
a = Renren(username, password)
a.login()
a.getFriendsImages()


