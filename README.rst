python-wordpress-json
=====================

.. image:: https://travis-ci.org/stylight/python-wordpress-json.svg?branch=master
    :target: https://travis-ci.org/stylight/python-wordpress-json

Super thin Python wrapper for the `Wordpress REST API V2<http://v2.wp-api.org/>`_ developed by
`Stylight <http://www.stylight.de/>`_. Supports the documented read and write endpoints. Extensions and pull requests are encouraged and welcome.

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

`Official PyPI wordpress-json page <https://pypi.python.org/pypi/wordpress-json/>`_

Before being able to use this package make sure you configure Wordpress properly;

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
  - Search for "WP REST API Meta Endpoints". Install the plugin named "WP REST API Meta Endpoints", by clicking on the "Install" button.
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

    from __future__ import print_function
    from wordpress_json import WordpressJsonWrapper
    import json

    # construct a wrapper

    wp = WordpressJsonWrapper("http://example.com/wp-json", "wp_user", "wp_password")

    # optional headers
    headers = {
        "User-Agent": "curl",
        "Content-Type": "text/json",
        # ...
    }

    # make requests, e.g. list posts
    print("----------- list posts -------------")

    posts = wp.get_posts()
    print(json.dumps(posts))

    # or with headers
    print("------------ list posts with headers------------")
    posts = wp.get_posts(headers=headers)
    print(json.dumps(posts))

    # list posts with filter
    print("-------------list posts with draft status-----------")
    posts = wp.get_posts(filter={"status": "draft"})
    print(json.dumps(posts))


    print("------------- create new post-----------")

    data = {
            "title": "My first pony",
            "content": "He's wild!",
            "exerpt": ""
            # ...
        }

    # only one of title, content and excerpt is required to create a post
    new_post = wp.create_post(data=data)
    print(json.dumps(new_post))

    # get metadata for a post
    print("------------- Get Metadata-----------")
    meta = wp.get_meta(post_id=1)
    print(json.dumps(meta));

    # or
    meta = wp.get_meta(post_id=1, meta_id=5)
