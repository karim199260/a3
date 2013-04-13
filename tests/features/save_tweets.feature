Feature: Store Tweets in Google DataStore
	Scenario: Store and retrieve dummy objects from the db
		Given I have the following tweets in the database
			| id	| text			| from_user		| profile_image_url		| created_at						| location_name		|
			| 1		| dummy tweet 1	| chrishaum		| http://goo.gl/vM8dS	| Thu, 06 Oct 2011 19:36:17 +0000	| New York, NY		|
			| 2		| dummy tweet 2	| mattmeisinger	| http://goo.gl/Yac5t	| Thu, 06 Oct 2013 19:36:17 +0000	| Long Island, NY	|
		When I search the "location_name" for "New York, NY" in the database
		Then I should see the following tweets:
			| 1		| dummy tweet 1	| chrishaum		| http://goo.gl/vM8dS	| Thu, 06 Oct 2011 19:36:17 +0000	| New York, NY		|
		But I should not see the following tweets:
			| 2		| dummy tweet 2	| mattmeisinger	| http://goo.gl/Yac5t	| Thu, 06 Oct 2013 19:36:17 +0000	| Long Island, NY	|