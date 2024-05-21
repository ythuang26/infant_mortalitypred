import streamlit as st
import numpy as np
import pickle
import pandas as pd
import time
import os
import zipfile
from zipfile import ZipFile 
import plotly.express as px
import plotly.graph_objects as go 

@st.cache_data # To prevent data from being loaded for every step

#Data from https://www.who.int/data/gho/data/indicators/indicator-details/GHO/infant-mortality-rate-(probability-of-dying-between-birth-and-age-1-per-1000-live-births)
def load_data():
    # Unzip the file
    with zipfile.ZipFile("data.zip", "r") as zip_ref:
        zip_ref.extractall("data")

    # Check if the folder exists
    if os.path.exists("data"):
        # Access the folder and load the CSV file into a DataFrame
        csv_file_path = os.path.join("data", "data.csv")
        df = pd.read_csv(csv_file_path)
        # Extract Infant Mortality Rate
        df['Value'] = df['Value'].str.extract(r'(\d+\.\d+)')
        df['Value'] = df['Value'].astype(float)
        df = df[['Period','Dim1','Value','Location']]
        df.columns = ['Year','Gender','Infant Mortality Rate','Country']
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
        df['Year'] = df['Year'] + pd.DateOffset(months=11)
        return df
    else:
        print("The folder data does not exist.")
        return None

df = load_data()

#Data from https://www.cdc.gov/maternal-infant-health/infant-mortality/index.html
def load_data():
    # Unzip the file
    with zipfile.ZipFile("Infant Mortality Rates by Race and Ethnicity, 2021.zip", "r") as zip_ref:
        zip_ref.extractall("Infant Mortality Rates by Race and Ethnicity, 2021")

    # Check if the folder exists
    if os.path.exists("Infant Mortality Rates by Race and Ethnicity, 2021"):
        # Access the folder and load the CSV file into a DataFrame
        csv_file_path = os.path.join("Infant Mortality Rates by Race and Ethnicity, 2021", "Infant Mortality Rates by Race and Ethnicity, 2021.csv")
        df1 = pd.read_csv(csv_file_path)
        df1 = df1.melt(var_name='Race and Ethnicity', value_name='Infant Mortality Rate')
        return df1
    else:
        print("The folder data does not exist.")
        return None

df1 = load_data()

def show_visualize_page():

    st.title(":rainbow[Infant Mortality Rates Over the Years - USA]")

    gender = st.selectbox("Select Infant Mortality Rate",("Both Sexes", "Female", "Male", "Maternal Race and Ethnicity", "All American Rates", "Comparisons with UK, Canada and Australia"), index = None, placeholder = "Choose...")

    #Create separate dataframes for the genders & countries
    df_both = df.loc[df['Gender'] == 'Both sexes']
    df_female = df.loc[df['Gender'] == 'Female']
    df_male = df.loc[df['Gender'] == 'Male']

    df_both_us = df_both.loc[df_both['Country'] == 'United States of America']
    df_female_us = df_female.loc[df_female['Country'] == 'United States of America']
    df_male_us = df_male.loc[df_male['Country'] == 'United States of America']

    df_both_uk = df_both.loc[df_both['Country'] == 'United Kingdom of Great Britain and Northern Ireland']
    df_female_uk = df_female.loc[df_female['Country'] == 'United Kingdom of Great Britain and Northern Ireland']
    df_male_uk = df_male.loc[df_male['Country'] == 'United Kingdom of Great Britain and Northern Ireland']

    df_both_ca = df_both.loc[df_both['Country'] == 'Canada']
    df_female_ca = df_female.loc[df_female['Country'] == 'Canada']
    df_male_ca = df_male.loc[df_male['Country'] == 'Canada']

    df_both_au = df_both.loc[df_both['Country'] == 'Australia']
    df_female_au = df_female.loc[df_female['Country'] == 'Australia']
    df_male_au = df_male.loc[df_male['Country'] == 'Australia']

    if gender == "Both Sexes":
        
        fig = px.line(df_both_us, x='Year', y='Infant Mortality Rate', title='Both Sexes Infant Mortality Rates Over Time',color_discrete_sequence=["lightseagreen"])
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20  # Add some space between the axis title and the axis
        ),
            title_x=0.5,  # Center the title
        )
        st.plotly_chart(fig)

    if gender == "Female":
     
        fig1 = px.line(df_female_us, x='Year', y='Infant Mortality Rate', title='Female Infant Mortality Rates Over Time',color_discrete_sequence=["hotpink"])
        fig1.update_layout(
            xaxis_title='Year',
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20  
        ),
            title_x=0.5 
        )
        st.plotly_chart(fig1)

    if gender == "Male":
        
        fig2 = px.line(df_male_us, x='Year', y='Infant Mortality Rate', title='Male Infant Mortality Rates Over Time',color_discrete_sequence=["blueviolet"])
        fig2.update_layout(
            xaxis_title='Year',
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20  
        ),
            title_x=0.5 
        )
        st.plotly_chart(fig2)

    if gender == "Maternal Race and Ethnicity":
        fig = px.bar(df1, x='Race and Ethnicity', y='Infant Mortality Rate', title='Infant Mortality Rate by Race and Ethnicity in 2021', color = 'Race and Ethnicity')

        fig.update_layout(
            xaxis_title='',
            xaxis=dict(
                tickvals=[],
                ticktext=[]
            )
        )
        st.plotly_chart(fig)

    if gender == "All American Rates": 
        trace_both = go.Scatter(x=df_both_us['Year'], y=df_both_us['Infant Mortality Rate'], mode='lines', line=dict(color='lightseagreen'), name='Both Sexes')
        trace_female = go.Scatter(x=df_female_us['Year'], y=df_female_us['Infant Mortality Rate'], mode='lines', line=dict(color='hotpink'), name='Female')
        trace_male = go.Scatter(x=df_male_us['Year'], y=df_male_us['Infant Mortality Rate'], mode='lines', line=dict(color='blueviolet'), name='Male')

        # Create a figure and add the traces
        fig = go.Figure()
        fig.add_trace(trace_both)
        fig.add_trace(trace_female)
        fig.add_trace(trace_male)

        # Update layout to move legend outside the plot
        fig.update_layout(
            title='All Infant Mortality Rates Over Time',
            title_x = 0.5,
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20
        ))

        fig1 = px.bar(df1, x='Race and Ethnicity', y='Infant Mortality Rate', title='Infant Mortality Rate by Maternal Race and Ethnicity in 2021', color = 'Race and Ethnicity')

        fig1.update_layout(
             xaxis_title='',
            xaxis=dict(
                tickvals=[],
                ticktext=[]
            ),
            yaxis_title='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            title={
            'text': "Infant Mortality Rate by Maternal Race and Ethnicity in 2021",
            'y':0.9,
            'x':0.35,
            'xanchor': 'left',
            'yanchor': 'top'}
            )
        
        st.plotly_chart(fig)
        st.plotly_chart(fig1)

    if gender == "Comparisons with UK, Canada and Australia":
        st.subheader("Comparisons between USA, UK, Canada and Australia")
        #All Sexes
        trace_both_us = go.Scatter(x=df_both_us['Year'], y=df_both_us['Infant Mortality Rate'], mode='lines', line=dict(color='goldenrod'), name='USA')
        trace_both_uk = go.Scatter(x=df_both_uk['Year'], y=df_both_uk['Infant Mortality Rate'], mode='lines', line=dict(color='cornflowerblue'), name='UK')
        trace_both_ca = go.Scatter(x=df_both_ca['Year'], y=df_both_ca['Infant Mortality Rate'], mode='lines', line=dict(color='pink'), name='Canada')
        trace_both_au = go.Scatter(x=df_both_au['Year'], y=df_both_au['Infant Mortality Rate'], mode='lines', line=dict(color='magenta'), name='Australia')

        # Create a figure and add the traces
        fig = go.Figure()
        fig.add_trace(trace_both_us)
        fig.add_trace(trace_both_uk)
        fig.add_trace(trace_both_ca)
        fig.add_trace(trace_both_au)

        # Update layout to move legend outside the plot
        fig.update_layout(
            title='Both Sexes Infant Mortality Rates Over Time',
            title_x = 0.5,
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20
        ))

        #Females
        trace_female_us = go.Scatter(x=df_female_us['Year'], y=df_female_us['Infant Mortality Rate'], mode='lines', line=dict(color='goldenrod'), name='USA')
        trace_female_uk = go.Scatter(x=df_female_uk['Year'], y=df_female_uk['Infant Mortality Rate'], mode='lines', line=dict(color='cornflowerblue'), name='UK')
        trace_female_ca = go.Scatter(x=df_female_ca['Year'], y=df_female_ca['Infant Mortality Rate'], mode='lines', line=dict(color='pink'), name='Canada')
        trace_female_au = go.Scatter(x=df_female_au['Year'], y=df_female_au['Infant Mortality Rate'], mode='lines', line=dict(color='magenta'), name='Australia')

        # Create a figure and add the traces
        fig1 = go.Figure()
        fig1.add_trace(trace_female_us)
        fig1.add_trace(trace_female_uk)
        fig1.add_trace(trace_female_ca)
        fig1.add_trace(trace_female_au)

        # Update layout to move legend outside the plot
        fig1.update_layout(
            title='Female Infant Mortality Rates Over Time',
            title_x = 0.5,
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20
        ))

        #Males
        trace_male_us = go.Scatter(x=df_male_us['Year'], y=df_male_us['Infant Mortality Rate'], mode='lines', line=dict(color='goldenrod'), name='USA')
        trace_male_uk = go.Scatter(x=df_male_uk['Year'], y=df_male_uk['Infant Mortality Rate'], mode='lines', line=dict(color='cornflowerblue'), name='UK')
        trace_male_ca = go.Scatter(x=df_male_ca['Year'], y=df_male_ca['Infant Mortality Rate'], mode='lines', line=dict(color='pink'), name='Canada')
        trace_male_au = go.Scatter(x=df_male_au['Year'], y=df_male_au['Infant Mortality Rate'], mode='lines', line=dict(color='magenta'), name='Australia')

        # Create a figure and add the traces
        fig2 = go.Figure()
        fig2.add_trace(trace_male_us)
        fig2.add_trace(trace_male_uk)
        fig2.add_trace(trace_male_ca)
        fig2.add_trace(trace_male_au)

        # Update layout to move legend outside the plot
        fig2.update_layout(
            title='Male Infant Mortality Rates Over Time',
            title_x = 0.5,
            yaxis_title=dict(
            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
            standoff=20
        ))

        st.plotly_chart(fig)
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)


        
