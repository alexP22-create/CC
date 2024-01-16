POSTOLACHE Alexandru-Gabriel EGOV1-B
BUZDUGAN Mihaela EGOV1-A
MEGELEA Diana-Mihaela SCPD2

==============================      README     ===================================

    Aplicatie web care ajuta la gestionarea unui restaurant. Este destinata pentru 
trei tipuri de utilizatori: administrator, client si ospatar. Administratorul
poate gestiona conturile de client si ospatar si poate modifica meniul. 
Clientul poate selecta produsele dorite, sa vada totalul de plata, iar apoi
sa trimita comanda. Ospatarul poate vedea comenzile clientilor si le poate 
gestiona, iar in cazul in care clientul nu doreste sa-si faca cont, ospatarul
ii poate prelua comanda din contul sau.

    Aplicatia noastra contine 5 servicii:
        -> serviciul de autentificare
        -> serviciul de business logic
        -> serviciul de baza de date ce ruleaza scriptul numit restaurant.sql
    ce creeaza baza de date si se ruleaza intr-un container de MySql.
        -> serviciul de management al bazei de date, ce utilizeaza phpmyadmin
        -> portainer pt managementul clusterului

    Serviciile de autentificare si business logic sunt scrise in python flask,
comunica prin cereri http requests(post, get, etc.) si sunt conectate la baza de date.
    Tehnologii folosite: Python Flask, MySql, Bootstrap, Html, CSS, Javascript, 
Kubernetes, Docker, Grafana, Terraform.

    Pasi deploy si rulare folosind docker, kubernetes si minikube:
    0) Creare aplicatie web si verficarea locala a acesteia
        - creare frontend
        - creare route backend
        - creare baza de date in MySql si legarea la backend
        - testare locala a functionalitatilor
        - impartirea pe servicii ce comunica prin cereri http 

    1) Creare Dockerfile-uri si fisiere .yaml pentru configuratiile de Kubernetes
        - Dockerfile
        - nume-deployment.yaml
        - nume-service.yaml

    2) Ex creare imaginini docker, update, eliberare de porturi si incarcare pe docker hub
        docker login -u "myusername" -p "mypassword" docker.io
        docker build -t alex22docker/auth:latest .
        docker build --no-cache -t alex22docker/auth:latest .
        docker ps -> extragere id
        docker stop <id>
        docker tag auth:latest alex22docker/auth:latest                                                  
        docker push alex22docker/auth:latest
    
    3) Pregatirea environmentului si pornire cluster
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Tools-All -All
        $Env:DOCKER_TLS_VERIFY = "1"
        $Env:DOCKER_HOST = "tcp://172.24.243.89:2376"
        $Env:DOCKER_CERT_PATH = "C:\Users\alexp.minikube\certs"
        $Env:MINIKUBE_ACTIVE_DOCKERD = "cluster-multinod"
        minikube -p cluster-multinod docker-env --shell powershell
        minikube start --nodes 3 -p cluster-multinod

    4) Creare secrete si aplicare configuratii kubernetes
        kubectl create secret docker-registry auth-secret --docker-server=docker.io 
    --docker-username=alex22docker --docker-password=<password> --docker-email=<email>
        kubectl apply -f auth-deployment.yaml
        kubectl apply -f auth-service.yaml
        ...

    5) Verificare imaginilor de docker
        docker run -p port:port alex22docker/auth:latest
        ...

    6) Pornire cluster si verificare
        minikube start --nodes 3 -p cluster-multinod
        kubectl get deployments
        kubectl get services
        kubectl get pods
        kubectl describe pod <pod name>
        kubectl logs pod <pod name>

    7) Accesare servicii
        minikube service phpmyadmin-service -p cluster-multinod

    8) Grafana:
    kubectl apply -f persistent-volume.yaml
    kubectl apply -f grafana-deployment.yaml
    kubectl apply -f grafana-service.yaml
    kubectl get deployments
    minikube service grafana