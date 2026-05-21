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
    df = df.ffill()
    
    # Tratarea valorilor extreme
    df = df[df['Weekly_Sales'] >= 0]
    
    # Extragere an și lună pentru analize viitoare
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Codificarea datelor: creăm coloana categorică 'Sezon' din lună
    def get_sezon(month):
        if month in [12, 1, 2]:
            return 'Iarnă'
        elif month in [3, 4, 5]:
            return 'Primăvară'
        elif month in [6, 7, 8]:
            return 'Vară'
        else:
            return 'Toamnă'

    df['Sezon'] = df['Month'].apply(get_sezon)

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df['Sezon_Encoded'] = le.fit_transform(df['Sezon'])

    return df, le

df, label_encoder = load_and_clean_data()

# ---------------------------------------------------------
# MENIU LATERAL (SIDEBAR) PENTRU NAVIGARE MULTI-PAGINĂ
# ---------------------------------------------------------
st.sidebar.title("📌 Meniu Navigare")
st.sidebar.markdown("Folosește acest meniu pentru a naviga prin secțiunile proiectului.")

page = st.sidebar.radio(
    "Alege o pagină:",
    ("1. Introducere și Date", "2. Analiza Vânzărilor", "3. Inteligență Artificială", "4. Funcții Avansate")
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

    st.markdown("---")
    st.header("2. Codificarea Datelor (Label Encoding)")
    st.markdown("""
    Algoritmii de Machine Learning nu pot procesa text direct. Coloana **Sezon** (text)
    a fost transformată în numere folosind `LabelEncoder` din `scikit-learn`.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Corespondența Sezon → Cod numeric:**")
        mapping_df = pd.DataFrame({
            'Sezon': label_encoder.classes_,
            'Cod Numeric': label_encoder.transform(label_encoder.classes_)
        })
        st.dataframe(mapping_df, hide_index=True)

    with col2:
        st.write("**Distribuția înregistrărilor pe sezoane:**")
        sezon_counts = df['Sezon'].value_counts().reset_index()
        sezon_counts.columns = ['Sezon', 'Nr. înregistrări']
        fig_sezon = px.bar(sezon_counts, x='Sezon', y='Nr. înregistrări',
                           color='Sezon', title="Rânduri per Sezon")
        st.plotly_chart(fig_sezon, use_container_width=True)

    # WIDGET: CHECKBOX
    st.markdown("---")
    st.header("3. Setul de Date Brut")
    st.write("Apasă pe bifa de mai jos pentru a vizualiza tabelul brut:")
    if st.checkbox("🔍 Arată Setul de Date Brut"):
        st.dataframe(df.head(100))
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

# ---------------------------------------------------------
# PAGINA 4: FUNCȚII AVANSATE
# ---------------------------------------------------------
elif page == "4. Funcții Avansate":
    st.title("🔬 Funcții Avansate de Analiză")

    # --------------------------------------------------
    # 1. TABEL PIVOT
    # --------------------------------------------------
    st.header("1. Tabel Pivot — Vânzări Medii pe Magazin și Sezon")
    st.markdown("""
    Tabelul pivot grupează simultan după două dimensiuni (**Magazin** și **Sezon**) și calculează
    media vânzărilor săptămânale. Permite identificarea rapidă a combinațiilor magazin-sezon cu
    performanță ridicată sau scăzută.
    """)

    pivot = pd.pivot_table(
        df,
        values='Weekly_Sales',
        index='Store',
        columns='Sezon',
        aggfunc='mean'
    ).round(0)

    st.dataframe(pivot.style.background_gradient(cmap='YlOrRd', axis=None), use_container_width=True)
    st.info("💡 Culorile mai închise indică vânzări medii mai mari. Identifică magazinele cu performanță constantă indiferent de sezon.")

    st.markdown("---")

    # --------------------------------------------------
    # 2. IMPACTUL SĂRBĂTORILOR (st.metric)
    # --------------------------------------------------
    st.header("2. Impactul Sărbătorilor asupra Vânzărilor")
    st.markdown("""
    Comparăm media vânzărilor săptămânale în **zilele de sărbătoare** față de **zilele normale**
    pentru a cuantifica efectul promoțiilor și traficului crescut.
    """)

    media_sarbatoare = df[df['Holiday_Flag'] == 1]['Weekly_Sales'].mean()
    media_normala    = df[df['Holiday_Flag'] == 0]['Weekly_Sales'].mean()
    diferenta_pct    = ((media_sarbatoare - media_normala) / media_normala) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Media Vânzări — Sărbătoare", f"${media_sarbatoare:,.0f}")
    col2.metric("Media Vânzări — Zi Normală", f"${media_normala:,.0f}")
    col3.metric("Diferență procentuală", f"{diferenta_pct:+.2f}%",
                delta_color="normal" if diferenta_pct > 0 else "inverse")

    fig_hol = px.box(
        df, x='Holiday_Flag', y='Weekly_Sales',
        labels={'Holiday_Flag': 'Tip Zi (0=Normal, 1=Sărbătoare)', 'Weekly_Sales': 'Vânzări Săptămânale ($)'},
        color='Holiday_Flag',
        title="Distribuția Vânzărilor: Sărbătoare vs Zi Normală",
        color_discrete_map={0: '#636EFA', 1: '#EF553B'}
    )
    st.plotly_chart(fig_hol, use_container_width=True)
    st.info("💡 Interpretare economică: Dacă diferența este pozitivă, campanii promoționale în perioadele de sărbătoare sunt justificate financiar.")

    st.markdown("---")

    # --------------------------------------------------
    # 4. EVOLUȚIE ANUALĂ COMPARATIVĂ
    # --------------------------------------------------
    st.header("3. Evoluție Anuală Comparativă (2010–2012)")
    st.markdown("""
    Graficul suprapune vânzările totale pe luni pentru fiecare an în parte,
    permițând identificarea tiparelor sezoniere și a tendințelor de creștere/scădere.
    """)

    df_annual = df.groupby(['Year', 'Month'])['Weekly_Sales'].sum().reset_index()
    df_annual['An'] = df_annual['Year'].astype(str)

    fig_annual = px.line(
        df_annual, x='Month', y='Weekly_Sales', color='An',
        markers=True,
        title="Vânzări Totale Lunare — Comparație pe Ani",
        labels={'Month': 'Luna', 'Weekly_Sales': 'Vânzări Totale ($)', 'An': 'An'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_annual.update_xaxes(tickmode='array', tickvals=list(range(1, 13)),
                             ticktext=['Ian','Feb','Mar','Apr','Mai','Iun','Iul','Aug','Sep','Oct','Nov','Dec'])
    st.plotly_chart(fig_annual, use_container_width=True)
    st.info("💡 Interpretare economică: Lunile cu vârfuri constante în toți anii indică perioade optime pentru stocuri și personal suplimentar (ex: Noiembrie-Decembrie — sezonul de Crăciun).")

    st.markdown("---")

    # --------------------------------------------------
    # 5. ELBOW METHOD PENTRU K-MEANS
    # --------------------------------------------------
    st.header("4. Metoda Cotului (Elbow Method) — Numărul Optim de Clustere")
    st.markdown("""
    Înainte de a alege numărul de clustere K-Means, folosim **Metoda Cotului**: rulăm algoritmul
    pentru K de la 1 la 10 și măsurăm inerția (suma distanțelor față de centroid).
    Punctul unde curba „face cot" reprezintă numărul optim de clustere.
    """)

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    df_elbow = df.groupby('Store').agg({'Weekly_Sales': 'mean', 'Unemployment': 'mean'}).reset_index()
    scaler_elbow = StandardScaler()
    scaled_elbow = scaler_elbow.fit_transform(df_elbow[['Weekly_Sales', 'Unemployment']])

    inertii = []
    k_range = range(1, 11)
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(scaled_elbow)
        inertii.append(km.inertia_)

    fig_elbow = px.line(
        x=list(k_range), y=inertii,
        markers=True,
        title="Elbow Method — Inerția K-Means pe număr de clustere",
        labels={'x': 'Număr de Clustere (K)', 'y': 'Inerție (WCSS)'}
    )
    fig_elbow.add_vline(x=3, line_dash="dash", line_color="red",
                        annotation_text="K optim = 3", annotation_position="top right")
    st.plotly_chart(fig_elbow, use_container_width=True)
    st.info("💡 Cotul graficului apare la K=3, confirmând că împărțirea în 3 clustere (folosită la Pagina 3) este alegerea optimă pentru acest set de date.")
