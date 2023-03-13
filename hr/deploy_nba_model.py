import json
from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf
import zipfile
import sys
import os
import tensorflow as tf

with open('creds.json') as f:
    connection_parameters = json.load(f)  
session = Session.builder.configs(connection_parameters).create()

session.add_packages("tensorflow")

# Create staging area 
session.sql("create or replace stage udf").collect()
# Upload file to the staging area
session.file.put("file://my_dnn_model.zip", "@udf", auto_compress=False)

@udf(name="predict_nba_salary", is_permanent=True, replace = True, stage_location="@udf", imports=[("my_dnn_model.zip")])
def udf_predict_nba_salary(years:int) -> float:    

    IMPORT_DIRECTORY_NAME = "snowflake_import_directory"
    import_dir = sys._xoptions[IMPORT_DIRECTORY_NAME]
    
    # Get the path to the ZIP file and set the location to extract to.
    zip_file_path = import_dir + "my_dnn_model.zip"
    
    extracted = '/tmp'

    # Extract the contents of the ZIP. This is done under the file lock
    # to ensure that only one worker process unzips the contents.
    # with FileLock():
    if not os.path.isdir(extracted + '/my_dnn_model/saved_model.pb'):
        with zipfile.ZipFile(zip_file_path, 'r') as myzip:
            myzip.extractall(extracted)

    my_model = tf.keras.models.load_model(extracted+'/my_dnn_model')

    x = tf.linspace(years, years, 1)
    y = my_model.predict_on_batch(x)

    return 1000000*y.tolist()[0][0]


print("test: "+session.sql("select predict_nba_salary(10)").collect())