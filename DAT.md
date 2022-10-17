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
- I IP Publique front-end pour l'application
  
### Besoins non fonctionnels :  

Niveau sécurité, l'application doit être accessible en https via un certificat TLS vérifié.  
L'utilisateur de l'application n'a accès qu'au site web via l'adresse fournie.  

## Représentation fonctionnelle :  

Le principe de l'application est très simple : il permet de voter pour votre boule de poils préférée.  

Peu de données sont sauvegardées, hormis le résultat des votes sur l'application  
Ces données sont sauvegardées dans la BDD Redis, sur un volume de stockage persistant lié au cluster.  
Pas de données utilisateur (login, mot de passe inexistants)  

## Représentaton applicative :  

L'application est déployée d'un container depuis un manifeste Kubernetes  
Il en est de même pour la bdd Redis  
Le reste de l'infrastructure étant déployé en amont avec le cluster, après création du resource group Azure.  

## Choix de l'architecture : 

L'architecture cloud est déployée via Azure,  
Ses composants ont été choisis afin d'assurer la stabilité et la sécurité de l'application déployée, à savoir :  


