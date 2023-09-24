#!/usr/bin/python
# -*- coding: utf-8 -*-

# url: "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/EG0LJI"
from pathlib import Path
import os
import mne
from src.dataset import Dataset
from typing import List
import matplotlib.pyplot as plt
import numpy as np


class Dataset1(Dataset):

    def __init__(self):
        super().__init__(description="Raw Resting State data: Frontiers in Neuroscience",
                         path='data/raw_eeg_data/dataset1/')
        self.event_dict = {'auditory/left': 101, 'auditory/right': 201, 'visual/left': 65536,
                           'visual/right': 65790}
        self.load_to_mne()

    def epochsExtraction(self, tmin: float, tmax: float, events: List[float], raw: mne.io.RawArray, event) -> mne.Epochs:
        epochs = mne.Epochs(raw, events=events, event_repeated='merge',
                            event_id=event, preload=True, tmax=tmax, tmin=tmin)
        return epochs

    def montageDekorator(self, raw: mne.io.RawArray) -> mne.io.RawArray:
        raw.set_channel_types({"NAS": "stim", "LVEOG": "eog", "RVEOG": "eog",
                              "LHEOG": "eog", "RHEOG": "eog", "NFpz": "stim"})
        return raw.set_montage('standard_1020')

    def readRawFromFile(self, path: Path) -> mne.io.RawArray:
        raw = mne.io.read_raw_bdf(self.path / path)
        return raw

    def eventExtraction(self, raw: mne.io.RawArray) -> List[float]:
        events1 = mne.preprocessing.find_eog_events(
            raw, event_id=101, ch_name='LVEOG', verbose=False)
        events2 = mne.preprocessing.find_eog_events(
            raw, event_id=201, ch_name='RVEOG', verbose=False)
        events3 = mne.preprocessing.find_eog_events(
            raw, event_id=65536, ch_name='LHEOG', verbose=False)
        events4 = mne.preprocessing.find_eog_events(
            raw, event_id=65790, ch_name='RHEOG', verbose=False)
        events = np.concatenate((events1, events2, events3, events4), axis=0)
        return events
