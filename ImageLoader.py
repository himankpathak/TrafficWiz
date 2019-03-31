import os

class ImageLoader(object):
    def __init__(self,path):
        self.path = path;
        self.index = -1;
    def next(self,index):
        index = int(index)
        print(index)
        if index == -1:
            self.index+=1;
        elif index == -2:
            self.index-=1;
        else:
            self.index = index;
        si = str(self.index)
        fpath = self.path+"/"+si+".jpg";
        return fpath
