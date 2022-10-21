# brief6

Schéma topologique basique de l'infra à déployer :  

![IMG](https://github.com/Simplon-AlainCaupin/brief6/blob/7c32326c9b39daf78f59f132acdab80e93f1c75b/IMG/topo%20brief6.png?raw=true)

## Etapes de réalisation de la partie 1 du brief :  

Création du resource group :

```
az group create -l westus -n brief6lain
```

Au besoin, pour suppression du rg :

```
az group delete --name brief6lain --no-wait --yes
```

Création du cluster AKS contenant 2 nodes :
```
az aks create -g brief6lain -n akslain --enable-managed-identity --node-count 2 --enable-addons monitoring --enable-msi-auth-for-monitoring  --generate-ssh-keys
```
Config des credentials pour le cli Kubernetes

```
az aks get-credentials --resource-group brief6lain --name akslain
```

sortie de la commande :  

```
Merged "akslain" as current context in /home/alain/.kube/config
```

Vérification :
```
alain@alain-VirtualBox:~$ kubectl get nodes
NAME                                STATUS   ROLES   AGE   VERSION
aks-nodepool1-14927201-vmss000000   Ready    agent   16m   v1.23.8
aks-nodepool1-14927201-vmss000001   Ready    agent   15m   v1.23.8
```

Connection redis avec redis-cli :  

```
sudo docker exec -it redis-brief6 sh
```
Création du manifeste pour le password redis, [redispwd.yml]()  

**Pour le mot de passe: il faut l'encoder en base64.**

Configuration du stockage persistant pour Redis :  

Création de 2 manifestes, le 1er pour le PV lui même : [redispv.yml](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/redispv.yml)  
Le second pour affecter ce volume au container Redis : [redispvclaim.yml](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/redispvclaim.yml)  

### Déploiement de l'infra :  
Dans le répertoire contenant les manifestes :  
```
kubectl apply -f .
```

---

Annexe commandes kubectl utiles : pour supprimer les containers :
```
kubectl delete -f .
```

Pour re-déployer un manifeste :  
```
kubectl replace -f ./nom_du_fichier.yml
```

---

# partie 2

Documentation suivie :  

https://learn.microsoft.com/en-us/azure/application-gateway/tutorial-ingress-controller-add-on-new

Création du cluster avec AGIC activé + application gateaway et 4 nodes

```
az aks create -n akslain -g brief6lain --network-plugin azure --enable-managed-identity --node-count 4 -a ingress-appgw --appgw-name appGWlain --appgw-subnet-cidr "10.225.0.0/16" --generate-ssh-keys
```
Config des credentials pour le cli Kubernetes, comme pour la partie 1 :  

```
az aks get-credentials --resource-group brief6lain --name akslain
```

Déploiement de l'infra :
Dans le répertoire contenant les manifestes
```
kubectl apply -f .
```

Nom de domaine et certificat TLS :  

En utilisant le nom de domaine sur Gandi :  
![Domaine](https://github.com/Simplon-AlainCaupin/brief6/blob/main/IMG/gandi_domain.png?raw=true)  

Affectation du DNS :  

![DNS_gandi](https://github.com/Simplon-AlainCaupin/brief6/blob/main/IMG/gandi_dns.png?raw=true)

Création du certificat via l'API Gandi pour certbot, sélection du certificat dans la "rule" créée par la suite,  

Sur le portail Azure, création de Rule redirigeant le back-end de l'application gateway et Listener sur le port https 443 pour la redirection du front-end (le site web de l'application / IP publique front-end de l'app gateway)  

Pour la partie Scaling de l'application :  

Dans le manifeste de l'application [app-deploy](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/app-deploy.yml) : 
ajout d'une limite de ressources (sur CPU et MEMORY) et création d'un manifeste pour l'auto-scaling : [scaling.yml](https://github.com/Simplon-AlainCaupin/brief6/blob/main/Part%202/scaling.yml)  

Stress test avec la commande
```
seq 100 | parallel --max-args 0  --jobs 10 "curl -k -iF 'vote=Dogs' https://appvote.alain-cpn.space"
```

# Fonctionnement de Kunernetes, tel que compris :  

Kubernetes est une plateforme d'automatisation open source, permettant de déployer applications et resources depuis des manifestes au format de fichier "yaml", via des containers, égalementdes services Azure dans le cas du brief 6.  

# Difficultés rencontrées :  

Absent car en arrêt maladie lors du brief 5, j'ai pris du retard, j'ai acheté un nom de domaine OVH pour progresser mais rien ne fonctionnait correctement malgrè la documentation suivie à la lettre. 
Le nom de domaine Gandi a pris quelques jours à être disponible, cela m'a freiné dans la partie 2 du brief mais au final le problème a été résolu et j'ai pu reprendre.  

J'ai choisi de passer par une vm Oracle virtual box (ubuntu 22.04), un incident est apparu vers la fin de la partie 1, ce qui m'a forcé à recommencer depuis un environnement Windows (commandes powershell pour Azure Cli et Kubectl, wsl Ubuntu pour la partie TLS), suite à quoi j'ai pu continuer. J'ai du faire la fin rapidement et sans pouvoir rentrer dans les détails.  

# Points positifs : 

Dans l'ensemble, j'ai compris le fonctionnement de Kubernetes, le brief était très dense mais intéressant, ça a été le plus gros challenge pour moi depuis le début de la formation.  

Mes collègues m'ont épaulé sur mon retard et certains points bloquants, sans quoi je n'aurais pas pu beaucoup avancer jusqu'à la date du rendu.  