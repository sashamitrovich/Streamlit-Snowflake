

# Setup

To run the app, you'll need a credentials file (creds.json) and a table on Snowflake that the app is using to write data to.

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