from backend import Application as App
from backend import load_file

app = App(__name__)

@app.rule('/api')
def index():
    return {"abc":1}

app.run()