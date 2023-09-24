#!/usr/bin/python
# -*- coding: utf-8 -*-

from pathlib import Path
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd #TODO freeze it in case
import json 
from zipfile import ZipFile
import re
from rich.console import Console
from time import sleep

class Downloader:
    def __init__(self):
        main_folder = Path(__file__).parent.parent.resolve()
        self.raw_eeg_folder = main_folder / 'data/raw_eeg_data/'
        self.webpage_folder = main_folder / 'data/html/'
        self.downloaded_datasets = []
        self.downloaded_webpages = []
        #dict containing datafiles and links to download them
        self.datafiles = {}
        self.console = Console()
        self.webpages = {
            "dataset2.html": "https://zenodo.org/record/2348892#.Y4C_czOZOV4",
            "dataset1.html": "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/EG0LJI",
        }

    def make_dir(self, directory):
        if not os.path.isdir(directory):
            try:
                print("Creating directory...")
                os.makedirs(directory)
            except OSError:
                print("Creation of the directory %s failed" % os.path)

    def download_and_parse_html(self, header):
        #download webpages (dataset I and IV)
        for filename, web_url in self.webpages.items():
            content = None 
            if filename not in self.downloaded_webpages:
                with open(self.webpage_folder / filename, 'w') as out_file:
                    response = requests.get(web_url, headers=header)
                    out_file.write(response.text)
                    content = response.text
            else:
                with open(self.webpage_folder / filename, 'r') as out_file:
                    out_file.seek(0, 0)
                    content = out_file.read()
            if filename == "dataset1.html":
                self.parse_files_webpage1(content)
            if filename == "dataset2.html":
                self.parse_files_webpage2(content)

    def download(self):
        # check if the downloader folder exists
        self.make_dir(self.raw_eeg_folder)

        # check if the html's folder exists
        self.make_dir(self.webpage_folder)
        
        #store files already in directories, to prevent repetitive downloads
        self.downloaded_datasets = os.listdir(self.raw_eeg_folder)
        self.downloaded_webpages = os.listdir(self.webpage_folder)

        # header for gentle requests
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "sk,en-US;q=0.7,en;q=0.3",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }

        # parse data from webpages
        self.download_and_parse_html(header)

        #download zip from git (dataset III)
        self.download_git_dataset(header)


        #download files from parsed html links(dataset I and IV)
        for dataset, content in self.datafiles.items():
            dataset_folder = self.raw_eeg_folder / dataset
            # create directory for given dataset 
            self.make_dir(dataset_folder)
            tasks = [f"Task {n}:" for n in range(1, len(content) + 1)]
            # check already downloaded files
            downloaded_datafiles = os.listdir(dataset_folder)
            with self.console.status("[bold green]Downloading files...") as status:
                for item in content:
                    filename = item["name"]
                    file_url = item["contentUrl"]
                    tasks.pop(0)
                    if filename not in downloaded_datafiles:
                        with open(dataset_folder / filename, 'wb') as out_file:
                            response_stream = requests.get(file_url, headers=header, stream=True)
                            out_file.write(response_stream.content)
                        self.console.log(f"Download of {filename} complete.")
                    else:
                        self.console.log(f"{filename} already downloaded.")


    def parse_files_webpage1(self, content):
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find('script', type="application/ld+json")
            result = json.loads(links.text)
            self.datafiles["dataset1"] = result["distribution"]
        else:
            print(content)
            raise Exception("Unexpected error while parsing website!")
    
    def parse_files_webpage2(self, content):
        if content:
            url_prefix = "https://zenodo.org"
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.findAll('a', class_="filename")
            result = []
            for link in links:
                item = {}
                url_suffix = link.get('href')
                filename = os.path.basename(url_suffix).replace("?download=1", "")
                item["name"] = filename
                item["contentUrl"] = url_prefix + url_suffix
                result.append(item)
            self.datafiles["dataset2"] = result
        else:
            print(content)
            raise Exception("Unexpected error while parsing website!")

    def download_git_dataset(self, header):
        dataset_folder = self.raw_eeg_folder / "dataset3/"
        self.make_dir(dataset_folder)
        downloaded_datafiles = os.listdir(dataset_folder)
        tasks = ["Task 1:"]
        file_url = "https://github.com/mastaneht/SPIS-Resting-State-Dataset/archive/refs/heads/master.zip"

        if "master.zip" not in downloaded_datafiles:
            with self.console.status("[bold green]Downloading files...") as status:
                tasks.pop(0)
                with open(dataset_folder / "master.zip", 'wb') as out_file:
                    response_stream = requests.get(file_url, headers=header, stream=True)
                    out_file.write(response_stream.content)
                    content = response_stream.content
                self.console.log(f"Download of master.zip complete.")
        else:
            self.console.log(f"master.zip already downloaded.")

        # opening the zip file in READ mode
        with ZipFile(dataset_folder / "master.zip", 'r') as zip:
            # printing all the contents of the zip file
            #zip.printdir()
            regex_mat = ".*mat"
            regex_desc = ".*Description"
            for file in zip.namelist():
                if re.match(regex_mat, file) or re.match(regex_desc, file):
                    zip.extract(file, (dataset_folder), None)
             

