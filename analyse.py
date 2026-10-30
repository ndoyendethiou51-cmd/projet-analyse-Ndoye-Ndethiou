import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path

# Création du dossier figures s'il n'existe pas
FIG_DIR = Path('figures')
FIG_DIR.mkdir(exist_ok=True)

def charger_et_nettoyer():
    print("Chargement et nettoyage des données...")
    df = pd.read_csv("data/logs_reseau.csv")
    
    # 1. Doublons
    df = df.drop_duplicates()
    
    # 2. Protocole en majuscules
    df['protocol'] = df['protocol'].str.upper()
    
    # 3. Médiane bytes_sent (après doublons)
    mediane = df['bytes_sent'].median()
    df['bytes_sent'] = df['bytes_sent'].fillna(mediane)
    
    # Conversion timestamp pour les graphiques
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def calculer_resultats(df):
    print("Calcul des résultats...")
    resultats = {
        "nb_connexions_total": int(len(df)),
        "top_port_destination": int(df["dst_port"].value_counts().idxmax()),
        "repartition_actions": df["action"].value_counts().to_dict(),
        "type_appareil_le_plus_actif": str(df["device_type"].value_counts().idxmax()),
        "ip_source_la_plus_bloquee": str(df[df["action"] == "DENY"]["src_ip"].value_counts().idxmax())
    }
    
    with open("resultats.json", "w", encoding="utf-8") as f:
        json.dump(resultats, f, indent=4, ensure_ascii=False)
    print("✅ resultats.json créé.")

def generer_figures(df):
    print("Génération des figures...")
    
    # Figure 1
    plt.figure(figsize=(10, 5))
    df['dst_port'].value_counts().head(10).plot(kind='bar', color='skyblue')
    plt.title('Top 10 des ports de destination')
    plt.xlabel('Port'); plt.ylabel('Nombre de connexions'); plt.xticks(rotation=0)
    plt.tight_layout(); plt.savefig(FIG_DIR / 'top_ports.png'); plt.close()

    # Figure 2
    plt.figure(figsize=(6, 6))
    df['action'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title('Répartition des actions (ALLOW / DENY)'); plt.ylabel('')
    plt.tight_layout(); plt.savefig(FIG_DIR / 'allow_deny.png'); plt.close()

    # Figure 3
    plt.figure(figsize=(8, 5))
    df.groupby('device_type')['bytes_sent'].sum().sort_values().plot(kind='barh', color='salmon')
    plt.title("Volume d'octets envoyés par type d'appareil")
    plt.xlabel('Total octets envoyés'); plt.ylabel("Type d'appareil")
    plt.tight_layout(); plt.savefig(FIG_DIR / 'bytes_device.png'); plt.close()

    # Figure 4
    plt.figure(figsize=(12, 5))
    df.set_index('timestamp').resample('h').size().plot(color='purple')
    plt.title('Nombre de connexions par heure')
    plt.xlabel('Heure'); plt.ylabel('Nombre de connexions')
    plt.tight_layout(); plt.savefig(FIG_DIR / 'connexions_heure.png'); plt.close()
    
    print("✅ Les 4 figures ont été enregistrées dans le dossier 'figures'.")

if __name__ == "__main__":
    df_propre = charger_et_nettoyer()
    calculer_resultats(df_propre)
    generer_figures(df_propre)
    print("🎉 Analyse terminée avec succès !")