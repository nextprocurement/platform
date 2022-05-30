from fastapi import FastAPI, File, UploadFile
from typing import Optional
from json2xml import json2xmlAPI
from xml2rdf_morph import xml2rdfAPI
from publish_rdf import publish_rdfAPI
import uvicorn
import shutil
from pathlib import Path
import os 

API_PORT = float(os.environ['API_PORT'])
LOG_LEVEL = os.environ['LOG_LEVEL']

app = FastAPI()

#
#@app.get("/")
#def read_root():
#    return {"Hello": "World"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}

@app.post("/uploadfiles/{item_id}")
def save_upload_file(upload_files: list[UploadFile], destination: Path) -> None:
    for upload_file in upload_files:
        try:
            destination_for_file = Path(str(destination) + "/" + upload_file.filename)
            if not os.path.exists(destination):
                try:
                    os.mkdir(destination)
                except OSError:
                    print("Creation of the directory %s failed" % destination)
                else:
                    print("Successfully created the directory %s " % destination)
            with destination_for_file.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()

@app.get("/json2xmlAPI/{item_id}")
def read_item(start_date: str, end_date: str, input_folder:str, output_folder:str):
    value = json2xmlAPI(start_date, end_date, input_folder, output_folder)
    return {"json2xml final value": value}

@app.get("/xml2rdfAPI/{item_id}")
def read_item(start_date: str, end_date: str, input_folder:str, output_folder:str):
    value = xml2rdfAPI(start_date, end_date, input_folder, output_folder)
    return {"xml2rdf final value": value}

@app.get("/publish_rdfAPI/{item_id}")
def read_item(start_date: str, end_date: str, input_folder:str):
    value = publish_rdfAPI(start_date, end_date, input_folder)
    return {"publish_rdf final value": value}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=API_PORT, log_level=LOG_LEVEL)


# '2019-01-01'
# '2019-01-01'
