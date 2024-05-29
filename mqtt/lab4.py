import sqlite3
import paho.mqtt.client as mqtt
import json

MQTT_Topic = "Home/BedRoom/#"
mqttBroker = "broker.hivemq.com"

# SQLite DB Name
DB_Name = "IoT.db"

# SQLite DB Table Schema
TableSchema = """
drop table if exists Temperature_Data ;
create table Temperature_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Temperature text
);

drop table if exists Humidity_Data ;
create table Humidity_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Humidity text
);

drop table if exists Pressure_Data ;
create table Pressure_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Pressure text
);
"""

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def fetch_all_records(self, table_name):
        self.cur.execute(f"SELECT * FROM {table_name}")
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.cur.close()
        self.conn.close()

def build_db(TableSchema):
    # Connect or Create DB File
    conn = sqlite3.connect(DB_Name)
    curs = conn.cursor()
    
    # Create Tables
    sqlite3.complete_statement(TableSchema)
    curs.executescript(TableSchema)
    
    # Close DB
    curs.close()
    conn.close()

# Function to save Temperature to DB Table
def Temp_Data_Handler(jsonData):
    # Parse Data 
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['SensorID']
    Data_and_Time = json_Dict['Date']
    Temperature = json_Dict['Temperature']
    
    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Temperature_Data (SensorID, Date_n_Time, Temperature) values (?,?,?)", [SensorID, Data_and_Time, Temperature])
    del dbObj
    print("Inserted Temperature Data into Database.")

# Function to save Humidity to DB Table
def Humidity_Data_Handler(jsonData):
    # Parse Data 
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['SensorID']
    Data_and_Time = json_Dict['Date']
    Humidity = json_Dict['Humidity']
    
    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Humidity_Data (SensorID, Date_n_Time, Humidity) values (?,?,?)", [SensorID, Data_and_Time, Humidity])
    del dbObj
    print("Inserted Humidity Data into Database.")

# Function to save Pressure to DB Table
def Pressure_Data_Handler(jsonData):
    # Parse Data 
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['SensorID']
    Data_and_Time = json_Dict['Date']
    Pressure = json_Dict['Pressure']
    
    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Pressure_Data (SensorID, Date_n_Time, Pressure) values (?,?,?)", [SensorID, Data_and_Time, Pressure])
    del dbObj
    print("Inserted Pressure Data into Database.")

def sensor_Data_Handler(Topic, jsonData):
    if Topic == "Home/BedRoom/1/Temperature":
        Temp_Data_Handler(jsonData)
    elif Topic == "Home/BedRoom/1/Humidity":
        Humidity_Data_Handler(jsonData)    
    elif Topic == "Home/BedRoom/1/Pressure":
        Pressure_Data_Handler(jsonData)    

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    sensor_Data_Handler(message.topic, message.payload)

def display_database_content():
    dbObj = DatabaseManager()
    
    print("\nTemperature Data:")
    temperature_data = dbObj.fetch_all_records("Temperature_Data")
    for row in temperature_data:
        print(row)
    
    print("\nHumidity Data:")
    humidity_data = dbObj.fetch_all_records("Humidity_Data")
    for row in humidity_data:
        print(row)
    
    print("\nPressure Data:")
    pressure_data = dbObj.fetch_all_records("Pressure_Data")
    for row in pressure_data:
        print(row)
    
    del dbObj

if __name__ == "__main__":
    build_db(TableSchema)
    client = mqtt.Client(client_id="", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    
    mqtt.Client()
    client.connect(mqttBroker)

    client.subscribe(MQTT_Topic)
    client.on_message = on_message
    
    client.loop_start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nFetching data from the database...")
        display_database_content()
        client.loop_stop()
        client.disconnect()
