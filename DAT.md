# Document d'Architecture Technique

## Contexte :

### Besoins fonctionnels :  

Déploiement d'une infrastructure via Kubernetes comprenant :

Un cluster Azure au sein d'un Virtual Network comprenant :  
- Une application web basique  
- Une DB Redis  
- 1 Application Gateway
- 1 loadbalancer
- 1 IP Publique back-end pour l'app gateway
- 1 IP Publique front-end pour l'application
- Certificat TLS pour l'accès en https à l'application
- Stockage persistant pour la BDD Redis
- 1 Scale Set en fonction de la charge CPU
  
### Besoins non fonctionnels :  

Niveau sécurité, l'application doit être accessible en https via un certificat TLS vérifié.  
L'utilisateur de l'application n'a accès qu'au site web via l'adresse DNS fournie.  

## Représentation fonctionnelle :  

Le principe de l'application est très simple : il permet de voter pour votre boule de poils préférée.  

Peu de données sont sauvegardées, hormis le résultat des votes sur l'application  
Ces données sont sauvegardées dans la BDD Redis, sur un volume de stockage persistant lié au cluster.  
Pas de données utilisateur (login, mot de passe inexistants)  

## Représentaton applicative :  

L'application est déployée d'un container depuis un manifeste Kubernetes,  
Il en est de même pour la bdd Redis.  
Le reste de l'infrastructure étant déployé en amont avec le cluster, après création du resource group Azure.  
D'autres services sont déployés en même temps que les containers, à savoir un stockage persistant pour conserver les données en cas d'incident sur le container BDD, un scale-set pour gérer l'accessibilité à l'application en fonction de la charge CPU sur le container applicatif.  

## Choix de l'architecture : 

L'architecture cloud est déployée via Azure,  
Ses composants ont été choisis afin d'assurer la stabilité et la sécurité de l'application déployée (voir Besoins Fonctionnels)  

## Plan de réalisation :  

- Côté utilisateur :  
  - accès au site web en https via un certificat TLS (Gandi)  
- Côté déploiement :  
via Kubernetes + deux containers :  
  - 1 pour Redis et les différents services nécessaires
  - 1 pour l'application et services  
- Pour la persistence des données :  
  - 1 stockage persistent pour la BDD Redis  
Côté sécurité :  
  - 1 Kubernetes Secret pour l'accès à la BDD Redis  
- Stabilité de l'infra :  
  - Scaleset augmentant les ressources en fonction de l'utilisation CPU