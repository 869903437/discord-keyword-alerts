import discord
from log import log as log

def read_from_txt(path):
    # Initialize variables
    raw_lines = []
    lines = []

    # Load data from the txt file
    try:
        f = open(path, "r")
        raw_lines = f.readlines()
        f.close()

    # Raise an error if the file couldn't be found
    except:
        log('e', "Couldn't locate <" + path + ">.")
        return None

    # Parse the data
    for line in raw_lines:
        lines.append(line.strip("\n"))
    print(lines)
    # Return the data
    return lines

# Create the Discord client
client = discord.Client()

# Read which channels to monitor
active_channels = read_from_txt("channels.txt")
role_to_notify = read_from_txt("role.txt")[0]

def keyword_check(text):
    keywords = read_from_txt("keywords.txt")
    negatives = read_from_txt("negatives.txt")

    for keyword_set in keywords:
        good = False
        matches = 0
        total = len(keyword_set.split('+'))
        for keyword in keyword_set.split('+'):
            if(keyword.lower() in text.lower()):
                matches += 1
        if(matches == total):
            good = True
            break
    
    for negative in negatives:
        if(negative.lower() in text.lower()):
            good = False
            break

    if(good):
        return (True, keyword_set)
    else:
        return (False, None)

@client.event
async def on_ready():
    log('s', "Kolaveri vanthutaal >:)")

@client.event
async def on_message(message):
    # Ignore messages made by the bot
    if(message.author == client.user):
        return

    # Ignore messages not in one of the specified channels
    if(message.channel.name not in active_channels):
        return

    # Parse embed
    total_text = ""
    try:
        total_text += message.embeds[0].description
    # Issue: Non embed messages will raise an error. Solution: Ignore.
    except:
        pass

    try:
        total_text += message.embeds[0].title
    # Issue: Non embed messages will raise an error. Solution: Ignore.
    except:
        pass

    # If the keyword is found
    keyword_match = keyword_check(total_text)
    if(keyword_match[0]):
        role = discord.utils.get(message.guild.roles, name=read_from_txt("role.txt")[0])
        
        # Create an embed to notify memvers
        em = discord.Embed(description="Keyword match detected.\n" ,
                           color=11177686)
        log('i', "Detected keyword match: " + keyword_match[1])

        em.add_field(name="Keyword Matched", value=keyword_match[1])

        em.set_footer(text=message.guild.name, icon_url="https://upload.cc/i1/2020/03/23/FiD6qx.png")

        # Send the notification
        await message.channel.send(embed=em)
        
        
        if str(role) == "@everyone":
            await message.channel.send(message.guild.default_role)
        else:
            await message.channel.send(role.mention)


client.run(read_from_txt("token.txt")[0])
