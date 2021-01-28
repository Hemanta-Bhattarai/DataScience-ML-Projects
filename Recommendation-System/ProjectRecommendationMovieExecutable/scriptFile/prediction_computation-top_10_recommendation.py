
# coding: utf-8

# In[4]:

import pandas as pan
import numpy as num
fileInput="small_train_set.csv"
Matrix=["cosineBasedSimilarityFast.out","correlatedBasedSimilarityFast.out","adjustedCosineSimilarityFast.out"]
fileMatrix=Matrix[1]
#number of most similar elemet taken during prediction
mostSimilarnum=30
dataFrame=pan.DataFrame(pan.read_csv(fileInput))
dataFrame=dataFrame.drop(dataFrame.columns[0],1)
print("\n\n\n+++++++++++++++++++++++++++++++++++++++++++++++++")
print("Similarity Matrix and data file loaded")

# In[5]:
#deterination of mean of the ratings for specified user i. \bar{R_u}, where u\epsilon U
#mean[i]=\frac{\sum_{usr=i} ratings}{total number of item watched movie i}
mean=num.zeros(max(dataFrame["userId"]))
for usr in range(1,max(dataFrame["userId"])+1):
    mean[usr-1]=num.mean(dataFrame[dataFrame["userId"]==usr]["ratings"])
    


"""


#dataMatrix[userid,movieid]
dataMatrix=num.ones(max(dataFrame["userId"])*max(dataFrame["movieId"])).reshape(max(dataFrame["userId"]),max(dataFrame["movieId"]))
dataMatrix[:]=num.NAN
ratingsOrginal=num.ones(max(dataFrame["userId"])*max(dataFrame["movieId"])).reshape(max(dataFrame["userId"]),max(dataFrame["movieId"]))
ratingsOrginal[:]=num.NAN
dataMatrix=dataMatrix.reshape(max(dataFrame["userId"]),max(dataFrame["movieId"]))
for user in range(1,max(dataFrame["userId"])+1):
    for movie in dataFrame[dataFrame["userId"]==user].movieId:
        dataMatrix[user-1,movie-1]=(dataFrame[(dataFrame["userId"]==user) &(dataFrame["movieId"]==movie)].ratings-mean[usr-1])
        ratingsOrginal[user-1,movie-1]=dataFrame[(dataFrame["userId"]==user) &(dataFrame["movieId"]==movie)].ratings
dataMatrix=num.nan_to_num(dataMatrix)
ratingsOrginal=num.nan_to_num(ratingsOrginal)


"""



dataMatrix=num.loadtxt("dataMatrix.out")
ratingsOrginal=num.loadtxt('ratingsOriginal.out')
#scaled rating matrix of the training data from mean
ratingMat=num.transpose(dataMatrix)
print("\n+++++++++++++++++++++++++++++++++++++++++++++++++")
print("Rating matrix generated")

# In[ ]:

simMat=num.loadtxt(fileMatrix) # similarity matrix
#testing
#using only top most similar movie for the prediction calculations
argSort=simMat.argsort()
totalMovies=num.shape(simMat)[0]
maxSimilarityMoviesConsidered=mostSimilarnum
for var in range(totalMovies):
    simMat[var][argSort[var,0:totalMovies-maxSimilarityMoviesConsidered]]=0

    
#sum of the similarity matrix for a movie i ie \sum_i(abs(s_ij))
sumSim=num.sum(num.abs(simMat),axis=0)

#not normalized rating prediction P[i,j] is not normalized prediciton of user j to movie i
nonNormalizedPrediction=num.matrix(simMat)*num.matrix(ratingMat)
# normalized prediction without scaling by the mean
NormalizedPrediction=num.divide(num.matrix(nonNormalizedPrediction),num.transpose(num.matrix(sumSim)))
# determining the prediction matrix
totalUsers=max(dataFrame["userId"])
totalMovies=max(dataFrame["movieId"])
matrixOfMeans=num.transpose(num.matrix(num.repeat(mean,totalMovies,axis=0)).reshape(totalUsers,totalMovies))
ScaledPrediction=(matrixOfMeans+NormalizedPrediction)
print("\n+++++++++++++++++++++++++++++++++++++++++++++++++")
print("Prediction matrix generated")

# In[47]:

user=raw_input("Enter the userId to whom movie is to be recommended 1-943\n")

user=int(user)-1
predictionsForUser=ScaledPrediction[:,user]
topMovieIdForUser=num.argsort(predictionsForUser,axis=0)
rec=topMovieIdForUser[-100:,:]
rec=rec+1
rec=rec[::-1]


movieWatched=num.matrix(dataFrame[dataFrame["userId"]==user].movieId)
recommendation=[]
for recommended in rec:
    if recommended in movieWatched[:]:
      continue;
    else:
        recommendation.append(recommended)
        
    if len(recommendation)==10:
        break;
            
recommendation=num.array(recommendation)
dataFrameMovie=pan.DataFrame(pan.read_csv("movies.csv"))

#list of movie recommended
print"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "The movies recommended for user with userId: ", user+1
print"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
for element in recommendation:
    print dataFrameMovie.title[element[0][0]-1]
print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n"


# In[ ]:



