#!/usr/bin/python
# -*- coding: utf-8 -*-

import mne
from typing import List, Union
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os


class Dataset:
    """api class for eeg extraction and

    Returns:
        _type_: Dataset
    """

    def __init__(self, description='Dataset', path=None):
        self.descrition = description
        # main folder + path to dataset
        self.path = Path(__file__).parent.parent.resolve() / path
        self.event_dict = {}
        self.subjects = []
        self.bad_files = []
        self.rawNames = []
        if path:
            self.raw_files = self.raw_files = os.listdir(self.path)
        self.select = {}
        self.sampling_freq = None
        self.ch_names = []
        self.ch_types = []
        self.info = None

    def load_to_mne(self) -> None:
        self.info = self.makeInfo()

        for file in self.raw_files:
            try:
                self.raw = self.readRawFromFile(self.path / file)
                self.raw = self.montageDekorator(self.raw)
                self.raw = self.filterRaw(self.raw)
                self.subjects.append(self.raw)
                self.select[file] = len(self.subjects)-1
                self.rawNames.append(file)
            except Exception as e:
                # some of the files contained empty values that caused errors
                error_msg = f"Error with class {e.__class__} occured!"
                bad_file = {}
                bad_file["name"] = file
                bad_file["error"] = error_msg
                self.bad_files.append(bad_file)

    def print_info(self) -> None:
        print("Files with some errors:")
        # for file in self.bad_files:
        #    print(f'File {file["name"]}: {file["error"]}.')
        print("Loaded files:")

        if len(self.subjects) <= 0:
            print("Data set is empty")
        else:
            try:
                print(self.subjects[0].info)
            except:
                print("Info cant be displayed - might bad file.")

    def printRawFilePaths(self) -> None:
        print(self.raw_files)

    def getRaw(self, index: int) -> Union[mne.io.RawArray, None]:
        """return raw object from subject on index

        Args:
            index (int): index of subject

        Returns:
            mne.io.RawArray|None: if subject not exist
        """
        try:
            return self.subjects[index]
        except:
            return None

    def getIdByFile(self, fileName: str):
        try:
            id = self.select[fileName]
            return self.getRaw(id)
        except:
            raise Exception("Such file isnt in raw database")

############################################## ˇˇ visualization part ˇˇ ##############################################

    def plotEEGchanelsEvents(self, raw, events) -> None:
        raw.plot(events=events, scalings='auto', block=True,)

    def plotPsd(self, raw) -> None:
        raw.plot_psd(fmax=50)

    def plotEpochs(self, epochs, events) -> None:
        epochs.plot(events=events, scalings='auto', block=True,)
        
    def makeReport(self, raw, tmin=-1, tmax=1, subjectName=""):
        raw.pick_types(eeg=True, eog=True, stim=True).load_data()

        report = mne.Report(title='Subject '+subjectName +
                            ' report  (set '+self.descrition+')')

        # This method also accepts a path, e.g., raw=raw_path
        report.add_raw(raw=raw, title='Raw', psd=False)  # omit PSD plot

        events = self.eventExtraction(raw)
        sfreq = raw.info['sfreq']
        report.add_events(events=events, title='Events', sfreq=sfreq)

        for i in self.event_dict:
            epochs = self.epochsExtraction(
                tmin, tmax, events, raw, self.event_dict[i])
            report.add_epochs(epochs=epochs, title='Epochs'+i)

        report.save('report'+subjectName+'.html', overwrite=True)

    def makeFolderReport(self, tmin=-1, tmax=1):
        report = mne.Report(title='Dataset report '+self.descrition+'.html')
        j = 0

        for raw in self.subjects:
            # omit PSD plot
            report.add_raw(raw=raw, title=self.rawNames[j]+'  Raw ', psd=True)

            events = self.eventExtraction(raw)
            sfreq = raw.info['sfreq']
            report.add_events(
                events=events, title=self.rawNames[j]+' Events', sfreq=sfreq)

            for i in self.event_dict:
                epochs = self.epochsExtraction(
                    tmin, tmax, events, raw, self.event_dict[i])
                report.add_epochs(
                    epochs=epochs, title=self.rawNames[j]+'Epochs ('+i+')')

            j += 1
        report.save('report_'+self.descrition+'.html', overwrite=True)



######################################### ˇˇ implemented by childs classes ˇˇ ########################################


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

   