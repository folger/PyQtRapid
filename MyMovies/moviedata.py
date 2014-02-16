import bisect
import codecs
import copy_reg
import cPickle
import gzip
from PyQt4.QtCore import *
from PyQt4.QtXml import *

CODEC = "UTF-8"
NEWPARA = unichr(0x2029)
NEWLINE = unichr(0x2028)

class Movie(object):
    UNKNOWNYEAR = 1890
    UNKNOWNMINUTES = 0

    def __init__(self, title=None, year=UNKNOWNYEAR, minutes=UNKNOWNMINUTES,
                acquired=None, notes = None):
        self.title = title
        self.year = year
        self.minutes = minutes
        self.acquired = acquired if acquired is not None else QDate.currentDate()
        self.notes = notes


class MovieContainer(object):
    MAGIC_NUMBER = 0x3051E
    FILE_VERSION = 100

    def __init__(self):
        self.__fname = QString()
        self.__movies = []
        self.__movieFromId = {}
        self.__dirty = False

    def __iter__(self):
        for pair in iter(self.__movies):
            yield pair[1]

    def __len__(self):
        return len(self.__movies)

    def clear(self, cleanFileName=True):
        self.__movies = []
        self.__movieFromId = {}
        if cleanFileName:
            self.__fname = QString()
        self.__dirty = False

    def add(self, movie):
        if id(movie) in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        bisect.insort_left(self.__movies, [key, movie])
        self.__movieFromId[id(movie)] = movie
        self.__dirty = True
        return True

    def key(self, title, year):
        text = unicode(title).lower()
        if text.startswith("a "):
            text = text[2:]
        elif text.startswith("an "):
            text = text[3:]
        elif text.startswith("the "):
            text = text[4:]
        parts = text.split(" ", 1)
        if parts[0].isdigit():
            text = "%08d " % int(parts[0])
            if len(parts) > 1:
                text += parts[1]
        return u"%s\t%d" % (text.replace(" ", ""), year)


if __name__ == "__main__":
    mc = MovieContainer()
    mc.add(Movie())


