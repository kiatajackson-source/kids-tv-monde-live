import json
import urllib.request
from pathlib import Path

BASE = "https://iptv-org.github.io/iptv/categories/"
CATEGORIES = {
    "kids": "Kids",
    "education": "Éducation",
    "music": "Musique",
    "news": "Actualités",
    "documentary": "Documentaires",
}

catalogue = []
vus = set()

for fichier, categorie in CATEGORIES.items():
    url = BASE + fichier + ".m3u"
    print("Récupération :", categorie)

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "KidsTVMondeLive/1.0"}
        )
        with urllib.request.urlopen(req, timeout=25) as reponse:
            texte = reponse.read().decode("utf-8", "replace")

        nom = ""
        pays = "International"

        for ligne in texte.splitlines():
            ligne = ligne.strip()

            if ligne.startswith("#EXTINF:"):
                nom = ligne.rsplit(",", 1)[-1].strip()
            elif ligne.startswith("http") and nom:
                flux = ligne
                nom_cle = nom.lower()

                if flux not in vus:
                    vus.add(flux)
                    catalogue.append({
                        "nom": nom,
                        "pays": pays,
                        "categorie": categorie,
                        "url": flux,
                        "type": "flux_public_a_verifier"
                    })
                nom = ""

        print("  Entrées récupérées :", len(catalogue))

    except Exception as erreur:
        print("  Liste indisponible :", erreur)

# Conserver RTNC comme entrée à configurer.
catalogue.append({
    "nom": "RTNC",
    "pays": "République démocratique du Congo",
    "categorie": "Actualités",
    "url": "",
    "type": "flux_officiel_a_configurer"
})

Path("chaines.json").write_text(
    json.dumps(catalogue, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nImportation terminée.")
print("Nombre total de chaînes :", len(catalogue))
print("Fichier créé : chaines.json")
print("Les flux doivent encore être testés et leurs droits vérifiés.")
