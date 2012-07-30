mutant
=============

Mutant is a django application to transform your html template or external link in a pdf file in a simple way.<br/>
Mutant has some dependences:<br/>
1) You have to install wkhtmltopdf. You can find it at: http://code.google.com/p/wkhtmltopdf/<br/>
2) You have to install pyzmq. For more informations look at: https://github.com/zeromq/pyzmq<br/>
3) It works only with uWSGI application server and its documentation is here: http://projects.unbit.it/uwsgi/<br/>
4) Obviously it's a django application, so...<br/>

## Usage

First af all you have to configure config.py in mutant package.

Then, set uwsgi parameters in your ini configuration:

``` ini
import = mutant
mule = 1

```

``` py
from mutant.views import pdf_to_response

def myview(request): 
    html= "template_name.html" #or external link like 'www.google.com'. In this case you have to set ext_url = True in pdf_to_response
    dest = "/path_to_destination_file/filename.pdf"
    
    return pdf_to_response(request,html,dest)

```
