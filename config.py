"""
This is the configuration file. It's necessary to set following parameters.
"""
WKHTMLTOPDF='/path_to/wkhtmltopdf-i386'
"""
It's the path of binary wkhtmltopdf file. It's necessary for the correct mutant work
"""
SOCKET_PATH='/path_to/mutant.socket'
"""
It's the socket that will process all tasks. It's important that socket file exists.
"""
MULE_ID=1
"""
It's the mule id. Mutant works only with uWSGI application server. 
For more informations look at: http://projects.unbit.it/uwsgi/
"""
TIMEOUT=30
"""
It's max time that client will wait
"""
