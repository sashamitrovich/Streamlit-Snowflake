import streamlit as st
import json

from snowflake.snowpark import Session, version, Window, Row

# connect to Snowflake
with open('creds.json') as f: # check the creds-fake.json file for format
    connection_parameters = json.load(f)  
session = Session.builder.configs(connection_parameters).create()

# get Snowflake table data
employeeDf = session.table("employee")

# main entry form
with st.form("my_form"):
    st.write("### Enter employee details")

    name_val = st.text_input("Name")
    age_val = st.slider("Age",18,99,30)

    experience_val = st.slider("Years of Experience",1,20,3)
    
    job_val  = st.selectbox(
     'Job title',
     ('Engineer', 'Marketing Manager', 'Sales Director', 'Executive'))

    salary_val = st.number_input("Salary", step= 1000, value=50000)

    insider_val = st.checkbox("Insider?")
    # Every form must have a submit button.
    submitted = st.form_submit_button("Save Employee")
    if submitted:
        # creates a new df and appends to the DB
        st.write("name:", name_val, "| age:", age_val, "| experience: ", experience_val, "| job:", job_val, "| salary: ", salary_val, "| insider:", insider_val)
        newEmployeeDf=session.createDataFrame([Row(employee_id=str(uuid.uuid4()) ,
            name=name_val, 
            age=age_val, 
            experience=experience_val,
            job=job_val, 
            salary = salary_val,
            insider=insider_val)])
        newEmployeeDf.write.mode("append").saveAsTable("employee")

if st.button('Delete database'):
    employeeDf.delete()

# refreshes automatically every time the data frame changes
st.write("Employees database:")
st.table(employeeDf.toPandas())

with st.expander("But wait, there's more, dont' leave just yet!", expanded=False):
    with st.form('nba_salary_form'):
        # st.write("### What would they earn in the NBA? *")
    
        st.markdown("### What would they earn in the NBA? * \n<sup>* Based on cutting edge data science</sup>", unsafe_allow_html=True)
        name_val  = st.selectbox("Select name",employeeDf.select("name").toPandas())
        hit = st.form_submit_button("Go")
        if hit:
            nba_salary= employeeDf.filter(col("name") == name_val).select(call_udf("predict_nba_salary", col("experience")),"salary").toPandas()
            st.metric(label="Projected NBA Salary", 
                value=str(int(nba_salary.iat[0,0])) + " USD", 
                delta= str(int( (nba_salary.iat[0,0]-nba_salary.iat[0,1])/nba_salary.iat[0,1] *100)) + " %"
            )
