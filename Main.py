#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''I was reading some manga on MangaHere and decided it'd be easier
to just scrape the images and compile them into a cbz for easy offline
reading. Remember, never archive any manga you don't own a hardcopy of.
'''

import sys
import os
import urllib

import requests
from lxml import html

VERSION = "0.1"

class MangaSlurp:

    def __init__(self):
        '''Get the core URL of the manga and parse it.'''

        self.directory = sys.argv[2]
        requested_url = sys.argv[1]

        get_url = requests.get(requested_url)
        self.parse_url = html.fromstring(get_url.text)

    def make_directory(self, directory="Manga"):
        '''See if a given directory exists.  If not, make it.
        Used for both the main manga file directory and the
        subsequent volume directories '''

        directory = os.getcwd() + "/" + directory

        if not os.path.exists(directory):
            os.makedirs(directory)

    def find_volumes(self):
        '''Quickly find a list of volumes and reverse their order
        as they are listed oldest first.'''

        self.volume_list = self.parse_url.xpath(
            "//span/a[@class='color_0077']/@href")

        self.volume_list = self.volume_list[::-1]

        return self.volume_list

    def find_pages(self, url):
        '''Makes a list of each page for a particular volume'''

        parse = html.fromstring(url.text)
        self.pagecount = parse.xpath(
            "//select[@class='wid60']/option/@value")

        self.pagecount = self.pagecount[:len(self.pagecount)/2]

        return self.pagecount

    def find_images(self, url):
        '''Find the image on a give page.'''

        page = html.fromstring(url.text)
        self.image = page.xpath(
            "//img[@id='image']/@src")

        return self.image


def main():

    #initialize blank variables
    volume_iter = 0
    volume_name = ''
    volume_collection = []
    page_number = 0
    cwd = os.getcwd()
    volume_path = ""
    manga_path = ""
    imagetrue = ""

    #create the slurper, make manga directory, & slurp volumes
    manga_slurp = MangaSlurp()
    manga_slurp.make_directory(manga_slurp.directory)
    volume_list = manga_slurp.find_volumes()

    #give the folks some feedback & options
    print manga_slurp.directory + " contains " + str(len(volume_list)) + " volumes"

    for volume in volume_list:
        page_number = 0
        #Create a name & collection for the volume, generate a folder
        volume_iter = volume_iter + 1
        volume_name = "Volume " + str(volume_iter)
        volume_collection.append(volume_name)
        manga_path = cwd + "/" + manga_slurp.directory
        volume_path = manga_path + "/" + volume_name
        manga_slurp.make_directory("/" + manga_slurp.directory +"/" + volume_name)

        #create a new unparsed buffer from the volume
        url = requests.get(volume)

        #get the pagelist for the volume
        pagelist = manga_slurp.find_pages(url)

        #give some user feedback
        print "now downloading " + volume_name
        print "it contains " + str(len(pagelist)) + " pages"

        for page in pagelist:
            #slurp the images & add them to the volume collection

            '''print page'''

            url = requests.get(page)
            page_number = page_number + 1
            image = manga_slurp.find_images(url)
            imagetrue = image[0].split(".jpg")
            imagetrue = imagetrue[0] + ".jpg"
            urllib.urlretrieve(imagetrue, volume_path + "/" + str(page_number) + ".jpg")


if __name__ == "__main__":
    main()
