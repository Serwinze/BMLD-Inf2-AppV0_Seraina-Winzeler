import streamlit as st
import pandas as pd

from utils.data_manager import DataManager  # --- NEW CODE: import data manager ---
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_history(df):
    fig, ax = plt.subplots()

    if df.empty:
        return fig

    # Falls timestamp existiert → als x-Achse nutzen
    if "timestamp" in df.columns:
        x = df["timestamp"]
    else:
        x = range(len(df))

    # Linien plotten
    if "C1" in df.columns:
        ax.plot(x, df["C1"], label="C1 (Start)")
    if "C2" in df.columns:
        ax.plot(x, df["C2"], label="C2 (Ziel)")
    if "V1" in df.columns:
        ax.plot(x, df["V1"], label="V1 (berechnet)")

    ax.set_title("Verlauf der Berechnungen")
    ax.set_xlabel("Zeit / Berechnungen")
    ax.set_ylabel("Werte")
    ax.legend()

    return fig
def plot_verduennung(C1, C2, V2, V1):
    fig, ax = plt.subplots()

    # Balken: Vergleich Stammlösung vs. Ziel
    labels = ["C1 (Start)", "C2 (Ziel)"]
    values = [C1, C2]

    ax.bar(labels, values)

    # Titel + Labels
    ax.set_title("Verdünnung: Konzentrationsvergleich")
    ax.set_ylabel("Konzentration")

    # Zusatzinfo als Text
    ax.text(0, C1, f"V1 = {round(V1,2)} ml", ha='center', va='bottom')
    ax.text(1, C2, f"V2 = {round(V2,2)} ml", ha='center', va='bottom')

    return fig

def plot_interactive_history(df):
    if df.empty:
        return None, None

    fig = go.Figure()

    # 👉 Zeitachse verwenden wenn vorhanden
    if "timestamp" in df.columns:
        x = df["timestamp"]
    else:
        x = df.index

    # 🔹 Konzentrationen
    if "C1" in df.columns:
        fig.add_trace(go.Scatter(
            x=x, y=df["C1"],
            mode='lines+markers',
            name="C1 (Startkonzentration)"
        ))

    if "C2" in df.columns:
        fig.add_trace(go.Scatter(
            x=x, y=df["C2"],
            mode='lines+markers',
            name="C2 (Zielkonzentration)"
        ))

    # 🔹 Volumen
    if "V1" in df.columns:
        fig.add_trace(go.Scatter(
            x=x, y=df["V1"],
            mode='lines+markers',
            name="V1 (benötigtes Volumen)"
        ))

    # 🔬 Verdünnungsfaktor (wichtiger!)
    if "C1" in df.columns and "C2" in df.columns:
        verduennung = df["C1"] / df["C2"].replace(0, None)

        fig.add_trace(go.Scatter(
            x=x,
            y=verduennung,
            mode='lines+markers',
            name="Verdünnungsfaktor (C1/C2)",
            line=dict(dash='dot')
        ))

    # 🎨 Layout verbessern
    fig.update_layout(
        title="📊 Erweiterte Analyse deiner Verdünnungen",
        xaxis_title="Zeit / Berechnungen",
        yaxis_title="Werte",
        hovermode="x unified",
        template="plotly_white"
    )

    # 📊 Statistiken
    stats = {}
    if "V1" in df.columns:
        stats["Ø V1"] = round(df["V1"].mean(), 2)
    if "C1" in df.columns:
        stats["Max C1"] = round(df["C1"].max(), 2)
    if "C2" in df.columns:
        stats["Min C2"] = round(df["C2"].min(), 2)

    return fig, stats

from functions.Verduenungsrechner import verduennungsrechner
st.title("Verdünnungsrechner")


st.write("Berechne das benötigte Volumen der Stammlösung mit der Formel C1 × V1 = C2 × V2. " \
"In diesem Rechner werden alle Volumen in Millilitern (ml) angegeben. Bitte gib daher sowohl das Endvolumen als auch die berechneten Werte in ml ein.")

# Session State initialisieren
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(columns=["timestamp","C1","C2","V2","V1"])

# Eingaben
C1 = st.number_input("Anfangskonzentration (C1) in ml", min_value=0.0)
C2 = st.number_input("Zielkonzentration (C2) in ml", min_value=0.0)
V2 = st.number_input("Endvolumen (V2) in ml", min_value=0.0)

# Button
if st.button("Berechnen"):
    
    if C1 > 0:
        result = verduennungsrechner(C1, C2, V2)
        st.success(f"Benötigtes Volumen der Stammlösung (V1): {result['V1']} ml")
         # --- NEW CODE to update history in session state and display it ---

        fig = plot_verduennung(C1, C2, V2, result["V1"])
        st.subheader("📊 Visualisierung der Verdünnung")
        st.pyplot(fig)
        
        result["timestamp"] = datetime.datetime.now()

        st.session_state['data_df'] = pd.concat(
            [st.session_state['data_df'], pd.DataFrame([result])],
            ignore_index=True
        )


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

    # --- CODE UPDATE: save data to data manager ---
    data_manager = DataManager()
    data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
    # --- END OF CODE UPDATE ---

# --- NEW CODE to display the history table ---
st.dataframe(st.session_state['data_df'])

# =========================
# 📈 VISUALISIERUNG
# =========================

if not st.session_state['data_df'].empty:

    # 🔹 Interaktive Analyse
    st.subheader("📊 Erweiterte Analyse deiner Berechnungen")

    fig, stats = plot_interactive_history(st.session_state['data_df'])

    if fig:
        st.plotly_chart(fig, use_container_width=True)

    # 🔹 Statistiken
    st.subheader("📊 Statistiken")

    col1, col2, col3 = st.columns(3)

    if "Ø V1" in stats:
        col1.metric("Ø V1 (ml)", stats["Ø V1"])
    if "Max C1" in stats:
        col2.metric("Max C1", stats["Max C1"])
    if "Min C2" in stats:
        col3.metric("Min C2", stats["Min C2"])

else:
    st.info("Noch keine Berechnungen vorhanden.")