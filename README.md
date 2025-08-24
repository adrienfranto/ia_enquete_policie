# Système d'Enquête Policière - PROLOG

Par : 

    ARSON Gype Elyse (1537H-F M1 IG Gr2)

    RAZAFINDRATOVO Adrien Franto (1555H-F M1 IG Gr2) 

    KALOU Nick Hardi Hervé



## 🛠 Installation

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Lancer l'application** :
```bash
python app.py
```

3. **Ouvrir le navigateur** :
```
http://localhost:5000
```

## 📁 Structure du Projet

```
prolog-investigation/
├── app.py                 # Backend Flask
├── investigation.pl       # Code PROLOG pur
├── requirements.txt       # Dépendances Python
├── templates/
│   └── index.html        # Interface web
└── README.md             # Documentation
```


### Interface Web
1. Sélectionner un suspect dans la liste déroulante
2. Choisir un type de crime
3. Cliquer sur "Analyser" pour voir le verdict
4. Utiliser "Voir tous les coupables" pour une vue d'ensemble

### Code PROLOG Direct
```prolog
?- is_guilty(john, vol).
true.

?- is_guilty(mary, assassinat).
true.

?- guilty_suspects(escroquerie, Suspects).
Suspects = [alice, sophie].
```

