from __future__ import print_function
from datetime import datetime
import logging
from simplemediawiki import MediaWiki


APIARY_URL = 'https://wikiapiary.com/w/api.php'
LOGGER = logging.getLogger()


def get_segment(segment_id):
    '''Get a specific segment from wikiapiary'''

    LOGGER.info("Connecting to %s", APIARY_URL)
    apiary_wiki = MediaWiki(APIARY_URL)

    print ("Retrieving segment", segment_id)
    my_query = ''.join([
        '[[Category:Website]]',
        '[[Is defunct::False]]',
        '[[Is active::True]]',
        "[[Has bot segment::%d]]" % segment_id,
        '|?Has API URL',
        '|?Has statistics URL',
        '|?Check every',
        '|?Creation date',
        '|?Page ID',
        '|?Collect general data',
        '|?Collect extension data',
        '|?Collect skin data',
        '|?Collect statistics',
        '|?Collect semantic statistics',
        '|?Collect logs',
        '|?Collect recent changes',
        '|?Collect statistics stats',
        '|sort=Creation date',
        '|order=asc',
        '|limit=1000'])

    sites = apiary_wiki.call({
        'action': 'ask',
        'query': my_query
        })

    if len(sites['query']['results']) > 0:
        for pagename, site in sites['query']['results'].items():
            print ("Processing", pagename)
    else:
        LOGGER.error("No records returned.")


def lambda_handler(event, context):
    try:
        get_segment(datetime.now().minute)
    except:
        LOGGER.error('Get segment failed.')
        raise
