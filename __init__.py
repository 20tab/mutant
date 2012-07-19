"""
Mutant is a module to transform your html template in a pdf file in a simple way.
Mutant has some dependences:
1) You have to install wkhtmltopdf. You can find it at: http://code.google.com/p/wkhtmltopdf/
2) You have to install pyzmq. For more informations look at: https://github.com/zeromq/pyzmq
3) It's work only with uWSGI application server and its documentation is here: http://projects.unbit.it/uwsgi/
4) Obviously it's a django application, so...
"""
from uwsgidecorators import *
import zmq
import subprocess
from mutant import config

VERSION = (0,0,1)
__version__ = '.'.join(map(str, VERSION))
DATE = "2012-07-18"

zmqcontext = None

@postfork
def create_zmq_context():
    """
    It starts a new zeroMQ thread for each process (also mule)
    """
    global zmqcontext
    zmqcontext = zmq.Context()
def enqueue(html, output, header='', footer='', opts=''):
    """
    It enqueues tasks in socket
    """
    global zmqcontex
    socket = zmqcontext.socket(zmq.REQ)
    socket.connect('ipc://%s' % config.SOCKET_PATH)

    socket.send("convert|%s|%s|%s|%s|%s" % (html, output, header, footer, opts))

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    # wait for response
    socks = poller.poll(config.TIMEOUT*1000)
    if not socks:
        return False
    response = socket.recv()
    if response == 'done':
        return True
    return False

# la funzione che richiama wkhtmltopdf
def convert_pdf(msg):
    items = msg.split('|')
    cmd = [config.WKHTMLTOPDF]
    for i in items[5].split():
        cmd.append(i)

    if items[3] != '':
        cmd.append('--header-html')
        cmd.append(items[3])

    if items[4] != '':
        cmd.append('--footer-html')
        cmd.append(items[4])
    # source
    cmd.append(items[1])
    #destination
    cmd.append(items[2])

    print "running %s" % cmd
    p = subprocess.Popen(cmd)
    if p.wait() == 0:
        return True
    return False

# il consumer della coda delle conversioni (gira in un mulo)
@mule(config.MULE_ID)
def pdf_convert_consumer():
    # setto il nome al processo (per essere piu' fico)
    uwsgi.setprocname('uWSGI mutant')

    # mi metto in ascolto sul socket della coda
    global zmqcontext
    socket = zmqcontext.socket(zmq.REP)
    socket.bind('ipc://%s' % config.SOCKET_PATH)
    print "ready to encode html to pdf..."
    while True:
        # un nuovo messaggio !!!
        msg = socket.recv()
        # lancio la conversione
        if convert_pdf(msg):
            socket.send("done")
        else:
            socket.send("error")

