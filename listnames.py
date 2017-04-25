import os,re,sys

def mfile(cd):
    files = os.listdir(cd)
    titles = []
    for f in files:
        if f.endswith('.flac'):
            m = re.match(r'(?P<idx>\d+)\.\s*(?P<title>.*).flac',f)
            f = m.group('title')
            titles.append(f)

    with open('zfn'+cd+'.txt','w',encoding='utf-8') as f:
        for line in titles:
            f.write(line+'\n')

for file in os.listdir():
    if os.path.isdir(file):
        mfile(file)
