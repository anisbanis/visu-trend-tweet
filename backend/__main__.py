#from .app import Application
#
#app = Application('prout')
#
#@app.rule('/prune')
#def prune():
#    print('test')
#    return 'bite'
#
#app.print_state()
#
#app.run()

from .server import main

main()
