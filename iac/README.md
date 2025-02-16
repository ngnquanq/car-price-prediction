# HEAD FIRST !

A lot of things need to do be done before can create aks cluster. 
az config set extension.dynamic_install_allow_preview=true
Notice that only LoadBalancer can be use for building 

1. Login azure and azure container registry. 

```shell
# Login into az
az login
# Create resource group 
az group create -l southeastasia -n carPricePrediction
# Create container registry (for pushing images)
az acr create --resource-group carPricePrediction --name carpredictionregistry --sku Standard
```
The next step is to create azure container registry (tldr: work as dockerhub but for azure)

```shell
# After that, you also need to login to registry as well
az acr login --name carpredictionregistry
# After that, push the image onto azure container registry
docker tag car-price-prediction carpredictionregistry.azurecr.io/car-price-prediction:v1
docker push carpredictionregistry.azurecr.io/car-price-prediction:v1
# Can also build the image to see whether it is able to be pull or not. 
docker pull carpredictionregistry.azurecr.io/car-price-prediction:v1
```



```
2. In order to use kubectl on AKS cluster, you musst give credential to it as well. 
```shell

```
3. Assure that you connect w the correct acr + the right image
