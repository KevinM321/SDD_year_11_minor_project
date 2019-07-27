import pickle

content = ['1', '2']
content[1] = '4 '
b = ['1']
b[0] = 3
with open('profile.p', 'wb') as f:
    pickle.dump(content, f)
with open('profile.p', 'rb') as f:
    body = pickle.load(f)
    o = pickle.load(f)
print(body[1])
print(o[0])

