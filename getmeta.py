import conf
import os
import sys
import taglib
import csv

class Track:
    def __init__(self):
        self.m = dict()
    def POTags(self):
        tinfo = conf.tu + conf.ts
        line = list()
        for k in tinfo:
            if k in self.m:
                line.append(self.m[k])
            else:
                line.append('')
        return line

class Disc:
    def __init__(self,tags,path):
        self.grp = dict()
        self.m = dict()
        self.t = list()
        self.m['f'] = os.path.abspath(path)
        for tag in conf.du:
            k = conf.abbr[tag]
            if k not in tags:
                continue
            self.m[tag] = tags[k][0]

    def POTags(self):
        lines = list()
        line = list()
        for k in conf.po:
            if k in self.m:
                line.append(self.m[k])
            else:
                line.append('')
        line.append(self.m['f'])
        lines.append(line)
        for track in self.t:
            lines.append(track.POTags())
        return lines

    def AddTrack(self, tags):
        for tag, v in self.m.items():
            if tag == 'f':
                continue
            k = conf.abbr[tag]
            if k in tags and tags[k][0] == v:
                continue
            return False
        track = Track()
        for tag in conf.tu:
            k = conf.abbr[tag]
            if k not in tags:
                track.m[tag] = conf.null
                continue
            track.m[tag] = tags[k][0]
        for tag in conf.ts:
            k = conf.abbr[tag]
            if k not in tags:
                track.m[tag] = conf.null
                continue
            v = tags[k][0]
            if k in self.grp and self.grp[k] == v:
                continue
            self.grp[k] = v
            track.m[tag] = v
        self.t.append(track)
        return True

class Album:
    def __init__(self,tags,path):
        self.grp = dict()
        self.m = dict()
        self.d = list()
        self.m['f'] = os.path.abspath(path)
        for tag in conf.am:
            k = conf.abbr[tag]
            if k not in tags:
                continue
            self.m[tag] = tags[k][0]
        self.d.append(Disc(tags,path))

    def AddTrack(self, tags):
        for tag, v in self.m.items():
            if tag == 'f':
                continue
            k = conf.abbr[tag]
            if k in tags and tags[k][0] == v:
                continue
            return False
        if self.d[-1].AddTrack(tags):
            return True
        self.d.append(Disc(tags,self.m['f']))
        return self.d[-1].AddTrack(tags)

    def POTags(self):
        lines = list()
        line = list()
        for k in conf.po:
            if k in self.m:
                line.append(self.m[k])
            else:
                line.append('')
        line.append(self.m['f'])
        lines.append(line)
        for disc in self.d:
            lines += disc.POTags()
        return lines

    @staticmethod
    def MakeAlbum(path):
        '''
        @path:
        the path to the direct enclosing dir of media
        '''
        files = os.listdir(path)
        tracks = list()
        for f in files:
            if f.endswith(conf.suffix):
                tracks.append(f)
        tracks = sorted(tracks)
        restore = os.getcwd()
        os.chdir(path)
        album = Album(taglib.File(tracks[0]).tags,path)
        for track in tracks:
            album.AddTrack(taglib.File(track).tags)
        os.chdir(restore)
        return album

    @staticmethod
    def DumpAlbum(album, path=''):
        aname = os.path.basename(album.m['f'])
        path = os.path.join(path,aname+'.csv')
        with open(path,'w',encoding='utf-8') as f:
            writer =\
            csv.writer(f,delimiter=conf.sep)#,dialect=csv.unix_dialect)
            for line in album.POTags():
                writer.writerow(line)

class Volume:
    def __init__(self):
        pass

if not conf.CheckConfig():
    sys.exit('Bad Conf.py')

path = sys.argv[1]
album = Album.MakeAlbum(path)
Album.DumpAlbum(album,'')
