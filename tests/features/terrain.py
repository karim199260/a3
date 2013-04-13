from lettuce import before, after, world

@after.all
def teardown_browser(total):
    world.browser.quit()