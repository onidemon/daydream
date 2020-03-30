from  logging import info

name = 'denissultu@hotmail.com'

if '@' in name:
    for i in name:
        if i == '@':
            start = (name.index(i)+1)


        
domain = name[start::]
print('your domain is {}'.format(domain))
print('your username is  ',name[:name.index('@'):])
print('your domain is ',name[name.index('@')+1::])
d = dict()

d[name[:name.index('@'):]] =  name[name.index('@')+1::]
print(d)