# Analiza Efectului de Amplificare în Tenis prin Simulare Monte Carlo 

Acest proiect implementează o simulare stocastică (Monte Carlo) pentru a prezice rezultatele meciurilor de tenis, analizând modul în care **Efectul de Amplificare** transformă micile avantaje statistice de la nivel de punct în victorii clare la nivel de meci.

## Descriere

Tenisul are un sistem de scor ierarhic și complex (Punct → Game → Set → Meci), ceea ce face dificilă calcularea analitică a probabilităților de victorie. Acest proiect rezolvă problema prin **Simulare Directă Monte Carlo**:

1.  Preia statistici reale ale jucătorilor (ATP) din fișiere CSV.
2.  Simulează mii de meciuri punct cu punct.
3.  Aplică **Inegalitatea Hoeffding** pentru a determina numărul necesar de simulări pentru o eroare controlată (< 1%).
4.  Generează vizualizări pentru Convergență, Amplificare (S-Curve) și Cote de Pariuri Fair.

## Funcționalități

* **Motor de Simulare Realist:** Respectă regulile ATP (Tie-break la 6-6, alternanța serviciului, avantaje).
* **Data-Driven:** Statistici specifice pe suprafețe (Hard, Clay, Grass) încărcate din `.csv`.
* **Analiză Matematică:**
    * **Convergența:** Demonstrează stabilitatea statistică a rezultatului (Legea Numerelor Mari).
    * **Amplificarea:** Vizualizează curba sigmoidă (S-Curve) specifică tenisului.
* **Output Comercial:** Calculează automat cotele "Fair" (Corecte) pe baza probabilităților simulate.

## Structura Proiectului

```text
├── date_tenis.csv       # Baza de date cu statistici (Nume, Suprafață, %Serve, %Retur)
├── main.py              # Scriptul principal de simulare
├── README.md            # Documentația proiectului
└── requirements.txt     # (Opțional) Lista de biblioteci necesare
```

## Fundament Teoretic

Proiectul se bazează pe ipoteza că un meci de tenis este o înlănțuire de evenimente Bernoulli.

**1. Estimatorul Monte Carlo:**
Probabilitatea estimată $\hat{p}$ după $N$ simulări este media aritmetică a rezultatelor $X_i$ (1=Victorie, 0=Înfrângere):
$$ \hat{p} = \frac{1}{N} \sum_{i=1}^{N} X_i $$

**2. Calibrarea (Hoeffding):**
Pentru a garanta o eroare $\epsilon = 0.01$ cu o încredere de 95% ($\alpha = 0.05$), numărul minim de simulări este calculat automat:
$$ N \ge \frac{\ln(2/\alpha)}{2\epsilon^2} $$

## Instalare și Utilizare

### 1. Clonare și Dependențe
Asigură-te că ai Python instalat. Instalează bibliotecile necesare:

```bash
pip install numpy matplotlib pandas
```

### 2. Configurarea Jucătorilor
Deschide fișierul `date_tenis.csv` și adaugă sau editează statisticile jucătorilor. Formatul este:

```csv
nume,suprafata,first_in,win_1st,win_2nd,ret_1st,ret_2nd
Jannik Sinner,Hard,0.64,0.78,0.56,0.32,0.54
...
```

### 3. Rulare
Editează liniile de configurare din `main.py` pentru a alege jucătorii:

```python
JUCATOR_A_NUME = "Jannik Sinner"
JUCATOR_B_NUME = "Carlos Alcaraz"
```

Apoi rulează scriptul:

```bash
python main.py
```

## Vizualizări Generate

Scriptul generează un dashboard complet cu 3 grafice:

1.  **Stânga-Sus (Convergența):** Arată cum probabilitatea se stabilizează pe măsură ce crește numărul de simulări.
2.  **Dreapta-Sus (Amplificarea):** Arată cât de mult crește șansa de victorie la meci pentru fiecare procent câștigat în plus la serviciu.
3.  **Jos (Rezultate):** Probabilitățile finale pe fiecare suprafață și cotele asociate.
