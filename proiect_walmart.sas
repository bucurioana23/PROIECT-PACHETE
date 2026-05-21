/* ====================================================================
   Proiect Pachete Software - Partea SAS
   Analiza Vânzărilor Walmart
==================================================================== */

/* 1. CREAREA UNUI SET DE DATE SAS DIN FIȘIERE EXTERNE (PROC IMPORT) */
PROC IMPORT DATAFILE="/home/u64485715/proiect_psw/Walmart_Sales.csv"
    OUT=WORK.walmart_brut
    DBMS=CSV
    REPLACE;
    GETNAMES=YES;
RUN;

/* 2. CREAREA ȘI FOLOSIREA DE FORMATE DEFINITE DE UTILIZATOR */
PROC FORMAT;
    VALUE hol_fmt 
        0 = 'Zi Normală'
        1 = 'Sărbătoare';
    VALUE temp_fmt 
        low - 50 = 'Frig'
        50 - 80 = 'Moderat'
        80 - high = 'Cald';
RUN;

/* 3. PROCESARE CONDIȚIONALĂ, FUNCȚII, MASIVE (ARRAYS) ȘI SUBSETURI */
DATA WORK.walmart_procesat;
    SET WORK.walmart_brut;
    
    /* Păstrăm doar primele 10 magazine pentru o analiză mai rapidă (Creare subset) */
    WHERE Store <= 10;
    
    /* Folosirea de funcții SAS: Rotunjim CPI și Șomajul la 2 zecimale */
    CPI = ROUND(CPI, 0.01);
    Unemployment = ROUND(Unemployment, 0.01);

    /* Procesare iterativă folosind MASIVE (ARRAY) */
    /* Vom crește prețul benzinei și șomajul cu 1% doar pentru o simulare de inflație */
    ARRAY factori_economici[*] Fuel_Price Unemployment;
    DO i = 1 TO DIM(factori_economici);
        factori_economici[i] = factori_economici[i] * 1.01;
    END;
    DROP i; /* Ștergem variabila contor */

    /* Procesare condițională (IF-THEN-ELSE) */
    LENGTH Performanta $15;
    IF Weekly_Sales > 1500000 THEN Performanta = 'Vânzări Mari';
    ELSE IF Weekly_Sales > 1000000 THEN Performanta = 'Vânzări Medii';
    ELSE Performanta = 'Vânzări Mici';

    /* Formatarea variabilelor */
    FORMAT Holiday_Flag hol_fmt. Temperature temp_fmt.;
RUN;

/* 4. PROCEDURI STATISTICE (PROC MEANS & PROC FREQ) */
TITLE "Statistici descriptive pentru Vânzări";
PROC MEANS DATA=WORK.walmart_procesat MIN MEAN MAX MAXDEC=2;
    VAR Weekly_Sales Temperature Fuel_Price;
    CLASS Store;
RUN;

TITLE "Frecvența sărbătorilor în setul de date";
PROC FREQ DATA=WORK.walmart_procesat;
    TABLES Holiday_Flag * Performanta / NOROW NOCOL NOPERCENT;
RUN;

/* 5. COMBINAREA SETURILOR DE DATE PRIN SQL */
/* Calculăm totalul vânzărilor pe magazin folosind PROC SQL */
PROC SQL;
    CREATE TABLE WORK.total_vanzari AS
    SELECT Store, 
           SUM(Weekly_Sales) AS Total_Incasari FORMAT=DOLLAR20.2,
           AVG(Unemployment) AS Somaj_Mediu
    FROM WORK.walmart_procesat
    GROUP BY Store
    ORDER BY Total_Incasari DESC;
QUIT;

/* 6. UTILIZAREA DE PROCEDURI PENTRU RAPORTARE (PROC REPORT) */
TITLE "Raport: Top Vânzări per Magazin";
PROC REPORT DATA=WORK.total_vanzari NOWD;
    COLUMNS Store Total_Incasari Somaj_Mediu;
    DEFINE Store / DISPLAY "Număr Magazin";
    DEFINE Total_Incasari / DISPLAY "Total Încasări ($)";
    DEFINE Somaj_Mediu / DISPLAY "Rata Șomajului (%)" FORMAT=8.2;
RUN;

/* 7. GENERAREA DE GRAFICE (PROC SGPLOT) */
TITLE "Evoluția vânzărilor în funcție de temperatură";
PROC SGPLOT DATA=WORK.walmart_procesat;
    VBOX Weekly_Sales / CATEGORY=Temperature;
    XAXIS LABEL="Temperatura de afară";
    YAXIS LABEL="Vânzări Săptămânale ($)";
RUN;

TITLE "Comparație Vânzări Sărbătoare vs Zi Normală";
PROC SGPLOT DATA=WORK.walmart_procesat;
    HBAR Holiday_Flag / RESPONSE=Weekly_Sales STAT=MEAN DATALABEL;
    XAXIS LABEL="Media Vânzărilor ($)";
    YAXIS LABEL="Tipul Zilei";
RUN;

TITLE; /* Curățăm titlurile la final */


/* 8. COMBINAREA SETURILOR DE DATE PRIN MERGE (DATA STEP) */
/* Creăm două seturi separate: statistici vânzări și indicatori economici */
PROC SQL;
    CREATE TABLE WORK.stats_vanzari AS
    SELECT Store,
           SUM(Weekly_Sales)  AS Total_Vanzari  FORMAT=DOLLAR20.2,
           AVG(Weekly_Sales)  AS Media_Vanzari  FORMAT=DOLLAR20.2,
           MAX(Weekly_Sales)  AS Max_Vanzari    FORMAT=DOLLAR20.2
    FROM WORK.walmart_procesat
    GROUP BY Store;

    CREATE TABLE WORK.stats_economici AS
    SELECT Store,
           AVG(Unemployment) AS Somaj_Mediu   FORMAT=8.2,
           AVG(Fuel_Price)   AS Benzina_Medie FORMAT=8.2,
           AVG(CPI)          AS CPI_Mediu     FORMAT=8.2
    FROM WORK.walmart_procesat
    GROUP BY Store;
QUIT;

/* Sortăm ambele seturi după Store înainte de MERGE */
PROC SORT DATA=WORK.stats_vanzari;    BY Store; RUN;
PROC SORT DATA=WORK.stats_economici;  BY Store; RUN;

/* MERGE prin DATA step — combină cele două seturi pe baza cheii Store */
DATA WORK.walmart_complet;
    MERGE WORK.stats_vanzari   (IN=a)
          WORK.stats_economici (IN=b);
    BY Store;
    IF a AND b; /* Păstrăm doar înregistrările prezente în ambele seturi */
RUN;

TITLE "Raport Complet: Vânzări + Indicatori Economici per Magazin";
PROC PRINT DATA=WORK.walmart_complet NOOBS;
    VAR Store Total_Vanzari Media_Vanzari Max_Vanzari Somaj_Mediu Benzina_Medie CPI_Mediu;
RUN;
TITLE;

/* 9. STATISTICI AVANSATE (PROC UNIVARIATE & PROC CORR) */
TITLE "Statistici avansate pentru Vânzările Săptămânale";
PROC UNIVARIATE DATA=WORK.walmart_procesat NORMAL PLOT;
    VAR Weekly_Sales;
    HISTOGRAM Weekly_Sales / NORMAL;
    INSET MEAN STD SKEWNESS KURTOSIS / POSITION=NE;
RUN;
TITLE;

TITLE "Matricea de Corelație — Factori care influențează Vânzările";
PROC CORR DATA=WORK.walmart_procesat PLOTS=MATRIX(HISTOGRAM);
    VAR Weekly_Sales Temperature Fuel_Price CPI Unemployment;
RUN;
TITLE;

/* 10. SAS ML — REGRESIE LINIARĂ (PROC REG) */
/* Modelăm impactul factorilor externi asupra vânzărilor săptămânale */
TITLE "SAS ML: Regresie Liniară — Factori care determină Vânzările";
PROC REG DATA=WORK.walmart_procesat PLOTS(MAXPOINTS=NONE)=DIAGNOSTICS;
    MODEL Weekly_Sales = Temperature Fuel_Price CPI Unemployment Holiday_Flag
          / STB COVB VIF;
    /* STB = coeficienți standardizați, VIF = verificare multicoliniaritate */
RUN;
QUIT;
TITLE;

/* 11. SAS ML — REGRESIE LOGISTICĂ (PROC LOGISTIC) */
/* Prezicere: va fi o săptămână cu vânzări MARI (1) sau MICI (0)? */
DATA WORK.walmart_ml;
    SET WORK.walmart_procesat;
    Media_Globala = 1200000; /* Pragul aproximativ pentru vânzări mari */
    IF Weekly_Sales > Media_Globala THEN Performanta_Flag = 1;
    ELSE Performanta_Flag = 0;
RUN;

TITLE "SAS ML: Regresie Logistică — Prezicerea Performanței Magazinului";
PROC LOGISTIC DATA=WORK.walmart_ml DESCENDING PLOTS(ONLY)=ROC;
    MODEL Performanta_Flag = Temperature Fuel_Price CPI Unemployment Holiday_Flag
          / SELECTION=STEPWISE SLENTRY=0.05 SLSTAY=0.05 LACKFIT RSQUARE;
RUN;
TITLE;

/* 12. SAS ML — CLUSTERING (PROC FASTCLUS — K-Means în SAS) */
/* Segmentarea magazinelor în 3 grupuri după vânzări și șomaj */
TITLE "SAS ML: Clusterizare K-Means (PROC FASTCLUS) — Segmentarea Magazinelor";
PROC FASTCLUS DATA=WORK.walmart_complet OUT=WORK.clustere MAXCLUSTERS=3 MAXITER=100;
    VAR Media_Vanzari Somaj_Mediu;
RUN;
TITLE;

TITLE "Raport Clustere — ce magazin a fost asignat în ce grup";
PROC REPORT DATA=WORK.clustere NOWD;
    COLUMNS Store Media_Vanzari Somaj_Mediu CLUSTER;
    DEFINE Store        / DISPLAY "Magazin";
    DEFINE Media_Vanzari / DISPLAY "Media Vânzări ($)" FORMAT=DOLLAR12.0;
    DEFINE Somaj_Mediu  / DISPLAY "Șomaj Mediu (%)";
    DEFINE CLUSTER      / DISPLAY "Cluster (Grup)";
RUN;
TITLE;
