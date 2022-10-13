# brief6

Simplon brief6 kubernetes
Création du resource group :

```
az group create -l westus -n brief6lain
```

Suppression du rg :

```
az group delete --name brief6lain
```

Création du cluster AKS contenant 2 nodes :
```
az aks create -g brief6lain -n akslain --enable-managed-identity --node-count 2 --enable-addons monitoring --enable-msi-auth-for-monitoring  --generate-ssh-keys
```

4 nodes pour la partie 2 :
```
az aks create -n akslain -g brief6lain --network-plugin azure --enable-managed-identity --node-count 4 --generate-ssh-keys
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

Connection redis avec redis-cli
```
sudo docker exec -it redis-brief6 sh
```
Création de manifeste pour le password redis

Tout virer :
kubectl delete -f .


Pour le mot de passe: il faut l'encoder en base64

# partie 2

Création du cluster avec AGIC
```
az aks create -n akslain -g brief6lain --network-plugin azure --enable-managed-identity --node-count 4 --generate-ssh-keys
```

Déploiement application gateway :
```
az network public-ip create -n publicIpLain -g brief6lain --allocation-method Static --sku Standard
az network vnet create -n VnetLain -g brief6lain --address-prefix 10.0.0.0/16 --subnet-name subNetLain --subnet-prefix 10.0.0.0/24
az network application-gateway create -n AppGatewayLain -l westus -g brief6lain --sku Standard_v2 --public-ip-address publicIpLain --vnet-name VnetLain --subnet subNetLain --priority 100
```

Activer AGIC sur le cluster AKS :
```
$appgwId=$(az network application-gateway show -n AppGatewayLain -g brief6lain -o tsv --query "id")
az aks enable-addons -n akslain -g brief6lain -a ingress-appgw --appgw-id $appgwId
```
Lier le vnet créé à celui du cluster AKS : 

$nodeResourceGroup=$(az aks show -n akslain -g brief6lain -o tsv --query "nodeResourceGroup")
$aksVnetName=$(az network vnet list -g $nodeResourceGroup -o tsv --query "[0].name")

$aksVnetId=$(az network vnet show -n $aksVnetName -g $nodeResourceGroup -o tsv --query "id")
az network vnet peering create -n AppGWtoAKSVnetPeering -g brief6lain --vnet-name VnetLain --remote-vnet $aksVnetId --allow-vnet-access

$appGWVnetId=$(az network vnet show -n VnetLain -g brief6lain -o tsv --query "id")
az network vnet peering create -n AKStoAppGWVnetPeering -g $nodeResourceGroup --vnet-name $aksVnetName --remote-vnet $appGWVnetId --allow-vnet-access

Config des credentials pour le cli Kubernetes

```
az aks get-credentials --resource-group brief6lain --name akslain
```