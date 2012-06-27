from renren import getPotraits

# get username and password for RenRen.com
username = raw_input('Email: ')
password = raw_input('Password: ')
print

# get portraits
getPotraits(username, password)
