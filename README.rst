python-wordpress-json
---------------------

Super thin Python wrapper for the `Wordpress REST API <http://wp-api.org/>`_ developed by
`Stylight <http://www.stylight.de/>`_. Supports the documented read and write endpoints. Extensions and pull requests are encouraged and welcome.

Limitations:

* doesn't check input parameters
* returns a single dictionary or a list of dictionaries, depending on the API endpoint
* only supports basic auth, and it currently cannot be used without authentication

Dependencies:

* requests

Installation
============

::

    pip install wordpress-json

`Official PyPI wordpress-json page <https://pypi.python.org/pypi/wordpress-json/>`_

Usage
============

.. code-block:: python

    from wordpress-json import WordpressJsonWrapper

    # construct a wrapper

    wp = WordpressJsonWrapper("http://example.com/wp-json", "wp_user", "wp_password")

    # make requests, e.g. list posts
    posts = wp.get_posts()

    # list posts with filter
    posts = wp.get_posts(filter={"status": "draft"})

    # create post
    data = {
        "title": "My first pony",
        "content": "He's wild!",
        "exerpt": ""
        # ...
    }
    # only one of title, content and excerpt is required to create a post
    wp.create_post(data=data)

    # get metadata for a post
    meta = wp.get_meta(post_id=4)
    # or
    meta = wp.get_meta(post_id=4, meta_id=5)

