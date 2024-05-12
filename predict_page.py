import streamlit as st
import numpy as np
import pickle
import pandas as pd
import time

#st.balloons()
#st.subheader("Progress Bar")
# st.progress(10)
# st.subheader("Waiting during Execution")
# with st.spinner('Wait for it...'): time.sleep(10)
#     #time.sleep(10)

st.snow()

def load_model():
    with open("ensemble1.pkl", "rb") as file:
        loaded_ensemble1 = pickle.load(file)
    return loaded_ensemble1

loaded_ensemble1 = load_model()

st.title('Prediction of Cause of Infant Death')
st.image("baby.jpg")

st.write('This app predicts the most probable cause of death based on 8 features.')

st.markdown("Please choose your 8 features.")

birthweight = st.number_input('Birthweight (grams)',max_value=9999)
st.write('Maximum weight allowed is 9999 grams.')

age = st.number_input('Age at Death (days)', max_value=365)
st.write('Maximum age is 365 days.')

obstetric_estimate = st.slider("Obstetric Estimate of the Infant’s Gestational Age in Completed Weeks",1,11,1)

row_values = [
    "Under 20 weeks",
    "20-27 weeks",
    "28-31 weeks",
    "32-33 weeks",
    "34-36 weeks",
    "37-38 weeks",
    "39 weeks",
    "40 weeks",
    "41 weeks",
    "42 weeks and over",
    "Unknown"
]

# Create a DataFrame with row values and numbered index
df_obs = pd.DataFrame(row_values, columns=['Obstetric Estimate'], index=range(1, len(row_values) + 1))
st.table(df_obs)

record_axis = st.slider("Number of Record-Axis Conditions",1,20,1)

combined_gestation = st.slider("Combined Gestation for Multiple Pregnancies",1,11,1)

row_values = [
    "Under 20 weeks",
    "20-27 weeks",
    "28-31 weeks",
    "32-33 weeks",
    "34-36 weeks",
    "37-38 weeks",
    "39 weeks",
    "40 weeks",
    "41 weeks",
    "42 weeks and over",
    "Unknown"
]

# Create a DataFrame with row values and numbered index
df_ges = pd.DataFrame(row_values, columns=['Combined Gestation'], index=range(1, len(row_values) + 1))

st.table(df_ges)

entity_axis = st.slider("Number of Entity-Axis Conditions",1,20,1)

agpar = st.slider("Five Minute APGAR: Health Evaluation of Newborn 5 minutes after birth",1,5,1)

row_values = [
    "A score of 0-3",
    "A score of 4-6",
    "A score of 7-8 ",
    "A score of 9-10",
    "Unknown or not stated"

]

# Create a DataFrame with row values and numbered index
df_agpar = pd.DataFrame(row_values, columns=['Five Minute APGAR'], index=range(1, len(row_values) + 1))

# Print the DataFrame
st.table(df_agpar)

hospd = st.slider("Place of Death and Descendent’s Status",1,8,1)

row_values = [
    "Hospital, clinic or Medical Center – Inpatient",
    "Hospital, clinic or Medical Center – Outpatient or admitted to Emergency Room",
    "Hospital, clinic or Medical Center – Dead on Arrival",
    "Descedent’s home",
    "Hospice facility",
    "Nursing home/long term care",
    "Other",
    "Place of death unknown"
]

# # Create a DataFrame with row values and numbered index
df_hosp = pd.DataFrame(row_values, columns=['Place of Death and Descendent’s Status'], index=range(1, len(row_values) + 1))

st.table(df_hosp)

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
        138: 'External causes of mortality',
        158: 'Other external causes'
    }
    
    ## Convert integer predictions to strings using the mapping
    string_predictions = [label_mapping[pred] for pred in predictions]
    
    return string_predictions

# def top_3_predictions(new_data):
#     predicted_probabilities = loaded_ensemble1.predict_proba(new_data)
    
#     for i, probs in enumerate(predicted_probabilities):
#         # Get indices of top 3 probabilities
#         top3_indices = probs.argsort()[-3:][::-1]
#         # Get corresponding class labels and probabilities
#         top3_classes = loaded_ensemble1.classes_[top3_indices]
#         top3_probs = probs[top3_indices] * 100  # Convert probabilities to percentages
        
#         # Convert integer predictions to strings using the mapping
#         top3_classes_strings = predictions_to_strings(top3_classes)
        
#         # Print predictions for each sample
#         print(f"Top 3 predictions for Infant Death:")
#         for j, (pred_class, pred_class_string, pred_prob) in enumerate(zip(top3_classes, top3_classes_strings, top3_probs)):
#             print(f"   Prediction {j + 1}: Class {pred_class_string}, Probability {pred_prob:.2f}%")

def top_3_predictions1(new_data):
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
        
        # Print predictions for each sample
        #print(f"Top 3 predictions for Sample {i+1}:")
        #for j, (pred_class, pred_class_string, pred_prob) in enumerate(zip(top3_classes, top3_classes_strings, top3_probs)):
        #    print(f"   Prediction {j + 1}: Class {pred_class_string}, Probability {pred_prob:.2f}%")
        
        # Add predictions for each sample to the output
        output += f"Top 3 predictions for Probable Cause of Infant Death:\n"
        for j, (pred_class, pred_class_string, pred_prob) in enumerate(zip(top3_classes, top3_classes_strings, top3_probs)):
            output += f"   Prediction {j + 1}: {pred_class_string}, Probability of {pred_prob:.2f}%\n"
        output += '\n'  # Add a newline after each sample's predictions
    
    return output

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

ok = st.button("Determine the Top 3 Most Probable causes of Infant Death")
if ok: 
    X = np.array([[birthweight,age,obstetric_estimate,record_axis,combined_gestation,
                   entity_axis,agpar,hospd]])
    X = X.astype(float)
    
    top_cause = loaded_ensemble1.predict(X)
    top_causes = top_3_predictions1(X)

    top_cause_string = predictions_to_strings(top_cause)
    #st.write("Hello")
    #st.subheader("Hello")
    #st.subheader(f"Top Probable Cause is {top_cause}")
    #st.write(f"Top Probable Cause is {top_cause}")
    st.write(f"Top Probable Cause of Infant Death is {top_cause_string[0]}")
    #st.write(f"{top_causes}")
    st.text(f"{top_causes}")
    #input_variable = X.all()
    #if input_variable:
    #    st.write(top_3_predictions(input_variable.reshape(-1,1)))
    #st.subheader(top_cause)

   #st.subheader = (f"{top_3_predictions(X)}")
    #print(top_3_predictions(X))
    #print(predictions_to_strings(top_cause))
    #print(top_cause)
