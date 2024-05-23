import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import zipfile
from zipfile import ZipFile 
import os

@st.cache_data # To prevent data from being loaded for every step
def load_data():
    # Unzip the file
    with zipfile.ZipFile("linkco2015usnum.zip", "r") as zip_ref:
        zip_ref.extractall("linkco2015usnum")

    # Check if the folder exists
    if os.path.exists("linkco2015usnum"):
        # Access the folder and load the CSV file into a DataFrame
        csv_file_path = os.path.join("linkco2015usnum", "linkco2015usnum.csv")
        df = pd.read_csv(csv_file_path, low_memory=False)
        #Create 17 Disease Classes
        df['ucodr130copy'] = df['ucodr130']
        df.loc[(df['ucodr130copy'] >= 1) & (df['ucodr130copy'] <= 22), 'ucodr130copy'] = 1
        df.loc[(df['ucodr130copy'] >= 23) & (df['ucodr130copy'] <= 28), 'ucodr130copy'] = 23
        df.loc[(df['ucodr130copy'] >= 29) & (df['ucodr130copy'] <= 32), 'ucodr130copy'] = 29
        df.loc[(df['ucodr130copy'] >= 33) & (df['ucodr130copy'] <= 38), 'ucodr130copy'] = 33
        df.loc[(df['ucodr130copy'] >= 39) & (df['ucodr130copy'] <= 44), 'ucodr130copy'] = 39
        df.loc[(df['ucodr130copy'] == 45), 'ucodr130copy'] = 45
        df.loc[(df['ucodr130copy'] >= 46) & (df['ucodr130copy'] <= 52), 'ucodr130copy'] = 46
        df.loc[(df['ucodr130copy'] >= 53) & (df['ucodr130copy'] <= 62), 'ucodr130copy'] = 53
        df.loc[(df['ucodr130copy'] >= 63) & (df['ucodr130copy'] <= 66), 'ucodr130copy'] = 63
        df.loc[(df['ucodr130copy'] >= 67) & (df['ucodr130copy'] <= 69), 'ucodr130copy'] = 67
        df.loc[(df['ucodr130copy'] >= 70) & (df['ucodr130copy'] <= 108), 'ucodr130copy'] = 70
        df.loc[(df['ucodr130copy'] >= 109) & (df['ucodr130copy'] <= 117), 'ucodr130copy'] = 109
        df.loc[(df['ucodr130copy'] >= 118) & (df['ucodr130copy'] <= 133), 'ucodr130copy'] = 118
        df.loc[(df['ucodr130copy'] >= 134) & (df['ucodr130copy'] <= 136), 'ucodr130copy'] = 134
        df.loc[(df['ucodr130copy'] == 137), 'ucodr130copy'] = 137
        df.loc[(df['ucodr130copy'] >= 138) & (df['ucodr130copy'] <= 157), 'ucodr130copy'] = 138
        df.loc[(df['ucodr130copy'] == 158), 'ucodr130copy'] = 158
        return df
    else:
        print("The folder linkco2015usnum does not exist.")
        return None

df = load_data()

def show_explore_page():

    st.title(":rainbow[Explore Disease Categories]")

    st.write("130 Selected Causes of Infant Death Adapted from the International Classification of Diseases, Tenth Revision")

    #First Selectbox for overview of major disease categories
    big_disease = st.selectbox("Explore the 17 Disease Categories and their Subcategories",
                            ("17 Major Disease Categories",None),
                            index= None, placeholder = "Discover Disease Categories and the Most Common Diseases among them...")

    big_group_mapping = {
        1: 'Certain infectious and parasitic diseases',
        23: 'Neoplasms',
        29: 'Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism',
        33: 'Endocrine, nutritional and metabolic diseases',
        39: 'Diseases of the nervous system',
        45: 'Diseases of the ear and mastoid process',
        46: 'Diseases of the circulatory system',
        53: 'Diseases of the respiratory system',
        63: 'Diseases of the digestive system',
        67: 'Diseases of the genitourinary system',
        70: 'Certain conditions originating in the perinatal period',
        109: 'Hemorrhagic and hematological disorders of newborn',
        118: 'Congenital malformations, deformations and chromosomal abnormalities',
        134: 'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified',
        137: 'All other diseases (Residual)',
        138: 'External causes of mortality',
        158: 'Other external causes'
    }

    #Pie Chart of Major Disease Categories
    if big_disease == "17 Major Disease Categories":

        #Get Disease Counts
        big_group = df.ucodr130copy.value_counts().reset_index()

        #Map disease integer to corresponding strings
        big_group.ucodr130copy = big_group.ucodr130copy.map(big_group_mapping)
        big_group.columns = ["17 Major Disease Categories", "Count"]
        
        fig = go.Figure(data=[go.Pie(
            labels=big_group["17 Major Disease Categories"],
            values=big_group['Count'],
            hoverinfo='label+percent',  # Customize hover information
            textinfo='percent',  # Show percentage and label on the slices
            textposition='inside',  # Position the text inside the slices
            textfont_size=18)])
     
        fig.update_layout(
            title={'text': "17 Major Disease Categories"},
            width=800,  # Set the width of the figure
            height=800,  # Set the height of the figusres
            legend=dict(
                orientation="h",  # Horizontal legend
                x=0.5,  # Center the legend horizontally
                y=-0.1,  # Position the legend just below the chart
                xanchor='center',  # Anchor the x position to the center
                yanchor='top'),  # Anchor the y position to the top       
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    #Explore subcategories of Major Disease Groups
    disease = st.selectbox("Explore the Disease Subcategories",
                        ("Certain infectious and parasitic diseases",
                        "Neoplasms",
                        "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism",
                        'Endocrine, nutritional and metabolic diseases',
                        'Diseases of the nervous system',
                        'Diseases of the ear and mastoid process',
                        'Diseases of the circulatory system',
                        'Diseases of the respiratory system',
                        'Diseases of the digestive system',
                        'Diseases of the genitourinary system',
                        'Certain conditions originating in the perinatal period',
                        'Hemorrhagic and hematological disorders of newborn',
                        'Congenital malformations, deformations and chromosomal abnormalities',
                        'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified',
                        'All other diseases (Residual)',
                        'External causes of mortality',
                        'Other external causes'),
                        index= None, placeholder = "Choose Disease Subcategory...")

    group1_mapping = {
        2: 'Certain intestinal infectious diseases',
        3: 'Diarrhea and gastroenteritis of infectious origin',
        7: 'Whooping cough',
        8: 'Meningococcal infection',
        9: 'Septicemia',
        10: 'Congenital syphilis',
        16: 'Human immunodeficiency virus (HIV) disease',
        18: 'Other and unspecified viral diseases',
        19: 'Candidiasis',
        22: 'All other and unspecified infectious and parasitic diseases'
    }

    group2_mapping = {
        26: 'Leukemia',
        27: 'Other and unspecified malignant neoplasms',
        28: 'In situ neoplasms, benign neoplasms and neoplasms of uncertain or unknown behavior'
    }

    group3_mapping = {
        30: 'Anemias',
        31: 'Hemorrhagic conditions and other diseases of blood and blood-forming organs',
        32: 'Certain disorders involving the immune mechanism'
    }

    group4_mapping = {
        34: 'Short stature, not elsewhere classified',
        35: 'Nutritional deficiencies',
        36: 'Cystic fibrosis',
        37: 'Volume depletion, disorders of fluid, electrolyte and acid-base balance',
        38: 'All other endocrine, nutritional and metabolic diseases'
    }

    group5_mapping = {
        40: 'Meningitis',
        41: 'Infantile spinal muscular atrophy, type I (Werdnig-Hoffman)',
        42: 'Infantile cerebral palsy',
        43: 'Anoxic brain damage, not elsewhere classified',
        44: 'Other diseases of nervous system'
    }

    group6_mapping = {
        47: 'Pulmonary heart disease and diseases of pulmonary circulation',
        48: 'Pericarditis, endocarditis and myocarditis',
        49: 'Cardiomyopathy',
        50: 'Cardiac arrest',
        51: 'Cerebrovascular diseases',
        52: 'All other diseases of circulatory system'
    }

    group7_mapping = {
        54: 'Acute upper respiratory infections',
        55: 'Influenza and pneumonia',
        56: 'Influenza',
        57: 'Pneumonia',
        58: 'Acute bronchitis and acute bronchiolitis',
        59: 'Bronchitis, chronic and unspecified',
        60: 'Asthma',
        61: 'Pneumonitis due to solids and liquids',
        62: 'Other and unspecified diseases of respiratory system'
    }

    group8_mapping = {
        64: 'Gastritis, duodenitis, and noninfective enteritis and colitis',
        65: 'Hernia of abdominal cavity and intestinal obstruction without hernia',
        66: 'All other and unspecified diseases of digestive system',
    }

    group9_mapping = {
        68: 'Renal failure and other disorders of kidney ',
        69: 'Other and unspecified diseases of genitourinary system',
    }

    group10_mapping = {
        72: 'Newborn affected by maternal hypertensive disorders',
        73: 'Newborn affected by other maternal conditions which may be unrelated to present pregnancy',
        75: 'Newborn affected by incompetent cervix',
        76: 'Newborn affected by premature rupture of membranes',
        77: 'Newborn affected by multiple pregnancy',
        78: 'Newborn affected by other maternal complications of pregnancy',
        80: 'Newborn affected by complications involving placenta',
        81: 'Newborn affected by complications involving cord',
        82: 'Newborn affected by chorioamnionitis',
        83: 'Newborn affected by other and unspecified abnormalities of membranes',
        84: 'Newborn affected by other complications of labor and delivery',
        85: 'Newborn affected by noxious influences transmitted via placenta or breast milk',
        87: 'Slow fetal growth and fetal malnutrition',
        89: 'Extremely low birthweight or extreme immaturity',
        90: 'Other low birthweight or preterm',
        91: 'Disorders related to long gestation and high birthweight',
        92: 'Birth trauma',
        94: 'Intrauterine hypoxia',
        95: 'Birth asphyxia',
        96: 'Respiratory distress of newborn',
        98: 'Congenital pneumonia',
        99: 'Neonatal aspiration syndromes',
        100: 'Interstitial emphysema and related conditions originating in the perinatal period',
        101: 'Pulmonary hemorrhage originating in the perinatal period',
        102: 'Chronic respiratory disease originating in the perinatal period',
        103: 'Atelectasis',
        104: 'All other respiratory conditions originating in the perinatal period',
        106: 'Bacterial sepsis of newborn',
        107: 'Omphalitis of newborn with or without mild hemorrhage',
        108: 'All other infections specific to the perinatal period'
    }

    group11_mapping = {
        110: 'Neonatal hemorrhage',
        111: 'Hemorrhagic disease of newborn',
        112: 'Hemolytic disease of newborn due to isoimmunization and other perinatal jaundice',
        113: 'Hematological disorders',
        114: 'Syndrome of infant of a diabetic mother and neonatal diabetes mellitus',
        115: 'Necrotizing enterocolitis of newborn',
        116: 'Hydrops fetalis not due to hemolytic disease',
        117: 'Other perinatal conditions'
    }

    group12_mapping = {
        119: 'Anencephaly and similar malformations',
        120: 'Congenital hydrocephalus',
        121: 'Spina bifida',
        122: 'Other congenital malformations of nervous system',
        123: 'Congenital malformations of heart',
        124: 'Other congenital malformations of circulatory system',
        125: 'Congenital malformations of respiratory system',
        126: 'Congenital malformations of digestive system',
        127: 'Congenital malformations of genitourinary system',
        128: 'Congenital malformations and deformations of musculoskeletal system, limbs and integument',
        129: "Down's syndrome",
        130: "Edward's syndrome",
        131: "Patau's syndrome",
        132: "Other congenital malformations and deformations",
        133: "Other chromosomal abnormalities, not elsewhere classified"
    }

    group13_mapping = {
        135: 'Sudden infant death syndrome',
        136: 'Other symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified'       
    }

    group14_mapping = {
        141: "Motor vehicle accidents",
        142: "Other and unspecified transport accidents",
        143: "Falls",
        144: "Accidental discharge of firearms",
        145: "Accidental drowning and submersion",
        146: 'Accidental suffocation and strangulation in bed',
        147: "Other accidental suffocation and strangulation",
        148: 'Accidental inhalation and ingestion of food or other objects causing obstruction of respiratory tract',
        149: "Accidents caused by exposure to smoke, fire and flames",
        150: 'Accidental poisoning and exposure to noxious substances',
        151: "Other and unspecified accidents",
        153: "Assault (homicide) by hanging, strangulation and suffocation",
        154: "Assault (homicide) by discharge of firearms",
        155: "Neglect, abandonment and other maltreatment syndromes",
        156: "Assault (homicide) by other and unspecified means",
        157: "Complications of medical and surgical care"
    }

    if disease == "Certain infectious and parasitic diseases":
        filtered_df1 = df.loc[(df.ucodr130 >= 1) & (df.ucodr130 <= 22)]
        filtered_df1.ucodr130 = filtered_df1.ucodr130.map(group1_mapping) #Map disease integer to corresponding strings
        filtered_df1 = filtered_df1.ucodr130.value_counts().reset_index()  #Get Disease Counts
        filtered_df1.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df1["Diseases"],
            values=filtered_df1['Count'],
            hoverinfo='label+percent',  # Customize hover information
            textinfo='percent',  # Show percentage and label on the slices
            textposition='inside',  # Position the text inside the slices
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': "Certain infectious and parasitic diseases"},
            width=800,  # Set the width of the figure
            height=800,  # Set the height of the figure
            legend=dict(
                orientation="h",  # Horizontal legend
                x=0.5,  # Center the legend horizontally
                y=-0.1,  # Position the legend just below the chart
                xanchor='center',  # Anchor the x position to the center
                yanchor='top'),  # Anchor the y position to the top
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=100))  # Adjust margins to give space for the legend
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == "Neoplasms":
        filtered_df2 = df[(df.ucodr130 >= 23) & (df.ucodr130 <= 28)]
        filtered_df2.ucodr130 = filtered_df2.ucodr130.map(group2_mapping)
        filtered_df2 = filtered_df2.ucodr130.value_counts().reset_index()
        filtered_df2.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df2["Diseases"],
            values=filtered_df2['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])

        fig.update_layout(
            title={'text': "Neoplasms"},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism":
        filtered_df3 = df[(df.ucodr130 >= 29) & (df.ucodr130 <= 32)]
        filtered_df3.ucodr130 = filtered_df3.ucodr130.map(group3_mapping)
        filtered_df3 = filtered_df3.ucodr130.value_counts().reset_index()
        filtered_df3.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df3["Diseases"],
            values=filtered_df3['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])

        fig.update_layout(
            title={'text': "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism"},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))

        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)    

    if disease == 'Endocrine, nutritional and metabolic diseases':
        filtered_df4 = df[(df.ucodr130 >= 33) & (df.ucodr130 <= 38)]
        filtered_df4.ucodr130 = filtered_df4.ucodr130.map(group4_mapping)
        filtered_df4 = filtered_df4.ucodr130.value_counts().reset_index()
        filtered_df4.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df4["Diseases"],
            values=filtered_df4['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Endocrine, nutritional and metabolic diseases'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Diseases of the nervous system':
        filtered_df5 = df[(df.ucodr130 >= 40) & (df.ucodr130 <= 44)]
        filtered_df5.ucodr130 = filtered_df5.ucodr130.map(group5_mapping)
        filtered_df5 = filtered_df5.ucodr130.value_counts().reset_index()
        filtered_df5.columns = ["Diseases", "Count"]  

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df5["Diseases"],
            values=filtered_df5['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Diseases of the nervous system'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)  

    if disease == 'Diseases of the ear and mastoid process':
        st.warning("No Subcategories for this Category") #Warning if there is no further categories
        st.image("stormtroppers.jpeg") #Picture that appears as warning

    if disease == 'Diseases of the circulatory system':
        filtered_df6 = df[(df.ucodr130 >= 47) & (df.ucodr130 <= 52)]
        filtered_df6.ucodr130 = filtered_df6.ucodr130.map(group6_mapping)
        filtered_df6 = filtered_df6.ucodr130.value_counts().reset_index()
        filtered_df6.columns = ["Diseases", "Count"]    

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df6["Diseases"],
            values=filtered_df6['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Diseases of the circulatory system'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Diseases of the respiratory system':
        filtered_df7 = df[(df.ucodr130 >= 54) & (df.ucodr130 <= 62)]
        filtered_df7.ucodr130 = filtered_df7.ucodr130.map(group7_mapping)
        filtered_df7 = filtered_df7.ucodr130.value_counts().reset_index()
        filtered_df7.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df7["Diseases"],
            values=filtered_df7['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Diseases of the respiratory system'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Diseases of the digestive system':
        filtered_df8 = df[(df.ucodr130 >= 64) & (df.ucodr130 <= 66)]
        filtered_df8.ucodr130 = filtered_df8.ucodr130.map(group8_mapping)
        filtered_df8 = filtered_df8.ucodr130.value_counts().reset_index()
        filtered_df8.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df8["Diseases"],
            values=filtered_df8['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Diseases of the digestive system'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)
        
    if disease == 'Diseases of the genitourinary system':
        filtered_df9 = df[(df.ucodr130 >= 68) & (df.ucodr130 <= 69)]
        filtered_df9.ucodr130 = filtered_df9.ucodr130.map(group9_mapping)
        filtered_df9 = filtered_df9.ucodr130.value_counts().reset_index()
        filtered_df9.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df9["Diseases"],
            values=filtered_df9['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Diseases of the genitourinary system'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Certain conditions originating in the perinatal period':
        filtered_df10 = df[(df.ucodr130 >= 70) & (df.ucodr130 <= 108)]
        filtered_df10.ucodr130 = filtered_df10.ucodr130.map(group10_mapping)
        filtered_df10 = filtered_df10.ucodr130.value_counts().reset_index()
        filtered_df10.columns = ["Diseases", "Count"]   

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df10["Diseases"],
            values=filtered_df10['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Certain conditions originating in the perinatal period'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Hemorrhagic and hematological disorders of newborn':
        filtered_df11 = df[(df.ucodr130 >= 109) & (df.ucodr130 <= 117)]
        filtered_df11.ucodr130 = filtered_df11.ucodr130.map(group11_mapping)
        filtered_df11 = filtered_df11.ucodr130.value_counts().reset_index()
        filtered_df11.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df11["Diseases"],
            values=filtered_df11['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Hemorrhagic and hematological disorders of newborn'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Congenital malformations, deformations and chromosomal abnormalities':
        filtered_df12 = df[(df.ucodr130 >= 119) & (df.ucodr130 <= 133)]
        filtered_df12.ucodr130 = filtered_df12.ucodr130.map(group12_mapping)
        filtered_df12 = filtered_df12.ucodr130.value_counts().reset_index()
        filtered_df12.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df12["Diseases"],
            values=filtered_df12['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Congenital malformations, deformations and chromosomal abnormalities'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified':
        filtered_df13 = df[(df.ucodr130 >= 134) & (df.ucodr130 <= 137)]
        filtered_df13.ucodr130 = filtered_df13.ucodr130.map(group13_mapping)
        filtered_df13 = filtered_df13.ucodr130.value_counts().reset_index()
        filtered_df13.columns = ["Diseases", "Count"]

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df13["Diseases"],
            values=filtered_df13['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'All other diseases (Residual)':
        st.warning("No Subcategories for this Category")
        st.image("stormtroppers.jpeg")

    if disease == 'External causes of mortality':
        filtered_df14 = df[(df.ucodr130 >= 138) & (df.ucodr130 <= 157)]
        filtered_df14.ucodr130 = filtered_df14.ucodr130.map(group14_mapping)
        filtered_df14 = filtered_df14.ucodr130.value_counts().reset_index()
        filtered_df14.columns = ["Diseases", "Count"]   

        fig = go.Figure(data=[go.Pie(
            labels=filtered_df14["Diseases"],
            values=filtered_df14['Count'],
            hoverinfo='label+percent', 
            textinfo='percent',  
            textposition='inside',
            textfont_size=18)])
        
        fig.update_layout(
            title={'text': 'External causes of mortality'},
            width=800,  
            height=800,  
            legend=dict(
                orientation="h",
                x=0.5,  
                y=-0.1,  
                xanchor='center',  
                yanchor='top'),
            showlegend = False,
            margin=dict(l=20, r=20, t=30, b=100))
        
        fig.update_traces(hoverlabel=dict(font=dict(size=16)))

        st.plotly_chart(fig)

    if disease == 'Other external causes':
        st.warning("No Subcategories for this Category")
        st.image("stormtroppers.jpeg")
