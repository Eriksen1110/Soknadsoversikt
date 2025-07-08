from gevent import monkey
monkey.patch_all()


from gevent.pywsgi import WSGIServer
from app import app


mode = 'production'
#mode = 'development'

def run_app():
    if (mode == 'production'):
        address  = '0.0.0.0'
        app.db_mode = 'production'
        port = 80
    
    elif (mode == 'development'):
        address     = 'localhost'
        app.db_mode = 'development'
        port = 5001
    return address, port

if __name__ == "__main__":
    address,port = run_app()
    http_server = WSGIServer((address, port), app)
    http_server.serve_forever()