#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `rfc3986_validator` package."""
import pytest
import rfc3987
from hypothesis import given, settings
import hypothesis.provisional as prov_st

from rfc3986_validator import validate_rfc3986

VALID_URIS = (
    'http://foo.com/blah_blah',
    'http://foo.com/blah_blah/',
    'http://foo.com/blah_blah_(wikipedia)',
    'http://foo.com/blah_blah_(wikipedia)_(again)',
    'http://www.example.com/wpstyle/?p=364',
    'https://www.example.com/foo/?bar=baz&inga=42&quux',
    'http://userid:password@example.com:8080',
    'http://userid:password@example.com:8080/',
    'http://userid@example.com',
    'http://userid@example.com/',
    'http://userid@example.com:8080',
    'http://userid@example.com:8080/',
    'http://userid:password@example.com',
    'http://userid:password@example.com/',
    'http://142.42.1.1/',
    'http://142.42.1.1:8080/',
    'http://foo.com/blah_(wikipedia)#cite-1',
    'http://foo.com/blah_(wikipedia)_blah#cite-1',
    'http://foo.com/(something)?after=parens',
    'http://code.google.com/events/#&product=browser',
    'http://j.mp',
    'ftp://foo.bar/baz',
    'http://foo.bar/?q=Test%20URL-encoded%20stuff',
    'http://-.~_!$&()*+,;=:%40:80%2f::::::@example.com',
    'http://1337.net',
    'http://a.b-c.de',
    'http://223.255.255.254',
    'http://foo.bar/%ba',
    'http://foo.bar/../../',
    'http://foo.bar/../...../asd',
    'http://foo.com/#)(',
    'http:foo',
    'http::foo',
    'mailto:John.Doe@example.com',
    'news:comp.infosystems.www.servers.unix',
    'tel:+1-816-555-1212',
    'telnet://192.0.2.16:80/',
    'urn:oasis:names:specification:docbook:dtd:xml:4.1.2',
    'ldap://[2001:db8::7]/c=GB?objectClass?one',
    'ldap://[2001:db8::7]:80/c=GB?objectClass?one',
    'http://[2001:db8:85a3:8d3:1319:8a2e:370:7348]/',
    'http://[2001:db8:a0b:12f0::1]:80/index.html',
)


INVALID_URIS = (
    '',
    'http://foo.bar?q=Spaces should be encoded',
    '//',
    '//a',
    '///a',
    '///',
    'foo.com',
    'http:// shouldfail.com',
    ':// should fail',
    'http://foo.bar/foo(bar)baz quux',
    'http://%jfoo.bar/',
    'http://foo.bar/%ja',
    'http://[foo.bar]/',
    'http://foo.bar/[asd]/',
    'http://foo.[bar]/',
    'http://foo.bar/##',
    'foo',
    'htt(ps://foo/',
    'http://:foo',
)


VALID_URI_REFS = (
    '//foo.com/blah_blah',
    '//foo.com/blah_blah/',
    '//foo.com/blah_blah_(wikipedia)',
    '//foo.com/blah_blah_(wikipedia)_(again)',
    '//www.example.com/wpstyle/?p=364',
    '//www.example.com/foo/?bar=baz&inga=42&quux',
    '//userid:password@example.com:8080',
    '//userid:password@example.com:8080/',
    '//userid@example.com',
    '//userid@example.com/',
    '//userid@example.com:8080',
    '//userid@example.com:8080/',
    '//userid:password@example.com',
    '//userid:password@example.com/',
    '//142.42.1.1/',
    '//142.42.1.1:8080/',
    '//foo.com/blah_(wikipedia)#cite-1',
    '//foo.com/blah_(wikipedia)_blah#cite-1',
    '//foo.com/(something)?after=parens',
    '//code.google.com/events/#&product=browser',
    'j.mp',
    '//-.~_!$&()*+,;=:%40:80%2f::::::@example.com',
    '-.~_!$&()*+,;=/:%40:80%2f::::::@example.com',
    '/foo.bar/baz',
    '//foo.bar/?q=Test%20URL-encoded%20stuff',
    '//1337.net',
    '//a.b-c.de',
    '//223.255.255.254',
    '//foo.bar/%ba',
    '//foo.bar/../../',
    '//foo.bar/../...../asd',
    '//foo.com/#)(',
    'foo:',
)

INVALID_URI_REFS = (
    ':foo',
    '-.~_!$&()*+,;=:%40:80%2f::::::@example.com',
)


@pytest.mark.parametrize('rule', ('URI', 'URI_reference'))
@pytest.mark.parametrize('url', VALID_URIS)
def test_valid_urls(url, rule):
    assert validate_rfc3986(url, rule=rule)


@pytest.mark.parametrize('url', VALID_URI_REFS)
def test_valid_urls_ref(url):
    assert validate_rfc3986(url, rule='URI_reference')


@pytest.mark.parametrize('url', INVALID_URIS)
def test_invalid_urls(url):
    assert not validate_rfc3986(url)


@pytest.mark.parametrize('url', INVALID_URI_REFS)
def test_invalid_urls_ref(url):
    assert not validate_rfc3986(url, rule='URI_reference')


@pytest.mark.parametrize('url', INVALID_URIS + VALID_URIS)
def test_against_legacy(url):
    legacy = True
    try:
        rfc3987.parse(url, rule='URI')
    except ValueError:
        legacy = False
    new = validate_rfc3986(url)
    assert legacy == bool(new)


@pytest.mark.parametrize('url', INVALID_URIS + VALID_URIS)
def test_against_legacy_ref(url):
    legacy = True
    try:
        rfc3987.parse(url, rule='URI_reference')
    except ValueError:
        legacy = False
    new = validate_rfc3986(url, rule='URI_reference')
    assert legacy == bool(new)


@settings(max_examples=1000)
@given(url=prov_st.urls())
def test_against_legacy_hypothesis(url):
    print(url)
    legacy = True
    try:
        rfc3987.parse(url, rule='URI')
    except ValueError:
        legacy = False
    new = validate_rfc3986(url)
    assert legacy == bool(new)
