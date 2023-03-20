
![Screenshot 2023-03-20 at 10 14 27](https://user-images.githubusercontent.com/73932533/226295616-e0a44e15-f944-4439-94fb-ae3a388505e8.png)

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
```

## Getting the free datasets used in the demo from Snowflake Marketplace

This demo uses 2 free datasets from the Snowflake Marketplace. Find them and click on "Get", make sure to add the role from the creds.json so the app will be able to read this data:

- ESG Scores (S&P500 Sample), provided by ESG Book
- Economy Data Atlas, provided by Knoema

![ESG](https://user-images.githubusercontent.com/73932533/226289060-fd63ad2b-27e2-4f38-b0d3-cd743ee98ba2.png)
![Knoema](https://user-images.githubusercontent.com/73932533/226289068-d765eb66-d604-442c-aceb-4560ccc08339.png)


I put the ESG Scores dataset into the database called ```ESG``` and the Economy Data Atlas is in the ```ECONOMY_DATA_ATLAS``` database. If you chose different name for your databases, make sure you adjust the code in app.py for the database names, lines 20 and 115.

Here's a quick video on how to get a dataset (click on the image):

[![Get the ESG dataset from the Snowflake Marketplace](https://user-images.githubusercontent.com/73932533/226289060-fd63ad2b-27e2-4f38-b0d3-cd743ee98ba2.png)](https://youtu.be/0HWnh9HsmgM)



# Run the app

Provided that the Setup worked properly, you can finally run the app. Don't forget to switch to the proper virtual environment.

```
conda activate esg # ignore this line if you're not using conda
streamlit run app.py
```
