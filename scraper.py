# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:37:02 2021

@author: kneub
"""

import requests
from bs4 import BeautifulSoup
from config import Urls, UserAgents, Constants, APIs
import time
import os
import json
from PIL import Image, ImageDraw, ImageFont
import math
import tweepy

def read_webpage(URL):
    # Returns BeautifulSoup html object for a webpage
    
    page = requests.get(URL, headers={ "user-agent" : UserAgents.DEFAULT_USER_AGENT })
    
    count = 0
    while page.status_code != 200:
        time.sleep(3)
        page = requests.get(URL, headers={ "user-agent" : UserAgents.DEFAULT_USER_AGENT })
        count += 1
        
        if count > 25:
            raise NameError("Unable to load webpage")
    
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def get_overall_rank_deaths(page_number):
    # Scrap overall hcim pages for deaths
    # Output: Dictionary of { pid : name }
    
    dead_names = {}

    URL = Urls.HCIM_PAGE + str(page_number)
    soup = read_webpage(URL)
        
    name_html = soup.find_all("tr",attrs={"class":"personal-hiscores__row"})
    
    # Verify successful ping
    attempt = 1
    success = False
    while not success:
        try:
            first_name_on_page = name_html[0].text
            success = True
        except:
            print("\tWARNING: Hiscore ping failure - 60 second cooldown...")
            time.sleep(60)
            attempt += 1
            print(f"Attempt #{attempt} - trying again")    
            URL = Urls.HCIM_PAGE + str(page_number)
            soup = read_webpage(URL)
            name_html = soup.find_all("tr",attrs={"class":"personal-hiscores__row"})

    dead_html = [x.text.split('\n') for x in name_html if x.find_all(attrs={"class":"hiscore-death"}) != [] ]
    
    for death in dead_html:
        data = [x for x in death if x != '']
        if data[1].lower() in Constants.IGNORED_PLAYERS:
            continue
        pid = (data[2]+data[3]).replace(',','')
        name = data[1]
        dead_names.update({ pid : name.replace('\xa0',' ') })
        
    return dead_names

def get_individual_rank_deaths():
    # Scrap individual skill/boss pages for deaths
    # Output: List of dead names (id's are added in get_dead_names())

    dead_names = []

    # Get list of all pages to loop through
    queries = {}
    queries.update(Constants.SKILL_DICT)
    queries.update(Constants.PVM_DICT)

    # Loop through each page
    for attr, table_id in queries.items():
        if attr in Constants.SKILL_DICT.keys():
            if attr == 'Overall':
                continue
            URL = Urls.HCIM_SKILL_PAGE + str(table_id)
        if attr in Constants.PVM_DICT.keys():
            URL = Urls.HCIM_BOSS_PAGE + str(table_id)
        print(f"Searching deaths for top: '{attr}'")
        soup = read_webpage(URL)

        name_html = soup.find_all("tr", attrs={"class": "personal-hiscores__row"})

        # Verify successful ping
        attempt = 1
        success = False
        while not success:
            try:
                first_name_on_page = name_html[0].text
                success = True
            except:
                print("\tWARNING: Hiscore ping failure - 60 second cooldown...")
                time.sleep(60)
                attempt += 1
                print(f"Attempt #{attempt} - trying again")
                soup = read_webpage(URL)
                name_html = soup.find_all("tr", attrs={"class": "personal-hiscores__row"})

        dead_html = [x.text.split('\n') for x in name_html if x.find_all(attrs={"class": "hiscore-death"}) != []]

        for death in dead_html:
            data = [x for x in death if x != '']
            name = data[1].replace('\xa0',' ')
            if name.lower() in Constants.IGNORED_PLAYERS or name in dead_names:
                continue
            dead_names.append(name)

    return dead_names

def get_player_stats(name):
    # Get all player statistics from a player's hiscores page
    
    player_info = {}
    
    name = name.replace(" ", "%A0")
    URL = Urls.HCIM_PERSONAL+name
    soup = read_webpage(URL)
    
    player_data = [x.text.split('\n') for x in soup.find_all('div',attrs={'id':'contentHiscores'})][0]
    player_data = [x for x in player_data if x != '']
    
    skill_data = {}
    for skill in Constants.SKILL_DICT.keys():
        if skill not in player_data:
            continue
        skill_index = player_data.index(skill)
        skill_data.update({ skill : {} })
        skill_data[skill].update({ 'rank'  : player_data[skill_index+1] })
        skill_data[skill].update({ 'level' : player_data[skill_index+2] })
        skill_data[skill].update({ 'xp'    : player_data[skill_index+3] })
        
    pvm_data = {}
    for boss in Constants.PVM_DICT.keys():
        if boss not in player_data:
            continue
        boss_index = player_data.index(boss)
        pvm_data.update({ boss : {} })
        pvm_data[boss].update({ 'rank' : player_data[boss_index+1] })
        pvm_data[boss].update({ 'kc'   : player_data[boss_index+2] })
        
    player_info.update({ 'skills' : skill_data })
    player_info.update({ 'pvm'    : pvm_data })
    
    return player_info

def get_dead_names(filename, sleep_time=Constants.SLEEP_TIME):

    # Get dead names from overall
    dead_names = {}
    for page in range(int(Constants.MAX_RANK/25)):
        if Constants.PRINTS:
            print(f"Searching Page {page+1} - {(page+1)*25}/{Constants.MAX_RANK}")
        dead_names.update(get_overall_rank_deaths(page+1))
        time.sleep(sleep_time)

    # Get dead names from boss/skills
    deaths_ind = get_individual_rank_deaths()

    # Open DB
    with open(filename, 'r') as read_file:
        database = json.load(read_file)
    pid_list = list(database.keys())
    name_list = list(database.values())

    # Check if names are in DB
    #   If they are -> skip
    #   If they are not -> check id
    #       If id in db, update name
    #       If id not in db, add to dead_names
    updated = False
    for name in deaths_ind:
        if name in name_list:
            pos = name_list.index(name)
            dead_names.update({ pid_list[pos] : name })
            continue

        stats = get_player_stats(name)
        xp = stats['skills']['Overall']['xp'].replace(',','')
        level = stats['skills']['Overall']['level'].replace(',','')
        pid = level+xp

        dead_names.update({ pid : name })
        if pid in pid_list:
            updated = True
            print(f"Name change detected: {database[pid]} -> {name}\nUpdating...")
            database[pid] = name

    # Update name changes
    if updated:
        with open(filename, 'w') as write_file:
            json.dump(database, write_file)

    return dead_names

def generate_backsplash(file, width=0, height=0):
    # Create background image for tweet

    im = Image.open(file).convert("RGBA")

    if width == 0:
        width = im.width
    if height == 0:
        height = im.height

    new_size = (width, height)
    if im.size != new_size:
        im = im.resize(new_size)

    return im

def generate_font(size=12):
    return ImageFont.truetype("fonts/runescape_uf.ttf", size)

def create_image(name, stats):
    # Create image for tweet and populate with player stats

    # Find which backsplash to use based on # of bosses
    bosses = set(stats['pvm'])-set(Constants.SKIPPED_BOSSES)
    num_bosses = len(bosses)
    print(f"{name} is ranked in {str(num_bosses)} bosses.")
    num_cols = math.ceil(num_bosses/8)
    file = f"blankstatsheets/blankstatsheet_{str(num_cols)}.png"

    # Get backsplash
    image = generate_backsplash(file)
    image_edit = ImageDraw.Draw(image)
    skill_font = generate_font(40)
    total_font = generate_font(24)
    boss_font = generate_font(40)
    text_color = (255,255,0)

    # Loop through skills
    for skill, coords in Constants.SKILL_COORDS.items():
        try:
            level = stats['skills'][skill]['level']
            if skill != 'Overall':
                image_edit.text(coords,level,text_color,font=skill_font)
            else:
                image_edit.text(coords, level, text_color, font=total_font)
        except:
            continue

    # Add name to image
    rank = stats['skills']['Overall']['rank']
    title_str = f"{name} - Rank {rank}"
    image_edit.text((35, 533), title_str, text_color, font=total_font)

    # Loop through bosses
    x0, y0 = Constants.X_0+math.ceil(2.6*Constants.X_SEP)-2, Constants.Y_0
    x, y = x0, y0
    row_count = 0
    boss_size = (40, 40)
    for boss in stats['pvm']:
        # Catch if bosses go off image
        if x > image.width:
            print("WARNING: Image not wide enough for bosses.")
            break

        # Skip clue scrolls all
        if boss in Constants.SKIPPED_BOSSES:
            continue

        # Place boss image
        boss_name = boss.replace(':', '')
        boss_name = boss_name.replace(' ', '_')
        if os.path.exists(f"images/{boss_name}.png"):
            boss_image = Image.open(f"Images/{boss_name}.png").convert("RGBA")
            boss_image = boss_image.resize(boss_size)
            image.paste(boss_image, (x, y), mask=boss_image)
        else:
            print(f"WARNING: No boss image for {boss}")
            boss_image = Image.open("images/blank.png")
            boss_image = boss_image.resize(boss_size)
            image.paste(boss_image, (x, y))

        # Place boss kc
        kc = stats['pvm'][boss]['kc']
        image_edit.text((x+math.ceil(1.5*boss_size[0]), y), kc, text_color, font=boss_font)

        # Move position
        row_count += 1
        x_new = x
        y_new = y + Constants.Y_SEP
        if row_count == 8:
            x_new = x + Constants.X_SEP_BOSS + boss_size[0]
            y_new = y0
            row_count = 0

        x = x_new
        y = y_new

    if not os.path.exists('tweet_images'):
        os.mkdir('tweet_images')
    image.save(f"tweet_images/{name.lower().replace(' ','_')}.PNG")
    return

def create_text(name, stats):
    # Create text for tweet and populate with player stats

    # Find which backsplash to use based on # of bosses
    text = f"{name} has died!\n"
    rank = stats['skills']['Overall']['rank']
    xp = stats['skills']['Overall']['xp']

    text += f" Rank {rank} Overall with {xp} XP\n"
    text += f" -- \n"

    pvm_data = stats['pvm']

    for boss in Constants.PVM_ORDER:

        if boss in pvm_data:
            rank = stats['pvm'][boss]['rank']
            kc = stats['pvm'][boss]['kc']
        else:
            continue

        if int(rank.replace(',', '')) <= Constants.BOSS_RANK:
          text += f"Rank {rank} {boss} - {kc} KC \n"
        else:
            continue

    text += f" -- \n"

    for skill in Constants.SKILL_DICT.keys():
        if skill == 'Overall':
            continue
        rank = stats['skills'][skill]['rank']
        xp = stats['skills'][skill]['xp']
        xp = float(xp.replace(',', ''))
        xp = xp/1000000
        xp = format(xp, ".1f")

        if int(rank.replace(',', '')) <= Constants.SKILL_RANK:
          text += f"Rank {rank} {skill} - {xp}M XP\n"
        else:
            continue

    return text

def create_tweets(names, sleep_time=Constants.SLEEP_TIME):
    # Creates tweets for each new dead name

    # Loop through each name
    for name in names:
        # Get stats of player
        stats = get_player_stats(name)

        # Create image for player tweet
        create_image(name, stats)

        # Sleep for jagex pepega-ness
        time.sleep(sleep_time)

    return

def post_tweet(tweet_text, image_path):

    # Get keys
    consumer_key = APIs.TWITTER_AUTH_KEYS['consumer_key']
    consumer_secret = APIs.TWITTER_AUTH_KEYS['consumer_secret']
    access_token = APIs.TWITTER_AUTH_KEYS['access_token']
    access_token_secret = APIs.TWITTER_AUTH_KEYS['access_token_secret']

    # Authenticate and start API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #Generate text tweet with media (image)
    media_id = api.media_upload(image_path).media_id
    api.update_status(status=tweet_text, media_ids=[media_id])

    return

def write_dead_names(filename, dead_names, tweet_mode=True):
    # Write names to file if entry does not exist and create tweet image

    # Create db if it doesnt exist
    if not os.path.exists(filename):
        print(f"{filename} does not exist. Creating...")
        with open(filename, 'w') as write_file:
            json.dump(dead_names, write_file)
        return

    # Load db if it exists
    print(f"Loading database: {filename}")
    with open(filename, 'r') as read_file:
        database = json.load(read_file)

    # Find ids not in db that were found from scrape
    keys_not_in_db = set(dead_names) - set(database)
    if len(keys_not_in_db) > 0:
        print("New deaths detected.")

    # Create tweets with new deaths
    tweet_names = [dead_names[pid] for pid in keys_not_in_db]
    print(f"Found the following {str(len(tweet_names))} new deaths:")
    print(tweet_names)
    if tweet_mode:
        create_tweets(tweet_names)

    # Update database
    print("Adding new deaths to database.")
    for pid in keys_not_in_db:
        database.update({pid : dead_names[pid]})

    # Write updated data to database
    with open(filename, 'w') as write_file:
        json.dump(database, write_file)

    print("Done.")

    return tweet_names

if __name__ == "__main__":
    # Initialize/Update Database w/o tweeting
    filename = 'hcim_deaths.json'
    names = get_dead_names(filename) # Gets all dead names in criteria
    write_dead_names(filename, names, False) # Writes/updates database with above names

    # General testing
    stats = get_player_stats('Lydia Kenney')
    create_tweets(['Not the 1st', 'Lydia Kenney'])
    print(create_text('Lydia Kenney', stats))
