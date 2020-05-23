from .app import Application

app = Application('test-app')

@app.rule('/prune', methods=('GET','POST'))
def prune(p1, p2, data=None):
    if app.method == 'POST':
        print(data)
        return '<h1>Got it</h1>'
    else:
        return f'<h1>Hello {p1} and {p2}</h1>'

app.print_state()

app.run()
