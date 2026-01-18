# 1. Introduction

## 1.1. Définir le périmètre de surveillance

Avant de choisir un outil, nous devons définir __quoi__ et __qui__ noous souhaitons surveiller :

- __Top Concurrents__ : Nous nous limitons aux 5-10 acteurs les plus agressifs ou directs (Pure players comme Amazon, ou enseignes physiques avec drive).
- __Segmentation produits__ : _KVI_ (_Known Value Items_) : Produits dont le client connaît le prix par coeur. Monitoring quotidien indispensable.
    - _Produits de fond de rayon_ : Monitoring hebdomadaire.
- __Localisation__ (Boutiques physiques) : Allez-vous surveiller les prix nationaux ou les spécificités locales (ex: via les sites de Drive ou de "Store Locator") ?

## 1.2. Choix de la méthode de collecte de données

Selon notre budget et nos ressources techniques, trois options s'offrent à nous :

| Méthodes | Avantages | Inconvénients |
|:---------|:----------|:--------------|
| __Logiciels SaaS (ex. : Paarly, PricingHub, Minderest))__ | Prêt à l'emploi, maintenance gérée par le prestataire, alertes automatiques. | Coût mensuel élevé, moins de flexibilité sur des sites très protégés. |
| __Solutions de Scraping (ex: Octoparse, Apify)__ | Plus économique, personnalisable. | Nécessite des compétences techniques pour gérer les blocages (Proxies, CAPTCHA). |
| __Développement interne (Python/Scrapy)__ | Contrôle total, intégration parfaite à ERP/PIM. | Coût de maintenance élevé (les sites web changent tout le temps). |

## 1.3. L'architecture du système

Pour que la donnée soit utile, elle doit suivre ce cycle :

- __Extraction__ : Récupération du prix, de la disponibilité (stock) et des frais de port.- __Matching (Le plus difficile)__ : Faire correspondre votre produit "A" avec le produit "B" du concurrent. L'utilisation des codes EAN/GTIN pour automatiser cela à 95%.
- __Analyse__ : Basée sur le calcul de l'indice de prix ($Indice = \frac{Prix_{Nous}}{Prix_{Concurrent}} \times 100$).
- __Action__ : Alerter les acheteurs ou modifier les prix automatiquement via un outil de __Dynamic Pricing__.

## 1.4. Les points de vigilance

- __Prix vs Frais de port__ : Un concurrent peut être moins cher sur le produit mais plus cher "livré". C'est la raison pour laquelle il faut toujours surveiller le prix total.
- __Promotions et Fidélité__ : Attention aux prix "carte membre" ou aux remises panier qui ne sont pas toujours visibles par les robots de scraping.
- __Légalité__ : Le scraping de données publiques est généralement autorisé, mais il faut veiller à ne pas surcharger les serveurs des concurrents (respect du fichier `robots.txt) pour éviter d'être banni.

### Recommandation pour démarrer

Il ne faut pas chercher à tout automatiser tout de suite. Il est préférable de commancer par un MVP (Produit Minimum Viable) :

1. Identifier les 100 produits les plus vendus.
2. Utiliser un outil simple de "Web Monitoring" pour suivre ces pages chez 3 concurrents.
3. Analyser les données dans un tableau de bord (type Looker Studio ou Power BI) pour voir si nos prix sont corrélés à nos ventes.

