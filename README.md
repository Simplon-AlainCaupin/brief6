# brief6

Simplon brief6 kubernetes
Création du resource group :

```
az group create -l westus -n brief6lain
```

Création du cluster AKS :
```
az aks create -g brief6lain -n akslain --enable-managed-identity --node-count 2 --enable-addons monitoring --enable-msi-auth-for-monitoring  --generate-ssh-keys
```

Ajout de nodes :

```
az aks nodepool add --resource-group brief6lain --cluster-name akslain --name nodepoolain --node-count 2
```

Création container redis :  
[lien vers doc suivie](https://phoenixnap.com/kb/docker-redis)


Récupérer container Redis
```
sudo docker run --name redis-brief6 -d redis
```

Connection redis avec redis-cli
```
sudo docker exec -it redis-brief6 sh
```