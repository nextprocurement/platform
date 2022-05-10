from json2xml import json2xmlAPI

start_date = "2019-01-01"
end_date = "2019-01-02"
input_folder = "/Users/Pedro/Desktop/TBFY_data/TBFY_DATA_DUMP_JSON/3_JSON_Enriched"
output_folder = "/Users/Pedro/Desktop/TBFY_data/TBFY_DATA_DUMP_JSON/XML"

value = json2xmlAPI(start_date, end_date, input_folder, output_folder)

print(value)
