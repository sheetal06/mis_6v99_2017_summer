#twitter analytics
import pandas as pd#importing pandas library
import requests
inputurl = "http://kevincrook.com/utd/tweets.json"#input url to extract the tweets
response = requests.get(inputurl)#response stores the http response
messages = pd.io.json.json_normalize(response.json())#normalizing json data using pandas
message = messages[['text','lang']]#extracting text and language properties from normalized json
message1 = message[message.text.notnull()]#considering events which are not null
twtr_analytcs = open("twitter_analytics.txt",'w',encoding="utf-8")#writing to text file with utf-8 coding
print(len(messages),file=twtr_analytcs)#printing the number of tweets
print(len(message1),file=twtr_analytcs)#Total no. of tweet events are printed
message3 = message1.groupby('lang').count()#taking count of each language
dictionary = message3.to_dict()
frequency_dictionary = dictionary['text']#language frequency to file
for k,v in sorted(frequency_dictionary.items(), key=lambda x: x[1], reverse = True):
    print(",".join([k,str(v)]),file=twtr_analytcs)
twtr_analytcs.close()
tweets_text = open(file="tweets.txt", mode="w", encoding="utf-8")# tweet content to a file 
for twt in message1['text']:
    print(twt,file=tweets_text)
tweets_text.close()
