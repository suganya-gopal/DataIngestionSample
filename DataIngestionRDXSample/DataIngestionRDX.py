import psycopg2
import json
from json import loads,dumps
import os
os.chdir(os.path.dirname(__file__))
from MasterConfig import MasterConfigReader
from pathlib import Path

class DataIngestionRDX(object):
    def __init__(self):
        conf_obj = MasterConfigReader()
        self.rdx_file_path = Path(conf_obj.get("data_ingestion_config","rdx_data_path"))
        self.host = conf_obj.get("db_config","hostname")
        self.db = conf_obj.get("db_config","db")
        self.user = conf_obj.get("db_config","user")
        self.port = conf_obj.get("db_config","port")
        self.pwd = conf_obj.get("db_config","password")
    
    def ingest_rdx_data(self):
        try:
            with open(self.rdx_file_path) as fobj:
                sampleData = fobj.read();
            sample_Data = json.loads(sampleData)
            print(type(sample_Data))
            conn = psycopg2.connect(host=self.host,database=self.db,user=self.user,password=self.pwd)
            cur=conn.cursor()
            for data in sample_Data["organizations"] :
                for key,value in data.items():
                    if value == None:
                        data[key] = "None"
                org_query = """INSERT INTO organization(id,name,alternate_name,description,email,url,tax_status,tax_id,year_incorporated,legal_status) 
                               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cur.execute(org_query,(data["id"],data["name"],data["alternateName"],data["description"],"Not Available",data["url"],data["taxStatus"],data["taxId"],data["yearIncorporated"],data["legalStatus"],))
                conn.commit()
                for service in data["services"]:
                    serv_query = """INSERT INTO service(id,organization_id,program_id,location_id,name,alternate_name,description,url,email,status,interpretation_services,
                                    application_process,wait_time,fees,accreditations,licenses,taxonomy_ids) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    taxonomy_ids = [i["code"] for i in service["taxonomy"]]
                    cur.execute(serv_query,(service["idService"],service["idOrganization"],"Not Available","Not Available",service["name"],service["alternateName"],service["description"],service["url"],service["email"],service["status"],"Not Available",service["applicationProcess"],service["waitTime"],service["fees"],service["accreditations"],"Not Available",",".join(taxonomy_ids),))
                    conn.commit()
                for loc in data["locations"]:
                    loc_query = """INSERT INTO location(id,organization_id,name,alternate_name,description,transportation,latitude,longitude) VALUES    
                                    (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cur.execute(loc_query,(loc["idLocation"],data["id"],loc["name"],loc["alternateName"],loc["description"],loc["transportation"],loc["latitude"],loc["longitude"],)) 
                    conn.commit()
                    for servAtLoc in loc["serviceAtLocation"]:
                        servatloc_query = """INSERT INTO service_at_location(id,service_id,location_id,description) VALUES(%s,%s,%s,%s)"""
                        cur.execute(servatloc_query,(servAtLoc["idServiceAtLocation"],servAtLoc["idService"],servAtLoc["idLocation"],"Not Available",))
                        conn.commit()
            cur.close()
        except Exception as e:
            print("Some error occurred while ingesting data to postgres - "+str(e))
            
            
            
DataIngestionRDX().ingest_rdx_data()