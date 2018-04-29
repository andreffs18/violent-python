# Violent Python

![https://www.goodreads.com/book/show/16192263-violent-python](https://images.gr-assets.com/books/1355072634l/16192263.jpg)

["Violent Python" by TJ O'Connor](https://www.amazon.ca/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579)
  
This repo contains exercices that I found interesting to explore from the book. I kept the book structure, altough some chapters tackle the same problems.

> In case you are searching for the original code snippets, you can find them [here](
http://booksite.elsevier.com/9781597499576/chapters.php).


 
### Chapter 1 and 2

All about penetration testing and understanding networks. Also, brute-force is fairly used. These first two chapters contain scripts to:
- Dictionary attacks
- Brute force password hash comparisons 
- Open secure zip files
- Port scanner
- SSH Botnet
- FTP Attack
- Replicate Conficker Attack

### Chapter 3 and 4

Geo-locating people and extrack meta data from apps.

- Geo-locate people using IPs and Images
- Firefox scrapper to download databases of saved cookies, download files list and past browser history
- Figure out where DDos attacks come from, from saved packets off the network

### Chapter 5
 
Manipulating Wifi packets.
- Wifi packet sniffer to find credit card number and google searches
- 802.11 protocol exploitation

### Chapter 6 and 7 

About Web Crawlers; Using Google and Twitter API and Antivirus evasion that I did not find that interesting, so nothing was added about that.



## Setup

To run all available scripts locally you must **create a new environment and install and required packages**:

```bash
$ mkvirtualenv violent-python 
$ pip install -r requirements.txt
```

> If you don't have `mkvirtualenv` installed, you can find it here: [Install **mkvirtualenv**](http://virtualenvwrapper.readthedocs.io/en/latest/index.html?highlight=install#introduction)


## License
All code here is under the MIT license.

## Disclaimer 

All code in this repo is for educational purpuses only. Some of these tools may be illegal to use on machines that you do not own or have no authorization to interact with. Use this programs at your own risk. 
