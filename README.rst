python-wordpress-json
=====================

.. image:: https://img.shields.io/travis/stylight/python-wordpress-json.svg
   :target:  https://travis-ci.org/stylight/python-wordpress-json

.. image:: https://img.shields.io/pypi/v/wordpress_json.svg
   :target:  https://pypi.python.org/pypi/wordpress_json

Super thin Python wrapper for the `Wordpress REST API V2 <http://v2.wp-api.org/>`_ developed by
`Stylight <http://www.stylight.com/>`_. Supports the documented read and write endpoints. Extensions and pull requests are encouraged and welcome.

Limitations:

* doesn't check input parameters
* returns a single dictionary or a list of dictionaries, depending on the API endpoint
* only supports basic auth, and it currently cannot be used without authentication

Dependencies:

* requests
* six

Installation
------------

::

    pip install wordpress-json

Before being able to use this package make sure you configure Wordpress properly.

Wordpress configuration
-----------------------

1. You need to install the WP-API Plugin. To do so:

   - Go to your Wordpress Dashboard
   - Click on Plugins in the left sidebar
   - Search for "REST API". Install the plugin named "WordPress REST API (Version 2)", by clicking on the "Install" button.
   - Activate the plugin on the next screen.

2. You need to install and activate the WP REST API Meta Endpoints plugin for the WP-API :

   - Click on Plugins in the left sidebar
   - Click on "Add New" on the top right, next to "Plugin"
   - Search for "WP REST API Meta Endpoints". Install the plugin named "WP REST API Meta Endpoints", by clicking on the  "Install" button.
   - Activate the plugin on the next screen.

3. You need to install and activate the Basic-Auth plugin for the WP-API :

   - download https://github.com/WP-API/Basic-Auth/archive/master.zip
   - Open your Wordpress Admin Dashboard
   - Click on Plugins in the left sidebar
   - Click on "Add New" on the top right, next to "Plugin"
   - Click on "Upload Plugin", Choose File, and select the file you downloaded at step 1 (master.zip)
   - Click on Install Now
   - Activate the plugin on the next screen.

4. Change permalink configuration to 'Post name' in Permalink Settings.

Usage
------------

.. code-block:: python

    >>> wp = WordpressJsonWrapper('http://example.com/wp-json/wp/v2', 'wp_user', 'wp_password')
    >>> posts = wp.get_posts()
    >>> posts[0].keys()
    dict_keys(['format', 'featured_media', 'author', ...])

    >>> posts[0].get('title')
    {'rendered': 'Tweetle Beetles'}

    >>> posts[0].get('content')
    {'rendered': '<p>What do you know about tweetle beetles? ...'}

    >>> posts[0].get('id')
    42

    >>> wp.create_meta(post_id=42, data=dict(key='genre', value='fanciful'))

    >>> meta = wp.get_meta(post_id=42)
    >>> meta[0].get('key')
    'genre'

    >>> meta[0].get('value')
    'fanciful'
