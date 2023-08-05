pycraigslist
============

|PyPI version fury.io| |PyPI pyversions|

.. |PyPI version fury.io| image:: https://badge.fury.io/py/pycraigslist.svg
    :target: https://pypi.python.org/pypi/pycraigslist
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pycraigslist.svg
    :target: https://pypi.python.org/pypi/pycraigslist/


A fast and expressive `Craigslist <https://www.craigslist.org/about/sites>`__ API wrapper.

Disclaimer
----------

* I do not work or have an affiliation with Craigslist.
* This library is intended for educational purposes. It is not advised to crawl and download data from Craigslist.

Installation
------------

::

    pip install pycraigslist

Jump Start
----------

Let's find posts with keyword "Mazda Miata" in the East Bay Area, California:

.. code:: python

    import pycraigslist

    miatas = pycraigslist.forsale.cta(site="sfbay", area="eby", query="Mazda Miata")
    for miata in miatas.search():
        print(miata)

    >>> {'country': 'US',
        'region': 'CA',
        'site': 'sfbay',
        'area': 'scz',
        'category': 'cto',
        'id': '7298072504',
        'repost_of': '',
        'last_updated': '2021-03-27 17:12',
        'title': '2005 Mazda MX-5 Miata',
        'neighborhood': 'santa cruz',
        'price': '$3,250',
        'url': 'https://sfbay.craigslist.org/scz/cto/d/santa-cruz-2005-mazda-mx-miata/7298072504.html'}
        # ...    

Background
----------

This library is intended to be expressive and easy to use.


pycraigslist classes
********************

.. |nbsp|   unicode:: U+00A0 .. NO-BREAK SPACE

* ``pycraigslist.community`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > community)
* ``pycraigslist.events`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > event calendar)
* ``pycraigslist.forsale`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > for sale)
* ``pycraigslist.gigs`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > gigs)
* ``pycraigslist.housing`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > housing)
* ``pycraigslist.jobs`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > jobs)
* ``pycraigslist.resumes`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > resumes)
* ``pycraigslist.services`` |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > services)

We can search for posts in parent classes. Let's find paid gigs in Portland, Oregon:

.. code:: python

    import pycraigslist

    paid_gigs = pycraigslist.gigs(site="portland", is_paid=True)
    for gig in paid_gigs.search():
        print(gig)

    >>> {'country': 'US',
        'region': 'OR',
        'site': 'portland',
        'area': 'mlt',
        'category': 'lbg',
        'id': '7295392821',
        'repost_of': '7292985211',
        'last_updated': '2021-03-22 13:00',
        'title': 'Packing and moving',
        'neighborhood': 'SE Portland',
        'price': '',
        'url': 'https://portland.craigslist.org/mlt/lbg/d/portland-packing-and-moving/7295392821.html'}
        # ...

pycraigslist subclasses
***********************

Most pycraigslist classes have subclasses to allow for categorical searches. For example:

* ``pycraigslist.forsale.bia`` |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > for sale > bikes)
* ``pycraigslist.forsale.cta`` |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > for sale > cars & trucks)
* ``pycraigslist.housing.apa`` |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > housing > apartments / housing for rent)
* ``pycraigslist.housing.roo`` |nbsp| |nbsp| |nbsp| |nbsp| (craigslist.org > housing > apartments / rooms & shares)

Finding pycraigslist subclasses
*******************************

To search for subclasses, use ``.get_categories()``. The resulting keys are the subclass names.

.. code:: python

    import pycraigslist

    print(pycraigslist.housing.get_categories())

    >>> {'apa': 'apartments / housing for rent',
        'swp': 'housing swap',
        'off': 'office & commercial',
        'prk': 'parking & storage',
        'rea': 'real estate',
        'reb': 'real estate - by dealer',
        'reo': 'real estate - by owner',
        'roo': 'rooms & shares',
        'sub': 'sublets & temporary',
        'vac': 'vacation rentals',
        'hou': 'wanted: apts',
        'rew': 'wanted: real estate',
        'sha': 'wanted: room/share',
        'sbw': 'wanted: sublet/temp'}

If we're interested in searching for vacation rentals, we'd use the subclass ``pycraigslist.housing.vac``.

Finding and using filters
*************************
As demonstrated in the jump-start example, we can apply filters to our Craigslist search.
To find valid filters for a class or subclass, use ``.get_filters()``.

.. code:: python

    import pycraigslist

    print(pycraigslist.housing.apa.get_filters())

    >>> {'query': '...', 'search_titles': 'True/False', 'has_image': 'True/False',
        'posted_today': 'True/False', 'bundle_duplicates': 'True/False', 'search_distance': '...',
        'zip_code': '...', 'min_price': '...', 'max_price': '...',
        'min_bedrooms': '...', 'max_bedrooms': '...', 'min_bathrooms': '...',
        'max_bathrooms': '...', 'min_ft2': '...', 'max_ft2': '...',
        'private_room': 'True/False', 'private_bath': 'True/False', 'cats_ok': 'True/False',
        'dogs_ok': 'True/False', 'is_furnished': 'True/False', 'no_smoking': 'True/False',
        'wheelchair_acccess': 'True/False', 'ev_charging': 'True/False', 'no_application_fee': 'True/False',
        'no_broker_fee': 'True/False',
        'housing_type': ['apartment', 'condo', 'cottage/cabin', 'duplex', 'flat',
                         'house', 'in-law', 'loft', 'townhouse', 'manufactured',
                         'assisted living', 'land'],
        'laundry': ['w/d in unit', 'w/d hookups', 'laundry in bldg', 'laundry on site', 'no laundry on site'],
        'parking': ['carport', 'attached garage', 'detached garage', 'off-street parking', 'street parking',
                    'valet parking', 'no parking']}

Using this information, let's search for apartments / housing for rent in Eugene, Oregon that have at least 1 bedroom and a carport.

.. code:: python

    import pycraigslist

    one_bedrooms = pycraigslist.housing.apa(site="eugene", min_bedrooms=1, parking="carport")
    for room in one_bedrooms.search():
        print(room)

    >>> {'country': 'US',
        'region': 'OR',
        'site': 'eugene',
        'area': '',
        'category': 'apa',
        'id': '7267556874',
        'repost_of': '',
        'last_updated': '2021-02-24 08:55',
        'title': 'High End, Spacious Top Floor Two Bedroom!',
        'neighborhood': 'Eugene',
        'price': '$1,550',
        'url': 'https://eugene.craigslist.org/apa/d/springfield-high-end-spacious-top-floor/7267556874.html',
        'bedrooms': '2',
        'area-ft2': '1000'}
        # ...

If we want to apply a bunch of filters, pass a dictionary of filters into the ``filters`` keyword parameter.
Note: keyword argument filters will override ``filters`` if there are conflicting keys. For example:

.. code:: python

    import pycraigslist

    bike_filters = {
    "bicycle_frame_material": "steel",
    # array of filter values are accepted
    "bicycle_wheel_size": ["650C", "700C"],
    "bicycle_type": "road",
    }
    # we'd still get titanium road bikes with size 650C or 700C wheels
    titanium_bikes = pycraigslist.forsale.bia(
        site="sfbay", area="sfc", bicycle_frame_material="titanium", filters=bike_filters
    )

Searching for posts
-------------------

General search
**************

To search for Craigslist posts, use the ``.search()`` method.
``.search()`` will return a dictionary of attributes (type ``str``) for every post and will get every post by default. 
Use the ``limit`` keyword parameter to add a stop limit to a query. For example, use ``limit=50`` if we want 50 posts.
There is a maximum of 3000 posts per query.

Let's find the first 20 posts for farming and gardening services in Denver, Colorado.

.. code:: python

    import pycraigslist

    gardening_services = pycraigslist.services.fgs(site="denver")
    for service in gardening_services.search(limit=20):
        print(service)

    >>> {'country': 'US',
        'region': 'CO',
        'site': 'denver',
        'area': '',
        'category': 'fgs',
        'id': '7301324564',
        'repost_of': '6974119634',
        'last_updated': '2021-04-03 11:47',
        'title': '🌲 Tree Removal/Trimming, Stump Grind: LICENSED/INSURED! 720-605-1584',
        'neighborhood': 'All Areas',
        'price': '',
        'url': 'https://denver.craigslist.org/fgs/d/littleton-tree-removal-trimming-stump/7301324564.html'}
        # ...

Detailed search
***************

Use the ``.search_detail()`` method to get detailed Craigslist posts.
The ``limit`` keyword argument in ``.search()`` also applies to ``.search_detail()``.
Set ``include_body=True`` to include the post's body in the output. By default, ``include_body=False``.
Disclaimer: ``.search_detail`` is more time consuming than ``.search``.

Let's get detailed posts with the post body for all cars & trucks for sale in Abilene, Texas.

.. code:: python

    import pycraigslist

    all_autos = pycraigslist.forsale.cta(site="abilene")
    for auto in all_autos.search_detail(include_body=True):
        print(auto)
        
    >>> {'country': 'US',
        'region': 'TX',
        'site': 'abilene',
        'area': '',
        'category': 'cto',
        'id': '7301439387',
        'repost_of': '',
        'last_updated': '2021-04-03 16:15',
        'title': 'Ford F-250 Super Duty XLT',
        'neighborhood': 'Abilene',
        'price': '$16,000',
        'url': 'https://abilene.craigslist.org/cto/d/abilene-ford-250-super-duty-xlt/7301439387.html',
        'lat': '32.255519',
        'lon': '-99.787999',
        'address': '1226 County Road 150',
        'misc': ['2005 chevrolet malibu', 'delivery available'],
        'condition': 'good',
        'cylinders': '6 cylinders',
        'drive': 'fwd',
        'fuel': 'gas',
        'odometer': '140000',
        'paint color': 'white',
        'size': 'full-size',
        'title status': 'clean',
        'transmission': 'automatic',
        'type': 'sedan',
        'body': '05 Chev. Malibu. Run out good, stingy on gas.\nReady to go.'}
        # ...

Additional attributes
---------------------

* ``__doc__``: Gets category name of a subclass.
* ``url``: Gets search URL of a pycraigslist object.
* ``count``: Gets number of posts of a pycraigslist object.

.. code:: python
    
    import pycraigslist

    east_bay_apa = pycraigslist.housing.apa(site="sfbay", area="eby", max_price=800)

    # 1
    print(east_bay_apa.__doc__)
    >>> 'apartments / housing for rent'

    # 2
    print(east_bay_apa.url)
    >>> 'https://sfbay.craigslist.org/search/eby/apa'

    # 3
    print(east_bay_apa.count)
    >>> 56

Contribute
----------

- `Issue Tracker <https://github.com/irahorecka/pycraigslist/issues>`__
- `Source Code <https://github.com/irahorecka/pycraigslist/tree/master/pycraigslist>`__

Support
-------

If you are having issues or would like to propose a new feature, please use the `issues tracker <https://github.com/irahorecka/pycraigslist/issues>`__.

License
-------

The project is licensed under the MIT license.
