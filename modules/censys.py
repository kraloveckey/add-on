# Library for creating a request.
import requests
# Library for formatting.
import re
# Library for parsing.
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

# Search for information in Censys by IP.
def SearchByIp(target):

    # Sheet, where we will store all the dug up information.
    infos=[]

    # Variable that Censys doesn't detect that we're a bot.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
    }
    i=0

    # Request to the site, all Censys links look like: https://search.censys.io/hosts/{TARGET}, we make a request along with a header and get a response.
    response = requests.get(f'''https://search.censys.io/hosts/{target}''', headers=headers)

    # We need to use response.content, it contains the data that Censys sends to us when processing the request.
    soup = BeautifulSoup(response.content, "html.parser")

    # We use BeautifulSoup to convert the data to another format and store it in the soup variable.
    # Having studied the page through F12, we will understand that the data we need regarding IP is stored in 'content', 
    # BeautifulSoup has the ability to search by id, use it.
    results = soup.find(id="content")

    # Find the ports and protocol that Censys detected, we will do this using a search by class.
    ports = results.find_all("div", class_="protocol-details")

    # We need to go through each port and do some transformations, format the strings a bit and get normal data.
    for port in ports:
        soup = BeautifulSoup(str(port), features="lxml")
        results = soup.h2
        results = str(results.text)
        results = results.replace(" ", "")
        results = results.split('\n')
        infos.append("Protocol:"+" "+results[1].split("/")[1]+" "+"is on port:"+" "+results[1].split("/")[0])
 
    # Redefine the soup variable and look for content.
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="content")

    # Let's try to find much more interesting information, such as:
    # OS information, network information, routing information.
    # And of course, services on ports and their version.
    try:
        dl_data = results.find('dt', string='OS').find_next_siblings('dd')
        infos.append("OS:"+dl_data[0].string.replace("\n", ""))
    except:
        infos.append("OS Can't be specified!")
    try:
        dl_data = results.find('dt', string='Network').find_next_siblings('dd')
        infos.append("Network:"+dl_data[0].text.replace(" ", "").replace("\n", ""))
    except:
        infos.append("Network Can't be specified!")
    try:
        dl_data = results.find('dt', string='Routing').find_next_siblings('dd')
        infos.append("Routing:"+dl_data[0].text.replace(" ", "").replace("\n", ""))
    except:
        infos.append("Routing Can't be specified!")
    ports=results.find_all("div", class_="protocol-details")

    # Again we go through each port and look for services.
    for portservice in ports:
        portlist=(portservice.find_next_siblings("div", class_="host-section"))
        port=re.sub('\n\n', '\n', portlist[0].text)
        port=re.sub(' +', ' ', port)
        port=port.split("\n")
        infos.append(portservice.text.split("\n")[2].replace(" ", "")+":")
        for el in port:
            if el!='' and el!=' ' and "\r" not in el and "\n" not in el:
                if(el.startswith(" ")==True):
                    infos.append(el.replace(" ", "-", 1))
                if(el.startswith(" ")==False):
                    infos.append(el+":")
            elif(el!=' '):
                infos.append(el)
    # Return variable.
    return(infos)

# Sometimes a site hides its IP through the same WAF.
# Censys has a search and it supports searching by domains, we implement this search in the function.
def SearchByDomain(target):
    # We will store all found IP in a variable.
    addr=[]
    # Like last time, let's set headers.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://search.censys.io/search?resource=hosts&q=artscp.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
    }
    # Also need to set additional search parameters.
    params = (
        ('resource', 'hosts'),
        ('q', f''' services.tls.certificates.leaf_data.names: {target}''')
    )
    # Now we make a request to the server along with all the parameters and headers.
    response = requests.get('https://search.censys.io/_search', headers=headers, params=params)
    # We need to start parsing, similarly with the previous function, use response.text.
    soup = BeautifulSoup(response.text, "html.parser")
    results=soup.text.replace("\n", "")
    results=re.sub(' +', ' ', results)
    results=results.split(" ")
    for result in results:
        preresult=str(result).replace("\n", "")
        preresult=preresult.replace(" ", "")
        resultis=(preresult.split("\n"))
        if(any(c.isalpha() for c in resultis[0])==False and ")" not in resultis[0] and resultis[0]!=""):
            addr.append(resultis[0])
    return(addr)

# It is necessary that when importing a file, all functions are not executed, but only the necessary ones are simply called.   
if __name__ == "__main__":
    SearchByDomain(target)
    SearchByIp(target)