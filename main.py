import base64
import filetype
import json

from fastapi import FastAPI, Request

app = FastAPI()

CHATTY_LOGS = False


@app.get("/")
def read_root():
    """ This endpoint proves that requests and responses are flowing."""
    return {"Hello": "World"}


@app.get("/agreement_all_events")
def agreement_all_events_get(request: Request):
    """This GET endpoint verifies the intent of the Webhook"""
    client_id = request.headers['x-adobesign-clientid']
    return {'xAdobeSignClientId': client_id}


@app.post("/agreement_all_events")
async def agreement_all_events_post(request: Request):
    """This POST endpoint prints some details of the Webhook request sent on all Agreement events"""
    body = await request.json()
    if CHATTY_LOGS:
        print(f"request-body: {json.dumps(body, indent=2)}")
    print('-' * 80)
    print(f'event: at {body["eventDate"]} {body["event"]}')
    print(f'agreement id: {body["agreement"]["id"]}')
    print(f'agreement id: {body["agreement"]["status"]}')
    print('-' * 80)
    return {}


@app.get("/agreement_workflow_completed")
def agreement_workflow_completed_get(request: Request):
    """This GET endpoint verifies the intent of the Webhook"""
    client_id = request.headers['x-adobesign-clientid']
    return {'xAdobeSignClientId': client_id}


@app.post("/agreement_workflow_completed")
async def agreement_workflow_completed_post(request: Request):
    """Respond to Agreement Workflow Completed events.
    Store and check the type of the final document, if it was requested in the Webhook definition.
    """
    body = await request.json()
    if CHATTY_LOGS:
        print(f"request-body: {json.dumps(body, indent=2)}")
    print('-' * 80)
    print(f'event: at {body["eventDate"]} {body["event"]}')
    agreement_id = body['agreement']['id']
    agreement_name = body['agreement']['name']
    print(f"agreement id: {agreement_id}\ndocument name: {agreement_name}")
    if body['agreement'].get('signedDocumentInfo', None):
        file_content = body['agreement']['signedDocumentInfo']['document']
        file_content = base64.b64decode(file_content)
        with open('received_file.pdf', 'wb') as received_file:
            received_file.write(file_content)
        kind = filetype.guess('received_file.pdf')
        print(f"MIME type from magic: {kind.mime}")
        # TODO: possibly store the file, or queue it for storage.
    print('-' * 80)
    return {}
