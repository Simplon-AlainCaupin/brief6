---
marp: true
theme: gaia
class:
    - lead
    - invert
paginate: true
---

INTRO :

Documentation suivie : Doc microsoft Azure / Kubernetes 

---

## Chapitre 1 : Déployer un cluster AKS

Déploiement d'un noveau rg :
```
az group create -l westus -n brief6lain
```
Déploiement du custer aks comprenant 2 nodes :
```
az aks create -g brief6lain -n akslain --enable-managed-identity --node-count 2 --enable-addons monitoring --enable-msi-auth-for-monitoring  --generate-ssh-keys
```

---

Chapitre 2 : Déployer un container Redis

Via manifest Kubernetes :
[Déploiemment Redis]()

---

Chapitre 3 : Déployer un container Voting App

---

Chapitre 4 : Un mot de passe pour Redis

---

Chapitre 5 : Configurer un stockage persistent pour Redis

---

Chapitre 6 : Utiliser Azure Application Gateway avec AKS

---

Chapitre 7 : Un nom de domaine pour Voting App

En utilisant ce qui a été appris lors du brief 5
Nom de domaine sur Gandi

---

Chapitre 8 : Un certificat TLS pour Voting App

---

Chapitre 9 : Scaling de la Voting App

Ajout d'une limite de ressources au déploiement de l'application :

```
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 250m
            memory: 256Mi
```