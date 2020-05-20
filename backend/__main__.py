from .app import Application

app = Application('test-app')

@app.rule('/prune')
def prune():
    print('test')
    return 'test'

app.print_state()

app.run()