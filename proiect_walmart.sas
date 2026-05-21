/* ====================================================================
   Proiect Pachete Software - Partea SAS
   Analiza Vânzărilor Walmart
==================================================================== */

/* 1. CREAREA UNUI SET DE DATE SAS DIN FIȘIERE EXTERNE (PROC IMPORT) */
/* Schimbă calea către locația exactă a fișierului tău dacă este nevoie */
PROC IMPORT DATAFILE="c:\Users\rebec\OneDrive\Desktop\PACHETE SOFTWARE\proiect\Walmart_Sales.csv"
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
