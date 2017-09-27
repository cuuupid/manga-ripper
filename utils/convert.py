# image utilities
from wand.image import Image as wand_img
from PIL import Image as pil_img
# io reqs
import sys
import os
# web interface
import requests
# scraping
from lxml import html
import unicodedata
# logging
from console_logging import console
##


def pdf_to_png(path_to_pdf):
    pdf_name = ''.join(path_to_pdf.split('/')[-1].split('.')[:-1])
    assert len(pdf_name) > 0, "Input PDF had no filename apart from extension."
    with wand_img(filename=path_to_pdf) as pdf_img:
        with pdf_img.convert('png') as converted:
            converted.save(filename='img/' + pdf_name + '/out.png')


def _download_image(link, save_to):
    try:
        if save_to.split('.')[0] == 'loading':
            return True
        r = requests.get(link, stream=True, allow_redirects=True)
        with open(save_to, 'wb') as save_file:
            for chunk in r.iter_content(1024):
                if chunk:
                    save_file.write(chunk)
        return True
    except Exception as e:
        print(e)
        return False


def _scrape_mangahere(l, pages=20):
    ''' requires chapter link e.g. mangahere.co/manga/c001/ '''
    img_links = [html.document_fromstring(requests.get(l + '{}.html'.format(page)).content).xpath(
        '//img/@src')[-1] for page in range(1, pages + 1)]
    console.info('Formed cluster of image links from pages.')
    save_dir = 'img/' + l.split('/')[-3] + '/'
    try:
        os.makedirs(save_dir)
    except:
        pass
    for img_link in img_links:
        assert _download_image(img_link, save_dir + ''.join(img_link.split('/')
                                                            [-1].split('.')[:-1]) + '.png'), "Failed in downloading image: " + img_link
        console.info('Downloaded ' + img_link)
    return True
