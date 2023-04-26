

# Setup

To run the app, you'll need to
- install neccessary Python packages (I use conda)
- create a credentials file (creds.json)
- create a table on Snowflake that the app is using to write data to
- install all the dependency packages. I use the conda package manager for this but I trust you're doing here so I will not provide detailed instructions on how to do this
- deploy the ML model for predicting a phantasy salary, based on the year of experience of an employee

## Packages

I use conda to create a virtual environment, the packages can also be installed using pip

conda create --name hr -c <https://repo.anaconda.com/pkgs/snowflake> python=3.8 pandas snowflake-snowpark-python
conda activate hr
conda install -c conda-forge streamlit

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
![Screenshot 2023-03-20 at 10 24 11](https://user-images.githubusercontent.com/73932533/226298015-26170767-7575-4be2-bf5c-a38222ad87e0.png)

