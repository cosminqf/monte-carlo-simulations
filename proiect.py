import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(script_dir, 'date_tenis.csv')

JUCATOR_A_NUME = "John Isner" 
JUCATOR_B_NUME = "Guillermo Coria"

EPSILON = 0.01
ALPHA = 0.05
N_CALCULAT = int(math.log(2/ALPHA) / (2 * EPSILON**2))
N_SIMS = max(N_CALCULAT, 10000)
SUPRAFETE_KEYS = ["Hard", "Clay", "Grass"]

def incarca_date_jucator(nume_jucator, df):
    df_jucator = df[df['nume'] == nume_jucator]
    if df_jucator.empty:
        raise ValueError(f"Jucatorul {nume_jucator} nu a fost gasit in CSV.")
    stats = {}
    for index, row in df_jucator.iterrows():
        surf = row['suprafata']
        stats[surf] = {
            "first_in": row['first_in'], "win_1st": row['win_1st'],
            "win_2nd": row['win_2nd'], "ret_1st": row['ret_1st'], "ret_2nd": row['ret_2nd']
        }
    return {"nume": nume_jucator, **stats}

def calculeaza_prob_punct(server, receiver, suprafata):
    if suprafata not in server or suprafata not in receiver: return 0.5 
    srv = server[suprafata]
    rcv = receiver[suprafata]
    p_win_1st = (srv["win_1st"] + (1.0 - rcv["ret_1st"])) / 2
    p_win_2nd = (srv["win_2nd"] + (1.0 - rcv["ret_2nd"])) / 2
    return (srv["first_in"] * p_win_1st) + ((1.0 - srv["first_in"]) * p_win_2nd)

def sim_game(p):
    srv, rcv = 0, 0
    while True:
        if np.random.random() < p: srv += 1
        else: rcv += 1
        if srv >= 4 and srv >= rcv + 2: return 1
        if rcv >= 4 and rcv >= srv + 2: return 0

def sim_tiebreak(p_A, p_B, start_A):
    pts_A, pts_B = 0, 0
    curr_A = start_A 
    
    while True:
        prob = p_A if curr_A else p_B
        if np.random.random() < prob:
            if curr_A: pts_A += 1 
            else: pts_B += 1      
        else:
            if curr_A: pts_B += 1 
            else: pts_A += 1     
            
        if pts_A >= 7 and pts_A >= pts_B + 2: return 1
        if pts_B >= 7 and pts_B >= pts_A + 2: return 0
        
        if (pts_A + pts_B) % 2 == 1:
            curr_A = not curr_A

def sim_set(p_A, p_B, start_A):
    g_A, g_B = 0, 0
    curr_A = start_A
    while True:
        if g_A == 6 and g_B == 6: return sim_tiebreak(p_A, p_B, curr_A)
        prob = p_A if curr_A else p_B
        if sim_game(prob):
            if curr_A: g_A += 1
            else: g_B += 1
        else:
            if curr_A: g_B += 1
            else: g_A += 1
        curr_A = not curr_A
        if g_A >= 6 and g_A >= g_B + 2: return 1
        if g_B >= 6 and g_B >= g_A + 2: return 0
        if g_A == 7 and g_B == 5: return 1
        if g_B == 7 and g_A == 5: return 0

def sim_meci(p_A, p_B):
    sets_A, sets_B = 0, 0
    curr_A = np.random.random() < 0.5
    while sets_A < 2 and sets_B < 2:
        if sim_set(p_A, p_B, curr_A): sets_A += 1
        else: sets_B += 1
        curr_A = not curr_A
    return 1 if sets_A > sets_B else 0

try:
    df = pd.read_csv(FILE_PATH)
    JUCATOR_A = incarca_date_jucator(JUCATOR_A_NUME, df)
    JUCATOR_B = incarca_date_jucator(JUCATOR_B_NUME, df)
    print(f"Start simulare: {JUCATOR_A_NUME} vs {JUCATOR_B_NUME}")
except Exception as e:
    print(f"Eroare: {e}")
    exit()

plt.figure(figsize=(15, 10)) 
plt.suptitle(f"Dashboard Monte Carlo: {JUCATOR_A_NUME} vs {JUCATOR_B_NUME}", fontsize=16)

plt.subplot(2, 2, 1)
conv_res = []
wins = 0
p_conv_A = calculeaza_prob_punct(JUCATOR_A, JUCATOR_B, "Hard")
p_conv_B = calculeaza_prob_punct(JUCATOR_B, JUCATOR_A, "Hard")

for i in range(1, 3001):
    if sim_meci(p_conv_A, p_conv_B): wins += 1
    conv_res.append(wins/i)

plt.plot(conv_res, color='green')
plt.axhline(conv_res[-1], linestyle='--', color='red', label=f'Estimat: {conv_res[-1]:.3f}')
plt.title("Stabilizarea Probabilitatii (Convergenta)")
plt.xlabel("Nr. Simulari")
plt.ylabel("Probabilitate Victorie")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
x_vals = np.linspace(0.55, 0.75, 15)
y_vals = []
opponent_p_avg = 0.65 

for p in x_vals:
    local_wins = sum([sim_meci(p, opponent_p_avg) for _ in range(500)])
    y_vals.append(local_wins/500)

plt.plot(x_vals, y_vals, 'b-o')
plt.axvline(opponent_p_avg, color='k', linestyle='--', label="Adversar (Fix 0.65)")
plt.axhline(0.5, color='gray', linestyle=':')
plt.title("Amplificarea: Cat conteaza fiecare punct in plus")
plt.xlabel("Probabilitate Castig Punct (Serva)")
plt.ylabel("Probabilitate Castig Meci")
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
labels = []
win_probs = []
errors = []

for surf in SUPRAFETE_KEYS:
    p_A = calculeaza_prob_punct(JUCATOR_A, JUCATOR_B, surf)
    p_B = calculeaza_prob_punct(JUCATOR_B, JUCATOR_A, surf)
    
    wins_A = sum([sim_meci(p_A, p_B) for _ in range(N_SIMS)])
    prob = wins_A / N_SIMS
    
    stderr = math.sqrt(prob * (1 - prob) / N_SIMS)
    margin = 1.96 * stderr
    
    labels.append(surf)
    win_probs.append(prob)
    errors.append(margin)
    
    cota = 1/prob if prob > 0 else 0
    print(f"[{surf}] Win {JUCATOR_A_NUME}: {prob:.2%} (Cota: {cota:.2f})")

colors = ['#3498db', '#e74c3c', '#2ecc71']
bars = plt.bar(labels, win_probs, yerr=errors, capsize=10, color=colors, alpha=0.9, edgecolor='black')

plt.axhline(0.5, color='black', linestyle='--')
plt.title(f"Probabilitati Finale & Cote Fair: {JUCATOR_A_NUME}", fontsize=14)
plt.ylabel("Probabilitate Victorie")
plt.ylim(0, 1.15)

for bar in bars:
    yval = bar.get_height()
    cota_afisata = 1 / yval if yval > 0 else 0
    
    plt.text(
        bar.get_x() + bar.get_width()/2, 
        yval + 0.05, 
        f"{yval:.1%}\n(Cota: {cota_afisata:.2f})", 
        ha='center', va='bottom', fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2)
    )

plt.tight_layout()
plt.show()