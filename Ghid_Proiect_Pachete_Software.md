# Ghid Pas cu Pas: Proiect Pachete Software (SAS & Python)

Acest document reprezintă planul tău de bătaie pentru realizarea proiectului la disciplina Pachete Software. Proiectul constă în analizarea datelor unei organizații/companii folosind două limbaje de programare: **Python (cu interfață în Streamlit)** și **SAS**. 

Miza principală este să demonstrezi că știi să folosești instrumentele tehnice, dar și să oferi **interpretări economice** (ce înseamnă cifrele obținute pentru afacere).

---

## Faza 1: Alegerea Setului de Date (Dataset)

Acesta este cel mai important pas. Fără date bune, nu poți aplica toate funcționalitățile cerute (regresie, clusterizare, etc.).

### De unde iei datele?
Cea mai bună platformă pentru a găsi date este **[Kaggle](https://www.kaggle.com/datasets)**. Este gratuit, iar seturile de date vin de obicei în format `.csv`, perfect pentru Python și SAS.

### Ce trebuie să conțină setul de date ideal?
Pentru a putea îndeplini cerințele de nota 10, alege un tabel cu măcar 1000 de rânduri și următoarele tipuri de coloane:
1. **Coloane numerice continue** (ex: *Vânzări, Profit, Preț, Vârstă, Salariu*) - necesare pentru regresie, statistici, clusterizare.
2. **Coloane categorice / text** (ex: *Categorie Produs, Gen, Departament, Țară, Regiune*) - necesare pentru grupări și agregări.
3. **Coloană de timp / dată** (ex: *Data Vânzării, Data Angajării*) - necesară pentru a urmări evoluția în timp.

### Exemple de teme de proiect și seturi de date:
1. **Analiza Vânzărilor unui Lanț de Magazine (Recomandat)**
   * *Exemplu:* Walmart Sales, Superstore Sales.
   * *Ce poți analiza:* Cum variază vânzările în funcție de regiune? Cât influențează promoțiile profitul? Prezicerea vânzărilor viitoare.
2. **Resurse Umane (HR) și Angajați**
   * *Exemplu:* IBM HR Analytics Employee Attrition.
   * *Ce poți analiza:* De ce pleacă angajații din firmă? Există o legătură între salariu, vechime și performanță? Clusterizarea angajaților pe departamente.
3. **Marketing și Comportamentul Clienților**
   * *Exemplu:* Mall Customer Segmentation, Bank Marketing Campaign.
   * *Ce poți analiza:* Crearea de profiluri de clienți (clustere). Cine răspunde cel mai bine la campaniile de marketing?

---

## Faza 2: Partea de Python & Streamlit

Aici vom construi o aplicație web interactivă. Vom crea un fișier de tip `app.py` pe care îl vom rula local.

**Bife de atins (minim 8):**
- [ ] Crearea interfeței (titluri, texte, grafice) folosind metode Streamlit (`st.title`, `st.plotly_chart`, etc.).
- [ ] Curățarea datelor: tratarea valorilor lipsă (`fillna` sau `dropna`) sau eliminarea extremelor (outliers).
- [ ] Codificarea datelor: transformarea datelor de tip text în numere (pentru algoritmii de Machine Learning) prin _LabelEncoding_ sau _OneHotEncoding_.
- [ ] Scalarea datelor (ex: _StandardScaler_ sau _MinMaxScaler_ din `scikit-learn`).
- [ ] Grupări și agregări de date folosind Pandas (`groupby`, `sum`, `mean`).
- [ ] Utilizare de funcții de grup și pivotări.
- [ ] **Clusterizare**: Gruparea datelor (ex. K-Means) folosind `scikit-learn` pentru a vedea tipologii de clienți/produse.
- [ ] **Regresie (simplă/multiplă/logistică)**: Folosind `statsmodels` sau `scikit-learn` pentru a prezice anumite rezultate (ex: prețul, probabilitatea de a cumpăra).

---

## Faza 3: Partea de SAS

Aici vom folosi mediul SAS pentru a scrie cod și a genera rapoarte și grafice statistice clasice.

**Bife de atins (minim 8):**
- [ ] Importul fișierului CSV (`PROC IMPORT`).
- [ ] Crearea de formate personalizate (`PROC FORMAT` - ex: transformarea valorii "F" în "Femei" la afișare).
- [ ] Crearea de subseturi de date (filtrare cu `WHERE`) și procesare iterativă/condițională (`IF-THEN-ELSE`).
- [ ] Folosirea masivelor (`ARRAY`) sau a funcțiilor SAS specifice (ex. funcții de string, date calendaristice).
- [ ] Combinarea seturilor de date (`MERGE` sau `PROC SQL`).
- [ ] Raportare pe tabele (`PROC REPORT`, `PROC PRINT`, `PROC FREQ`).
- [ ] Statistici descriptive (`PROC MEANS`, `PROC UNIVARIATE`).
- [ ] Generarea de grafice (`PROC SGPLOT` - histograme, grafice de dispersie, bar chart).

---

## Faza 4: Redactarea Documentului Final (Word/PDF)

Proiectul nu se rezumă doar la cod. Trebuie redactat un fișier Word (salvat PDF) care să conțină structurat fiecare pas pe care l-ai făcut:
* **Definirea problemei:** Ce ai vrut să afli sau să demonstrezi cu bucata respectivă de cod?
* **Informații necesare:** Ce variabile / coloane ai folosit?
* **Metode utilizate:** Ce procedură SAS sau algoritm Python ai rulat?
* **Prezentarea rezultatelor:** Screenshot cu tabelul / graficul / aplicația Streamlit.
* **Interpretare economică (CEL MAI IMPORTANT):** Ce decizie ar lua un manager văzând acele rezultate? (Ex: "Vânzările scad mereu marțea, sugerăm lansarea unor oferte speciale marțea").

---

## Cum procedăm mai departe?

1. Te decizi asupra domeniului care ți se pare cel mai interesant (Vânzări, HR, Marketing, Financiar).
2. Căutăm împreună un set de date pe Kaggle, îl descărcăm și îl punem în folder.
3. Începem cu **Python și Streamlit**: curățăm datele, facem niște grafice de bază și ne asigurăm că aplicația merge.
4. Adăugăm partea de **Machine Learning** în Python (Regresie, Clusterizare).
5. Ne mutăm în **SAS** și scriem codul pentru rapoarte și statistici.
6. La final, extragem graficele și concluziile în documentul PDF.
