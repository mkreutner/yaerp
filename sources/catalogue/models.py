from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.postgres.fields import JSONField # Pour les sélecteurs complexes

class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    ean = models.CharField(max_length=13, unique=True, db_index=True)
    id_interne = models.CharField(max_length=50, unique=True, db_index=True)
    nom = models.CharField(max_length=255)
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name="produits")
    
    # Données Internes
    url_interne = models.URLField(max_length=500)
    url_image_interne = models.URLField(max_length=500, blank=True, null=True)
    stock_interne = models.IntegerField(default=0)
    
    # Utilisation de MoneyField pour la précision financière
    prix_achat_ht = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    prix_vente_ht = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')

    def __str__(self):
        return f"{self.ean} - {self.nom}"

class Concurrent(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    url_accueil = models.URLField()
    
    # Stratégie de scraping
    utiliser_json_ld = models.BooleanField(default=True)
    
    # Sélecteurs stockés en JSON (ex: {"prix_ttc": ".price", "stock_status": "#in-stock"})
    # PostgreSQL permet de requêter directement dans ce champ
    selecteurs_config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.nom

class LiaisonProduitConcurrent(models.Model):
    """Lien entre ton produit et la page spécifique chez le concurrent"""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="liens_concurrents")
    concurrent = models.ForeignKey(Concurrent, on_delete=models.CASCADE)
    url_produit_concurrent = models.URLField(max_length=500)
    actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ('produit', 'concurrent')

class HistoriqueScan(models.Model):
    """Le résultat d'un passage du robot"""
    liaison = models.ForeignKey(LiaisonProduitConcurrent, on_delete=models.CASCADE, related_name="historique")
    date_scan = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Données extraites
    prix_ht = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', null=True)
    prix_ttc = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', null=True)
    en_promotion = models.BooleanField(default=False)
    stock_disponible = models.BooleanField(default=True)
    frais_livraison = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR', null=True)
    delai_livraison = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadata pour debug
    status_code = models.IntegerField(null=True) # Ex: 200, 404, 503

    class Meta:
        ordering = ['-date_scan']