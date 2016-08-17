#! /usr/bin/env python
# encoding: utf-8

"""
WordpressJsonWrapper
~~~~~~~~~~~~~~~~~~~~

This library provides a very thin wrapper around the
Wordpress JSON API (WP-API).

:copyright: (c) 2015 Stylight GmbH
:licence: MIT, see LICENSE for more details.

"""

import requests
import six

__version__ = '0.2.4',
__author__ = 'Raul Taranu, Dimitar Roustchev'

methods = {
    'get': 'GET',
    'read': 'GET',
    'retrieve': 'GET',
    'list': 'GET',
    'post': 'POST',
    'create': 'POST',
    'put': 'PUT',
    'update': 'PUT',
    'edit': 'PUT',
    'delete': 'DELETE',
}

component_conversions = {
    'post': 'posts',
    'user': 'users',
    'taxonomy': 'taxonomies',
    'category': 'categories',
    'status': 'statuses',
    'tag': 'tags',
    'type': 'types',
}

component_expansions = {
    'revisions': ['posts', 'revisions'],
    'meta': ['posts', 'meta'],
}


class WordpressError(Exception):
    """Baseclass for all API errors."""
    pass


class WordpressAuthenticationError(WordpressError):
    """Raised if there was a problem authenticating with the API."""
    pass


class WordpressJsonWrapper(object):

    def __init__(self, site, user, pwd):
        self.auth = (user, pwd)
        self.site = site

    def __getattr__(self, method_name):
        def api_method(**kw):
            return self._request(method_name, **kw)
        return api_method

    def _expand_url_components(self, url_components, ids):
        """
        >>> wp = WordpressJsonWrapper(None, None, None)
        >>> type(wp._expand_url_components(['foo'], {})) is list
        True
        >>> wp._expand_url_components(['revisions'], {'post': 3})
        ['posts', 'revisions']
        """
        expanded_url_components = list()
        if component_expansions.get(url_components[0]):
            expanded_url_components = component_expansions[url_components[0]]
            return expanded_url_components
        return url_components

    def _get_ids(self, **kw):
        """
        >>> wp = WordpressJsonWrapper(None, None, None)
        >>> type(wp._get_ids()) is dict
        True
        >>> wp._get_ids(test='foo', bar_id=42, foo_id=37)['foo']
        37
        >>> wp._get_ids(test='foo', bar_id=42, foo_id=37)['bar']
        42
        >>> wp._get_ids(test='foo', bar_id=42, foo_id=37).get('test') == None
        True
        >>> len(wp._get_ids(filter='test', bar_id=42, foo_id=37).keys())
        2
        """
        ids = dict()
        for key in kw.keys():
            if len(key.split('_id')) > 1:
                ids.update({'%s' % key.split('_id')[0]: kw.get(key)})
        return ids

    def _build_endpoint(self, url_components, ids):
        """
        >>> wp = WordpressJsonWrapper(None, None, None)
        >>> wp._build_endpoint(['posts'], {'post': 42})
        '/posts/42'
        >>> wp._build_endpoint(['post'], {'post': 24})
        '/posts/24'
        >>> wp._build_endpoint(['revisions'], {'post': 12})
        '/posts/12/revisions'
        >>> wp._build_endpoint(['categories'], {'post': 12})
        '/categories'
        >>> wp._build_endpoint(['categories'], {'category': 1})
        '/categories/1'
        >>> wp._build_endpoint(['statuses'], {'status': 3})
        '/statuses/3'
        >>> wp._build_endpoint(['posts', 'meta'], {'post': 42})
        '/posts/42/meta'
        >>> wp._build_endpoint(['posts', 'meta'], {'post': 42, 'meta': 37})
        '/posts/42/meta/37'
        >>> wp._build_endpoint(['foo', 'bar'], {'bar': 37})
        '/foo/bar/37'
        """
        endpoint = ''
        url_components = self._expand_url_components(url_components, ids)
        for component in url_components:
            if component_conversions.get(component):
                component = component_conversions.get(component)
            endpoint += '/%s' % component
            if ids.get(component):
                endpoint += '/%s' % ids.get(component)
            elif ids.get(component[:-1]):
                endpoint += '/%s' % ids.get(component[:-1])
            elif component.endswith('ies') and ids.get(component[:-3] + 'y'):
                endpoint += '/%s' % ids.get(component[:-3] + 'y')
            elif component.endswith('es') and ids.get(component[:-2]):
                endpoint += '/%s' % ids.get(component[:-2])
        return endpoint

    def _determine_method(self, verb):
        """
        >>> wp = WordpressJsonWrapper(None, None, None)
        >>> wp._determine_method('get')
        'GET'
        >>> wp._determine_method('list')
        'GET'
        >>> wp._determine_method('showme')
        Traceback (most recent call last):
            File "<stdin>", line 1, in ?
        AssertionError
        """
        assert methods.get(verb.lower()) is not None
        return methods.get(verb.lower())

    def _prepare_req(self, method_name, **kw):
        """
        >>> wp = WordpressJsonWrapper(None, None, None)
        >>> wp._prepare_req('get_posts')
        ('GET', '/posts', {}, {}, {})
        >>> wp._prepare_req('list_posts')
        ('GET', '/posts', {}, {}, {})
        >>> wp._prepare_req('get_posts', filter={'post_status': 'draft'})
        ('GET', '/posts', {'filter[post_status]': 'draft'}, {}, {})
        >>> wp._prepare_req('get_posts', post_id=5)
        ('GET', '/posts/5', {}, {}, {})
        >>> wp._prepare_req('get_post', post_id=6)
        ('GET', '/posts/6', {}, {}, {})
        >>> wp._prepare_req('edit_post', post_id=7, data={'foo': 'bar'})
        ('PUT', '/posts/7', {}, {'foo': 'bar'}, {})
        >>> wp._prepare_req('create_post', data={'foo': 'bar'})
        ('POST', '/posts', {}, {'foo': 'bar'}, {})
        >>> wp._prepare_req('delete_post', post_id=8)
        ('DELETE', '/posts/8', {}, {}, {})
        >>> wp._prepare_req('get_post_revisions', post_id=9)
        ('GET', '/posts/9/revisions', {}, {}, {})
        >>> wp._prepare_req('get_revisions', post_id=9)
        ('GET', '/posts/9/revisions', {}, {}, {})
        >>> wp._prepare_req('get_post_meta', post_id=91)
        ('GET', '/posts/91/meta', {}, {}, {})
        >>> wp._prepare_req('get_meta', post_id=91)
        ('GET', '/posts/91/meta', {}, {}, {})
        >>> wp._prepare_req('get_meta', post_id=91, meta_id=5)
        ('GET', '/posts/91/meta/5', {}, {}, {})
        >>> wp._prepare_req('create_meta', post_id=91, meta_id=5)
        ('POST', '/posts/91/meta/5', {}, {}, {})
        >>> wp._prepare_req('update_meta', post_id=91, meta_id=5)
        ('PUT', '/posts/91/meta/5', {}, {}, {})
        >>> wp._prepare_req('get_user', user_id=4)
        ('GET', '/users/4', {}, {}, {})
        >>> wp._prepare_req('get_user', user_id='me')
        ('GET', '/users/me', {}, {}, {})
        >>> wp._prepare_req('get_taxonomies')
        ('GET', '/taxonomies', {}, {}, {})
        >>> wp._prepare_req('get_taxonomies', taxonomy_id='category')
        ('GET', '/taxonomies/category', {}, {}, {})
        >>> wp._prepare_req('get_taxonomies', taxonomy_id='post_tag')
        ('GET', '/taxonomies/post_tag', {}, {}, {})
        >>> wp._prepare_req('get_taxonomy', taxonomy_id='post_format')
        ('GET', '/taxonomies/post_format', {}, {}, {})
        >>> wp._prepare_req('get_taxonomy', taxonomy_id='post_status')
        ('GET', '/taxonomies/post_status', {}, {}, {})
        >>> wp._prepare_req('get_categories')
        ('GET', '/categories', {}, {}, {})
        >>> wp._prepare_req('get_tags')
        ('GET', '/tags', {}, {}, {})
        >>> wp._prepare_req('get_types')
        ('GET', '/types', {}, {}, {})
        >>> wp._prepare_req('get_statuses')
        ('GET', '/statuses', {}, {}, {})
        >>> wp._prepare_req('get_posts', headers={'foo': 'bar'})
        ('GET', '/posts', {}, {}, {'foo': 'bar'})
        >>> wp._prepare_req('get_posts', params={'context': 'edit'})
        ('GET', '/posts', {'context': 'edit'}, {}, {})
        """
        assert len(method_name.split('_')) > 1
        method = self._determine_method(method_name.split('_')[0])
        endpoints = method_name.split('_')[1:]
        ids = self._get_ids(**kw)
        endpoint = self._build_endpoint(endpoints, ids)

        # filters
        url_params = dict()
        if kw.get('filter'):
            for query_param, value in six.iteritems(kw.get('filter')):
                url_params.update({'filter[%s]' % query_param: value})

        # url params
        if kw.get('params'):
            for query_param, value in six.iteritems(kw.get('params')):
                url_params.update({query_param: value})

        # post data
        post_data = dict()
        if kw.get('data'):
            post_data = kw.get('data')

        # headers
        headers = dict()
        if kw.get('headers'):
            headers = kw.get('headers')

        return (method.upper(), endpoint, url_params, post_data, headers)

    def _request(self, method_name, **kw):
        method, endpoint, params, data, headers = self._prepare_req(
            method_name, **kw
        )

        http_response = requests.request(
            method,
            self.site + endpoint,
            auth=self.auth,
            params=params,
            json=data,
            headers=headers
        )

        if http_response.status_code not in [200, 201]:
            if 'application/json' in http_response.headers.get('Content-Type'):
                code = http_response.json().get('code')
                message = http_response.json().get('message')
            else:
                code = http_response.status_code
                message = http_response.text
            raise WordpressError(" ".join([
                str(http_response.status_code),
                str(http_response.reason),
                ":",
                '[{code}] {message}'.format(code=code, message=message)
            ]))
        else:
            return http_response.json()


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-vv', '--with-doctest'])
