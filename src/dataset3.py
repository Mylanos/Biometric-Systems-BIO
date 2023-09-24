#!/usr/bin/python
# -*- coding: utf-8 -*-

# url: https://github.com/mastaneht/SPIS-Resting-State-Dataset
from pathlib import Path
import os
import mne
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from src.dataset import Dataset
from typing import List


class Dataset3(Dataset):
    def __init__(self):
        super().__init__(description='SPIS-Resting-State',
                         path='data/raw_eeg_data/dataset3/SPIS-Resting-State-Dataset-master/Pre-SART EEG')
        self.sampling_freq = 256
        self.event_dict = {'b': 69, 'g': 420, 'r': 1337}
        self.ch_names = ["Fp1", "AF7", "AF3", "F1", "F3", "F5", "F7", "FT7", "FC5", "FC3", "FC1", "C1",  "C3",  "C5",  "T7",  "TP7",  "CP5",  "CP3",  "CP1",  "P1",  "P3",  "P5",  "P7",  "P9",  "PO7",  "PO3",  "O1",  "Iz",  "Oz",  "POz",  "Pz",  "CPz",  "Fpz",  "Fp2",
                         "AF8",  "AF4",  "AFz",  "Fz",  "F2",  "F4",  "F6",  "F8",  "FT8",  "FC6",  "FC4",  "FC2",  "FCz",  "Cz",  "C2",  "C4",  "C6",  "T8",  "TP8",  "CP6",  "CP4",  "CP2",  "P2",  "P4",  "P6",  "P8",  "P10",  "PO8",  "PO4",  "O2",  "EOG1",  "EOG2",  "EOG3",  "STI 001"]
        self.ch_types = ['eeg'] * 64+['eog']*3+['stim']
        self.load_to_mne()

    def makeInfo(self) -> mne.Info:
        self.info = mne.create_info(
            ch_names=self.ch_names, ch_types=self.ch_types, sfreq=self.sampling_freq)
        self.info['description'] = self.descrition

        return self.info

    def montageDekorator(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        return raw.set_montage('standard_1020')

    def epochsExtraction(self, tmin: float, tmax: float, events: List[float], raw: mne.io.RawArray, event) -> mne.Epochs:
        epochs = mne.Epochs(raw, events=events, event_repeated='merge',
                            event_id=event, preload=True, tmax=tmax, tmin=tmin)

        self.load_to_mne()

    def makeInfo(self) -> mne.Info:
        self.info = mne.create_info(
            ch_names=self.ch_names, ch_types=self.ch_types, sfreq=self.sampling_freq,)
        self.info['description'] = self.descrition

        return self.info

    def montageDekorator(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        return raw.set_montage('standard_1020')

    def epochsExtraction(self, tmin: float, tmax: float, events: List[float], raw: mne.io.RawArray,event) -> mne.Epochs:
        epochs = mne.Epochs(raw, events=events, event_repeated='merge', event_id=event, preload=True)
        return epochs

    def readRawFromFile(self, path: Path) -> mne.io.RawArray:
        data = loadmat(self.path / path)
        np_data = np.array(data['dataRest'])
        np_data[0:67, :] *= 1e-6
        np_data[67, :] = np.around(np_data[67, :])

        raw = mne.io.RawArray(np_data, self.info, verbose=False)
        raw.set_channel_types(
            {"EOG1": 'eog', "EOG2": 'eog', "EOG3": 'eog', "STI 001": "stim"})
        return raw

    def filterRaw(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        fmin = 3
        fmax = 40
        raw.filter(fmin, fmax, verbose=False)
        raw.resample(sfreq=128, verbose=False)
        return raw

    def eventExtraction(self, raw: mne.io.RawArray) -> List[float]:
        events1 = mne.preprocessing.find_eog_events(
            raw, event_id=69, ch_name='EOG1', verbose=False)
        events2 = mne.preprocessing.find_eog_events(
            raw, event_id=420, ch_name='EOG2', verbose=False)
        events3 = mne.preprocessing.find_eog_events(
            raw, event_id=1337, ch_name='EOG3', verbose=False)
        events = np.concatenate((events1, events2, events3), axis=0)
        return events

    def plotSubject(self, index: int) -> None:
        raw = self.getRaw(index)
        events = self.eventExtraction(raw)
        epochs = self.epochsExtraction(-1, 2, events, raw)

        epochs.plot(block=True, events=events, scalings='auto')
        plt.show()
