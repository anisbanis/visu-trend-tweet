[1mdiff --git a/vtt.py b/vtt.py[m
[1mindex 4a8e33d..8a415d4 100644[m
[1m--- a/vtt.py[m
[1m+++ b/vtt.py[m
[36m@@ -1,5 +1,7 @@[m
 from backend import Application as App[m
 from backend import load_file[m
[32m+[m[32mimport pandas as pd[m
[32m+[m[32mimport json[m
 [m
 app = App(__name__)[m
 [m
[36m@@ -7,4 +9,59 @@[m [mapp = App(__name__)[m
 def index():[m
     return {"abc":1}[m
 [m
[31m-app.run()[m
\ No newline at end of file[m
[32m+[m
[32m+[m[32m@app.rule('/prune', methods=('GET','POST'))[m
[32m+[m[32mdef prune(p1, p2, data=None):[m
[32m+[m[32m    if app.method == 'POST':[m
[32m+[m[32m        print(data)[m
[32m+[m[32m        return '<h1>Got it</h1>'[m
[32m+[m[32m    else:[m
[32m+[m[32m        return '<h1>Hello {p1} and {p2}</h1>'[m
[32m+[m[41m    [m
[32m+[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mdf = pd.read_csv("tweets.csv")[m
[32m+[m
[32m+[m[32m@app.rule('/tweets_number', methods=('GET,'))[m
[32m+[m[32mdef get_number_tweets():[m
[32m+[m[32m    return len(df)[m
[32m+[m[41m [m
[32m+[m[41m    [m
[32m+[m[32m@app.rule('/tweets_place', methods=('GET,'))[m
[32m+[m[32mdef places_country_tweets():[m
[32m+[m[32m    tmp = df.groupby('place_country_code').count().sort_values(by='id', ascending = False)[m
[32m+[m[32m    places_count = tmp['id'].values.tolist()[:10][m
[32m+[m[32m    ville = tmp.index.tolist()[:10][m
[32m+[m[32m    l={}[m
[32m+[m[32m    idx=0[m
[32m+[m[32m    for v in ville:[m
[32m+[m[32m        l[str(v)]=places_count[idx][m
[32m+[m[32m        idx+=1[m
[32m+[m[32m    return json.dumps(l)[m
[32m+[m
[32m+[m[32m@app.rule('/search', methods=('GET,'))[m
[32m+[m[32mdef search(p):[m
[32m+[m[32m    tmp=df.loc[df['text'].str.contains(p)][m
[32m+[m[32m    print(p)[m
[32m+[m[32m    l =len(tmp)[m
[32m+[m[32m    l[m
[32m+[m[32m    tmp = tmp.groupby('place_country_code').count().sort_values(by='id', ascending = False)[m
[32m+[m[32m    places_count = tmp['id'].values.tolist()[:10][m
[32m+[m[32m    ville = tmp.index.tolist()[:10][m
[32m+[m[32m    rep={}[m
[32m+[m[32m    idx=0[m
[32m+[m[32m    """[m
[32m+[m[32m    h0=df.loc[df["hashtag_0"].notnull()].groupby('hashtag_0').count().sort_values(by='id', ascending = False)[m[41m [m
[32m+[m[32m    h1=df.loc[df["hashtag_1"].notnull()].groupby('hashtag_1').count().sort_values(by='id', ascending = False)[m[41m [m
[32m+[m[32m    h2=df.loc[df["hashtag_2"].notnull()].groupby('hashtag_2').count().sort_values(by='id', ascending = False)[m
[32m+[m[32m    """[m
[32m+[m[32m    for v in ville:[m
[32m+[m[32m        rep[str(v)]=places_count[idx][m
[32m+[m[32m        idx+=1[m
[32m+[m[32m    return json.dumps({'l':l,'rep':rep})[m
[32m+[m[41m    [m
[32m+[m
[32m+[m
[32m+[m[32mapp.run()[m
