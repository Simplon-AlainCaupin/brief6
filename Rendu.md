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

Contexte : Déploiement d'une infra avec un site web en front-end
le déploiement se fera via Kubernetes, 
avec 1 container Redis pour la bdd
1 container Appli pour le site-web
Le but est de créer l'infra de bout en bout, avec, entre autres, un stockage persistent et certificat tls pour sécuriser l'accès au site web

---

## Chapitre 1 : Déployer un cluster AKS

Déploiement d'un nouveau rg :
```
az group create -l westus -n brief6lain
```
Déploiement du custer aks comprenant 2 nodes :
```
az aks create -g brief6lain -n akslain --enable-managed-identity --node-count 2 --enable-addons monitoring --enable-msi-auth-for-monitoring  --generate-ssh-keys
```

---

Chapitre 2 : Déployer un container Redis

Via manifest Kubernetes, détails ci-dessous :

[Déploiement Redis](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%201/redis-deploy.yml)
[Déploiement Cluster IP Redis](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%201/rediscluster.yml)

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

Chapitre 8 : Certificat TLS pour Voting App

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

---

# Explications sur Kubernetes :

Le 