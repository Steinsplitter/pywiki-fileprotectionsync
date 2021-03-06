# -*- coding: utf-8  -*-
# Script to create a gallery of files used on one or more pages on
# another wiki. Main purpose being to automatically protect files
# from a central repository that are used on a local wiki's main page.
# For this to work, the gallery page must have cascading protection as well.
#
# @author Betacommand
# @author Krinkle
# @license CC-BY-SA 3.0
import json
import urllib

import fileprotectionsync_config as config
import pywikibot
commons_site = pywikibot.Site('commons', 'commons')


def main():
    for wiki in config.wikis:
        wt = config.wikitext_start
        mpimages = []
        for pg in wiki['sourcepages']:
            mpimages.extend(get_images(wiki['sourcewiki'], pg))
        mpimages = sorted(set(mpimages))
        for cimage in mpimages:
            wt += 'File:%s\n' % cimage
        wt += config.wikitext_end
        pywikibot.Page(commons_site, wiki['targetpage']).put(wt, config.editsummary)


def get_images(site, title):
    # TODO: Use pywikibot's built-in API stuff instead of this
    title = urllib.urlencode({'titles': title})
    mpimages = []
    path = 'https://%s/w/api.php?action=query&prop=images&%s&imlimit=500&redirects&format=json' % (site, title)
    print path
    tx = urllib.urlopen(path)
    json_resp = tx.read()
    data = json.loads(json_resp)
    images = data['query']['pages'][data['query']['pages'].keys()[0]]['images']
    for image in images:
        if image['ns'] == 6:
            # Extract file name (remove File namespace prefix)
            # This allows non-English wikis to be fetched into an English wiki
            # Datei:Awesome_collection:_The_Example_(2006).jpg -> Awesome_collection:_The_Example_(2006).jpg
            mpimages.append(image['title'].split(':', 1)[1])
    return mpimages


if __name__ == '__main__':
        main()
