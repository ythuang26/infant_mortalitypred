# Infant Mortality Predictions

Infant mortality is the death of an infant within the first year of life and continues to be a very prominent issue within developed nations such as the United States. According to the Centers for Disease Control and Prevention (CDC), a total of 23,455 deaths occurred in children under the age of 1 year in 2015, which represents an increase of 240 deaths from the previous year. The infant mortality rate is an important marker of the overall health of a society. 

There are many determinants that impact infant mortality. The Linked Death files collected by the National Bureau of Economic Research from the National Vital Statistics System of the National Center for Health Statistics includes death to all infants born in the same calendar year for which the death certificate can be linked to a birth certificate in the denominator file. We will be working with the 2015 Linked Death files, the last calendar year for which such data is available.

The objective of this project was to create a model that would predict the top 3 causes of infant death based on 8 user feature inputs. The causes of death were categorized according to the International Classification of Diseases, Tenth Revision (ICD-10). 

View deployed model here:

### File Descriptions:

- Infant Mortality Predictions: Jupyter Notebooks.
  -   [Part 1](https://github.com/ythuang26/infant_mortalitypred/blob/main/Infant%20Mortality%20Predictions-Part%201.ipynb) comprises Exploratory Data Analysis, Basic Data Transformation, Constructing the DataFrame and Search for Best Features and Fine-Tuning Parameters.
  -   [Part 2](https://github.com/ythuang26/infant_mortalitypred/blob/main/Infant%20Mortality%20Predictions-Part%202.ipynb) includes Creating a Machine Learning Model, Saving the Model, and Making Predictions with the Model.

- [Infant Mortality Rates by Race and Ethnicity, 2021.zip](https://github.com/ythuang26/infant_mortalitypred/blob/main/Infant%20Mortality%20Rates%20by%20Race%20and%20Ethnicity%2C%202021.zip): 2021 US infant mortality rates separated by maternal race and ethnicity. From the CDC. Used specifically in visualize_page.py.

- [app.py](https://github.com/ythuang26/infant_mortalitypred/blob/main/app.py): Launches app. 

- [baby.jpg](https://github.com/ythuang26/infant_mortalitypred/blob/main/baby.jpg): Picture used in predict_page.py.
  
- [data-table.zip](): CSV file from CDC containing Infant Mortality data from across states. Used in visualize_page.py
- 
- [data.zip](https://github.com/ythuang26/infant_mortalitypred/blob/main/data.zip): Infant mortality rates from the World Health Organization. Contains information from various countries from over the years. Used Used specifically in visualize_page.py.

- [df_intx.csv](https://github.com/ythuang26/infant_mortalitypred/blob/main/df_intx.csv): Dataframe created at the end of Infant Mortality Predictions - Part 1. Final dataframe used to create model.

- [ensemble1.pkl.zip](https://github.com/ythuang26/infant_mortalitypred/blob/main/ensemble1.pkl.zip): Model. Used specifically in predict_page.py.

- [explore_page.py](https://github.com/ythuang26/infant_mortalitypred/blob/main/explore_page.py): Explore page of the app.

- [linkco2015usnum.csv](https://github.com/ythuang26/infant_mortalitypred/blob/main/linkco2015usnum.csv), [linkco2015usnum.zip](https://github.com/ythuang26/infant_mortalitypred/blob/main/linkco2015usnum.zip): Original dataset from the National Bureau of Economic Research. Used also in explore_page.py.

- [predict_page.py](https://github.com/ythuang26/infant_mortalitypred/blob/main/predict_page.py): Predict page of the app.

- [requirements.txt](https://github.com/ythuang26/infant_mortalitypred/blob/main/requirements.txt): Lists libraries used and version numbers.

- [stormtroppers.jpeg](https://github.com/ythuang26/infant_mortalitypred/blob/main/stormtroppers.jpeg): Picture used specifically in explore_page.py.

- [visualize_page.py](https://github.com/ythuang26/infant_mortalitypred/blob/main/visualize_page.py): Visualize page of the app.



