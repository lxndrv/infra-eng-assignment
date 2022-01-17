

# Code assignment: document search

This assignment aims to explore multiple aspects of taking a simple Python web application and making it production-grade.

## Background

The `doc-search` application implements a simple search endpoint over a set of documents. More specifically, given a dataset of documents, where each document has a numeric identifier, the endpoint returns a list of all of the document IDs containing ALL words in the `q` query parameter.

For example, if the web server is serving at http://localhost:8080, and the words `hello` and `world` both exist only in document 1, then the command `curl http://localhost:8080/?q=hello+world` should return:

```json
{
    "results": ["1"]
}
```

### Sanity checks

1. Run unit tests `cd doc-search/src/ && python -m unittest -b test_index`
2. Build the container image: `docker build . -t doc-search`
3. Run the app: `docker run -p 8080:8080 doc-search`. 
4. Test the app: you can use `curl` to query it, for example: `curl http://localhost:8080/?q=hello+world` will return a JSON document with all of the documents containing both `hello` and `world`

## Tasks

### Part 1: Improving the build

The app currently has a `Dockerfile` included under `doc-search/`.

1. Every commit to application code (`.py` files) results in a slow build of the container image. Modify the `Dockerfile` to make the build faster.
> **Moved the application code to the later layer**
2. How can you minimize the size of the resulting container image? Modify the `Dockerfile` or describe your solution.
> **The samples/data folder should be on the mounted volume.
The persistent volume configuration differ for different platforms**
```
https://stackoverflow.com/questions/50016515/mounting-a-directory-for-pods-in-kubernetes

https://minikube.sigs.k8s.io/docs/handbook/mount/

https://kubernetes.io/docs/concepts/storage/volumes/

https://docs.docker.com/storage/bind-mounts/

```

### Part 2: Deploying to Kubernetes

Here you will deploy the application to a local Minikube.

1. Implement a minimal Helm chart for this application.
> <https://github.com/lxndrv/infra-eng-assignment/tree/main/doc-search-helm>
2. Deploy the chart to Minikube, under the `default` namespace.
> ``` helm install doc-search doc-search-helm ```
3. Verify that you can call the service from outside the cluster.
> 
``` 
helm list
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                APP VERSION
doc-search      default         1               2022-01-16 18:39:59.74429776 +0000 UTC  deployed        doc-search-helm-0.1.01.0.0

kubectl get pods
NAME                                          READY   STATUS    RESTARTS   AGE
doc-search-doc-search-helm-84f648b65d-cxxhc   1/1     Running   0          15m

kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT Forwarding from 127.0.0.1:8080 -> 8080

curl http://localhost:8080?q=think
{"results": ["993945", "994348", "999503", "996147", "994616", "998237", "997488"]}

```
4. We want Kubernetes to tolerate a slow start for our app. Implement this behavior in your chart. Bonus points if you can simulate a slow start and test your solution.
> **index_init function with a sleep to simulate slow start:**
<https://github.com/lxndrv/infra-eng-assignment/blob/main/doc-search/src/__init__.py#L35>

> **When finished index_init sets index.isReady to True
The index.isReady is used to determine response status code in /readiness endpoint:** 
<https://github.com/lxndrv/infra-eng-assignment/blob/main/doc-search/src/__init__.py#L21>

> **livenessProbe and readinessProbe settings:**
<https://github.com/lxndrv/infra-eng-assignment/blob/main/doc-search-helm/templates/deployment.yaml#L40>


---

Good luck!