"""
Tests for ``contexts`` submodule
"""
from unittest import TestCase

from pagerdutyapi.contexts import Image, Link


class ImageContextTestCase(TestCase):
    """
    Test case for ``Image`` class
    """
    def test_instantiating_minimal_image(self):
        """
        Check if image with minimal properties will work
        """
        img_src = 'http://www.example.com'
        image = Image(src=img_src)
        self.assertEqual('image', image.type)
        self.assertEqual(img_src, image.src)

    def test_instantiating_maximum_image(self):
        """
        Check if image with maximum properties will work
        """
        img_src = 'http://www.example.com'
        img_href = '{}/href'.format(img_src)
        img_alt = 'This is image'
        image = Image(src=img_src, href=img_href, alt=img_alt)
        self.assertEqual('image', image.type)
        self.assertEqual(img_src, image.src)
        self.assertEqual(img_href, image.href)
        self.assertEqual(img_alt, image.alt)

    def test_serializing_minimal_image(self):
        """
        Check if image with minimal properties will serialize properly
        """
        expected = {
            'src': 'http://www.example.com',
        }
        image = Image(**expected)
        expected['type'] = 'image'
        self.assertEqual(expected, image.to_dict())

    def test_serializing_maximum_image(self):
        """
        Check if image with maximum properties will serialize properly
        """
        expected = {
            'alt': 'This is image',
            'href': 'http://www.example.com/href',
            'src': 'http://www.example.com',
        }
        image = Image(**expected)
        expected['type'] = 'image'
        self.assertEqual(expected, image.to_dict())


class LinkContextTestCase(TestCase):
    """
    Test case for ``Link`` class
    """
    def test_instantiating_minimal_link(self):
        """
        Check if link with minimal properties will work
        """
        link_href = 'http://www.example.com'
        link = Link(href=link_href)
        self.assertEqual('link', link.type)
        self.assertEqual(link_href, link.href)

    def test_instantiating_maximum_link(self):
        """
        Check if link with maximum properties will work
        """
        link_href = 'http://www.example.com'
        link_text = 'This is link text'
        link = Link(href=link_href, text=link_text)
        self.assertEqual('link', link.type)
        self.assertEqual(link_href, link.href)
        self.assertEqual(link_text, link_text)

    def test_serializing_minimal_link(self):
        """
        Check if link with minimal properties will serialize properly
        """
        expected = {
            'href': 'http://www.example.com',
        }
        link = Link(**expected)
        expected['type'] = 'link'
        self.assertEqual(expected, link.to_dict())

    def test_serializing_maximum_link(self):
        """
        Check if link with maximum properties will serialize properly
        """
        expected = {
            'text': 'This is link',
            'href': 'http://www.example.com',
        }
        link = Link(**expected)
        expected['type'] = 'link'
        self.assertEqual(expected, link.to_dict())
