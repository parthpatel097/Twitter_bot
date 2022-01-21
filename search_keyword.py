import tweepy
import config



def getClient():
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN, 
                           consumer_key=config.CONSUMER_KEY, 
                           consumer_secret=config.CONSUMER_SECRET,
                           access_token=config.ACCESS_TOKEN,
                           access_token_secret=config.ACCESS_TOKEN_SEC)
    
    return client
def searchKeyword(query):
    client = getClient()
    tweets = client.search_recent_tweets(query=query, max_results=10)
    tweet_data = tweets.data
    results = []
    
    if not tweet_data is None and len(tweet_data) > 0:
        for tweet in tweet_data:
            results.append(tweet.id)
    else:
        return []      
    
    return results

def getComment(comment):
    # id = '1470263879326441475'
    tweets = searchKeyword('KashiVishwanathDham')
    newDict = []
    if len(tweets) > 0 :
        for x in tweets :
            newDict.append(x)
           
    print(newDict)       
    for id in newDict:
        try:
            client = getClient()
            response = client.create_tweet(text=comment, in_reply_to_tweet_id=id)
            print(" Successfully Commented!!! ")
        except:
            print("Error creating tweet")

    return response

# call the function 
post_comment = getComment("I liked your thoughts")

