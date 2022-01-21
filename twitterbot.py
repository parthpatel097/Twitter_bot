import tweepy
import config
import argparse
import time
from mysql.connector.constants import ClientFlag
import mysql.connector
from mysql.connector.errors import IntegrityError


conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='twitterbot',
    charset='utf8')


cursor = conn.cursor()
print('Connect')


ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="query keyword for find from tweets data")
ap.add_argument("-m", "--comment", required=True,
	help="comment which want to post on twitter")
args = vars(ap.parse_args())

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
            # print(results)
        for i in results:
                sql1 = "INSERT INTO tweet_info(tweet_id) VALUES (%s)"
                val1= (i,)
                cursor.execute(sql1, val1)
                conn.commit()    
    else:
        return []      
    
    return results

def getComment(comment):
    # id = '1470263879326441475'
    tweets = searchKeyword(args["query"])
    newDict = []
    if len(tweets) > 0 :
        for x in tweets :
            newDict.append(x)
           
    # print(newDict)
    for id in newDict:
        try:
            cursor.execute("select posted from tweet_info")
        # get all records
            records = cursor.fetchall()
            # print("Total number of rows in table: ", cursor.rowcount)
            for row in records:
                print(row)
                if row[0]==0:
                    client = getClient()
                    time.sleep(60) # Dealy of 1 Minute to post reply 
                    response = client.create_tweet(text=comment, in_reply_to_tweet_id=id)
                    update_db = "Update tweet_info set posted=1 Where tweet_id= %s"
                    val2 = (id,)
                    cursor.execute(update_db,val2)
                    # conn.commit()
                    print(" Successfully Commented!!! ")
                else:
                    print("Not update")
        except IntegrityError:
            print("Duplicate tweet found!")
        except:
            print("Not created!")
            
    conn.commit()
    return ""


# call the function 
post_comment = getComment(args["comment"])

# searchKeyword(args["query"])