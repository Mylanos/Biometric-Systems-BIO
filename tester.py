#!/usr/bin/python
# -*- coding: utf-8 -*-

import mne
from src.dataset1 import Dataset1
from src.dataset2 import Dataset2
from src.dataset3 import Dataset3


if __name__ == "__main__":
    #downloader = Downloader()
    var ="2"
    #var =input("zadej číslo sady:\n")
    if(var=="1"):
        dataset1 = Dataset1()
        dataset1.plotSubject(0)
    elif(var=="2"):
        dataset2 = Dataset2()
        dataset2.makeFolderReport()
    elif(var=="3"):
        dataset3=Dataset3()
        dataset3.plotSubject(0)

