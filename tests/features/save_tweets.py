from lettuce import step, world

# Feature: Save Tweets

@step(u'Given I have the following tweets in the database')
def given_tweets_in_the_database(step):
    assert False, u"#FIXME Haven't figured out how to import with lettuce"
    for tweet_dict in step.hashes:
        tweet = world.Tweet(tweet_dict)
        tweet.put()
    


@step(u'When I search the "([^"]*)" for "([^"]*)" in the database')
def when_i_search_the_group1_for_group2_in_the_database(step, group1, group2):
    assert False, 'This step must be implemented'
@step(u'Then I should see the following tweets:')
def then_i_should_see_the_following_tweets(step):
    assert False, 'This step must be implemented'
@step(u'But I should not see the following tweets:')
def but_i_should_not_see_the_following_tweets(step):
    assert False, 'This step must be implemented'