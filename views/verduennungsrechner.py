import streamlit as st
from functions.Verduenungsrechner import verduennungsrechner
st.title("Verdünnungsrechner")

st.write("Berechne das benötigte Volumen der Stammlösung mit der Formel C1 × V1 = C2 × V2. " \
"In diesem Rechner werden alle Volumen in Millilitern (ml) angegeben. Bitte gib daher sowohl das Endvolumen als auch die berechneten Werte in ml ein.")

# Eingaben
C1 = st.number_input("Anfangskonzentration (C1) in ml", min_value=0.0)
C2 = st.number_input("Zielkonzentration (C2) in ml", min_value=0.0)
V2 = st.number_input("Endvolumen (V2) in ml", min_value=0.0)

# Button
if st.button("Berechnen"):
    
    if C1 > 0:
        V1 = verduennungsrechner(C1, C2, V2)
        st.success(f"Benötigtes Volumen der Stammlösung (V1): {V1:.2f} ml")
    else:
        st.error("Bitte eine Anfangskonzentration größer als 0 eingeben.")

st.caption("""
Formel: C1 × V1 = C2 × V2

C1 = Anfangskonzentration der Stammlösung  
V1 = Volumen der Stammlösung, das benötigt wird  
C2 = gewünschte Zielkonzentration  
V2 = gewünschtes Endvolumen der Lösung  

Das berechnete Ergebnis (V1) zeigt, wie viele Milliliter der Stammlösung entnommen werden müssen.
Diese Menge wird anschließend mit Lösungsmittel auf das gewünschte Endvolumen (V2) aufgefüllt.
""")

 # --- NEW CODE to update history in session state and display it ---
st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])])
        
# --- NEW CODE to display the history table ---
st.dataframe(st.session_state['data_df'])