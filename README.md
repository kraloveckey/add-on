# add-on
add-on is telegram bot for basic web-application analysis

# What for?
Sometimes there is no access to your main PC, where you can scan web-site and search for exploits, and you only have for e.g your phone.
Some people would say, that you can just connect with ssh, but is is not really easy to type on small screen.
This telegram bot, where it is simpler to analyse the website for further testing.

# What can it do?
1. Testing if site uses WAF.
2. Search for real IP via Censys if site uses WAF to hide it.
3. Scan IP for open ports.
4. Get additional info about services and network.
5. SearchSploit right in your telegram, to look up some exploits for further testing.

# How to use it?
To set up the bot, you need to:
1. Create a new bot at @FatherBot and get the token.
2. Place the token (TOKEN_BOT) and users ID (RESTRICTED_IDS) in config.py.
3. Run bot.py.
4. Use the bot after /start:
    ● First, let's see if the site has firewall protection: /waf https://site.com
      Answer: The site https://site.com is behind Cloudflare (Cloudflare Inc.) WAF.
    ● So there isn't point in scanning now, let's try to find the real IP and scan: /scan IP.
      Answer: Opened Ports 22 80 443
    ● Now we want to know in more detail about what is on the ports: /searchbyip IP.
    ● Let's try to find exploits for openssh VERSION: /searchsploit openssh VERSION.
      From the response, we get the following exploits suitable for the version. 

There are following command for bot:
/searchbyip IP — Gets information from search.censys.io about the IP.
/searchbydomain DOMAIN — Searches for IPS by given domain, can be usefull when site is behind WAF.
/scan IP/DOMAIN — Scan targets for opened ports, by default it scans from port 1, to 65535 with 5000 threads, you should test diffrent numbers of threads to get fastest scan time on your server.
/searchsploit NAME — Searches for exploits in exploit-db by name.