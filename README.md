django-mutant
=============

Mutant is a module to transform your html template in a pdf file in a simple way.<br/>
Mutant has some dependences:<br/>
1) You have to install wkhtmltopdf. You can find it at: http://code.google.com/p/wkhtmltopdf/<br/>
2) You have to install pyzmq. For more informations look at: https://github.com/zeromq/pyzmq<br/>
3) It works only with uWSGI application server and its documentation is here: http://projects.unbit.it/uwsgi/<br/>
4) Obviously it's a django application, so...<br/>

## Usage

First af all you have to configure config.py in mutant package.

``` py
from mutant.views import pdf_to_response

def home(request): 
    html= "/path_to_source_file/filename.html"
    dest = "/path_to_destination_file/filename.pdf"
    
    return pdf_to_response(request,html,dest)

```
