

# Setup

To run the app, you'll need to
- create a credentials file (creds.json)
- get the 2 free datasets from the Snowflake Marketplace
- install all the dependency packages into your Python environment. I manage my virtual environments using the conda package manager for this

## Credentials

Copy the creds-sample.json to creds.json and add the values for your environment.

## Install dependencies to your (virtual) environment

I create a conda virtual environment with following commands on the terminal:

```
conda create --name esg -c https://repo.anaconda.com/pkgs/snowflake python=3.8 altair snowflake-snowpark-python

conda activate esg 

conda install streamlit


## Getting the free datasets used in the demo from Snowflake Marketplace

This demo uses 2 free datasets from the Snowflake Marketplace. Find them and click on "Get", make sure to add the role from the creds.json so the app will be able to read this data:

- ESG Scores (S&P500 Sample), provided by ESG Book
- Economy Data Atlas, provided by Knoema

I put the ESG Scores dataset into the database called "ESG" and the Economy Data Atlas is in the ECONOMY_DATA_ATLAS database. If you chose different name for your databases, make sure you adjust the code in app.py for the database names, lines 20 and 115.


# Run the app

Provided that the Setup worked properly, you can finally run the app. Don't forget to switch to the proper virtual environment.

```
conda activate esg # ignore this line if you're not using conda
streamlit run app.py
```