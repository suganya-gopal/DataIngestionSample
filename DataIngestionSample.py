import psycopg2
import json
from json import loads,dumps
import os
os.chdir(os.path.dirname(__file__))

with open(r"C:\Users\suganya.gopal\Desktop\Suganya\python-postgres\sampledata.txt.") as fobj:
    sampleData = fobj.read();
sample_Data = json.loads(sampleData)
print(type(sample_Data))
conn = psycopg2.connect(host="localhost",database="sampledb",user="postgres",password="admin")
cur=conn.cursor()
for data in sample_Data["employeedetails"] :
    print(data["id"])
    print(data["name"])
    query = """INSERT INTO company(empid,empName,empEmail) VALUES(%s,%s,%s)"""
    cur.execute(query,(data["id"],data["name"],data["email"],))
    conn.commit()
    for skills in data["skills"]:
        skill_query = """INSERT INTO skillset(idSkill,skillName,duration) VALUES(%s,%s,%s)"""
        cur.execute(skill_query,(skills["idskill"],skills["skillname"],skills["duration"],))
        conn.commit()
cur.close()