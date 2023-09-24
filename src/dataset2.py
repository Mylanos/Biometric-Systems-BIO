#!/usr/bin/python
# -*- coding: utf-8 -*-

# source="https://zenodo.org/record/2348892#.Y4C_czOZOV4"

from pathlib import Path
import os
import mne
from src.dataset import Dataset
import scipy
import numpy
import matplotlib.pyplot as plt
from typing import List


class Dataset2(Dataset):

    def __init__(self) -> None:
        super().__init__(description='EEG Alpha Waves dataset',
                         path='data/raw_eeg_data/dataset2/')
        self.sampling_freq = 512
        self.ch_names = ['Fp1', 'Fp2', 'FC5', 'FC6', 'Fz', 'T7', 'Cz',
                         'T8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'O1', 'Oz', 'O2', "STI 001"]
        self.ch_types = ['eeg'] * 16 + ['stim']
        self.event_dict = {'closed': 1, 'open': 2}
        self.load_to_mne()

    def makeInfo(self) -> mne.Info:
        self.info = mne.create_info(
            ch_names=self.ch_names, ch_types=self.ch_types, sfreq=self.sampling_freq,)
        return self.info

    def montageDekorator(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        return raw.set_montage('standard_1020')

    def readRawFromFile(self, path: Path) -> mne.io.RawArray:
        data = scipy.io.loadmat(path)
        S = data['SIGNAL'][:, 1:17]
        stim_close = data['SIGNAL'][:, 17]
        stim_open = data['SIGNAL'][:, 18]

        stim = 1 * stim_close + 2 * stim_open

        S = S*pow(10, -6)

        X = numpy.concatenate([S, stim[:, None]], axis=1).T

        raw = mne.io.RawArray(data=X, info=self.info, verbose=False)
        return raw

    def filterRaw(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        fmin = 3
        fmax = 40
        raw.filter(fmin, fmax, verbose=False)
        raw.resample(sfreq=128, verbose=False)
        return raw

    def eventExtraction(self, raw: mne.io.RawArray) -> List[float]:
        return mne.find_events(raw=raw, stim_channel="STI 001", verbose=False)

    def epochsExtraction(self, tmin: float, tmax: float, events: List[float], raw: mne.io.RawArray, event) -> mne.Epochs:
        epochs = mne.Epochs(raw, events, tmin=tmin, tmax=tmax,
                            baseline=None, verbose=False, preload=True, event_id=event)
        epochs.pick_types(eeg=True)
        return epochs
