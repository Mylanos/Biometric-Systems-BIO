#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import mne
import scipy
import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np

class Visualizer:
    dataset=None
    raw=None
    rawWork=None
    events=None
    epochs=None
      
    def __init__(self, dataset):
        self.dataset = dataset
    
    def selector(self):
        def load(dir):
            try:
                self.raw=self.dataset.getIdByFile(dir)
                print(self.raw.info)
                self.raw.plot_sensors(show_names=True)
                self.croper()
            except:
                print("Nelze načíst")
                
        select=widgets.Dropdown(options=self.dataset.raw_files, description="Nahrávka:")
        widgets.interact(load, dir=select)

    def croper(self):
        def crp(val):
            self.rawWork= mne.io.Raw.copy(self.raw).crop(val[0],val[1])
            self.plotPsd()
            self.plotEEGchanelsEvents()         
            self.plotEpochs()
            self.plotExactEpoch()
            
        slider=widgets.FloatRangeSlider(min=self.raw.tmin,max=self.raw.tmax,value=[self.raw.tmin,self.raw.tmax] ,
            step=0.01,description='Ořezávač:', disabled=False, continuous_update=False, orientation='horizontal',
            readout=True, readout_format='.2f',
        )     
        widgets.interact(crp, val=slider)

    def plotEEGchanelsEvents(self,)->None:
        self.events=self.dataset.eventExtraction(self.rawWork) 
        mne.viz.plot_events(self.events, event_id=self.dataset.event_dict, sfreq=self.rawWork.info['sfreq'],
                          first_samp=self.rawWork.first_samp)   
        
        self.rawWork.plot(events=self.events,scalings='auto',block=True,)  

    def plotPsd(self)->None:
        self.rawWork.compute_psd().plot()
        
    def plotEpochs(self)->None: 
        def onSetWindow(val,ev):
            try:
                self.epochs = self.dataset.epochsExtraction(val[0],val[1],self.events, self.rawWork,{ev:self.dataset.event_dict[ev]})
                self.dataset.plotEpochs(self.epochs,self.events)
            except FileNotFoundError:
                print('Výtisk epoch se nezdařil')
        
        epSld=widgets.FloatRangeSlider(min=-10,max=10,value=[-1,1] ,step=0.1,description='Délka:', disabled=False, continuous_update=False, readout=True, readout_format='.1f',)
        eventSel= widgets.Dropdown(options=self.dataset.event_dict.keys(), description="event:")
        widgets.interact(onSetWindow, val=epSld,ev=eventSel)
        
    def printInfo(self):
        print(self.rawWork.info)
        print(self.events)
        print(self.epochs.info)
        
    def plotExactEpoch(self):
        def selected(val):
            try:
                self.epochs[val].plot_psd(picks='eeg')
                self.epochs[val].plot_image(picks='eeg', combine='mean')
            except:
                print('Výtisk epochy se nezdařil')
        
        slider=widgets.IntSlider(
            value=0,
            min=0,
            max=len(self.epochs)-1 if self.epochs!=None else 0 ,
            step=1,
            description='Č. epochy:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        widgets.interact(selected, val=slider)    
        
    def timeFreqAnalysys(self,epochs):
        frequencies = np.arange(7, 30, 3)
        power = mne.time_frequency.tfr_morlet(epochs, n_cycles=2, return_itc=False,
                                            freqs=frequencies, decim=3)
        power.plot(['MEG 1332'])
                