import streamlit as st
import json

from snowflake.snowpark import Session, version, Window, Row

# connect to Snowflake
with open('creds.json') as f: # check the creds-fake.json file for format
    connection_parameters = json.load(f)  
session = Session.builder.configs(connection_parameters).create()

# get Snowflake table data
employeeDf = session.table("employee")

# used to trigger refresh of the rendered table
refresh_employee_db_display = True

# main entry form
with st.form("my_form"):
    st.write("Enter employee details")

    name_val = st.text_input("Name")
    age_val = st.slider("Age",18,99,30)
    
    job_val  = st.selectbox(
     'Job title',
     ('Engineer', 'Marketing Manager', 'Sales Director', 'Executive'))

    insider_val = st.checkbox("Insider?")
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        # creates a new df and unions with existing data in Snowflake, writes to table
        st.write("name:", name_val, "| age:", age_val, "| job:", job_val, "| insider:", insider_val)
        newEmployeeDf=session.createDataFrame([Row(name=name_val, age=age_val, job=job_val, insider=insider_val)])
        employeeDf = employeeDf.union(newEmployeeDf)
        employeeDf.write.mode("overwrite").saveAsTable("employee")
        refresh_employee_db_display = True

if st.button('Delete database'):
    employeeTable = session.table("employee")
    employeeTable.delete()
    refresh_employee_db_display = True

# refreshes every time new record gets added or table is deleted
while refresh_employee_db_display == True:
    employeeDf = session.table("employee")
    st.write("Employees database:")
    st.write(employeeDf.toPandas())
    refresh_employee_db_display = False