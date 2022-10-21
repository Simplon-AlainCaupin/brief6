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

Via manifeste Kubernetes, détails ci-dessous :

[Déploiement Redis](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%201/redis-deploy.yml)
[Déploiement Cluster IP Redis](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%201/rediscluster.yml)
Le manifeste "redis-deploy" permet de déployer l'image redis depuis un container.
Au départ une image basique, et un manifeste pour déployer le "cluster IP" contenant le service associé à l'application Redis

---

Chapitre 3 : Déployer un container Voting App  

[Déploiement Appli](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/app-deploy.yml)  
[Déploiement LB](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/lbapp.yml)  
Comme pour Redis, 2 manifestes : 1 pour le container Appli, 1 pour le service, dans ce cas un "loadbalancer"

---

Chapitre 4 : Un mot de passe pour Redis

Après vérification du fonctionnement de Redis :  
Ajout d'un mot de passe dans un manifeste à part  
[Redispwd](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/redispwd.yml)  
Pas optimisé car le mot de passe encodé en base64 apparaît en clair dans le manifeste  

---

Chapitre 5 : Configurer un stockage persistent pour Redis

Création manifeste pour le pv en lui même [redispv.yml](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/redispv.yml)  
Pour "claim" le pv : [redispvclaim.yml](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/redispvclaim.yml)  
et enfin lier le pv au manifeste [redis-deploy.yml](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/redis-deploy.yml)  
Permet de conserver les données lorsque l'image Redis est détruite (à condition que le même manifeste soit utilisé pour re-déployer)  

---

Chapitre 6 : Utiliser Azure Application Gateway avec AKS

Création d'un cluster AKS à zéro comprenant 4 nodes + 1 application gateway sur son propre sous-réseau  
```
az aks create -n akslain -g brief6lain --network-plugin azure --enable-managed-identity --node-count 4 -a ingress-appgw --appgw-name appGWlain --appgw-subnet-cidr "10.225.0.0/16" --generate-ssh-keys
```
option "ingress-appgh" pour activer AGIC (Application Gateway Ingress Controller) permettant de communiquer avec les pods directement depuis leur adresse ip privée, limitant le traffic de données (supprimant le besoin d'un autre application gateway)

---

Chapitre 7/8 : Un nom de domaine pour Voting App

En utilisant ce qui a été appris lors du brief 5
Nom de domaine sur Gandi, puis création de listener / rule pour utiliser le certificat TLS sur l'adresse front end de l'application gateway

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

Kubernetes est un outil permettant l'orchestration de services, containers, applications
Mots clés :  
Nodes : machines exécutant les taches
Pods : 1 ou plusieurs containers déployés sur 1 node
Service : méthode exposant 1 app en tant que service réseau, le service sépare les taches des pods  
Kubectl : 