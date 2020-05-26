from backend import Application as App
from backend import load_file
import pandas as pd
import json

app = App(__name__, host='0.0.0.0', port=8080)

df = pd.read_csv("tweets.csv")

@app.rule('/tweets_number', methods=('GET,'))
def get_number_tweets():
    return len(df)
 
    
@app.rule('/tweets_place', methods=('GET,'))
def places_country_tweets():
    tmp = df.groupby('place_country_code').count().sort_values(by='id', ascending = False)
    places_count = tmp['id'].c
    ville = tmp.index.tolist()[:10]
    l={}
    idx=0
    for v in ville:
        l[str(v)]=places_count[idx]
        idx+=1
    return json.dumps(l)

@app.rule('/search', methods=('GET,'))
def search(p):
    tmp=df.loc[df['text'].str.lower().str.contains(p)]
    print(p)
    l =len(tmp)
    l
    tmp = tmp.groupby('place_country_code').count().sort_values(by='id', ascending = False)
    places_count = tmp['id'].values.tolist()[:10]
    ville = tmp.index.tolist()[:10]
    rep={}
    idx=0
    """
    h0=df.loc[df["hashtag_0"].notnull()].groupby('hashtag_0').count().sort_values(by='id', ascending = False) 
    h1=df.loc[df["hashtag_1"].notnull()].groupby('hashtag_1').count().sort_values(by='id', ascending = False) 
    h2=df.loc[df["hashtag_2"].notnull()].groupby('hashtag_2').count().sort_values(by='id', ascending = False)
    """
    for v in ville:
        rep[str(v)]=places_count[idx]
        idx+=1
    return json.dumps({'l':l,'rep':rep})

@app.rule('/tweet_pos', methods=('GET,'))
def tweet_pos(txt):
    tmp=df.loc[df['text'].str.contains (txt)]
    pos=tmp[['longitude','latitude']].values.tolist()
    return json.dumps(pos)

app.run()
