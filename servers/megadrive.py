# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para megadrive
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[megadrive.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)

    data_pack = scrapertools.find_single_match(data, "(eval.function.p,a,c,k,e,.*?)\s*</script>")
    if data_pack != "":
        from core import unpackerjs3
        data_unpack = unpackerjs3.unpackjs(data_pack)
        if data_unpack == "":
            from core import jsunpack
            data_unpack = jsunpack.unpack(data_pack)
        data = data_unpack

    video_url = scrapertools.find_single_match(data, 'file"?\s*:\s*"([^"]+)",')
    video_urls.append(["[megadrive]", video_url])

    for video_url in video_urls:
        logger.info("[megadrive.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra v�deos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = r"""http://megadrive.tv/(?:embed-)?([a-z0-9A-Z]+)"""
    logger.info("[megadrive.py] find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[megadrive]"
        url = 'http://megadrive.tv/embed-%s-640x360.html' % match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'megadrive'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve