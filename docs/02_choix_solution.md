# 2. Choix de la solution

Nous partons pour construire une solution "maison" avec peu de budget, tout en garantissant la confidentialité totale de nos données commerciales.

Pour un développement interne (probablement en Python, qui est la référence pour ce sujet), l'enjeu n'est pas seulement de récupérer le prix, mais de maintenir le système en vie, car les sites concurrents changent de structure régulièrement.

Voici l'architecture technique que nous pourions mettre en place :

## 2.1. Architecture technique du "Price Bot"

Pour que le système soit efficace, nous devons séparer la collecte de l'analyse.

### 2.1.1 Le moteur de scraping (Collecte)

- __Langage__ : Python avec les bibliothèques Playwright ou Selenium (pour simuler un vrai navigateur et contourner les protections JavaScript).
- __Rotation d'IP__ : C'est le seul poste de dépense inévitable. Si nous scrappons trop souvent avec la même IP, nous serons banni. Nous pouvons nous orienter vers un service de proxies résidentiels.
- __User-Agents__ : Changer régulièrement l'identité du navigateur (Chrome, Firefox, Safari, Mobile) dans le code pour ne pas être repéré comme un robot.

### 2.1.2. Le module de "Matching" (Intelligence)

C'est ici que le projet réussit ou échoue. Si nous n'avons pas de codes __EAN__ communs :

- Utiliser la recherche par mot-clé sur le site concurrent.
- Implémenter un algorithme de similarité de texte (comme la distance de Levenshtein) pour comparer nos titres de produits avec les leurs.

### 2.1.3. Le stockage (Base de données)

Nous utiliserons une base de données simple comme PostgreSQL. Nous deveons stocker à minimum :

- L'__ID__ produit interne.
- L'__URL__ du concurrent.
- Le __prix__ capturé.
- Le "__Timestamp__" (date et heure précise).

## 2.2. Organisation des données pour la décision

Une fois les données en base, ne pas pass afficher le données "brutes" aux équipes. 
Nous créerons un tableau de bord (via Streamlit en Python ou un simple Excel automatisé) avec ces indicateurs clés :

- __L'Indice de Compétitivité__ : $$IC = \frac{\text{Votre Prix}}{\text{Prix Moyen Concurrent}} \times 100$$
   - Si `IC > 100` : Nous sommes plus cher.
   - Si `IC < 100` : Nous sommes moins cher.
- __Alerte de rupture__ : Si le concurrent est moins cher mais __hors stock__, nous n'avons pas besoin de baisser notre prix. C'est une opportunité de marge.

## 2.3. Les "Pièges" du développement interne

- __Le Shadow Ban__ : Le concurrent nous affiche des prix erronés ou des stocks fictifs s'il détecte notre robot.
- __Le changement de structure HTML__ : Un bouton qui change de nom ou de place et votre script s'arrête. Il faut prévoir un système d'alertes (par email ou Slack) pour savoir quand un script "__casse__".
- __Le coût humain__ : Il faut bien comprendre que "__gratuit en outils__" ne veut pas dire "__gratuit en temps__". La maintenance prendra environ 10 à 20% du temps d'un développeur.

