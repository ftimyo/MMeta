abbr =\
    {'a':'ALBUM',
     'b':'ALBUMARTIST',
     'c':'COMPOSER',
     'd':'DATE',
     'g':'GENRE',
     'i':'TITLE',
     'k':'DISCNUMBER',
     'p':'COMPILATION',
     'r':'ARTIST',
     's':'SUPERTITLE',
     't':'TRACKNUMBER',
     #'f' is not used for meta
     'f':'FILEPATH',
    }

#single charactor null indicator
null = 'x'
#single charactor separator
sep = '@'

#precedence order
po = ['t','i','s','r','c','k','g','d','p','a','b',]
#album meta, shared by all disc(s) in the album
am = ['g','d','p','a','b',]
#disc unique, shared by all tracks in the disc
du = ['k',]
#track shared meta, maybe shared by a group of tracks
ts = ['s','r','c']
#track unique meta
tu = ['t','i',]

suffix = 'flac'
prefix = 'CD'
verbose = True

levels = ['Chopin_ Complete Edition']

def CheckConfig():
    if tu + ts + du + am != po:
        return False
    if null in abbr or sep in abbr:
        return False
    for k in po:
        if k not in abbr:
            return False
    return True
