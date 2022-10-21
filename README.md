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

En utilisant le nom de domaine sur Gandi,  


# Fonctionnement de Kunernetes, tel que compris :  

