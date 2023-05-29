import telebot
import config
import modules.censys as censys
import modules.exploitsearch as exploitsearch
import modules.scanner as scanner
import modules.wafmod as wafmod
from restrict import restricted

# @BotFather - bot token.
bot = telebot.TeleBot(config.TOKEN_BOT)

@bot.message_handler(commands=['start'])
@restricted
def send_welcome(message):
    info=f'Hello and welcome @{message.from_user.username}.\nYour Telegram ID is {message.from_user.id}.\n\nFollow the White Rabbit :)'
    bot.send_message(message.chat.id, info)

# Extract arguments from message.
def extract_arg(arg):
    return arg.split()[1:]

# Searching for information in Censys by IP.
@bot.message_handler(commands=['searchbyip'])
@restricted
def searchbyip(message):
    try:
        IP=extract_arg(message.text)[0]
        info="\n".join(censys.SearchByIp(IP))
        bot.send_message(message.chat.id, info)
    except:
        bot.send_message(message.chat.id, "Error!")

# Searching for information in Censys by domain.
@bot.message_handler(commands=['searchbydomain'])
@restricted
def searchbydomain(message):
    try:
        domain=extract_arg(message.text)[0]
        info="\n".join(censys.SearchByDomain(domain))
        bot.send_message(message.chat.id, info)
    except:
        bot.send_message(message.chat.id, "Error!")

# Port scanner.
@bot.message_handler(commands=['scan'])
@restricted
def scan(message):
    try:
        target=extract_arg(message.text)[0]
        # Informing about the start of the scan.
        bot.send_message(message.chat.id, "Scanning Started!")
        # Scan ports and get open.
        openedports=scanner.portscan(target)
        # Convert to string.
        info="\n".join(str(port) for port in openedports)
        # Sending information about open ports.
        bot.send_message(message.chat.id, "Opened Ports\n"+info)
    except:
        bot.send_message(message.chat.id, "Error!")

# WAF test.
@bot.message_handler(commands=['waf'])
@restricted
def waf(message):
    try:
        target=extract_arg(message.text)[0]
        # If the argument contains https.
        if("https" in target):
            # Then use https and get a response.
            firewall=wafmod.wafsearch(target.replace("https://", ""), "https://")
            bot.send_message(message.chat.id, firewall)
        # If the argument contains http.
        if("http" in target):
            # Then use http and get a response.
            firewall=wafmod.wafsearch(target.replace("http://", ""), "http://")
            # Send a response.
            bot.send_message(message.chat.id, firewall)
        else:
            # If there isn't scheme, then send a message about it.
            bot.send_message(message.chat.id, "No scheme is provided, use either http or https!")
    except:
        bot.send_message(message.chat.id, "Error!")

# SearchSploit.
@bot.message_handler(commands=['searchsploit'])
@restricted
def searchsploit(message):
    try:
        # Getting a search request.
        query=" ".join(extract_arg(message.text))
        print(query)
        # Looking for exploits, getting a dictionary.
        info=exploitsearch.searchsploit(query)
        # For each exploit link...
        for exploit in info:
            # Send a link to the exploit along with the name.
            bot.send_message(message.chat.id, exploit+": "+info[exploit])
    except:
        bot.send_message(message.chat.id, "Error!")

bot.polling()