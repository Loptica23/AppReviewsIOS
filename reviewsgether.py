import requests
import xmltodict
from dbconnector import DBConnector

first_part_of_url = 'https://itunes.apple.com/'
second_part_of_url = 'rss/customerreviews/id='
third_part_of_url = '/xml'
wrong_url_part = 'sortby=mostrecent/xml?urlDesc=/'

first_part_of_url_all = 'https://itunes.apple.com/'
#country code
second_part_of_url_all = '/rss/customerreviews/page='
#page
third_part_of_url_all = '/id='
#id
fourth_part_of_url_all = '/xml'

class ReviewsGether(object):
    def __init__(self, configurator):
        self._configurator = configurator
        self._looping_time = configurator.getLoopingTime()
        self._database_connection = DBConnector(configurator)
        self._application_id = configurator.getApplicationID()
        self._countries = configurator.getCountries()
        self._initUrls()

    def getReviewsAndPutInDatabase(self):
        self._getReviewsInXML()

    def getReviewsForAllCountries(self):
        self._getReviewsInXMLForAllCountries()

    def _getReviewsInXMLForAllCountries(self):
        for country in self._countries:
            try:
                for page in range(1,10):
                    self._initUrlsAll(country, page)
                    print self._url
                    response = requests.post(self._url)
                    body = xmltodict.parse(response.content, xml_attribs=True)
                    feed = body['feed']
                    links = feed['link']
                    entries = feed['entry']

                    # nalazenje sledeceg urla
                    self._setNextUrlAllCountries(links)

                    # citanje komentara
                    if (not self._readComments(entries)):
                        break

            except Exception, e:
                print str(e)

    def _getReviewsInXML(self):
        try:
            while self._next_url != self._url:
                self._url = self._next_url
                print self._url
                response = requests.post(self._url)
                body = xmltodict.parse(response.content, xml_attribs=True)
                feed = body['feed']
                links = feed['link']
                entries = feed['entry']

                # nalazenje sledeceg urla
                self._setNextUrl(links)

                # citanje komentara
                if (not self._readComments(entries)):
                    break

        except Exception, e:
            print str(e)

    def _initUrls(self):
        self._url = ''
        self._next_url = first_part_of_url + second_part_of_url + self._application_id + third_part_of_url

    def _initUrlsAll(self, country, page):
        self._url = first_part_of_url_all + country + second_part_of_url_all + str(page) + third_part_of_url_all + self._application_id + fourth_part_of_url_all

    def _setNextUrl(self, links):
        for single_link in links:
            if single_link['@rel'] == 'next':
                self._next_url = single_link['@href']
                first_part_of_next_url = self._next_url.rpartition(wrong_url_part)[0]
                second_part_of_next_url = 'xml'
                self._next_url = first_part_of_next_url + second_part_of_next_url

    def _setNextUrlAllCountries(self, links):
        for single_link in links:
            if single_link['@rel'] == 'next':
                self._next_url = single_link['@href']
                first_part_of_next_url = self._next_url.rpartition(wrong_url_part)[0]
                second_part_of_next_url = 'xml'
                self._next_url = first_part_of_next_url + second_part_of_next_url

    def _readComments(self, entries):
        for entry in entries:
            try:
                if type(entry['id']) == unicode:
                    id = int(entry['id'])
                text = entry['content'][0]['#text']
                raiting = int(entry['im:rating'])
                title = entry['title']
                updated = entry['updated']
                author = entry['author']['name']
                if (not self._database_connection.insertReview(id, raiting, text, title, updated, author)):
                    return False

            except Exception, e:
                print str(e)

        return True