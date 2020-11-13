# Discord-Bot

This is a discord bot for discord focused on providing information relating to World of Warcraft. It accesses information using the World of Warcraft API and returns it to desired channels within a discord server.

## Features:

- Posts new additions to guild activity in specified channel
- Checks realm status and if server is down, checks every 20 seconds until it comes online, then notifies discord channel.
- Runs countdown to Shadowlands
- Requests WoW Token gold value
- Creates 3d character renders
- Creates link to raidbots quicksim with populated character information
- Checks weekly Mythic+ affixes
- Runs WoWhead searches

## Commands: 

- Each of these commands will begin with your chosen bot name. (for readme purposes we will call it "!bot"):

- Example
  - "!bot command"
- !bot help
  - lists the services that can be called by bot commands
- !bot status
  - updates the "playing" status of the bot in discord
- !bot hello
  - bot replies to sender, "Hello [author], you rat..."
- !bot wowhead
  - performs a wowhead search with entered information. Example: !bot wowhead invincible's reins
- !bot token
  - replies with current gold value of WoW tokens
- !bot showme
  - replies with 3d render of requested character. Example" !bot wowhead "character name" "character server"
- !bot affixes
  - replies with Mythic+ affixes for current week
- !bot shadowlands
  - replies with days, hours, minutes, seconds until Shadowlands release date/time.
- !bot quicksim
  - replies with link to raidbots quicksim for requested character. Example: !bot quicksim "character server" "character name"
- !bot servers
  - replies with current server status of default (or specified) server. if server is down, begins a loop which repeats until server comes online - then notifies sender.
  
  ## Setup
  
  For first time setup - complete the following check list:
  
  1. You will need to acquire a battle.net developer account & API key.
  2. You will also need a discord developer account, and to create a discord bot and invite it to your server.
  3. You will need to know the server slug for your main WoW server.
  4. You will need to know the guild slug for your WoW guild.
  5. You will need to know the channel code for the text channel you'd like to use for guild activity updates
  6. Download the code and copy it into the folder of your choice.
  7. Run the program in your text editor of choice.
  8. Follow the prompts to create the credentials file.
  9. Test your bot.
  
  
