import sys
from index import Index
from bottle import route, run, template, request, response

# to simulate readiness delay 
import time
import threading

index = Index(None)

@route('/')
def search():
    q = request.query.q
    print(q, type(q))
    return dict(results=list(index.search(str(q))))

@route('/readiness')
def readiness():
 
    print('readiness', index.isReady)
    if index.isReady:
        response.status = 200
        return dict({"Status":"Ready."})
    else:
        response.status = 503
        return dict({"Status":"Not ready."})

def init_index():
    global index
    print('init_index started index.isReady:', index.isReady)
    index = Index.new(sys.argv[1])
    time.sleep(40)
    index.isReady = True
    print('init_index finished index.isReady:', index.isReady)

if __name__ == '__main__':
   
    thread = threading.Thread(target=init_index, args=())
    thread.daemon = True                            
    thread.start()                                  

    

    run(host='0.0.0.0', port=8080, debug=True)
