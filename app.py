import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------
# Setare pagina Streamlit (trebuie sa fie prima comanda)
# ---------------------------------------------------------
st.set_page_config(page_title="Analiza Vânzări Walmart", layout="wide")

# ---------------------------------------------------------
# Interfață
# ---------------------------------------------------------
st.title("🛒 Analiza Vânzărilor - Walmart")
st.markdown("""
Acest dashboard analizează vânzările magazinelor Walmart și factorii care le influențează 
(temperatura, prețul combustibilului, rata șomajului, sărbătorile).
""")

# ---------------------------------------------------------
# Încărcarea datelor
# ---------------------------------------------------------
# Folosim @st.cache_data ca să nu încarce fișierul de fiecare dată când dăm click pe ceva
@st.cache_data
def load_data():
    # Citim fișierul CSV
    df = pd.read_csv("Walmart_Sales.csv")
    
    # Transformăm coloana Date în format recunoscut de timp (din formatul Zi-Lună-An)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y') 
    
    return df

df = load_data()

st.header("1. Vizualizarea Setului de Date Brut")
st.write(f"Setul de date conține **{df.shape[0]} rânduri** și **{df.shape[1]} coloane**.")
st.dataframe(df.head(10)) # Afișăm primele 10 rânduri

# ---------------------------------------------------------
# Curățarea Datelor (Bifăm cerința: tratarea valorilor lipsă)
# ---------------------------------------------------------
st.header("2. Curățarea datelor")

# Verificăm dacă sunt valori lipsă
missing_values = df.isnull().sum().sum()
if missing_values == 0:
    st.success("Datele sunt curate, nu există valori lipsă! (Perfect pentru analiză)")
else:
    st.warning(f"S-au găsit {missing_values} valori lipsă. Le vom trata.")
    df = df.fillna(method='ffill')

# Bifează cerința: tratarea valorilor extreme (outliers). Vom tăia vânzările negative (dacă există)
nr_negative = (df['Weekly_Sales'] < 0).sum()
if nr_negative > 0:
    df = df[df['Weekly_Sales'] >= 0]
    st.info(f"Am eliminat {nr_negative} valori extreme (vânzări negative).")

# ---------------------------------------------------------
# Gruparea Datelor (Bifăm cerința: prelucrări statistice, grupare pandas)
# ---------------------------------------------------------
st.header("3. Evoluția vânzărilor în timp")

# Extragem Anul și Luna din dată pentru a putea face grupări
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Grupăm datele după dată și calculăm suma vânzărilor
df_grouped_date = df.groupby('Date')['Weekly_Sales'].sum().reset_index()

st.write("Grafic: Suma vânzărilor pe parcursul celor 3 ani (pentru toate magazinele).")
st.line_chart(data=df_grouped_date, x='Date', y='Weekly_Sales')

st.write("### Top 10 magazine cu cele mai mari vânzări medii")
df_top_stores = df.groupby('Store')['Weekly_Sales'].mean().reset_index()
df_top_stores = df_top_stores.sort_values(by='Weekly_Sales', ascending=False).head(10)
df_top_stores['Store'] = df_top_stores['Store'].astype(str) # Transformăm în text pentru a afișa corect pe axa X

fig_bar = px.bar(df_top_stores, x='Store', y='Weekly_Sales', color='Weekly_Sales', 
                 text_auto='.2s', title='Top Magazine Walmart',
                 color_continuous_scale='Sunsetdark')
st.plotly_chart(fig_bar, use_container_width=True)

st.write("### Cum se leagă factorii externi de Vânzări? (Matrice de Corelație)")
st.markdown("Acest **Heatmap (Hartă termică)** calculează corelația matematică între variabile. Ne arată cu ce factor ar trebui să fim mai atenți.")
cols = ['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
corr = df[cols].corr()

fig_corr = px.imshow(corr, text_auto=True, aspect="auto", 
                     color_continuous_scale='RdBu_r')
st.plotly_chart(fig_corr, use_container_width=True)

# ---------------------------------------------------------
# 4. Machine Learning - Scalare & Clusterizare (scikit-learn)
# ---------------------------------------------------------
st.header("4. Segmentarea Magazinelor (Clusterizare K-Means)")
st.markdown("Grupăm magazinele folosind algoritmul K-Means în funcție de **Vânzări** și **Rata Șomajului**.")

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    # Pregătim datele pentru clusterizare (agregam pe magazin)
    df_clustering = df.groupby('Store').agg({'Weekly_Sales': 'mean', 'Unemployment': 'mean'}).reset_index()

    # Scalarea datelor (Bifăm cerința: metode de scalare)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_clustering[['Weekly_Sales', 'Unemployment']])

    # K-Means
    kmeans = KMeans(n_clusters=3, random_state=42)
    df_clustering['Cluster'] = kmeans.fit_predict(scaled_features)
    df_clustering['Cluster'] = df_clustering['Cluster'].astype(str) # Pentru o afișare mai frumoasă a culorilor

    # Grafic interactiv cu Plotly
    fig = px.scatter(df_clustering, x='Unemployment', y='Weekly_Sales', color='Cluster', 
                     hover_data=['Store'], title="Clustere: Magazine vs Șomaj")
    st.plotly_chart(fig)
except ImportError:
    st.error("Pachetele scikit-learn sau plotly nu sunt instalate. Deschide terminalul și rulează: pip install scikit-learn plotly")

# ---------------------------------------------------------
# 5. Regresie Logistică (scikit-learn)
# ---------------------------------------------------------
st.header("5. Regresie Logistică (Prezicerea performanței)")
st.markdown("Vom prezice dacă un magazin va avea o săptămână **Peste Medie (1)** sau **Sub Medie (0)**.")

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # Creăm variabila țintă (target) binară
    media_vanzarilor = df['Weekly_Sales'].mean()
    df['Performanta_Buna'] = (df['Weekly_Sales'] > media_vanzarilor).astype(int)

    # Alegem variabilele independente
    X_log = df[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']]
    y_log = df['Performanta_Buna']

    # Împărțim datele în antrenare și testare
    X_train, X_test, y_train, y_test = train_test_split(X_log, y_log, test_size=0.2, random_state=42)

    # Antrenăm modelul
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)

    # Acuratețe
    y_pred = log_reg.predict(X_test)
    acuratete = accuracy_score(y_test, y_pred)
    
    st.success(f"Acuratețea modelului de Regresie Logistică este: **{acuratete * 100:.2f}%**")
except ImportError:
    st.error("Pachetul scikit-learn nu este instalat.")

# ---------------------------------------------------------
# 6. Regresie Multiplă (statsmodels)
# ---------------------------------------------------------
st.header("6. Ce influențează vânzările? (Regresie Multiplă)")
st.markdown("Folosim `statsmodels` pentru a vedea cum influențează factorii externi vânzările.")

try:
    import statsmodels.api as sm

    # Alegem variabilele independente (X) și dependenta (Y)
    X_multi = df[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']]
    Y_multi = df['Weekly_Sales']

    # Adăugăm constanta
    X_multi_sm = sm.add_constant(X_multi)

    # Antrenăm modelul
    model = sm.OLS(Y_multi, X_multi_sm).fit()

    # Afișăm rezultatul
    st.text(model.summary())

    st.info("💡 **Interpretare economică:** Ne uităm la valoarea `P>|t|`. Dacă este sub 0.05, factorul respectiv influențează semnificativ vânzările. De asemenea, coeficientul (coef) arată direcția: dacă e negativ la Șomaj (Unemployment), înseamnă că vânzările scad când șomajul crește.")
except ImportError:
    st.error("Pachetul statsmodels nu este instalat. Deschide terminalul și rulează: pip install statsmodels")
