Acest proiect pentru seminarul de **Pachete Software** (anul III, CSIE) este o lucrare de sinteză care îți cere să demonstrezi că știi să folosești două tehnologii diferite pentru a analiza activitatea unei organizații: **SAS** (pentru procesare stabilă și raportare statistică) și **Python/Streamlit** (pentru interfață interactivă și Machine Learning).

Iată un ghid pas cu pas pentru a structura acest proiect, bazat pe cerințele oficiale și pe modelul Rossmann analizat în PDF-ul tău.

### ---

**Pasul 1: Alegerea Setului de Date**

Nu poți începe fără date. Ai nevoie de un set de date de tip **Business/Organizație** (vânzări, resurse umane, marketing, producție).

* **Unde cauți?** Cel mai bun loc este [Kaggle.com](https://www.kaggle.com).  
* **Ce fel de date?** Caută seturi de date care au:  
  * Cel puțin o variabilă temporală (Ex: *Date*) – pentru trenduri.  
  * Variabile categorice (Ex: *StoreType, Category, Region*) – pentru grupări.  
  * Variabile numerice (Ex: *Sales, Profit, Quantity, Temperature*) – pentru statistici și regresie.  
* **Exemple de teme:** Vânzări de retail (ca în modelul Rossmann), performanța angajaților (HR), analiza unui lanț de restaurante sau date bursiere.

### ---

**Pasul 2: Înțelegerea Structurii Proiectului**

Proiectul tău final trebuie să fie un document **PDF** (scris în Word) care să conțină pentru fiecare funcționalitate implementată:

1. **Definirea problemei** (ex: "Vrem să vedem distribuția vânzărilor pe regiuni").  
2. **Informații necesare** (ce coloane din tabel folosești).  
3. **Metode de calcul** (formule, algoritmi de tip regresie/clusterizare).  
4. **Rezultate** (screenshot-uri din SAS și Streamlit).  
5. **Interpretare economică** (ce înseamnă cifrele alea pentru afacere).

### ---

**Pasul 3: Implementarea în SAS (Minim 8 facilități)**

Folosește SAS pentru "partea grea" de procesare și raportare statistică oficială. Din fișierul de cerințe și model, ar trebui să incluzi:

* **Import:** PROC IMPORT pentru fișierele CSV.

* **Formate:** Crearea de formate proprii cu PROC FORMAT (ex: transformarea codului '1' în 'Promoție').

* **Procesare:** Utilizarea de DATA steps cu IF/THEN și ARRAYS pentru a crea variabile noi (ex: flag pentru vânzări mari).

* **Statistici:** PROC MEANS pentru medii, min/max și PROC FREQ pentru tabele de frecvență.

* **Raportare:** PROC REPORT sau PROC PRINT pentru a genera liste curate de date.

* **Grafice:** PROC SGPLOT pentru grafice de tip serie temporală sau boxplot.

### ---

**Pasul 4: Implementarea în Python/Streamlit (Minim 8 facilități)**

Aici creezi aplicația web interactivă. Modelul tău arată o aplicație organizată pe pagini. Trebuie să incluzi:

* **Metode Streamlit:** Coloane (st.columns), formulare (st.form), metrici (st.metric) și meniuri de navigare.

* **Prelucrare Pandas:** Gruparea și agregarea datelor (ex: df.groupby('Region').sales.sum()).  
* **Data Cleaning:** Tratarea valorilor lipsă (fillna) sau scalarea datelor cu StandardScaler.

* **Reprezentări grafice:** Folosește Plotly pentru grafice interactive (Histogram, Heatmap, Scatter Plot).

* **Scikit-learn:** \* **Clusterizare:** K-Means pentru a grupa clienții sau magazinele (cu un slider pentru numărul de clustere).

  * **Regresie Logistică:** Pentru a prezice o categorie (ex: va fi o zi cu vânzări mari? Da/Nu).

* **Statmodels:** Regresie multiplă pentru a vedea impactul factorilor asupra profitului/vânzărilor.

### ---

**Pasul 5: Concluziile și Interpretarea Economică**

Nu uita că acesta este un proiect pentru o facultate de profil economic. Profesorul vrea să vadă ce decizii iei pe baza datelor.

* **Exemplu:** "Deoarece corelația dintre numărul de clienți și vânzări este de 0.89, recomandăm campanii de marketing pentru creșterea traficului în magazine".

* **Exemplu:** "Clusterul 2 de magazine are distanța cea mai mare față de competitori, deci acolo putem mări prețurile fără a pierde clienți".

### ---

**Ce trebuie să predai?**

1. **Documentul PDF** (cu toate explicațiile și screenshot-urile).  
2. **O arhivă** care să conțină:  
   * Codul Python (.py sau .ipynb).  
   * Codul SAS (.sas).  
   * Setul de date utilizat.

**Sfat de început:** Descarcă acum un set de date de pe Kaggle și încearcă să faci primul PROC IMPORT în SAS și primul st.title în Streamlit. Pe care dintre cele două vrei să o atacăm prima dată cu un cod concret?