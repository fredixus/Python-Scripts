import logging

import azure.functions as func

import json
from datetime import datetime as dt
import ast

def transformToObject(date):
    return dt.strptime(date, "%Y%M%d")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #Transoform data formats
    try:
        req = req.get_body()
        json_req = json.loads(req)
        logging.info("Requested values: "+ str(json_req))
        #json_req = ["20220515"] YYYYMMDD
        
        datesToTransform = ast.literal_eval(json_req['dates'])
        transformedObjectList = [transformToObject(date) for date in datesToTransform]

        if (json_req['type'] == 'year'):
            logging.info("Returns Year")
            listToReturn = [date.year for date in transformedObjectList]
        elif (json_req['type'] == 'month'):
            logging.info("Returns Month")
            listToReturn = [date.strftime('%M') for date in transformedObjectList]
        elif (json_req['type'] == 'year-month'):
            logging.info("Returns Year-Month")
            listToReturn = [date.strftime('%Y-%M') for date in transformedObjectList]
        elif (json_req['type'] == 'full'):
            logging.info("Returns Year-Month-Day")
            listToReturn = [date.strftime('%Y-%M-%d') for date in transformedObjectList]
        elif (json_req['type'] == 'en' or  json_req['type'] == 'EN'):
            logging.info("Returns English date")
            listToReturn = [date.strftime('%d %B %Y') for date in transformedObjectList]
        elif (json_req['type'] == 'us' or  json_req['type'] == 'US'):
            logging.info("Returns US date")
            listToReturn = [date.strftime('%B %d, %Y') for date in transformedObjectList]
        elif (json_req['type'].find('custom')==0):
            logging.info("Returns Custom Mask for datetime")
            #custom %Y/%M/%d
            customText = json_req['type'].replace("custom ","")
            listToReturn = [date.strftime(customText) for date in transformedObjectList]
        else:
            return func.HttpResponse(
                "No info of return type.",
                status_code=401
            )

        return func.HttpResponse(
                json.dumps([str(date) for date in listToReturn]),
                status_code=200
            )
    except:
        logging.warning('Error wrong request')
        return func.HttpResponse(
             "Wrong request was sended to API, try Again.",
             status_code=404
        )
