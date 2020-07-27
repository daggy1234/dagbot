"""
    Dagbot is a discord meme bot that does nothing useful
    Copyright (C) 2020  Daggy1234

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
cmdhelp = {
    "clapify": "*inert slow clap*",
    "monospace": "adds a black box around text to make it fancy",
    "under": "__underlines text__",
    "blue": "makes text blue in color",
    "orange": "makes text orange in color",
    "yellow": "makes text yellow color",
    "green": "makes text green in color",
    "cyan": "makes text cyan in color",
    "red": "makes text red",
    "spoiler": "text in a black box to click",
    "box": "puts text in a BBB",
    "bold": "**makes text bold**",
    "italics": "*puts text in italics*",
    "striked": "~~strikes the text~~",
    "emojify": "every letter is replaced by an emoji",
    "ping": "SHows the bot's latency",
    "test": "testing.....testing..123",
    "dadjoke": "A joke only a dad would tell",
    "yomama": "insult yo mama",
    "cn": "I <3 chcuk norris",
    "joke": "Random joke to make you :kek:",
    "highfive": "initiate the high5",
    "udef": "gets an urban dictionary definiton",
    "bacon": "play the oracle of bacon sand get the bacon number of an actor",
    "gif": "get a gif menu for a query",
    "cf": "geta fun fact about a cat",
    "nou": "UNO REVERSE CARD",
    "wrongopinion": "bruh",
    "f": "f in the chat for thing",
    "hug": "give a user a big hug",
    "advice": "get advice from Dagbot",
    "slap": "give a user a big slap",
    "rate": "Have me rate someone **everything final**",
    "rps": "rock-paper-Scissors-shoot",
    "russianroulette": "lets dance with death",
    "trivia": "MCQ trivia",
    "jeopardy": "Fun game",
    "hangman": "Use hangman help",
    "numgame": "fun number guessing game",
    "google": "get a google search result",
    "weather": "get live weather of a city",
    "randomint": "random integer is generated",
    "taco": "random taco recipe",
    "wikipedia": "get wikipedia results",
    "youtube": "get a you tube result for a query",
    "define": "get a dictionary define for word",
    "quote": "famous quote from database",
    "hp": "use hp help for harry potter",
    "fact": "get a kickass fact",
    "numfact": "get a random number fact",
    "numsearch": "get a number fact for a particluar number",
    "pokedex": "get pokedex info for pokemon",
    "poem": "get a poem from a title",
    "meme": " random meme from a  meme subreddit",
    "sub": "Gets content from a random subreddit! supply the sub and time(optional)",
    "thought": "r/Showerthoughts",
    "facepalm": "r/facepalm",
    "meirl": "r/meirl",
    "askreddit": "r/AskReddit",
    "greentext": "from r/greentext",
    "rip": "f in the chat for thing",
    "reverse": "!poow ,ffuts esreveR",
    "reaction": "get your slow ass reaction time",
    "yoda": "Yoda speak, you will get",
    "oeis": "Online Encyclopedia of Integer Sequences",
    "aww": "r/aww",
    "dex": "r/DankExchange",
    "pun": "r/puns",
    "starwarsmeme": "r/PrequelMemes",
    "discord": "r/Discordmemes",
    "comic": "r/comics",
    "copypasta": "r/copypasta",
    "prefix": "commands to help you modify or see the prefix (prefix help)",
    "suggest": "add a suggestion for Dagbot",
    "bug": "report a bug in Dagbot",
    "weebhug": "hugs, only with weeby anime",
    "encrypt": "returns encrypted text for a string",
    "decrypt": "can be used to decrypt encrypted text",
    "headlinegame": "guess wether a headline is false or true",
    "chat": "interact with an ai powered chatbot.",
    "drake": "let Dagbot help you make the famous drake meme",
    "cog": "allows a user to control which commands are allowed or not",
    "xkcd": "random xkcd comic",
    "art": "gets textart for a specific type (keyword)",
    "randomart": "gets a random textart",
    "ascii": "makes your text asciified",
    "randomfont": "gives a random font to your text",
    "fontify": "you give the font and we apply that font",
    "create": "create amazing memes from 100+ templates! view available options using `createmenu`",
    "createmenu": "View available templates and how to use ",
    "Dagbotmeme": "Memes from just r/memes and r/dankmemes",
}

grouphelp = {
    "tag": """`tags`:
`tag <name>`: has the bot output the content of the tag
`tag create <name> <content>`: stores tga with the content
`tag update <name> <content>`: changes the content of tag
`tag rename <name> <newname>`: changes the name of a tag
`tag delete <name> `: deletes the tag only if you created it
`tag info <name>`: gets the information about a particluar tag
`tag list <member>`: gets a list of all of a members tags (mention them {sorry but ping}) """,
    "cog": """`Cog Commands`:
A cog is a command category, you can enable or disable cogs and all of the commands inside them. Use the help menu to see all the available cogs. NOTE Meta and Help cogs cannot be disabled.
`cog enable <cog> `: enables the cog to be used
`cog disable <cog>` : disabled the cog
`cog status <cog>`: shows teh status on wether a cog is enabled or disabled""",
    "hp": """`Harry Potter API`,
`hp char <character>` : gets character information
`hp spell <spell> `: gets information about spell    """,
    "prefix": """
`prefix`: mention Dagbot or just use the prefix command to get the prefix
`prefix help` To get info about orefix related commands
""","hangman":"""
`DAGBOT hangman\nCatgeories:\nmovies\nword\nanimals\nthing\ncountry\n just enter cancel to terminate the game. `
"""
}


emojilist = {
    "text": "\U0001f1f9",
    "games": "\U0001f3b2",
    "reddit": "\U0001f534",
    "image": "\U0001f5bc",
    "util": "\U0001f5a5",
    "smart": "\U0001f9e0",
    "fun": "\U0001f973",
    "animals": "\U0001f436",
    "help": "\U00002753",
    "tags": "\U0001f4c1",
    "misc": "\U0001f6e0",
    "memes": "\U0001f58d",
    "Jishaku": "\U000026a0",
    "ai": "\U0001f916",
    "settings": "\U00002699",
}
notfoundelist = [
    "Error 404: That member does not exist",
    "Hey see the member list  and find dude I actually know ",
    "Imaginary members and your imaginary gf sound like a dream team",
    "I don't have enough sentience to understand what you're saying so please find a real dude",
    "Buddy, you're mistaken if you think I know what you want me to do based on that",
    "Quit wastin' my time with your fake Members. You're eating up my bandwidth",
    "I don't know if you bother reading these but please focus on your keyboard and type members correctly",
    "Stop making errors on purpose! I'm running out of witty one-liners for errors",
    "The person you have mentioned....... Does not exist....... Please try again later",
    "I cannot make people out of thin air smh",
    "Please mention some actual people and not your imaginary friends",
]
missingargs = [
    "Hey, you lazy bum! Add some arguments first, 'kay?",
    "Learn how to type in the correct info ,doof",
    "I am a bot, I do not understand idiots who CANNOT TYPE IN EVERYTHING REQUIRED",
    "Buddy, you're mistaken if you think I know what you want me to do based on that",
    "How bout we try that again ",
    "I don't know if you bother reading these but please focus on your keyboard and type parameters correctly",
    "Stop making errors on purpose! I'm running out of witty one-liners for errors",
    "If do not have arguments, I wonder what else you do not have",
    "Oh boy! Here I go teaching humands how to type again",
]
cooldowncom = [
    "Bruh chill tf out I need a break gimme about ",
    "Slow your roll buddy these take a lot of energy to do and I'm lazy so can you wait for ",
    "Bruh, can you chill and do a vibe check, I’ll be here in ",
    "I have to use the toilet brb in ",
    "Running kinda hot right now. Lemme Cooldown a bit",
]
missingperms = [
    "Come back when you have real power to do this ",
    "Are you really in charge here?",
    "I will wait for the  return of the king",
    "Hmmm stop acting like my boss",
    "Ngl I am not wasting my time  on you.Come back with more power",
]
concur = [
    "I am running at 100%",
    "Too much happening......Process Overload",
    "BEEP BOOP , I AM A BOT NOT  FRICKIN GOD",
    "Roses are red\nViolets are blue\nI am kinda busy atm\nTry again soon",
    "The Command you have used.... Is being used by someone else...... You may Try again or wait untill later",
    "I'm ghosting you for some time.",
    "Can you like not be so desperate and wait your turn?",
]
