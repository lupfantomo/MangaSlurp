MangaSlurp v0.1
==========

A scraper to rip scans from MangaHere.

Requirements:
Tested on Python 2.7.6 may work on other releases.
It also requires lxml and requests, each of which can be installed through pip:

pip install lxml
pip install requests


Use:
When running MangaSlurp enter first the url of the core location of the manga on MangaHere for the first argument and the name you desire for the archived manga.  As this is only an alpha, at the moment it only takes single word names.

Example:

./Main.py http://www.mangahere.co/manga/rosario_vampire/ Rosario+Vampire
