

# Setup

To run the app, you'll need to
- create a credentials file (creds.json)
- create a table on Snowflake that the app is using to write data to
- install all the dependency packages. I use the conda package manager for this but I trust you're doing here so I will not provide detailed instructions on how to do this
- deploy the ML model for predicting a phantasy salary, based on the year of experience of an employee

## Credentials

Copy the creds-sample.json to creds.json and add the values for your environment.

## Employee table on Snowflake

In the database and schema from your credentials, using the same role as in the credentials, create table *employee* with the following SQL:

```
create or replace TABLE employee (
    EMPLOYEE_ID string primary key,
	NAME VARCHAR(16777216),
	AGE NUMBER(38,0),
    EXPERIENCE integer,
	JOB VARCHAR(16777216),
    SALARY integer,
	INSIDER BOOLEAN
);
```
## Deploy the ML Model

Make sure you have the creds.json file (you should if you didn't skip the Setup steps). Then run this:

```
python deploy_nba_model.py
```

This will deploy a permanent UDF function in the same DB/Schema as specified in creds.json, called "predict_nba_salary". You run this Python code only once and, once deployed, you can call this function as any other Snowflake function, simple SQL example:

```
select predict_nba_salary(10)
```

will return a value in $$$.


# Run the app

Provided that the Setup worked properly, you can finally run the app:

```
streamlit run hr_app.py
```
![App Screenshot](https://user-images.githubusercontent.com/73932533/225003126-be559854-6381-4c52-9e0c-dcd7e36bbb36.png)

