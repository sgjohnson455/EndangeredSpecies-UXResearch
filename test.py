# where i'm testing my code

import pygame # frontend
import random

import csv # data collection
import time
from pathlib import Path

# STORING collected data ------
    # setting folder path
collected_data_path = Path("collected_data") # results stored in 'collected_data' folder
collected_data_path.mkdir(exist_ok=True)

    # setting data paths for specific data
user_demographics_path = Path(collected_data_path / "user_demographics.csv") # stores user demographic data
global_matchups_path = Path(collected_data_path / "species_matchup_data.csv") # stores global matchup data
global_species_scores_path = Path(collected_data_path / "species_individual_scores.csv") # stores pickrate for each species

    # header definitions
user_demographics_headers = ["Age", "Familiar with ICUN Red List"]
species_matchups_headers = ["UserIndex", "SpeciesA", "SpeciesB", "Winner", "TimeTaken"]
species_scores_headers = ["Species", "TotalMatchups", "Wins"]

    # only relevant for first ever run of program - adding file headers
if not user_demographics_path.exists(): 
    with open(user_demographics_path, 'w', newline='', encoding="utf-8") as file: # write new file
        writer = csv.writer(file)
        writer.writerow(user_demographics_headers) 
if not global_matchups_path.exists(): 
    with open(global_matchups_path, 'w', newline='', encoding="utf-8") as file: # write new file
        writer = csv.writer(file)
        writer.writerow(species_matchups_headers) 
if not global_species_scores_path.exists(): 
    with open(global_species_scores_path, 'w', newline='', encoding="utf-8") as file: # write new file
        writer = csv.writer(file)
        writer.writerow(species_scores_headers)   



#  MY TESTS ///////////////////////////////////////////////////



def format_commmon_names(names):
    formatted = []

    for name in names.split(","): # split and clean
        cleaned = name.strip()
        
        caps = []

        for word in cleaned.split():
            caps.append(word.capitalize())

        whole_word = " ".join(caps) # join parts of the same name

        formatted.append(whole_word)
    return formatted # return list of names to display

print(format_commmon_names("Bawean deer, Bawean Deer, Bawean Hog Deer, Kuhl's Hog Deer, Kuhl’s Hog Deer"))