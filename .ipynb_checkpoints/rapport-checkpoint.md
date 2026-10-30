# Rapport d'analyse réseau

## Résumé de l'observation
L'analyse d'une semaine de connexions réseau a permis d'étudier 5 440 connexions uniques après nettoyage. Le trafic est largement dominé par le protocole sécurisé HTTPS (port 443) et par les actions autorisées (86,4 % d'ALLOW contre 13,6 % de DENY). Cependant, deux comportements suspects ressortent : un volume d'octets anormalement élevé émis par les caméras IoT, et une concentration de tentatives de rejet (DENY) provenant d'une adresse IP unique. Ces éléments indiquent un possible appareil compromis et une tentative d'accès non autorisé.

## Comportements suspects identifiés

### Suspect 1 : Exfiltration de données via la caméra IoT
**Preuve :** La figure `figures/bytes_device.png` montre que le type d'appareil `camera_IoT` génère un volume d'octets à l'écart de tous les autres appareils (représenté par la barre rouge écrasante).
**Interprétation :** Une caméra de surveillance ne devrait envoyer que de petits paquets de données (flux vidéo compressé). Un tel volume d'octets suggère que l'appareil a été infecté par un malware (comme un botnet type Mirai) et qu'il exfiltre des données ou participe à une attaque par déni de service (DDoS).
**Recommandation :** Isoler immédiatement le segment réseau des caméras (VLAN dédié), bloquer les connexions sortantes non essentielles et mettre à jour le firmware.

### Suspect 2 : Tentatives d'accès répétées depuis l'IP 192.168.1.99
**Preuve :** Les résultats calculés indiquent que l'IP `192.168.1.99` est l'adresse source ayant généré le plus de connexions bloquées (`DENY`). 
**Interprétation :** Cette machine tente régulièrement d'accéder à des ports ou des ressources interdites par le pare-feu. Cela peut être le signe d'un ver informatique qui se propage ou d'une machine compromise cherchant à se connecter à des serveurs (ex: scan de ports).
**Recommandation :** Isoler cette machine du réseau et analyser ses logs de sécurité (antivirus, EDR).

## Recommandations de sécurité
1. **Segmentation des objets IoT :** Placer les caméras et capteurs sur un réseau séparé (VLAN) avec des règles de pare-feu strictes pour limiter leur communication.
2. **Bloquer les protocoles obsolètes :** Fermer immédiatement les ports non sécurisés comme Telnet (port 23) au niveau du pare-feu.
3. **Mise en quarantaine :** Appliquer une règle de sécurité pour bloquer temporairement l'IP `192.168.1.99` et forcer la réinstallation de la machine concernée.