
#helm uninstall doc-search
helm install doc-search doc-search-helm
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=doc-search-helm,app.kubernetes.io/instance=doc-search" -o jsonpath="{.items[0].metadata.name}")
echo $POD_NAME
export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
echo $CONTAINER_PORT
kubectl get pods
sleep 5
kubectl get pods
kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
kubectl logs $POD_NAME