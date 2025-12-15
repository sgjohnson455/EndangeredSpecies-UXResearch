import pygame # frontend
import random

import csv # data collection
import time
from pathlib import Path

# Prep for the Research Game //////////////////////////////
# //////////////////////////////////////

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
species_matchups_headers = ["UserIndex", "SpeciesA", "SpeciesB", "Winner", "TimeTaken(Seconds)"]
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

    # get user index (relevant for parts 1 and 2)
userIdx = 1
with open(user_demographics_path,'rt', encoding='utf-8') as infile:
    headers, *data = csv.reader(infile)
    userIdx = len(data) + 1 # gets us the current user index (last filled index + 1)


# End of prep

# Frontend Setup - Now with Pygame

# Runs local pygame instance for user data collection - this
# was easier than creating and deploying a react website in the end

# Code ----------------------------------------------

pygame.init() # start game

    # window setup
screen_height = 600
screen_width = 800
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Endangered Species Research") # window name
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# PART 1 - COLLECTING USER DEMOGRAPHICS --------------------------------
# ------------------------------------

    # helper to display text for user demographics
def draw_text(text, y, x = 400):
    surf = font.render(text, True, (0, 0, 0)) # create surface object "text" (in black)
    rect = surf.get_rect(center=(x, y)) # center text (parameter for height)
    screen.blit(surf, rect) # draws object
    
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

    # helper to append csv
# species_matchups_headers = ["UserIndex", "SpeciesA", "SpeciesB", "Winner", "TimeTaken"]
def write_species_winner(userIdx, speciesA, speciesB, winner, timeTaken):
    with open(global_matchups_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            userIdx,
            speciesA,
            speciesB,
            winner,
            timeTaken
            
    ])

    # helper to update csv data for species (that have data)
# species_scores_headers = ["Species", "TotalMatchups", "Wins"]
def write_species_scores(species, win):
    # get correct index
    species_idx = -1 
    rows = []
# read existing data
    with open(global_species_scores_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)

        for i, row in enumerate(reader):
            rows.append(row)
            if row[0] == species:
                species_idx = i

    # if species does not exist, add it
    if species_idx == -1:
        rows.append([
            species,
            "1",                  # totalMatchups
            "1" if win else "0"    # Wins
        ])
    else:
        # update existing row
        rows[species_idx][1] = str(int(rows[species_idx][1]) + 1)  # total matchups
        if win:
            rows[species_idx][2] = str(int(rows[species_idx][2]) + 1)

    # write everything back ot the original file
    with open(global_species_scores_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


    # (all animal access is using the random 2 indexes)

def format_commmon_names(names):
    formatted = []

    for name in names.split(","): # split and clean
        cleaned = name.strip()
        
        caps = []

        for word in cleaned.split():
            caps.append(word.capitalize())

        whole_word = " ".join(caps) # join parts of the same name

        # check if the name is already there (there are duplicates)
        dupe = False
        for word in formatted:
            if word == whole_word:
                dupe = True
                break
        if not dupe:
            formatted.append(whole_word)

    return formatted # return list of names to display

def display_formatted_names(name_list, x, y):
    for i, name in enumerate(name_list):
        draw_text(name, y + i * 25, x)

def collect_animal_choice(times, totalTimes):

# GETTING original endangered species data from wikiquery (stored in originalspeciesdata.csv) -----
    # get data from csv
    orig_data_path = Path("originalspeciesdata.csv") # pathname

    # open and read only line data
    with open('originalspeciesdata.csv','rt', encoding='utf-8') as infile:
        headers, *data = csv.reader(infile)

    # select 2 species from the list of species
    s_idx1, s_idx2 = random.sample(range(len(data)), 2) # pick 2 indexes from the list
    left = data[s_idx1][3]
    right = data[s_idx2][3]

    formatted_left = format_commmon_names(left)
    formatted_right = format_commmon_names(right)

    # track if user has responded to restart the loop
    question_answered = False

    while question_answered is False:
        screen.fill((255, 255, 255))

        draw_text("Press key on keyboard to answer:", screen_height/8)
        draw_text("Question " + str(times) + "/ " + str(totalTimes), screen_height/4)
        
        display_formatted_names(formatted_left, screen_width * 1/4, screen_height/2)
        display_formatted_names(formatted_right, screen_width * 3/4, screen_height/2)

        pygame.display.flip() # display rendered screen

         #  begin starttime
        timeStart = time.time()

        for event in pygame.event.get(): # wait and collect answer
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # speciesA won
                    write_species_scores(left, True)
                    write_species_scores(right, False)

                    # update matchup instance
                    write_species_winner(userIdx, left, right, 'A', round(time.time() - timeStart, 3))
                    question_answered = True
                if event.key == pygame.K_2:

                    write_species_scores(left, False)
                    write_species_scores(right, True)

                    # update matchup instance
                    write_species_winner(userIdx, left, right, 'B', round(time.time() - timeStart, 3))
                    question_answered = True

        
        clock.tick(30) # limit loop speed (again)


# RUN the second part of the game:
totalRounds = 20
for i in range(totalRounds):
    collect_animal_choice(i, totalRounds)

# End of file/game
pygame.quit()
