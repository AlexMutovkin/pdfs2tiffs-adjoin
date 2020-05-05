#! /usr/bin/python
# -*- coding: utf-8 -*-

# converting PDFs in the working path to TIFFs and collecting them
# in the multipage TIFFs, sorted by 8-digit order number taken from a PDF's file name.

import os
import re
from shutil import copyfile

path2IM = "E:\\ImageMagick\\"
path2IM = "N:\\Watson\\distr\\portable\\LiberKey\\MyApps\\ImageMagick\\"
workingpath = "c:\\temp\\555\\"
tag4collection = "_ALL_IN_ONE"


class ListOfFiles:

    def __init__(self, keyname):
        self.keyname = keyname
        self.files = []
        self.lastmtime = 0
        self.lastmtimecollect = 0

    def add(self, root, name, sortcriteria):
        fname = os.path.join(root, name)
        mtime = os.path.getmtime(fname)
        if not re.match(".*" + tag4collection + ".*", name):
            if self.lastmtime < mtime : self.lastmtime = mtime
            self.files.append({"c": sortcriteria,
                               "f": fname,
                               "r": root,
                               "mtime": mtime})
        else:
            if self.lastmtimecollect < mtime : self.lastmtimecollect = mtime

    def sort(self):
        self.files.sort(key=lambda x: x["c"])

    def print(self):
        print("№ " + self.keyname)
        print([x["f"] for x in self.files])

    def convert_f2tif(self, f, remove=False):
        sf = f.split(".")
        if len(sf) >= 2:
            sf[-1] = "tif"
            df = ".".join(sf)
            print(f + " -> " + df)
            retcode = os.system(
                path2IM + "convert.exe -units PixelsPerInch -density 300 \"" + f
                + "\" -units PixelsPerInch -density 300 -compress Fax -trim \"" + df + "\"")
            if remove and retcode == 0:
                os.remove(f)

    def convert2tif(self, remove=False):
        print("№ " + self.keyname)
        for f in self.files:
            self.convert_f2tif(f["f"], remove)

    def join_f2tif(self, f):
        df = os.path.join(self.files[0]["r"], self.keyname + tag4collection + ".tif")
        if (f == self.files[0]["f"]):
            print(f + " >> " + df)
            copyfile(f, df)
        else:
            print(f + " +> " + df)
            os.system(
                path2IM + "convert.exe \"" + df + "\" \"" + f + "\" -adjoin \"" + df + "\"")

    def join2tif(self):
        print("№ " + self.keyname)
        if len(self.files) > 1 and self.keyname != "others":
            if self.lastmtimecollect < self.lastmtime:
                for f in self.files:
                   self.join_f2tif(f["f"])
            else:
                print("...no need to join files")

    def remove(self):
        print("№ " + self.keyname)
        for f in self.files:
            print("remove " + f["f"])
            os.remove(f["f"])


class BunchOfLists:

    def __init__(self, catalog, ext):
        self.catalog = catalog
        self.ext = ext
        self.bunch = []

    def findlist(self, keyname):
        for elbunch in self.bunch:
            if elbunch.keyname == keyname:
                return elbunch
        return None

    def add2bunch(self, keyname, root, name, sortcriteria):
        flist = self.findlist(keyname)
        if flist == None:
            flist = ListOfFiles(keyname)
            self.bunch.append(flist)
        flist.add(root, name, sortcriteria)

    # Функция ищет все файлы с именем filename во всех подкаталогах каталога catalog
    def fill(self):
        for root, dirs, files in os.walk(self.catalog):
            for name in files:
                m0 = re.match("(.*)\." + self.ext + "$", name, re.IGNORECASE)
                if m0:

                    m1 = re.match(".*(\d{8}).*", name)

                    if m1:
                        keyname = m1[1]
                        sortcriteria = m0[1].replace(keyname, '')
                    else:
                        keyname = "others"
                        sortcriteria = m0[1]

                    self.add2bunch(keyname, root, name, sortcriteria)

    def print(self):
        for elbunch in self.bunch:
            elbunch.print()

    def sort(self):
        for elbunch in self.bunch:
            elbunch.sort()

    def convert2tif(self, remove=False):
        for elbunch in self.bunch:
            elbunch.convert2tif(remove)

    def join2tif(self):
        for elbunch in self.bunch:
            elbunch.join2tif()

    def remove(self):
        for elbunch in self.bunch:
            elbunch.remove()


if __name__ == "__main__":
    b = BunchOfLists(workingpath, "pdf")
    b.fill()
    b.sort()
    b.convert2tif(remove=True)

    b2 = BunchOfLists(workingpath, "tif")
    b2.fill()
    b2.sort()
    b2.join2tif()
