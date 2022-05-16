import logging
import azure.functions as func

import io, os
import mimetypes

import pandas as pd
import numpy as np

def openfile(name="index.html"):
    """
    Function to open file from /static/ folder with HTML files.
    """
    path = 'static'
    filename = f"{path}/{name}"
    with open(filename, 'rb') as f:
        mimetype = mimetypes.guess_type(filename)
        return f.read(), mimetype

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        #Base on name parameter display given web page
        if name == 'index.html':
            #Local http://localhost:7071/api/HttpTrigger?name=index.html
            file, mimetype = openfile("index.html")
            file = str(file.decode('UTF-8'))

            return func.HttpResponse(
                body = file,
                headers={'content-type':'text/html'},
                status_code=200
            )

        else:
            return func.HttpResponse(body = f"404: You pass, {name}. Web page is missing.", status_code=404)
    else:
        func.HttpResponse(body = f"404: Youdo not passpage name as parameter. Web page is missing.", status_code=404)
