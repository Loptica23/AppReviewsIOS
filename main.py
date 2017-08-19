from configurator import Configurator
from reviewsgether import ReviewsGether


#countries_string = config.get('countries', 'list')
#countries_codes = countries_string.split(',')


configurator = Configurator()
reviews_gether = ReviewsGether(configurator)
reviews_gether.getReviewsForAllCountries()


