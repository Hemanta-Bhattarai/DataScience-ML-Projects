# This package generates the network from the tweeter user name

## Different folders and their content
1. **Network_Data**:

	Each .dat file contains tab separated node ids in a network. The first node ( first node id ) is the is connected to all the remaining nodes ( node ids). So, the first node can be considered as parent node and all the remaining node are children node to first node. All all nodes in all given .dat files are used it forms a network.
	

	
2. **scr**:
	Contains all source files:
	
	a. **key.dat**:
		
	This file contains the user information about tweeter api.It is json formatted file 
	
	`{"consumer_key":"<your_consumerkey>",
	"consumer_secret":"<your consumer_secret>",
	"access_token":"<your_access_token>",
	"access_secret":"<your_access_secret>"}`
	
	b. **FollowerNetwork.ipynb**:
		Contains python code for generation of the network
		
	c. **convertUItoUnique.py**: Python code to change the tweeter user id in the nodes to some unique integer to hide the nodes identity.


3. data_souce.dat: contains the link for full data source
	
	[https://drive.google.com/drive/folders/1qoPNC5CzqpnXhI-TkT48DJ6YvJceQ5jK?usp=sharing]