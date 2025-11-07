# Compararea algoritmilor Beam Search și IDA* pentru Sokoban

## 🧩 Descriere
Acest proiect implementează și compară doi algoritmi de căutare (Beam Search și IDA*) pentru rezolvarea jocului **Sokoban**, în varianta standard **push-only**. Proiectul explorează impactul diferitelor euristici asupra eficienței și complexității algoritmilor.

- **Beam Search:** folosește o euristică bazată pe distanța Manhattan, matching greedy între cutii și ținte, și detectarea deadlock-urilor.
- **IDA***: folosește o adaptare globală a matching-ului greedy și penalizează deadlock-urile, incluzând costul deplasării jucătorului.

Toate mișcările de „pull” sunt dezactivate pentru a respecta specificația standard a jocului.

---

## 🔍 Structura proiectului
- `src/` – codul sursă Python pentru implementarea algoritmilor.
- `maps/` – hărți Sokoban utilizate pentru testare.
- `results/` – grafice și statistici despre numărul de stări explorate și timpul de execuție.
- `README.md` – documentația proiectului.

---

## 🔧 Detalii implementare

### Restricții
- Jocul este în varianta **push-only** (nu sunt permise mișcări de „pull”).
- Funcția `is_valid_move` din clasa `Map` blochează mișcările nepermise.

### Beam Search
- Euristică:
  - Distanța Manhattan între cutii și ținte.
  - Matching greedy: fiecare cutie este asociată celei mai apropiate ținte libere.
  - Detectarea deadlock-urilor: penalizare mare pentru colțuri, penalizare moderată pentru blocaje parțiale.
  - Se include jumătate din distanța minimă jucător–cutie.
- Observații:
  - Pe hărți complexe, numărul de stări crește semnificativ.
  - Operările cu `heapq.nsmallest` cresc costul de calcul la niveluri mari.

### IDA*
- Euristică:
  - Matching global greedy: cel mai apropiat cuplu cutie–țintă la fiecare pas.
  - Penalizarea deadlock-urilor: 300 de puncte.
  - Include întreaga distanță minimă jucător–cutie.
- Observații:
  - Primele versiuni bazate pe distanța Euclidiană au explorat prea multe stări redundante.
  - Utilizarea Manhattan + matching + deadlock reduce semnificativ timpul de execuție.

---

## Rezultate
- Graficele afișează timpul de execuție și numărul total de stări explorate pentru fiecare hartă.
- Beam Search tinde să exploreze mai multe stări pe hărți complexe, dar poate găsi soluții rapid datorită euristicii optimizate.
- IDA* poate fi mai lent, dar explorează stări într-un mod DFS iterativ, păstrând complexitatea controlată.

---

## 🎯 Observații și concluzii
- Alegerea unei euristici eficiente (Manhattan + matching + deadlock) reduce drastic numărul de stări explorate și timpul de execuție.
- Beam Search este sensibil la lățimea beam-ului și numărul de succesori generați.
- IDA* necesită euristici bine calibrate pentru a evita explorarea excesivă a stărilor redundante.
- Viitoare îmbunătățiri: implementarea unei euristici mai bune pentru hărți mai complexe.

---

