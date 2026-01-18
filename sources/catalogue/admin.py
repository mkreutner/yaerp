from django.contrib import admin
from django.utils.html import format_html
from .models import Marque, Produit, Concurrent, LiaisonProduitConcurrent, HistoriqueScan

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ('ean_display', 'nom', 'marque', 'prix_achat_ht', 'prix_vente_ht', 'get_lowest_competitor')
    # Filtres latéraux (crucial pour 20k produits)
    list_filter = ('marque', 'stock_interne')
    # Recherche rapide
    search_fields = ('ean', 'nom', 'id_interne')
    # Optimisation SQL pour les ForeignKeys
    list_select_related = ('marque',)

    def ean_display(self, obj):
        return format_html("<b>{}</b>", obj.ean)
    ean_display.short_description = "EAN"

    def get_lowest_competitor(self, obj):
        """Affiche le prix le plus bas trouvé chez les concurrents"""
        # On cherche le dernier scan le moins cher pour ce produit
        last_scans = HistoriqueScan.objects.filter(
            liaison__produit=obj
        ).order_by('prix_ttc')
        
        if last_scans.exists():
            scan = last_scans.first()
            return f"{scan.prix_ttc} ({scan.liaison.concurrent.nom})"
        return "-"
    get_lowest_competitor.short_description = "Prix Min Concurrent"

@admin.register(Concurrent)
class ConcurrentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'url_accueil', 'utiliser_json_ld')
    # Permet de modifier la checkbox directement dans la liste
    list_editable = ('utiliser_json_ld',)

@admin.register(LiaisonProduitConcurrent)
class LiaisonAdmin(admin.ModelAdmin):
    list_display = ('produit', 'concurrent', 'actif')
    list_filter = ('concurrent', 'actif')
    search_fields = ('produit__nom', 'produit__ean')
    # Pour ne pas charger 20 000 produits dans un menu déroulant (crash RAM)
    autocomplete_fields = ['produit'] 

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'afficher_logo')

    def afficher_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 45px; height: auto;" />', obj.logo.url)
        return "Pas de logo"
    afficher_logo.short_description = 'Logo'

admin.site.register(HistoriqueScan)