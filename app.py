import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------
# Setare pagina Streamlit
# ---------------------------------------------------------
st.set_page_config(page_title="Analiza Vânzări Walmart", layout="wide", page_icon="🛒")

# ---------------------------------------------------------
# Încărcarea și Curățarea Datelor (Global)
# ---------------------------------------------------------
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("Walmart_Sales.csv")
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y') 
    
    # Tratarea valorilor lipsă
    df = df.fillna(method='ffill')
    
    # Tratarea valorilor extreme
    df = df[df['Weekly_Sales'] >= 0]
    
    # Extragere an și lună pentru analize viitoare
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    return df

df = load_and_clean_data()

# ---------------------------------------------------------
# MENIU LATERAL (SIDEBAR) PENTRU NAVIGARE MULTI-PAGINĂ
# ---------------------------------------------------------
st.sidebar.title("📌 Meniu Navigare")
st.sidebar.markdown("Folosește acest meniu pentru a naviga prin secțiunile proiectului.")

page = st.sidebar.radio(
    "Alege o pagină:",
    ("1. Introducere și Date", "2. Analiza Vânzărilor", "3. Inteligență Artificială")
)

# ---------------------------------------------------------
# PAGINA 1: INTRODUCERE ȘI DATE
# ---------------------------------------------------------
if page == "1. Introducere și Date":
    st.title("🛒 Analiza Vânzărilor - Walmart")
    st.markdown("""
    Bine ai venit! Acest dashboard analizează vânzările magazinelor Walmart și modul în care diverși factori 
    economici (temperatura, prețul combustibilului, rata șomajului, sărbătorile) le influențează.
    """)
    
    st.header("1. Pregătirea Setului de Date")
    st.write(f"În urma încărcării, setul de date are **{df.shape[0]} rânduri** și **{df.shape[1]} coloane**.")
    st.success("Datele au fost curățate automat (s-au tratat valorile lipsă și s-au eliminat vânzările negative).")

    # WIDGET: CHECKBOX
    st.markdown("---")
    st.write("Apasă pe bifa de mai jos pentru a vizualiza tabelul brut:")
    if st.checkbox("🔍 Arată Setul de Date Brut"):
        st.dataframe(df.head(100)) # Afișăm primele 100 de rânduri pentru performanță
        st.info("💡 Sfat: Poți da scroll în tabel pentru a vedea datele detaliate.")

# ---------------------------------------------------------
# PAGINA 2: ANALIZA VÂNZĂRILOR
# ---------------------------------------------------------
elif page == "2. Analiza Vânzărilor":
    st.title("📈 Analiza Vânzărilor (EDA)")
    
    # WIDGET: SELECTBOX
    st.header("1. Evoluția vânzărilor în timp")
    
    # Creăm o listă cu toate magazinele, adăugând și opțiunea "Toate Magazinele"
    lista_magazine = ["Toate Magazinele"] + list(df['Store'].unique())
    magazin_ales = st.selectbox("Alege magazinul pentru a-i vedea evoluția:", lista_magazine)
    
    # Filtrăm datele în funcție de ce a ales utilizatorul din Drop-Down
    if magazin_ales == "Toate Magazinele":
        df_plot = df.groupby('Date')['Weekly_Sales'].sum().reset_index()
        st.write("Afișăm **suma vânzărilor** pentru întreaga rețea Walmart.")
    else:
        df_plot = df[df['Store'] == magazin_ales].groupby('Date')['Weekly_Sales'].sum().reset_index()
        st.write(f"Afișăm vânzările **doar pentru Magazinul {magazin_ales}**.")
        
    st.line_chart(data=df_plot, x='Date', y='Weekly_Sales')

    st.markdown("---")
    st.header("2. Top 10 Magazine cu cele mai mari vânzări medii")
    
    df_top_stores = df.groupby('Store')['Weekly_Sales'].mean().reset_index()
    df_top_stores = df_top_stores.sort_values(by='Weekly_Sales', ascending=False).head(10)
    df_top_stores['Store'] = df_top_stores['Store'].astype(str) # Transformăm în text pt axa X

    fig_bar = px.bar(df_top_stores, x='Store', y='Weekly_Sales', color='Weekly_Sales', 
                     text_auto='.2s', title='Top Magazine Walmart',
                     color_continuous_scale='sunsetdark')
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# PAGINA 3: INTELIGENȚĂ ARTIFICIALĂ
# ---------------------------------------------------------
elif page == "3. Inteligență Artificială":
    st.title("🤖 Inteligență Artificială și Econometrie")
    
    st.write("### Cum se leagă factorii externi de Vânzări? (Matrice de Corelație)")
    st.markdown("Acest **Heatmap** calculează corelația matematică între variabile. Ne arată cu ce factor ar trebui să fim mai atenți.")
    cols = ['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
    corr = df[cols].corr()

    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("---")
    st.header("1. Segmentarea Magazinelor (Clusterizare K-Means)")
    
    # WIDGET: SLIDER
    numar_clustere = st.slider("Alege numărul de clustere (grupuri) în care să împărțim magazinele:", min_value=2, max_value=5, value=3)
    
    try:
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans

        df_clustering = df.groupby('Store').agg({'Weekly_Sales': 'mean', 'Unemployment': 'mean'}).reset_index()

        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(df_clustering[['Weekly_Sales', 'Unemployment']])

        kmeans = KMeans(n_clusters=numar_clustere, random_state=42)
        df_clustering['Cluster'] = kmeans.fit_predict(scaled_features)
        df_clustering['Cluster'] = df_clustering['Cluster'].astype(str)

        fig = px.scatter(df_clustering, x='Unemployment', y='Weekly_Sales', color='Cluster', 
                         hover_data=['Store'], title=f"Gruparea în {numar_clustere} Clustere: Magazine vs Șomaj")
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.error("Pachetul scikit-learn nu este instalat.")

    st.markdown("---")
    st.header("2. Regresie Logistică (Prezicerea performanței)")
    st.markdown("Vom prezice dacă un magazin va avea o săptămână **Peste Medie (1)** sau **Sub Medie (0)**.")

    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score

        media_vanzarilor = df['Weekly_Sales'].mean()
        df['Performanta_Buna'] = (df['Weekly_Sales'] > media_vanzarilor).astype(int)

        X_log = df[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']]
        y_log = df['Performanta_Buna']

        X_train, X_test, y_train, y_test = train_test_split(X_log, y_log, test_size=0.2, random_state=42)

        log_reg = LogisticRegression()
        log_reg.fit(X_train, y_train)

        y_pred = log_reg.predict(X_test)
        acuratete = accuracy_score(y_test, y_pred)
        
        st.success(f"Acuratețea modelului de Regresie Logistică este: **{acuratete * 100:.2f}%**")
    except ImportError:
        st.error("Pachetul scikit-learn nu este instalat.")

    st.markdown("---")
    st.header("3. Ce influențează vânzările? (Regresie Multiplă)")
    st.markdown("Folosim `statsmodels` pentru a vedea cum influențează factorii externi vânzările.")

    try:
        import statsmodels.api as sm

        X_multi = df[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']]
        Y_multi = df['Weekly_Sales']

        X_multi_sm = sm.add_constant(X_multi)
        model = sm.OLS(Y_multi, X_multi_sm).fit()

        st.text(model.summary())
    except ImportError:
        st.error("Pachetul statsmodels nu este instalat.")
