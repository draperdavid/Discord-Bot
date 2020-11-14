# Imports
import discord
import datetime
from bs4 import BeautifulSoup
import requests
import random
import os
import json
import time
import asyncio
import difflib

# Set basic bot information
cwd = os.path.dirname(__file__)

# First time setup - create personalized JSON credentials file
my_creds = os.path.join(cwd, 'my_creds.json')

if os.path.exists(my_creds):
    print('Credentials Acquired...')
    exit
else:
    with open(my_creds, 'w+') as my_creds:

        bot_token = input("Add your Discord bot's API Token: ")
        disc_bot = input("Add your Discord bot's name (start with '!'): ")
        client_id = input("Add your WoW API client ID: ")
        client_secret = input("Add your WoW API client secret: ")
        guild_activity_channel = input("Add your Guild Activity Text Channel ID: ")
        default_server_slug = input("Add your default WoW server slug: ")
        guild_slug = input("Add your guild slug: ")

        credentials_list = {"client_id": str(client_id), "client_secret": str(client_secret), "bot_token": str(bot_token), "discbot_name": str(disc_bot), 
        "guild_activity_channel": int(guild_activity_channel), "default_server_slug": str(default_server_slug), "guild_slug": str(guild_slug)}

        # Write to JSON
        json.dump(credentials_list, my_creds, indent=2)

# Get personalized bot information from JSON credentials file
with open(my_creds, 'r') as f:
    creds_file = f.read()
    creds = json.loads(creds_file)

bot_token = creds['bot_token']
disc_bot = creds['discbot_name']
client_id = creds['client_id']
client_secret = creds['client_secret']
guild_activity_channel = creds['guild_activity_channel']
default_server_slug = creds['default_server_slug']
guild_slug = creds['guild_slug']

# # API URL
token_url = 'https://us.battle.net/oauth/token'

# Function to get current/refresh token
def generate_token():
    global my_token
    data = {'grant_type': 'client_credentials'}
    # Fetch token response
    response = requests.post(token_url, data=data, auth=(client_id, client_secret))
    # Read response as json
    token = response.json()
    # Set variable from json response
    my_token = token['access_token']
    return my_token

# Create discord bot
client = discord.Client()

# Create server status object for bot
wow_server = False

# Set datetime
now = datetime.datetime.now()

# Bot "playing" status game list
game_list = [
    'Super Mario Bros 3',
    'Among Us, and is definitely not the imposter',
    'The Legend of Zelda: Ocarina of Time',
    'Halo 2: Team Slayer on Lockout',
    'Donkey Kong Country',
    'Tony Hawks Pro Skater',
    'Crash Team Racing',
    'Soulcalibur',
    'Sonic Adventure 2',
    'Power Stone',
    'NFL Blitz',
    'Quake III Arena',
    'Hydro Thunder',
    'Final Fantasy X',
    'The Elder Scrolls V: Skyrim',
    'Gears of War 2',
    'Shower With Your Dad Simulator',
    'Portal',
    'Street Figher II',
    'F-Zero',
    'Star Fox 64',
    'Wave Race',
    'Star Wars: Rogue Squadron',
    'Pokemon Stadium',
    'Mario Party',
    'Doom 64',
    'GoldenEye 007',
    "Playerunknown's Battlegrounds",
    'League of Legends',
    'World of Warcraft (Never Classic)',
    'Fall Guys',
    'Sea of Thieves',
    'ARK: Survival Evolved',
    'Grounded',
    'Horizon Zero Dawn',
    'Call of Duty: Blackops',
    '1080 Snowboarding',
    'Rocket League',
    'Escape From Tarkov',
]

# Creat function to compare existing file and new JSON for "guild_activity"
def compare_array(guild_activity_file, guild_activities):
    if not guild_activity_file:
        new_activities = guild_activities
        return new_activities
    else:
        new_activities = [i for i in guild_activities if i not in guild_activity_file]
        return new_activities

# Guild Activity Feed
async def guild_activity(guild_activity_channel):
    generate_token()
    
    # Set path
    guild_activity = os.path.join(cwd, 'guildactivity.json')

    # Check if Guild Activity File Exists
    if os.path.exists(guild_activity):
        print("Guild Activity File Verified...")
        exit
    
    # If no Guild Activity File, Create Guild Activity File from current JSON
    elif not os.path.exists(guild_activity):
        with open(guild_activity, "w+") as guild_activity_file:
        
            guild_activity_api = (f"https://us.api.blizzard.com/data/wow/guild/{default_server_slug}/{guild_slug}/activity?namespace=profile-us&locale=en_US&access_token={my_token}") 
            guild_activity_req = requests.get(guild_activity_api)
            guild_activity_j = guild_activity_req.json()

            json.dump(guild_activity_j['activities'], guild_activity_file, indent=2)

            print("Guild Activity File Created...")

    # Create Loop
    while True:
        # Retrieve Guild Activity Feed
        guild_activity_api = (f"https://us.api.blizzard.com/data/wow/guild/{default_server_slug}/{guild_slug}/activity?namespace=profile-us&locale=en_US&access_token={my_token}") 
        guild_activity_req = requests.get(guild_activity_api)
        guild_activity_j = guild_activity_req.json()

        # Open Guild Activity JSON file
        with open(guild_activity, 'r') as f:
            my_f = f.read()

            guild_activity_read = json.loads(my_f)

        # Compare API result to Old Guild Activity JSON
        new_achieves = compare_array(guild_activity_read, guild_activity_j['activities'])
        
        if new_achieves:

            # Get Achievement details from JSON
            for new_achieve in new_achieves:

                # Get latest guild activity achievement character
                guild_activity_latest = new_achieve['character_achievement']['character']['name']

                # Get latest guild activity achievement
                guild_activity_latest_achiev = new_achieve['character_achievement']['achievement']['name']

                # Get latest guild activity timestamp
                guild_activity_latest_time = new_achieve['timestamp']

                # Convert timestamp to date and time
                guild_time = datetime.datetime.fromtimestamp(guild_activity_latest_time / 1000)

            # Print to Guild-Activity Channel
            channel = client.get_channel(guild_activity_channel)
            await channel.send(f'{guild_activity_latest}: {guild_activity_latest_achiev} ' '(' f'{guild_time}' ')')

            # Print to JSON file
            with open(guild_activity, 'w+') as guild_activity_file:
                json.dump(guild_activity_j['activities'], guild_activity_file, indent=2)

        # Notify in terminal
        print('Guild Activity File Updated', datetime.datetime.now())
        await asyncio.sleep(600)

# Weekly Mythic+ Affixes Request
async def weekly_affixes(message):
    affixes = "https://raider.io/api/v1/mythic-plus/affixes?region=us"
    affixes_req = requests.get(affixes)
    affixes_j = affixes_req.json()

    # Set Variables
    real_weekly_affixes = affixes_j['title']

    # Send reply to discord
    await message.channel.send('{0.author.mention} The weekly Mythic+ affixes are: ' f'{real_weekly_affixes}' '.'.format(message))

# Bot Status Update
async def status_update():
    await client.wait_until_ready()
    while True:

        # Changes Bot Game Playing Status
        await client.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(game_list)))
        print('status updated', datetime.datetime.now())
        
        # Chooses new game at random time between 1 hour and 10 hours
        await asyncio.sleep(random.randrange(3600, 36000))

# WoW Token Request
async def wow_token(message):
    generate_token()

    wow_token_api = "https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token=" + my_token
    wow_token_req = requests.get(wow_token_api)
    wow_token_j = wow_token_req.json()

    # Set Variables
    wow_token_price = wow_token_j['price']

    # Format wow token price to gold
    wow_token_price_final = "{:,}".format(int(wow_token_price / 10000))

    # Send reply to discord
    await message.channel.send('{0.author.mention} WoW Tokens are currently: ' f'{wow_token_price_final}' 'g'.format(message))

# WoW Character Render Request
async def character_render(message, char_render, render_server):
    generate_token()

    # API Call
    char_render_api = (f"https://us.api.blizzard.com/profile/wow/character/{render_server}/{char_render}/character-media?namespace=profile-us&locale=en_US&access_token={my_token}")
    char_render_req = requests.get(char_render_api)
    char_render_j = char_render_req.json()

    if "code" in char_render_j:
        print('Error code: ', char_render_j["code"])
        print('Realm Detail: ', char_render_j["detail"])
        await message.channel.send('{0.author.mention}'f' {default_server_slug} isnt a server or {char_render} isnt a character, dumbass...'.format(message))
        return
    else:
        # Set Variable
        character_render_link = char_render_j['assets'][3]['value']

        # Send reply to discord
        await message.channel.send('{0.author.mention}, Here is your character: ' f'{character_render_link}'.format(message))

# Server Status Request
async def server_status(slug, message):
    global wow_server

    # Execute function
    generate_token()

    # Search for server realm by slug
    realm_api = "https://us.api.blizzard.com/data/wow/realm/" + slug + "?namespace=dynamic-us&locale=en_US&access_token=" + my_token
    realm_req = requests.get(realm_api)
    realm_j = realm_req.json()

    # Check if entered realm is valid
    if "code" in realm_j:
        print('Error code: ', realm_j["code"])
        print('Realm Detail: ', realm_j["detail"])
        wow_server = 'Invalid'
        await message.channel.send('{0.author.mention}'f' {default_server_slug} isnt a server...'.format(message))
        return
    else:
        # Lookup the selected realm connected-realm ID
        url = realm_j['connected_realm']['href'] + "&locale=en_US&access_token=" + my_token

        # Fetch info from Blizzard
        req = requests.get(url)

        # Read req as json
        json_req = req.json()

        # Set variables from the json results
        status = json_req['status']['name']
        realms = json_req['realms']

        if status == 'Up':
            wow_server = True

            # Send reply to discord
            await message.channel.send('{0.author.mention} ' f'{default_server_slug} is up nerd! Go play!'.format(message))
        else:
            wow_server = False

            # Send reply to discord
            await message.channel.send('{0.author.mention} 'f' {default_server_slug} is Down, I will notify you when the server comes online.'.format(message))

        # Get connected-realm group status
        i = 0
        while wow_server is False:
            i += 1

            # Fetch info from Blizzard
            req = requests.get(url)
            
            # Read req as json
            json_req = req.json()

            # Set variables from the json results
            status = json_req['status']['name']
            realms = json_req['realms']
            print([realm['name'] for realm in realms])

            # Checks server status every 20 seconds until verifying server is online
            if status == 'Down':
                print(f"The above realms are {status}.")
                print("This updates every 20 seconds. Number of updates: " + str(i))
                await asyncio.sleep(20)

            # Verifies server is online
            else:
                print(f"The above realms are {status}.")
                wow_server = True

                # Send reply to discord
                await message.channel.send('{0.author.mention}' f'{default_server_slug} is up nerd! Go play!'.format(message))
                break

# Bot Commands & Interactions
@client.event
async def on_message(message):
    global default_server_slug

    # Convert messages to lower case
    message_to_lower = message.content.lower()

    # Insures bot doesn't speak to itself
    if message.author == client.user:
        return
      
    # Check message to see if it's calling me
    if message_to_lower.startswith(disc_bot):

        # Remove !botname and remove leading whitespace
        bot_command = (message_to_lower.replace(disc_bot, '')).lstrip()

        #  After this point command check will determine what command if any is used

        # WoWhead Database Search
        if bot_command.startswith('wowhead'):
            search = bot_command.replace('wowhead ', '')
            search_final = ((search.strip()).replace(" ","+"))
            await message.channel.send('{0.author.mention} : ' f'https://www.wowhead.com/search?q={search_final}'.format(message))

        # Basic Hello message from bot
        if bot_command.startswith('hello'):
            await message.channel.send('Hello {0.author.mention}, you rat...'.format(message))

        # Weekly Affixes
        if bot_command.startswith('affixes'):
            await weekly_affixes(message)

        # Raider.io
        if bot_command.startswith('raiderio'):
            raider_info = (bot_command.replace('raiderio', '')).lstrip()
            raider_character_info = raider_info.split(" ", 1)
            raider_character = raider_character_info[0]
            raider_server = raider_character_info[1]

            await message.channel.send('{0.author.mention} Here is the Raider.io profile: ' f'https://raider.io/characters/us/{raider_server}/{raider_character}'.format(message))

        # Raw Character Render Request
        if bot_command.startswith('showme'):
            render_info = (bot_command.replace('showme', '')).lstrip()
            char_render_info = render_info.split(" ", 1)
            char_render = char_render_info[0]
            render_server = ((char_render_info[1].strip()).replace("'","")).replace(' ','-')
            
            await character_render(message, char_render, render_server)

        # Request Raidbots quick sim URL
        if bot_command.startswith('quicksim'):
            info = (bot_command.replace('quicksim', '')).lstrip()
            charinfo = info.split(" ", 1)
            char_server = charinfo[0]
            char_name = charinfo[1]

            quick_sim = (f'https://www.raidbots.com/simbot/quick?region=us&realm={char_server}&name={char_name}')

            # Send reply to discord
            await message.channel.send('{0.author.mention} Your quicksim url is: ' f'{quick_sim}'.format(message))

        # Shadowlands Countdown -  Counts seconds between current date/time and shadowlands release
        if bot_command.startswith('shadowlands countdown') or bot_command.startswith('shadowlands'):

            futuredate = datetime.datetime.strptime('Nov 23 2020 18:00', '%b %d %Y %H:%M')
            nowdate = datetime.datetime.now()
            count = int((futuredate - nowdate).total_seconds())
            days = count // 86400
            hours = (count - days * 86400) // 3600
            minutes = (count - days * 86400 - hours * 3600) // 60
            seconds = count - days * 86400 - hours * 3600 - minutes * 60

            SL_Countdown = "{} days {} hours {} minutes {} seconds left until Shadowlands!".format(days, hours, minutes,
                                                                                                   seconds)
            
            # Send reply to discord
            await message.channel.send(SL_Countdown)

        # What should I play
        if bot_command.startswith('what should i play?'):
            await message.channel.send('A rat like you, {0.author.mention} ...how should I know?'.format(message))

        # Check WoW Token Price
        if bot_command.startswith('token'):
            await wow_token(message)    

        # Checks WoW server status and notifies discord channel via bot if server is up or down.
        if bot_command.startswith('servers'):
            await message.channel.send('Checking...')

            # Strips input to server slug - replaces specified command with stripped input
            realminfo = bot_command.replace('servers','')
            if realminfo != '':
                default_server_slug = ((realminfo.strip()).replace("'","")).replace(' ','-')

            # Execute server_status function
            await server_status(default_server_slug, message)

        # Gives list of possible commands
        if bot_command.startswith('help'):
            await message.channel.send('I only respond to: "hello", "servers", "status", "token", "shadowlands", "affixes", "quicksim server character", "showme character server", "wowhead", "raiderio character server')

        # Change Bot Status
        if bot_command.startswith('status'):
            await client.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(game_list)))
            print('status updated', datetime.datetime.now())

# Ready Check
@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print(now)
    print('------------------------------------------------------')

    # Start guild activity loop
    await guild_activity(guild_activity_channel)

client.loop.create_task(status_update())
client.run(bot_token)