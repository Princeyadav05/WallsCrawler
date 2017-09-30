import urllib
import requests
import bs4
import re
import os

os.makedirs('Wallhaven', exist_ok=True)

print ('''\n\n
    Welcome to the Wallpaper Downloader
    With this Script you can download wallpapers from Wallhaven site''')

def latest():
    print('''
    Downloading Latest Wallpapers from Wallhaven.''')
    urllatest = 'https://alpha.wallhaven.cc/latest?page='
    return (urllatest, dict())

def top():
    print('''
    Downloading Top Wallpapers from Wallhaven.''')
    urltop = 'https://alpha.wallhaven.cc/toplist?page='
    return (urltop, dict())

def search():
    keyword = input('\n    Enter the Keyword : ')
    print('''
    Downloading Wallpapers related to %s''' %keyword)
    urlsearch = 'https://alpha.wallhaven.cc/search?q=' + \
                urllib.parse.quote_plus(keyword) + '&page='
    return (urlsearch, dict())

def main():
    select = str(input('''\n
    Choose how you want to download the image:

    1. Latest Wallpapers 
    2. Top Wallpapers
    3. Search Wallpapers

    Enter choice: '''))

    while select not in ['1', '2', '3']:
        if select != None:
            print('\n    You entered an incorrect value.')
        select = input('    Enter choice again: ')

    if select == '1':
        BASEURL, cookies = latest()
    elif select == '2':
        BASEURL, cookies = top()
    elif select == '3':
        BASEURL, cookies = search()

    page_id = int(input('''
    How many pages you want to Download ( There are 24 wallpapers on a single page ) : '''))
    total_images = str(24 * page_id)
    print('''
    Number of Wallpapers to Download: %s
    Sit Back and Relax :D \n''' %total_images )

    for i in range(1, page_id + 1):
        url = BASEURL + str(i)  # url of the page
        urlreq = requests.get(url, cookies=cookies) #response of the url
        soup = bs4.BeautifulSoup(urlreq.text, 'lxml') # Complete html
        soupid = soup.findAll('a', {'class': 'preview'}) # picking up all the 'preview' classes
        res = re.compile(r'\d+') # picking up all the decimal values from the 'preview' links
        image_id = res.findall(str(soupid)) # storing all the decimal values

        image_extension = ['jpg', 'png', 'bmp']

        for j in range(len(image_id)):
            currentImage = (((i - 1) * 24) + (j + 1)) #formula for current Image
            url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % image_id[j]

            for extension in image_extension:
                final_url = url + extension
                path = os.path.join('Wallhaven', os.path.basename(final_url))

                if not os.path.exists(path):
                    imgreq = requests.get(final_url, cookies=cookies) #image response

                    if imgreq.status_code == 200:
                        print('''    Downloading : %s - %s / %s''' % ((os.path.basename(final_url)), currentImage, total_images))
                        with open(path, 'ab') as imageFile:
                            for chunk in imgreq.iter_content(1024):
                                imageFile.write(chunk)
                        break
                else:
                    print("%s already exist - %s / %s" % os.path.basename(final_url), currentImage, total_images)


if __name__ == '__main__':
    main()
