# This package generates data from a tweeter user and helps to do temporal analysis of the data.

## Different folders and their content
1. **Data**:

	Each .csv file contains pipe(|) separated data.
	The columns are

	`tweet_id | language | time_created | Retweet_flag | Retweet_count | tweet |`
	

	
2. **src**:
	Contains all source files:
	
	a. **key.dat**:
		
	This file contains the user information about tweeter api.It is json formatted file 
	
	`{"consumer_key":"<your_consumerkey>",
	"consumer_secret":"<your consumer_secret>",
	"access_token":"<your_access_token>",
	"access_secret":"<your_access_secret>"}`
	
	b. **TweetDataMining.ipynb**:
		Contains python code for gathers tweeter data from a user
		
	c. **twitter_analysis.ipynb**: Python code to analyze the temporal data of tweet time and date.
