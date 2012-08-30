from mutant import enqueue
from django.http import HttpResponse
from django.template.loader import render_to_string
import os

def pdf_to_response(request,html, output, header='', footer='', opts='', vars_dict = {}, save_as = False, ext_url = False):
    """
    It returns a response as pdf attached file. It accepts following parameters:
    - request: simply http request
    - html: this is the source html file you want to transform in pdf. You must define it as file path
    - output: this is the destination pdf file. Also it must be a file path
    - header: it's the html file contains header you want repeat in all pages 
    - footer: it's the html file contains footer you want repeat in all pages 
    - opts: it's a string as a list of parameters like written in a command line. For more informations
    look http://madalgo.au.dk/~jakobt/wkhtmltoxdoc/wkhtmltopdf-0.9.9-doc.html
    - vars_dict: it's a dictionary containing all context variables used in your template
    - save_as: if True, response is a file to save on your pc 
    - ext_url: if True there isn't template to render but an external link.
    """
    output = os.path.abspath(output)
    if not ext_url:
        html = render_local_file(html,vars_dict,'body')
        if header != '':
            header = render_local_file(header,vars_dict,'header')
        if footer != '':
            footer = render_local_file(footer,vars_dict,'footer')
    if enqueue(html, output, header, footer, opts):
        data = None
        with open(output, "rb") as f:
            data = f.read()
        response = HttpResponse(data, mimetype='application/pdf')
        response['X-Sendfile'] = output
        response['Content-Type'] = 'application/pdf'
        if save_as:
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(output)
        remove_all(html,header,footer,ext_url)
        return response
    else:
        remove_all(html,header,footer,ext_url)
        return HttpResponse("Warning!! Something was wrong in mutant.views.pdf_to_response")

def render_local_file(html,vars_dict,tpl_type):
    rendered = render_to_string(html,vars_dict)
    with open('%s.html' % tpl_type,'w+') as fp:
        fp.write(rendered)
    return os.path.abspath('%s.html' % tpl_type)

def remove_temp_file(temp_file):
    if os.path.exists(temp_file):
        os.remove(temp_file)

def remove_all(html,header,footer,ext_url):
    if not ext_url:
        if html:
            remove_temp_file(html)
        if header:
            remove_temp_file(header)
        if footer:
            remove_temp_file(footer)