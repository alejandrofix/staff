import streamlit as st
import pandas as pd
import pickle
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier


#loading the training model as a pickle

pickle_input = open('DTC_no_scaled.pkl','rb')
classifier=pickle.load(pickle_input)


#@st.cache()

st.image('./logo_negro.png')

#st.title(""" Modelo de predicción de FUGA
#""")

#CAT_Sucursal   
#CAT_tipo_pago  
#CAT_tipo_contrato  
#ValorContrato  
#PagoPrimeraCuota   
#%PagoContrato  
#CuotasTotales  
#Edad   



# defining the function which will make the prediction using the data which the user inputs 
def prediction(CAT_tipo_pago, CAT_tipo_contrato, ValorContrato, PagoPrimeraCuota, CuotasTotales, Edad):   
    
    # Pre-processing user input    
    if CAT_tipo_pago == "Directo":
        CAT_tipo_pago = 1
    elif CAT_tipo_pago == "PAC":
        CAT_tipo_pago = 2
    else:
        CAT_tipo_pago = 3

    if CAT_tipo_contrato == "Contrato Nuevo":
        CAT_tipo_contrato = 1
    elif CAT_tipo_contrato == "Recontratación":
        CAT_tipo_contrato = 2
    else:
        CAT_tipo_contrato = 3
        
    # Making predictions 
    prob_prediction = classifier.predict_proba([[CAT_tipo_pago, CAT_tipo_contrato, ValorContrato, PagoPrimeraCuota, CuotasTotales, Edad]])
    class_prediction = classifier.predict([[CAT_tipo_pago, CAT_tipo_contrato, ValorContrato, PagoPrimeraCuota, CuotasTotales, Edad]])

    #print(prediction)
    if prob_prediction[0][0] < 0.5:
        pred = "Probable fuga de Cliente"
    else:
        pred = "Probable Cliente Activo"
    return pred, [prob_prediction[0][0],prob_prediction[0][1]]

def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:#FEC300;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Modelo de Predicción de FUGA de Clientes</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 

    
    CAT_tipo_pago = st.selectbox("Forma de Pago", ("Directo","PAC","PAT"))
    CAT_tipo_contrato = st.selectbox("Tipo de Contrato",("Contrato Nuevo", "Recontratación","Modificación de Contrato"))    
    ValorContrato = st.number_input("Valor de Contrato") 
    PagoPrimeraCuota = st.number_input("Monto Primera Cuota") 
    CuotasTotales = st.number_input("Número de Cuotas Totales")
    Edad = st.number_input("Edad del Cliente")
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result, classes = prediction(CAT_tipo_pago, CAT_tipo_contrato, ValorContrato, PagoPrimeraCuota, CuotasTotales, Edad) 
        st.success('La situción del cliente es: {}. La probabilidad de no fuga es: {}, mientras que la probabilidad de fuga es: {}'.format(result,classes[0],classes[1]))
        print('éxito')
     
if __name__=='__main__': 
    main()