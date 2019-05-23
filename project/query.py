#!/usr/bin/env python3
import pymongo
from datetime import datetime
import pprint

## Before running this, plese make sure MongoDB is runing on 
## "mongodb://127.0.0.1:27017" and you have imported listings


''' Add an API for querying the DB based on the
following parameters

Find accommodations based on

1. Number of beds and bath-rooms
2. Number of guests
3. Zip Code (Mandatory)
4. Neighborhood names
5. Near Landmarks
6. Cost
7. Home type
'''

listing_cols = '''
id
listing_url
scrape_id
last_scraped
name
summary
space
description
experiences_offered
neighborhood_overview
notes
transit
access
interaction
house_rules
thumbnail_url
medium_url
picture_url
xl_picture_url
host_id
host_url
host_name
host_since
host_location
host_about
host_response_time
host_response_rate
host_acceptance_rate
host_is_superhost
host_thumbnail_url
host_picture_url
host_neighbourhood
host_listings_count
host_total_listings_count
host_verifications
host_has_profile_pic
host_identity_verified
street
neighbourhood
neighbourhood_cleansed
neighbourhood_group_cleansed
city
state
zipcode
market
smart_location
country_code
country
latitude
longitude
is_location_exact
property_type
room_type
accommodates
bathrooms
bedrooms
beds
bed_type
amenities
square_feet
price
weekly_price
monthly_price
security_deposit
cleaning_fee
guests_included
extra_people
minimum_nights
maximum_nights
calendar_updated
has_availability
availability_30
availability_60
availability_90
availability_365
calendar_last_scraped
number_of_reviews
first_review
last_review
review_scores_rating
review_scores_accuracy
review_scores_cleanliness
review_scores_checkin
review_scores_communication
review_scores_location
review_scores_value
requires_license
license
jurisdiction_names
instant_bookable
is_business_travel_ready
cancellation_policy
require_guest_profile_picture
require_guest_phone_verification
calculated_host_listings_count
reviews_per_month
'''

good_col_names = [ l.strip() for l in listing_cols.split('\n') ]
def_mongodb_uri = "mongodb://127.0.0.1:27017"
def_db = "client_database"
pymondo = None

def connect_db(uri = def_mongodb_uri, db_name = def_db):
    return pymongo.MongoClient(uri)[db_name]

def query_listings(query):
    global pymondo
    # Connect to db if not yet done
    # use client_database   
    # db.listings.find(({'country_code':'AU'}, {'zipcode':'3188'}))
    if not pymondo:
       pymondo = connect_db()

    ret = []
    houses = pymondo.listings.find(query)
    for house in houses:
       ret.append(house) 
    return ret
        
#  Zip & Country/Code are mandatory. Everything else is optional
# Pass all params in a Dict with the above mentioned params as keys
# Returns a True is query params are correct and a list matching the entries
def find_listings(params):
    query = {}
    for k,v in params.items():
        if k != '' and k in good_col_names:
            query[k] = v

    # Ensure that we have the mandatory stuff
    country = None
    country_code = None

    try:
        country = query['country']
    except KeyError:
        pass

    try:
        country_code = query['country_code']
    except KeyError:
        pass

    if not country and not country_code:
        return (False, None)

    # At this point we have country or country_code
    zipcode = None

    try:
        zipcode = query['zipcode']
    except KeyError:
        pass

    if not zipcode:
        return (False, None)

    listing = query_listings(query)
    return (True, listing)
   

if __name__ == '__main__':
    # TC 1
    params = { 'country_code' : 'AU', 'zipcode' : '3188' }
    r, l = find_listings(params)
    assert r, "Listings not found"
    assert len(l) == 31, "Listings count not enough"
    #pprint.pprint(l)

    # TC 2
    params = { 'country_code' : 'AU', 'state' : 'aa' }
    r, l = find_listings(params)
    assert r == False, "Should have not entries"
      
    # TC 3
    params = { 'country_code' : 'AU', 'state' : 'VIC', 'price': '$345.00',
               'zipcode' : '3188', 'beds': 3.0, 'accommodates': 4 }
    r, l = find_listings(params)
    assert r, "Listings not found"
    assert len(l) == 1, "Listings count not enough"
         





