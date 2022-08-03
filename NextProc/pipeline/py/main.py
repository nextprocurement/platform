from fastapi import FastAPI, File, UploadFile
from typing import Optional
from json2xml import json2xmlAPI
from xml2rdf_morph import xml2rdfAPI
from publish_rdf import publish_rdfAPI
from json2xml import json2xmlAPI_noDate
from xml2rdf_morph import xml2rdfAPI_noDate
from publish_rdf import publish_rdfAPI_noDate
from applyRules import processingAPI_noDate
import uvicorn
import shutil
from pathlib import Path
import os 

API_PORT = float(os.environ['API_PORT'])
LOG_LEVEL = os.environ['LOG_LEVEL']

description = """
Next Procurement es un proyecto que pretende reutilizar y armonizar
las enormes cantidades de datos abiertos sobre contratación pública disponibles 
en el portal de datos de la UE en combinación con los conjuntos de datos abiertos 
sobre contratación pública de los portales de los Estados miembros.

## Next Procurement API

Esta API aloja el entrypoint de la pipeline de ingesta de documentos. Proporciona 
servicio de subida y procesamiento de documentos para su porterior inclusion en
el sistema de almacenamiento en formato rdf 

## Servicios

Los servicios disponibles son

* **pipeline**: Este servicio permite subir, procesar y publicar datos en el servidor con una simple llamada y los datos.
* **uploadfiles**: Servicio de subida de documentos.
* **json2xmlAPI**: Servicio de transformacion de json a xml.
* **xml3rdfAPI**: Servicio construccion del grafo de conocimiento empleando la herrmienta morph-kgc.
* **publish_rdfAPI**: Servicio de publicacion de datos rdf en el servidor de almacenamiento de NextProcurement.
"""

tags_metadata = [
    {
        "name": "pipeline",
        "description": "Este servicio permite subir, procesar y publicar datos en el servidor con una simple llamada y los datos.",
    },
    {
        "name": "uploadfiles",
        "description": "Servicio de subida de documentos.",
    },
    {
        "name": "json2xmlAPI",
        "description": "Servicio de transformacion de json a xml.",
    },
    {
        "name": "xml2rdfAPI",
        "description": "Servicio construccion del grafo de conocimiento empleando la herrmienta morph-kgc.",
    },
    {
        "name": "processingAPI",
        "description": "Traducción parquet a nt.",
    },
    {
        "name": "publish_rdfAPI",
        "description": "Servicio de publicacion de datos rdf en el servidor de almacenamiento de NextProcurement.",
    },
]

app = FastAPI(
    title="Next Procurement",
    description=description,
    version="0.0.1",
    
    #terms_of_service="http://example.com/terms/",
    #contact={
    #    "name": "Deadpoolio the Amazing",
    #    "url": "http://x-force.example.com/contact/",
    #    "email": "dp@x-force.example.com",
    #},
    #license_info={
    #    "name": "Apache 2.0",
    #    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    #},
    openapi_tags=tags_metadata,
)

#
#@app.get("/")
#def read_root():
#    return {"Hello": "World"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}

# @app.post("/pipeline/{item_id}",  tags=["pipeline"])
# def pipeline(upload_files: list[UploadFile], destination: Path) -> None:
#     for upload_file in upload_files:
#         try:
#             destination_for_file = Path(str(destination) + "/files/" + upload_file.filename)
#             if not os.path.exists(destination):
#                 try:
#                     os.mkdir(destination)
#                 except OSError:
#                     print("Creation of the directory %s failed" % destination)
#                 else:
#                     print("Successfully created the directory %s " % destination)

#             destination_file = Path(str(destination) + "/files/")
#             if not os.path.exists(destination_file):
#                 try:
#                     os.mkdir(destination_file)
#                 except OSError:
#                     print("Creation of the directory %s failed" % destination_file)
#                 else:
#                     print("Successfully created the directory %s " % destination_file)
            
#             with destination_for_file.open("wb") as buffer:
#                 shutil.copyfileobj(upload_file.file, buffer)
#         finally:
#             upload_file.file.close()
    
#     input_folder = str(destination) + "/files/"
#     output_folder = str(destination) + "/xml/"
#     value_json2xml = json2xmlAPI_noDate(input_folder, output_folder)
#     input_folder = output_folder
#     output_folder = str(destination) + "/rdf/"
#     value_xml2rdf = xml2rdfAPI_noDate(input_folder, output_folder)
#     input_folder = output_folder
#     value_publishrdf = publish_rdfAPI_noDate(input_folder)

#     return {"json2xml: " + str(value_json2xml) + " | xml2rdf: " + str(value_xml2rdf) + " | publish: " + str(value_publishrdf)}



@app.post("/pipeline/{item_id}",  tags=["pipeline"])
def pipeline(upload_files: list[UploadFile], destination: Path) -> None:
    for upload_file in upload_files:
        try:
            destination_for_file = Path(str(destination) + "/files/" + upload_file.filename)
            if not os.path.exists(destination):
                try:
                    os.mkdir(destination)
                except OSError:
                    print("Creation of the directory %s failed" % destination)
                else:
                    print("Successfully created the directory %s " % destination)

            destination_file = Path(str(destination) + "/files/")
            if not os.path.exists(destination_file):
                try:
                    os.mkdir(destination_file)
                except OSError:
                    print("Creation of the directory %s failed" % destination_file)
                else:
                    print("Successfully created the directory %s " % destination_file)
            
            with destination_for_file.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()
    
    input_folder = str(destination) + "/files/"
    output_folder = str(destination) + "/parquet/"
    value_parquet = processingAPI_noDate(input_folder, output_folder)
    input_folder = output_folder
    value_publishrdf = publish_rdfAPI_noDate(input_folder)

    return {"processingParquet: " + str(value_parquet) + " | publish: " + str(value_publishrdf)}



@app.post("/uploadfiles/{item_id}",  tags=["uploadfiles"])
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

@app.get("/json2xmlAPI/{item_id}",  tags=["json2xmlAPI"])
def read_item(start_date: str, end_date: str, input_folder:str, output_folder:str):
    value = json2xmlAPI(start_date, end_date, input_folder, output_folder)
    return {"json2xml final value": value}

@app.get("/xml2rdfAPI/{item_id}",  tags=["xml2rdfAPI"])
def read_item(start_date: str, end_date: str, input_folder:str, output_folder:str):
    value = xml2rdfAPI(start_date, end_date, input_folder, output_folder)
    return {"xml2rdf final value": value}

@app.get("/publish_rdfAPI/{item_id}",  tags=["publish_rdfAPI"])
def read_item(start_date: str, end_date: str, input_folder:str):
    value = publish_rdfAPI(start_date, end_date, input_folder)
    return {"publish_rdf final value": value}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=API_PORT, log_level=LOG_LEVEL)


# '2019-01-01'
# '2019-01-01'
