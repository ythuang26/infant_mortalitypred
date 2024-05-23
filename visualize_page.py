import streamlit as st
import numpy as np
import pickle
import pandas as pd
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
        df.columns = ['Year','Sex','Infant Mortality Rate','Country']
        df['Sex'] = df['Sex'].replace('Both sexes', 'Both Sexes')
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

#Data from https://www.cdc.gov/nchs/pressroom/sosmap/infant_mortality_rates/infant_mortality.htm
def load_data():
    # Unzip the file
    with zipfile.ZipFile("data-table.zip", "r") as zip_ref:
        zip_ref.extractall("data-table")

    # Check if the folder exists
    if os.path.exists("data-table"):
        # Access the folder and load the CSV file into a DataFrame
        csv_file_path = os.path.join("data-table", "data-table.csv")
        df2 = pd.read_csv(csv_file_path)
        #df2['YEAR'] = df2['YEAR'].replace('Provisional 2022', '2022')
        return df2
    else:
        print("The folder data does not exist.")
        return None

df2 = load_data()

def show_visualize_page():

    st.title(":rainbow[Infant Mortality Rates: National and International Perspectives]")

    mortality = st.selectbox("Select American or International Infant Mortality Rates",
                             ("United States of America", "International",
                              ),
                             index = None, placeholder = "National or International ...")
    
    if mortality == "United States of America":

        #Filter for American dataframe
        filtered_df = df.loc[df['Country'] == "United States of America"]
        
        # New multiselect box pops up when mortality == "United States of America"
        us_rates = st.multiselect("Select Infant Mortality Rate by Sex", ["Both Sexes", "Female", "Male"], placeholder = "Choose option...")

        #New selectbox appears mortality == "United States of America"
        bonus = st.selectbox("Bonus Information", 
                            ("Maternal Race and Ethnicity", "Infant Mortality Rates Across States", "Comparisons with English speaking Countries"),
                            index=None)
        
        if us_rates:

            # Define colors for each sex
            colors = {
                "Both Sexes": "lightseagreen",
                "Female": "hotpink",
                "Male": "blueviolet",
            }

            fig = go.Figure()

            for sex in us_rates:
                sex_df = filtered_df.loc[filtered_df["Sex"] == sex]
                fig.add_trace(go.Scatter(
                    x=sex_df['Year'],
                    y=sex_df['Infant Mortality Rate'],
                    mode='lines',
                    name=sex,
                    line=dict(color=colors[sex]),
                    visible=True))

            fig.update_layout(
                title={
                    'text': f'Infant Mortality Rates Over Time by Gender: {", ".join(us_rates)}',
                    'y': 0.95,  # Adjust the title position
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',},
                xaxis_title='Year',
                yaxis_title='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
                legend=dict(
                    orientation="v",
                    x=1,
                    y=1,  # Adjusted to move legend further below the plot
                    xanchor='right',
                    yanchor='top'),
                margin=dict(t=100),  # Adjust top margin to fit the title
                hovermode='x unified')
            
            st.plotly_chart(fig)
        
        else: 
            None

        #Bar plot for rates separated by maternal race and ethnicity
        if bonus == "Maternal Race and Ethnicity":
            fig = px.bar(df1, x='Race and Ethnicity', y='Infant Mortality Rate', title='Infant Mortality Rate by Maternal Race and Ethnicity in 2021', color = 'Race and Ethnicity')

            fig.update_layout(
                xaxis_title='',
                xaxis=dict(
                    tickvals=[],
                    ticktext=[]),
                yaxis_title=dict(
                    text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
                    standoff=20))
            
            st.plotly_chart(fig)

        #Chloropleth Maps for Infant Mortality Rates Across States
        if bonus == "Infant Mortality Rates Across States":
            
            #Map State abbreviations to full names
            state_mapping= {
                'AL': 'Alabama',
                'AK': 'Alaska',
                'AZ': 'Arizona',
                'AR': 'Arkansas',
                'CA': 'California',
                'CO': 'Colorado',
                'CT': 'Connecticut',
                'DE': 'Delaware',
                'DC': 'District of Columbia',
                'FL': 'Florida',
                'GA': 'Georgia',
                'HI': 'Hawaii',
                'ID': 'Idaho',
                'IL': 'Illinois',
                'IN': 'Indiana',
                'IA': 'Iowa',
                'KS': 'Kansas',
                'KY': 'Kentucky',
                'LA': 'Louisiana',
                'ME': 'Maine',
                'MD': 'Maryland',
                'MA': 'Massachusetts',
                'MI': 'Michigan',
                'MN': 'Minnesota',
                'MS': 'Mississippi',
                'MO': 'Missouri',
                'MT': 'Montana',
                'NE': 'Nebraska',
                'NV': 'Nevada',
                'NH': 'New Hampshire',
                'NJ': 'New Jersey',
                'NM': 'New Mexico',
                'NY': 'New York',
                'NC': 'North Carolina',
                'ND': 'North Dakota',
                'OH': 'Ohio',
                'OK': 'Oklahoma',
                'OR': 'Oregon',
                'PA': 'Pennsylvania',
                'RI': 'Rhode Island',
                'SC': 'South Carolina',
                'SD': 'South Dakota',
                'TN': 'Tennessee',
                'TX': 'Texas',
                'UT': 'Utah',
                'VT': 'Vermont',
                'VA': 'Virginia',
                'WA': 'Washington',
                'WV': 'West Virginia',
                'WI': 'Wisconsin',
                'WY': 'Wyoming'
            }
            
            #selectbox allows to choose year of interest
            select_year = st.selectbox("Select Year", df2["YEAR"].unique())

            #select filtered dataframe for selected year
            year_df = df2.loc[df2["YEAR"] == select_year]
            
            #new column with full state name
            year_df["STATE_NAME"] = year_df["STATE"].map(state_mapping)

            if select_year: #year has been selected

                #create horizontal radio buttons to select for rate or absolute deaths
                rate_or_number = st.radio("Select Infant Mortality Rate or Total Number of Infant Deaths",
                                              ("Infant Mortality Rate", "Total Number of Infant Deaths"),
                                              horizontal = True)
                
                #choropleth map for infant mortality rate
                if rate_or_number == "Infant Mortality Rate":

                    fig_map = go.Figure(data=go.Choropleth(
                        locations = year_df["STATE"], #spatial coordinates
                        z = year_df["RATE"], #data to be color-coordinated
                        locationmode = "USA-states",
                        text = year_df["STATE_NAME"], #hover text with full state names
                        colorscale = "agsunset",
                        colorbar_title = "Percentage"))

                    fig_map.update_layout(
                        title_text = f"Infant Mortality by State {select_year}",
                        geo_scope = "usa")

                    st.plotly_chart(fig_map)
                
                #choropleth map for infant deaths
                if rate_or_number == "Total Number of Infant Deaths":
                    fig_map = go.Figure(data=go.Choropleth(
                    locations = year_df["STATE"], #spatial coordinates
                    z = year_df["DEATHS"], #data to be color-coordinated
                    locationmode = "USA-states",
                    text = year_df["STATE_NAME"], #hover text with full state names
                    colorscale = "portland",
                    colorbar_title = "DEATHS"))

                    fig_map.update_layout(
                        title_text = f"Total Number of Infant Deaths by State in {select_year}",
                        geo_scope = "usa")

                    st.plotly_chart(fig_map)


        if bonus == "Comparisons with English speaking Countries": #Compare US rates with other English-speaking countries

            #map countries to specific colors
            country_colors = {
                "United States of America": "goldenrod",
                "United Kingdom of Great Britain and Northern Ireland": "cornflowerblue",
                "Canada": "pink",
                "Australia": "magenta"
}
            comparison_df = df[df['Country'].isin(["United States of America", "United Kingdom of Great Britain and Northern Ireland", "Canada", "Australia"])]

            # Plot for both sexes
            fig_both_sexes = px.line(comparison_df.loc[comparison_df['Sex'] == 'Both Sexes'], x='Year', y='Infant Mortality Rate', color='Country', 
                                     title='Infant Mortality Rate Comparison for Both Sexes',
                                     color_discrete_map=country_colors)
            
            fig_both_sexes.update_layout(hovermode='x unified',
                                        title={
                                            'text': 'Infant Mortality Rate Comparison for Both Sexes',
                                            'xanchor': 'center',
                                            'yanchor': 'top',
                                            'x': 0.5,
                                            'y': 0.95 },
                                        legend=dict(
                                            orientation="h",  # Make the legend horizontal
                                            yanchor="bottom",  # Anchor the legend at the bottom
                                            y=-0.3,  # Place the legend below the plot
                                            xanchor="center",  # Center the legend horizontally
                                            x=0.5),  # Place the legend in the center of the plot
                                        yaxis_title=dict(
                                            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
                                            standoff=20),
                                        margin=dict(l=20, r=20, t=50, b=100))  # Adjust margins to give space for the legend,
                                        
            
            st.plotly_chart(fig_both_sexes)

            # Plot for female
            fig_female = px.line(comparison_df.loc[comparison_df['Sex'] == 'Female'], x='Year', y='Infant Mortality Rate', color='Country', 
                                 title='Infant Mortality Rate Comparison for Females',
                                 color_discrete_map=country_colors)
            
            fig_female.update_layout(hovermode='x unified',
                                     title={
                                            'text': 'Infant Mortality Rate Comparison for Females',
                                            'xanchor': 'center',
                                            'yanchor': 'top',
                                            'x': 0.5,
                                            'y': 0.95 },
                                        legend=dict(
                                            orientation="h",  # Make the legend horizontal
                                            yanchor="bottom",  # Anchor the legend at the bottom
                                            y=-0.3,  # Place the legend below the plot
                                            xanchor="center",  # Center the legend horizontally
                                            x=0.5),  # Place the legend in the center of the plot
                                        yaxis_title=dict(
                                            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
                                            standoff=20),
                                            margin=dict(l=20, r=20, t=50, b=100))  # Adjust margins to give space for the legend
                                     
            st.plotly_chart(fig_female)

            # Plot for male
            fig_male = px.line(comparison_df.loc[comparison_df['Sex'] == 'Male'], x='Year', y='Infant Mortality Rate', color='Country', 
                               title='Infant Mortality Rate Comparison for Males',
                               color_discrete_map=country_colors)
            
            fig_male.update_layout(hovermode='x unified',
                                   title={
                                            'text': 'Infant Mortality Rate Comparison for Males',
                                            'xanchor': 'center',
                                            'yanchor': 'top',
                                            'x': 0.5,
                                            'y': 0.95 },
                                    legend=dict(
                                        orientation="h",  # Make the legend horizontal
                                        yanchor="bottom",  # Anchor the legend at the bottom
                                        y=-0.3,  # Place the legend below the plot
                                        xanchor="center",  # Center the legend horizontally
                                        x=0.5),  # Place the legend in the center of the plot
                                    yaxis_title=dict(
                                            text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
                                            standoff=20),
                                    margin=dict(l=20, r=20, t=50, b=100))  # Adjust margins to give space for the legend
            
            st.plotly_chart(fig_male)

    #Display infant mortality rates for international countries
    if mortality ==  "International":

        countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda', 
                    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 
                    'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia (Plurinational State of)', 
                    'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei Darussalam', 
                    'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 
                    'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Cook Islands', 
                    'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Democratic Republic of the Congo', 
                    "Democratic People's Republic of Korea", 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 
                    'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 
                    'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 
                    'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 
                    'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 
                    'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 
                    'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 
                    'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 
                    'Micronesia (Federated States of)', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 
                    'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands (Kingdom of the)', 'New Zealand', 
                    'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North Macedonia', 'Norway', 'occupied Palestinian territory, including east Jerusalem', 
                    'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 
                    'Portugal', 'Qatar', 'Republic of Korea', 'Republic of Moldova', 'Romania', 'Russian Federation', 'Rwanda', 
                    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 
                    'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 
                    'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 
                    'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Thailand', 'Timor-Leste', 
                    'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 
                    'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 
                    'United Republic of Tanzania', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 
                    'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe', 'Kosovo (in accordance with UN Security Council resolution 1244 (1999))']
        
        select_countries = st.multiselect("Historical Trends in Infant Mortality Rates Globally",countries, placeholder = "Select Countries...")
   
        if select_countries:

            #Filter for the selected countries
            filtered_df = df[df['Country'].isin(select_countries)]

            #Further filter for the selected gender
            selected_sex = st.selectbox("Select Sex",("Both Sexes", "Female", "Male",), index=None, placeholder="Choose Sex...")

            if selected_sex == "Both Sexes":
                filtered_df = filtered_df.loc[filtered_df['Sex'] == "Both Sexes"]
            if selected_sex == "Female":
                filtered_df = filtered_df.loc[filtered_df['Sex'] == "Female"]
            if selected_sex == "Male":
                filtered_df = filtered_df.loc[filtered_df['Sex'] == "Male"]

            fig = go.Figure()

            #Add a line plot for each country
            for country in select_countries:
                country_df = filtered_df.loc[filtered_df['Country'] == country]
                fig.add_trace(go.Scatter(
                x=country_df['Year'],
                y=country_df['Infant Mortality Rate'],
                mode='lines',
                name=country))
            
            fig.update_layout(
                title=f'{selected_sex} Infant Mortality Rates Over Time',
                title_x=0.5,
                xaxis_title='Year',
                yaxis_title=dict(
                    text='Infant Mortality Rate<br><sup>Deaths Per 1000 Live Births</sup>',
                    standoff=20),
                hovermode='x unified',
                legend=dict(
                    orientation="h",  # Make the legend horizontal
                    yanchor="bottom",  # Anchor the legend at the bottom
                    y=-0.3,  # Place the legend below the plot
                    xanchor="center",  # Center the legend horizontally
                    x=0.5),  # Place the legend in the center of the plot
                margin=dict(l=20, r=20, t=50, b=100),  # Adjust margins to give space for the legend
                    hoverlabel=dict(
                        bgcolor='rgba(0,0,0,0)'))

            st.plotly_chart(fig)

        
