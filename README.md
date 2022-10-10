# brief6

Simplon brief6 kubernetes
Création du resource group :

```
az group create -l westus -n brief6lain
```

Suppression du rg au besoin :

```
az group delete --name brief6lain
az group delete --name MC_brief6lain_akslain_westus
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



Récupérer container Redis
```
sudo docker run --name redis-brief6 -d redis
```

récupérer id de l'image:
sudo docker image ls

démarrer le container avezc l'id :
sudo docker run -i -t [id de l'image]


Connection redis avec redis-cli
```
sudo docker exec -it redis-brief6 sh
```


Création du "secret" kubernetes:

```
kubectl create secret generic redis --from-literal="REDIS_PASS=toto1234"
```