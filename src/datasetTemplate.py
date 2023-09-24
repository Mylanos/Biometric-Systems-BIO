#!/usr/bin/python
# -*- coding: utf-8 -*-

from pathlib import Path
import os
import mne
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from src.dataset import Dataset
from typing import List


class DatasetX(Dataset):
    def __init__(self):
        super().__init__(description='SPIS-Resting-State',
                         path='data/raw_eeg_data/dataset3/SPIS-Resting-State-Dataset-master/Pre-SART EEG') # path to files
        self.sampling_freq = 256 
        self.event_dict = {'b': 69, 'g': 420, 'r': 1337, ...} #list of events
        self.ch_names = ["Fp1", "AF7",...] # chanels names
        self.load_to_mne()

    def epochsExtraction(self, tmin: float, tmax: float, events: List[float], raw: mne.io.RawArray, event) -> mne.Epochs:
        """This is api method, which extract epochs from raw mneArray.

        Args:
            tmin (float): epoch start range
            tmax (float): epoch end range
            events (List[float]): list of events - can be accesed from 'eventExtraction' method
            raw (mne.io.RawArray): mne rawArray
            event- {'event name':id}-exapmle: {'eyeMove':45}
        Returns:
            mne.Epochs: extracted epochs
        """
        raise Exception("Not implemented function 'epochsExtraction'")

    def montageDekorator(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        """This is api method, which add montage of electrodes to raw file

        Args:
            raw (mne.io.RawArray): 
        Returns:
            mne.io.RawArray: decorated RawArray
        """
        return raw

    def readRawFromFile(self, path: Path) -> mne.io.RawArray:
        """This is api method, which parses files to mne raw

        Args:
            path (Path): path to file

        Returns:
            mne.io.RawArray: parsed raw from file
        """
        raise Exception("Not implemented function 'readRawFromFile'")

    def filterRaw(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        """This is api method, where you can modifi raw date using filters and other modifications before parsing 

        Args:
            raw (mne.io.RawArray): 

        Returns:
            mne.io.RawArray:
        """
        return raw

    def eventExtraction(self, raw: mne.io.RawArray) -> List[float]:
        """This is api method, which extract events from raw 

        Args:
            raw (mne.io.RawArray): raw array

        Returns:
            List[float]: events list
        """
        raise Exception("Not implemented function 'eventExtractinon'")

    def makeInfo(self) -> Union[None, mne.Info]:
        """This is api method. If input files dont have information about them, you must specified

        Returns:
            None|mne.Info: if implemented
        """
        print("dwadw")
        return self.info