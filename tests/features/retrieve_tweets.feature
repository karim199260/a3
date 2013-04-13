Feature: Retrieve Tweets for given Location
    Scenario: Tweets for New York, NY
    	When I go to the "/" URL
        And I fill in "Location name" with "New York, NY"
        And I fill in "Search term" with "bitcoins"
        And I click "Submit"
        Then I should see "Results"
        And I should see "Tweets"