# Violent Python

![https://www.goodreads.com/book/show/16192263-violent-python](https://images.gr-assets.com/books/1355072634l/16192263.jpg)

["Violent Python" by TJ O'Connor](https://www.amazon.ca/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579)
  
This repo contains exercices that I found interesting to explore from the book. I kept the book structure, altough some chapters tackle the same problems.

> In case you are searching for the original book code snippets, you can find them [here](
http://booksite.elsevier.com/9781597499576/chapters.php).


 
### Chapter 1 and 2

All about penetration testing and understaing network. Also, brute-force is fairly used.

These first chapters contain scripts to:
- Dictionary attacks
- Brute force password hash comparisons 
- Open an secure zip files.
- Port scanner
- SSH Botnet
- FTP Attack
- Replicate Conficker Attack

### Chapter 3 and 4

Geo-locating and extrack meta data from apps.

- Geo-locate people using IPs and Images
- Firefox scrapper to download databases of saved cookies, download list and past browser history.
- Figure out where DDos attack came from from packets on the network.

### Chapter 5
 
Manipulating wiki packets
- Wifi packet sniffer to find credit card number and google searches
- 802.11 protocol exploitation

### Chapter 6 and 7 

About Web Crawlers, using Google and Twitter api and Antivirus evasion that I did not find that interesting, so nothing was added about that.



## Setup

To run all available scripts locally you must **create a new environment and install and required packages**:

```bash
$ mkvirtualenv violent-python 
$ pip install -r requirements.txt
```

## License

## Disclaimer 
