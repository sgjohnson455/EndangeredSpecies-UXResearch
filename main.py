import pygame # frontend
import random

import csv # data collection
import time
from pathlib import Path

# Frontend Setup - Now with Pygame

# Runs local pygame instance for user data collection - this
# was easier than creating and deploying a react website in the end

# Code ----------------------------------------------

pygame.init() # start game

    # window setup
screen_height = 600
screen = pygame.display.set_mode((800, screen_height)) 
pygame.display.set_caption("Endangered Species Research") # window name
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


# GETTING original endangered species data from wikiquery (stored in originalspeciesdata.csv) -----
    # get data from csv
orig_data_path = Path("originalspeciesdata.csv") # pathname

    # open and read only line data
with open('originalspeciesdata.csv','rt', encoding='utf-8') as infile:
    headers, *data = csv.reader(infile)

    # select 2 species from the list of species
speciesidx1, speciesidx2 = random.sample(range(len(data)), 2) # pick 2 indexes from the list
left = data[speciesidx1]
right = data[speciesidx2]

    #  begin starttime
start_time = time.time()

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
species_scores_headers = ["Species", "TotalMatchups", "Wins", "Losses"]

    # only relevant for first ever run of program - adding file headers
if not user_demographics_path.exists(): 
    with open(user_demographics_path, 'w', newline='') as file: # write new file
        writer = csv.writer(file)
        writer.writerow(user_demographics_headers) 
if not global_matchups_path.exists(): 
    with open(global_matchups_path, 'w', newline='') as file: # write new file
        writer = csv.writer(file)
        writer.writerow(species_matchups_headers) 
if not global_species_scores_path.exists(): 
    with open(global_species_scores_path, 'w', newline='') as file: # write new file
        writer = csv.writer(file)
        writer.writerow(species_scores_headers)   

# PART 1 - COLLECTING USER DEMOGRAPHICS --------------------------------
# ------------------------------------

    # helper to display text for user demographics
def draw_text(text, y):
    surf = font.render(text, True, (0, 0, 0)) # create surface object "text" (in black)
    rect = surf.get_rect(center=(400, y)) # center text (parameter for height)
    screen.blit(surf, rect) # draws object

    # user input helper function (so i don't have to keep rewriting the quit thing)
def answer_collection():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    # collection helper (does the sequence of screens; use keyboard for inputs)
def collect_demographics():
    # data to collect (per specific user)
    age = None
    ICUN_familiar = None

    # Screen 1: Ask for their age range (I used a random scale)
    while age is None:
        screen.fill((255, 255, 255))

        draw_text("Press key on keyboard to answer:", screen_height/4)
        draw_text("Select your age", screen_height/2)
        draw_text("1: <18   2: 18–30   3: 31–50   4: 50+", screen_height * (3 / 4))
        pygame.display.flip() # display rendered screen

        for event in pygame.event.get(): # wait and collect answer
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    age = event.unicode
        
        clock.tick(30) # limit loop speed (computer was dying)

    while ICUN_familiar is None:
        screen.fill((255, 255, 255))

        draw_text("Press key on keyboard to answer:", screen_height/4)
        draw_text("Familiar with IUCN Red List? (Y / N)", 260)
        pygame.display.flip() # display rendered screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    ICUN_familiar = "Yes"
                if event.key == pygame.K_n:
                    ICUN_familiar = "No"

        clock.tick(30)

    return age, ICUN_familiar


# Write answers to the csv
age_group, familiar_iucn = collect_demographics()

with open(user_demographics_path, "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow([
        age_group,
        familiar_iucn
    ])


# PART 2: COLLECTING USER DATA --------------------------------------
# -----------------------------------------------------------







# End of file
pygame.quit()
