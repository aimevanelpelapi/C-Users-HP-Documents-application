# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st 
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
st.header("Détection de fraude en assurance automobile")
 
st.image("tof1.png")

st.write("Choisissez les caractéristiques de la déclaration")
col1,col2,col3,col4=st.columns(4)
with col1:
    Month = st.sidebar.selectbox('Month',('Dec', 'Jan', 'Oct', 'Jun', 'Feb', 'Nov', 'Apr', 'Mar', 'Aug','Jul', 'May', 'Sep'))
    Make =st.selectbox('Make',('Honda', 'Toyota', 'Ford', 'Mazda', 'Chevrolet', 'Pontiac','Accura', 'Dodge', 'Mercury', 'Jaguar', 'Nisson', 'VW', 'Saab','Saturn', 'Porche', 'BMW', 'Mecedes', 'Ferrari', 'Lexus'))
    AccidentArea   =st.selectbox('Accident Area',('Urban','Rural'))
    MonthClaimed = st.sidebar.selectbox('MonthClaimed',('Dec', 'Jan', 'Oct', 'Jun', 'Feb', 'Nov', 'Apr', 'Mar', 'Aug','Jul', 'May', 'Sep')) 
    Sex = st.selectbox('Sex',('Female','Male'))

    Age = st.sidebar.slider('Age:',0,80,30)
    Fault = st.selectbox('Fault',('Policy Holder','Third Party'))
with col2:     
    PolicyType = st.selectbox('PolicyType',('Sport - Liability', 'Sport - Collision', 'Sedan - Liability','Utility - All Perils', 'Sedan - All Perils', 'Sedan - Collision','Utility - Collision', 'Utility - Liability', 'Sport - All Perils'))
    VehicleCategory = st.selectbox('VehicleCategory',('Sport','Utility','Sedan'))
    VehiclePrice = st.selectbox('VehiclePrice',('more than 69000', '20000 to 29000', '30000 to 39000','less than 20000', '40000 to 59000', '60000 to 69000'))
 
    Deductible = st.sidebar.slider('Deductible:',0,700,300)
    Days_Policy_Accident = st.selectbox('Days_Policy_Accident',('more than 30', '15 to 30', 'none', '1 to 7', '8 to 15'))
with col3:   
    PastNumberOfClaims =st.selectbox('PastNumberOfClaims',('none', '1', '2 to 4', 'more than 4'))
                                                                                                            
    AgeOfVehicle= st.selectbox('AgeOfVehicle',('3 years', '6 years', '7 years', 'more than 7', '5 years', 'new','4 years', '2 years'))
    AgeOfPolicyHolder = st.selectbox('AgeOfPolicyHolder',('26 to 30', '31 to 35', '41 to 50', '51 to 65', '21 to 25','36 to 40', '16 to 17', 'over 65', '18 to 20')) 
    
    AgentType =  st.selectbox('AgentType',('External', 'Internal'))
with col4:     
    NumberOfSuppliments =  st.selectbox('NumberOfSuppliments',('none', 'more than 5', '3 to 5', '1 to 2'))
    AddressChange_Claim =  st.selectbox('AddressChange_Claim',('1 year', 'no change', '4 to 8 years', '2 to 3 years','under 6 months'))                              
    Year =  st.sidebar.slider('Year:',1994,1996,1995)
    BasePolicy =  st.selectbox('BasePolicy',('Liability', 'Collision', 'All Perils'))
def client_caract_entree():
    data = {'Year':Year, 'Deductible':Deductible,'Age':Age,'Month':Month,'Make':Make,
            'AccidentArea':AccidentArea,'MonthClaimed':MonthClaimed,'Sex':Sex,'Fault':Fault,'PolicyType':PolicyType,'VehicleCategory':VehicleCategory,
            'VehiclePrice':VehiclePrice,'Days_Policy_Accident':Days_Policy_Accident,
            'PastNumberOfClaims':PastNumberOfClaims,'AgeOfVehicle':AgeOfVehicle,
            'AgeOfPolicyHolder':AgeOfPolicyHolder,
            'AgentType':AgentType,
            'NumberOfSuppliments':NumberOfSuppliments,
            'AddressChange_Claim':AddressChange_Claim,
            'BasePolicy':BasePolicy}
    profil_client = pd.DataFrame(data, index = [0]) 
    return profil_client                                                                                                         
input_df = client_caract_entree()

    
# Traiter les données
fraud=pd.read_csv("C:/Users/HP/Documents/application/fraud_oracle.csv")
fraud.drop(['PolicyNumber','RepNumber','WeekOfMonth','WeekOfMonthClaimed','DriverRating','DayOfWeek','DayOfWeekClaimed','MaritalStatus','Days_Policy_Claim','PoliceReportFiled','WitnessPresent','NumberOfCars'], axis = 1, inplace = True)
X=fraud.drop(columns='FraudFound_P')
y=fraud.FraudFound_P
    
#X['Age']=X['Age'].replace(0,X['Age'].median())
donnee_entree = pd.concat([input_df, X], axis = 0)


# Normalisation 
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler()
donnee_entree['Year']=scaler.fit_transform(donnee_entree[['Year']])
donnee_entree['Deductible']=scaler.fit_transform(donnee_entree[['Deductible']])
donnee_entree['Age']=scaler.fit_transform(donnee_entree[['Age']])
donnee_entree['Age']=donnee_entree['Age'].replace(0,X['Age'].median())
    # Encodage des variables
donnee_entree = pd.get_dummies(donnee_entree,drop_first = True)
    
    # On prend uniquement la premiere ligne
donnee_entree = donnee_entree[:1]
#st.subheader("Donnees transformées")
st.write(donnee_entree)

# Importer le modèle


# Appliquer le modèle sur les données 
@st.cache(allow_output_mutation = True, show_spinner = True,suppress_st_warning = True) 
def load_model():
    filename = 'C:/Users/HP/Documents/application/modele.sav'
    rd = joblib.load(open(filename,'rb')) 
    return rd
# Appliquer le modele

if st.button("Valider"):
    rd = load_model() 
    prevision = rd.predict(donnee_entree)
    # on charge le modele

    if prevision ==1:
        st.image("tof3.png")
        st.subheader("Risque de Fraude")
      
    else:
        st.image("tof4.png")
        st.subheader("Il n'y a pas Fraude")
#st.write("#Detection de Fraude en Assurance Auto")
#st.sidebar.header("Description de la")

