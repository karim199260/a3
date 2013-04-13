from splinter import Browser
from lettuce import *
import ipdb
import urllib

# world.browser = Browser('chrome')
world.browser = Browser('zope.testbrowser')

@step(u'I go to the "(.*)" URL')
def i_go_to_the_url(step, url):
    url = 'http://localhost:8080{}'.format(url)
    world.browser.visit(url)
    assert world.browser.url == url
    assert world.browser.is_text_present('Get the Buzz')

@step(u'I fill in "(.*)" with "(.*)"')
def i_fill_in(step, field, value):
    world.browser.fill(field, value)
    assert world.browser.find_by_name(field).first.value == value

@step(u'I click "(.*)"')
def i_click(step, button_name):
    button = world.browser.find_by_name(button_name).first
    button.click()

@step(u'I should see "(.*)"')
def i_see(step, text):
    assert 'get_coordinates' not in world.browser.url
    assert text in world.browser.html