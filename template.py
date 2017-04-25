import conf
import os
import sys
import taglib
import csv

class Track:
    def __init__(self,filen = "",ntrack = None,totalntrack = None):
        self.m = dict()
        for p in conf.po:
            self.m[p] = ""
        self.m['f'] = filen
        if ntrack is not None:
            tn = '{0:d}/{1:d}'.format(ntrack,totalntrack)
            self.m['t'] = tn

    def ToLine(self):
        line = list()
        for p in conf.po:
            line.append(self.m[p])
        line.append(self.m['f'])
        return line

    def GuessName(self):
        self.m['i'] = conf.Translate(self.m['f'])
        self.m['f'] = ''

    def SetDefaultValue(self):
        for p in conf.po:
            if p in conf.dv:
                self.m[p] = conf.dv[p]
            else:
                self.m[p] = p

class Disc:
    def __init__(self,path,ndisc,totalndisc):
        self.ts = list()
        self.ts.append(Track(path))
        self.ts[0].SetDefaultValue()
        self.ts[0].m['k'] = '{0:d}/{1:d}'.format(ndisc,totalndisc)
        files = os.listdir(path)
        ts = list()
        for f in files:
            if f.endswith(conf.suffix):
                ts.append(f)
        total = len(ts)
        for i in range(0,total):
            self.ts.append(Track(ts[i],i+1,total))
            self.ts[-1].GuessName()

    def ToLines(self):
        lines = list()
        for t in self.ts:
            lines.append(t.ToLine())
        return lines

class Volumn:
    def __init__(self):
        self.cds = []
        dirs = os.listdir()
        cds = []
        for dir in dirs:
            if dir.startswith(conf.prefix) and os.path.isdir(dir):
                cds.append(dir)
        for i in range(0,len(cds)):
            self.cds.append(Disc(cds[i],i+1,len(cds)))

    def DumpCSV(self,path):
        with open(path,'w',encoding='utf-8') as f:
            writer = csv.writer(f,delimiter=conf.sep)
            for cd in self.cds:
                for line in cd.ToLines():
                    writer.writerow(line)

vol = Volumn()
vol.DumpCSV(os.path.basename(os.getcwd()+'.csv'))
