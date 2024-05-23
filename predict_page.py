import streamlit as st
import numpy as np
import pickle
import pandas as pd
import time
import os
import zipfile
from zipfile import ZipFile 

def show_predict_page():

    #Create a sidebar where Users can look up explanations of the features
    definition = st.sidebar.selectbox(":rainbow[Feature Explanation]", 
                                    ("Birthweight (grams)","Age at Death (days)", 
                                    "Obstetric Estimate", "Record-Axis Conditions",
                                    "Combined Gestation","Entity-Axis Conditions",
                                    "Five Minute APGAR","Place of Death and Decendent’s Status"),
                                        index = None, placeholder = "Choose Feature...")
    
    if definition == "Birthweight (grams)":
        st.sidebar.write("Birthweight is the first weight of a baby, taken just after being born. A low birthweight is less than 2500 grams while a very low birthweight is less than 1500 grams. The Guinness Book of World Record lists the heaviest newborn birth on record at 22 pounds (approximately 9980 grams) in 1879, who died around 11 hours after their birth. As a result, the highest permissible birthweight for this app has been set to 9999 grams.")
    if definition == "Age at Death (days)":
        st.sidebar.write("Age of death refers to the age of the infant at death in days. A child is referred to as an infant from 0-1 years of age. The maximum permissible age is 365 days.")
    if definition == "Obstetric Estimate":
        st.sidebar.write("Obstetric Estimate refers to the best estimate of the infant’s gestational age in completed weeks. It is based on the clinician’s final estimate of gestation. ")
        st.sidebar.write("Gestational age is the common term used during pregnancy to describe how far along the pregnancy is. It is a measure of the age of a pregnancy taken from the beginning of the woman’s last menstrual period (LMP) or the corresponding age of the gestation as estimated by a more accurate method, if available. A normal pregnancy can range from 38-42 weeks. Infants born before 37 weeks are considered premature.")
    if definition == "Record-Axis Conditions":
        st.sidebar.write("Record-Axis conditions refers to coding conditions listed on the death certificate. Record-Axis codes are assigned in terms of the set codes that best describe the overall medical certification portion of the death certificate.")
        st.sidebar.write("Where appropriate, they link two or more diagnostic conditions to form composite code that are classifiable to a single code. They are preferred for multiple cause tabulation to better convey the intent of the certifier, and to eliminate redundant cause-of-death information.")
    if definition == "Combined Gestation":
        st.sidebar.write("Combined Gestation is the obstetric estimate for multiple pregnancies.")
    if definition == "Entity-Axis Conditions":
        st.sidebar.write("Entity-Axis conditions, like record-axis conditions, also refer to conditions that are recorded on the death certificate. Entity-Axis codes reflect the placement of each condition on the certificate for each decedent.") 
        st.sidebar.write("They represent what is actually written on the death certificate by the certifier expressed in terms of ICD (International Classification of Disease) codes including an indicator of which line the code came from and which position on the line it came from (if more than one code was listed per line). Multiple cause of death data has been used to look at trends in certain diseases, e.g. HIV. ")
    if definition == "Five Minute APGAR":
        st.sidebar.write("The Agpar score is a rapid method for evaluating neonates immediately after birth and in response to resuscitation.  It is recorded in all newborn infants at 1 minute and 5 minutes after birth. In our case we are specifically looking at the AGPAR score taken at 5 minutes. AGPAR is also a useful mnemonic to describe the components of the score: appearance (color), pulse (heart rate), grimace (grimace response or reflex irritability in response to stimulation), activity (muscle tone), and respiration (breathing rate).")
        st.sidebar.write("Each category is weighted evenly and assigned a value of 0, 1, or 2. The components are then added together to give a total score. A score of 7-10 is considered reassuring, a score of 4-6 is moderately abnormal, and a score of 0-3 is deemed to be low in full-term and late preterm infants. ")
    if definition == "Place of Death and Decendent’s Status":
        st.sidebar.write("Place of death refers to the specific venue death occurs. More comprehensively, it could refer to the site where a dying person lives and/or receives care for the later stages of their life.") 
        st.sidebar.write("Decedent is a term that is generally used in the law governing estates and trusts, in reference to a person who has died.")

    @st.cache_data
    def load_model():
        with zipfile.ZipFile("ensemble1.pkl.zip", "r") as zip_ref:
            with zip_ref.open("ensemble1.pkl", "r") as file:
                loaded_ensemble1 = pickle.load(file)
        return loaded_ensemble1

    loaded_ensemble1 = load_model()

    st.title(':rainbow[Prediction of Cause of Infant Death]')
    st.image("baby.jpg")

    st.write('This app predicts the most probable cause of infant death based on 8 features.')

    st.markdown("Please choose your 8 features.")

    #Input features and their mapping to integers (if needed)
    birthweight = st.number_input('Birthweight (grams)',max_value=9999)

    age = st.number_input('Age at Death (days)', max_value=365)

    obstetric_estimate = st.selectbox(
        "Obstetric Estimate",
        ("Under 20 weeks",
        "20-27 weeks",
        "28-31 weeks",
        "32-33 weeks",
        "34-36 weeks",
        "37-38 weeks",
        "39 weeks",
        "40 weeks",
        "41 weeks",
        "42 weeks and over",
        "Unknown"),
        index=None,
        placeholder = "Select Obstetric Estimate..."
    )

    obstetric_estimate_mapping = {
            "Under 20 weeks": 1,
            "20-27 weeks": 2,
            "28-31 weeks": 3,
            "32-33 weeks": 4,
            "34-36 weeks": 5,
            "37-38 weeks": 6,
            "39 weeks": 7,
            "40 weeks": 8,
            "41 weeks": 9,
            "42 weeks and over": 10,
            "Unknown": 11
        }

    #Since our model cannot intake strings as variables, we map our strings to integers
    if obstetric_estimate in obstetric_estimate_mapping:
        obstetric_estimate_mapped = obstetric_estimate_mapping[obstetric_estimate]

    record_axis = st.slider("Number of Record-Axis Conditions",1,20,1)

    combined_gestation = st.selectbox(
        "Combined Gestation",
        ("Under 20 weeks",
        "20-27 weeks",
        "28-31 weeks",
        "32-33 weeks",
        "34-36 weeks",
        "37-38 weeks",
        "39 weeks",
        "40 weeks",
        "41 weeks",
        "42 weeks and over",
        "Unknown"),
        index=None,
        placeholder = "Select Combined Gestation..."
    )

    combined_gestation_mapping = {
            "Under 20 weeks": 1,
            "20-27 weeks": 2,
            "28-31 weeks": 3,
            "32-33 weeks": 4,
            "34-36 weeks": 5,
            "37-38 weeks": 6,
            "39 weeks": 7,
            "40 weeks": 8,
            "41 weeks": 9,
            "42 weeks and over": 10,
            "Unknown": 11
        }

    #Since our model cannot intake strings as variables, we map our strings to integers
    if combined_gestation in combined_gestation_mapping:
        combined_gestation_mapped = combined_gestation_mapping[combined_gestation]

    entity_axis = st.slider("Number of Entity-Axis Conditions",1,20,1)

    agpar = st.selectbox(
        "Five Minute APGAR",
        ("A score of 0-3", "A score of 4-6", "A score of 7-8 ", "A score of 9-10", "Unknown or not stated"),
        index=None,
        placeholder = "Select AGPAR score..."
    )

    agpar_mapping = {
            "A score of 0-3": 1,
            "A score of 4-6": 2,
            "A score of 7-8 ": 3,
            "A score of 9-10": 4,
            "Unknown or not stated":5
        }

    #Since our model cannot intake strings as variables, we map our strings to integers
    if agpar in agpar_mapping:
        agpar_mapped = agpar_mapping[agpar]

    hospd = st.selectbox(
        "Place of Death and Decendent’s Status",
        ("Hospital, clinic or Medical Center – Inpatient",
        "Hospital, clinic or Medical Center – Outpatient or admitted to Emergency Room",
        "Hospital, clinic or Medical Center – Dead on Arrival",
        "Decedent’s home",
        "Hospice facility",
        "Nursing home/long term care",
        "Other",
        "Place of death unknown"),
        index=None,
        placeholder = "Select Place of Death and Decendent’s Status..."
    )

    hospd_mapping =  {
            "Hospital, clinic or Medical Center – Inpatient": 1,
            "Hospital, clinic or Medical Center – Outpatient or admitted to Emergency Room": 2,
            "Hospital, clinic or Medical Center – Dead on Arrival": 3,
            "Decedent’s home": 4,
            "Hospice facility": 5,
            "Nursing home/long term care": 6,
            "Other": 7,
            "Place of death unknown": 8
        }

    #Since our model cannot intake strings as variables, we map our strings to integers
    if hospd in hospd_mapping:
        hospd_mapped = hospd_mapping[hospd]

    #Map our integer predictions to strings
    def predictions_to_strings(predictions):
        label_mapping = {
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
        
        #Convert integer predictions to strings using the mapping
        string_predictions = [label_mapping[pred] for pred in predictions]
        
        return string_predictions

    #Give our top 3 predictions and their probabilities
    def top_3_predictions(new_data):
        predicted_probabilities = loaded_ensemble1.predict_proba(new_data)
        output = ""
        
        for i, probs in enumerate(predicted_probabilities):
            # Get indices of top 3 probabilities
            top3_indices = probs.argsort()[-3:][::-1]
            # Get corresponding class labels and probabilities
            top3_classes = loaded_ensemble1.classes_[top3_indices]
            top3_probs = probs[top3_indices] * 100  # Convert probabilities to percentages
            
            # Convert integer predictions to strings using the mapping
            top3_classes_strings = predictions_to_strings(top3_classes)
            
            # Add predictions for each sample to the output
            output += f"Top 3 predictions for Probable Cause of Infant Death:\n" 
            for j, (pred_class, pred_class_string, pred_prob) in enumerate(zip(top3_classes, top3_classes_strings, top3_probs)):
                output += f"   Prediction {j + 1}: {pred_class_string}, Probability of {pred_prob:.2f}%\n" 
            output += '\n'  # Add a newline after each sample's predictions
        
        return output

    ok = st.button(":rainbow[Calculate the Top 3 Most Probable Causes of Infant Death]")

    if ok: 
        # Check if any input is provided
        if birthweight is None or age is None or obstetric_estimate not in obstetric_estimate_mapping \
            or combined_gestation not in combined_gestation_mapping or agpar not in agpar_mapping \
            or hospd not in hospd_mapping:
            st.warning("Please provide input for all features.")
        else:
            #Insertion of a progress bar
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()

            #Input features
            X = np.array([[birthweight, age, obstetric_estimate_mapped, record_axis, combined_gestation_mapped,
                        entity_axis, agpar_mapped, hospd_mapped]])
            X = X.astype(float)

            #Make predictions
            top_cause = loaded_ensemble1.predict(X)
            top_causes = top_3_predictions(X)


            #Print out top 3 predictions
            st.text(top_causes)
   
            
            
