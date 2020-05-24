from .app import Application
import pandas as pd
import json

app = Application('test-app')

@app.rule('/prune', methods=('GET','POST'))
def prune(p1, p2, data=None):
    if app.method == 'POST':
        print(data)
        return '<h1>Got it</h1>'
    else:
        return '<h1>Hello {p1} and {p2}</h1>'
    




df = pd.read_csv("tweets.csv")

@app.rule('/tweets_number', methods=('GET,'))
def get_number_tweets():
    return len(df)
 
    
@app.rule('/tweets_place', methods=('GET,'))
def places_country_tweets():
    tmp = df.groupby('place_country_code').count().sort_values(by='id', ascending = False)
    places_count = tmp['id'].values.tolist()[:10]
    ville = tmp.index.tolist()[:10]
    l={}
    idx=0
    for v in ville:
        l[f'{v}']=places_count[idx]
        idx+=1
    return json.dumps(l)

@app.rule('/search', methods=('GET,'))
def search(p):
    tmp=df.loc[df['text'].str.contains(p)]
    print(p)
    l =len(tmp)
    l
    tmp = tmp.groupby('place_country_code').count().sort_values(by='id', ascending = False)
    places_count = tmp['id'].values.tolist()[:10]
    ville = tmp.index.tolist()[:10]
    rep={}
    idx=0
    for v in ville:
        rep[f'{v}']=places_count[idx]
        idx+=1
    return json.dumps({'l':l,'rep':rep})
    





app.print_state()

app.run()
