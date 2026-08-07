\# CSE644 Assignment 02 — Local Kubernetes Application Platform



\## Student



\*\*Name:\*\* Abhi Shah



\## Kubernetes Environment



This assignment uses \*\*Docker Desktop Kubernetes\*\* as the local Kubernetes environment.



Kubernetes was accessed and verified using the `kubectl` command-line tool.



\## Architecture Summary



This project deploys two custom applications on a local Kubernetes cluster:



1\. A customized Nginx web application

2\. A Python web application listening on port 8888



The project also includes:



\* Kubernetes Deployments

\* Kubernetes Services

\* HAProxy as an independent edge component

\* ClusterIP

\* NodePort

\* LoadBalancer

\* Ingress

\* Persistent storage using a PersistentVolumeClaim

\* ConfigMap for non-secret application configuration

\* Opaque Secret for a dummy protected value

\* Readiness and liveness probes

\* Kubernetes labels and service selectors



\### Application Flow



```text

&#x20;                   Ingress

&#x20;                      |

&#x20;                      v

&#x20;                 Nginx Service

&#x20;                      |

&#x20;                      v

&#x20;               Nginx Deployment

&#x20;                /            \\

&#x20;             Pod              Pod



Client

&#x20; |

&#x20; v

HAProxy

&#x20; |

&#x20; v

Nginx Service

&#x20; |

&#x20; v

Nginx Pods





Python Service

&#x20;     |

&#x20;     v

Python Deployment

&#x20;   /       \\

&#x20;Python     Python

&#x20;  Pod        Pod

&#x20;     |

&#x20;     v

Persistent Storage

```



\## Repository Structure



```text

cse644-assignment02/

│

├── nginx-app/

│   ├── Dockerfile

│   └── index.html

│

├── python-app/

│   ├── app.py

│   ├── Dockerfile

│   └── requirements.txt

│

├── k8s/

│   ├── namespace.yaml

│   ├── nginx-deployment.yaml

│   ├── nginx-service.yaml

│   ├── python-deployment.yaml

│   ├── python-service.yaml

│   ├── python-pvc.yaml

│   ├── python-configmap.yaml

│   ├── python-secret.yaml

│   ├── haproxy-deployment.yaml

│   ├── haproxy-service.yaml

│   ├── haproxy-configmap.yaml

│   └── ingress.yaml

│

├── evidence/

├── .gitignore

└── README.md

```



\## Prerequisites



The following software is required:



\* Docker Desktop

\* Docker Desktop Kubernetes

\* kubectl

\* Git

\* GitHub account



Verify Docker:



```powershell

docker version

```



Verify Kubernetes:



```powershell

kubectl version --client

kubectl get nodes

```



\## Local Image Loading



Docker Desktop Kubernetes uses the Docker Desktop container runtime, so locally built images are available to the Kubernetes cluster.



The custom application images were built locally with versioned tags.



Example:



```powershell

docker build -t shah990/python-web:1.1 ./python-app

```



The Kubernetes resources use versioned image tags rather than floating `latest` tags.



\## Build Applications



Build the Nginx application:



```powershell

docker build -t shah990/custom-nginx:1.0 ./nginx-app

```



Build the Python application:



```powershell

docker build -t shah990/python-web:1.1 ./python-app

```



Verify images:



```powershell

docker images

```



\## Deploy Kubernetes Resources



Create the namespace:



```powershell

kubectl apply -f k8s/namespace.yaml

```



Apply the Kubernetes resources:



```powershell

kubectl apply -f k8s/

```



Verify:



```powershell

kubectl get all -n cse644

```



\## Kubernetes Workload Operations



A public container image was used to demonstrate Kubernetes workload operations.



The workload was created and inspected using Kubernetes commands such as:



```powershell

kubectl get pods

kubectl describe pod <pod-name>

kubectl logs <pod-name>

kubectl exec -it <pod-name> -- sh

```



These commands demonstrate workload creation, inspection, logs, and interactive shell access.



\## Application Deployment



The customized Nginx application runs with multiple replicas.



Verify:



```powershell

kubectl get deployments -n cse644

kubectl get pods -n cse644

```



The Python application listens on port 8888.



Verify:



```powershell

kubectl get svc -n cse644

```



\## Internal Service Discovery



Kubernetes Services provide stable internal DNS names for the workloads.



The applications communicate using Kubernetes Service names instead of individual Pod IP addresses.



Example:



```text

python-web.cse644.svc.cluster.local

```



HAProxy also connects to the Nginx Service through Kubernetes service discovery.



\## HAProxy



HAProxy is deployed as an independent edge component.



HAProxy forwards requests to the Nginx Kubernetes Service rather than directly to an individual Pod IP.



The HAProxy configuration is stored in a Kubernetes ConfigMap and mounted into the HAProxy container.



Successful proxied requests were verified using Kubernetes port forwarding and HTTP requests.



\## Service Exposure



\### ClusterIP



ClusterIP provides internal-only access to a Kubernetes Service.



Traffic enters through the Kubernetes Service virtual IP and is forwarded to matching Pods.



Example:



```powershell

kubectl get svc -n cse644

```



\### NodePort



NodePort exposes the Service through a port on the Kubernetes node.



Traffic enters through the node port and Kubernetes forwards the request to the Service and then to the selected Pods.



\### LoadBalancer



LoadBalancer provides a load-balancer style Service interface.



Docker Desktop Kubernetes provides a local implementation suitable for demonstrating the mechanism without requiring a public cloud address.



\### Ingress



Ingress provides HTTP/HTTPS routing into Kubernetes.



The Ingress controller receives the request and routes it to the configured Kubernetes Service.



Verify:



```powershell

kubectl get ingress -n cse644

```



\## Persistent Storage



The Python application uses a PersistentVolumeClaim.



Data was written through a running workload. The application Pod was then replaced by deleting the Pod.



The Deployment automatically created a replacement Pod.



The stored data remained available after replacement, demonstrating persistent storage.



Verify:



```powershell

kubectl get pvc -n cse644

```



The PVC should show:



```text

STATUS: Bound

```



\## ConfigMap



A ConfigMap is used for a non-secret application setting.



The Python application's visible greeting is controlled through the ConfigMap.



The ConfigMap value can be changed without rebuilding the container image.



Example:



```text

GREETING=Hello from the Production Environment!

```



After changing the ConfigMap and restarting the Deployment, the application displayed the updated greeting.



\## Kubernetes Secret



An Opaque Kubernetes Secret supplies a dummy protected application value.



The application receives the value through an environment variable.



The secret value is intentionally not displayed in:



\* Application responses

\* Logs

\* Screenshots

\* Source code

\* GitHub



No real credentials or API keys are stored in this repository.



\### Secret Security



Kubernetes Secrets are \*\*not encrypted by default in the API server's underlying data store\*\*.



A production Kubernetes cluster should use:



\* Encryption at rest

\* Least-privilege RBAC access controls

\* Appropriate secret management practices

\* Restricted access to the Kubernetes API



\## Health Checks



The Python application includes readiness and liveness probes.



\### Readiness Probe



The readiness probe checks:



```text

/ready

```



A successful readiness check means the application is ready to receive traffic.



\### Liveness Probe



The liveness probe checks:



```text

/health

```



A successful liveness check indicates that the application process is healthy.



Verify:



```powershell

kubectl describe deployment python-web -n cse644

```



\## Validation Commands



Check the Kubernetes cluster:



```powershell

kubectl get nodes

```



Check workloads:



```powershell

kubectl get pods -n cse644

```



Check services:



```powershell

kubectl get svc -n cse644

```



Check deployments:



```powershell

kubectl get deployments -n cse644

```



Check persistent storage:



```powershell

kubectl get pvc -n cse644

```



Check Ingress:



```powershell

kubectl get ingress -n cse644

```



Check ConfigMap:



```powershell

kubectl get configmap -n cse644

```



Check Secret without exposing its value:



```powershell

kubectl get secret -n cse644

```



\## Evidence



Focused screenshots and command output are provided in the `evidence` directory.



Evidence covers:



1\. Running Kubernetes cluster

2\. Public image workload

3\. Workload inspection and logs

4\. Interactive shell

5\. Nginx application

6\. Python application

7\. Internal service discovery

8\. HAProxy proxying

9\. ClusterIP

10\. NodePort

11\. LoadBalancer

12\. Ingress

13\. Persistent storage after Pod replacement

14\. ConfigMap behavior change

15\. Secret configuration without exposing the value

16\. Readiness and liveness checks



\## Cleanup



To remove the assignment resources:



```powershell

kubectl delete namespace cse644

```



To remove the Docker images:



```powershell

docker rmi shah990/python-web:1.1

docker rmi shah990/custom-nginx:1.0

```



\## Security



No passwords, access tokens, private keys, kubeconfig files, API keys, or real credentials are included in this repository.



The `.gitignore` file is used to prevent accidental submission of sensitive local files.



