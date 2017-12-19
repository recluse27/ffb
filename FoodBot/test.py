import os

# for root, dirs, files in os.walk("./adapters"):
#     for filename in files:
#         print(filename)
mypath = './adapters'
files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
cafes = [s.split('_')[0] for s in files if s.split('_')[0] != 'generic' and s != '__init__.py']
print(cafes)
