from fastapi import FastAPI
import requests

app = FastAPI()

ARGOCD_SERVER = "http://argocd-server.argocd.svc.cluster.local:80"
ARGOCD_AUTH_TOKEN = "FZsmpTtmetHSw3v3%"  

def get_headers():
    """Returns headers with ArgoCD authentication."""
    return {"Authorization": f"Bearer {ARGOCD_AUTH_TOKEN}"}

@app.get("/api/v1/argocd/application_status")
def get_application_status():
    """Fetches the status of ArgoCD applications."""
    url = f"{ARGOCD_SERVER}/api/v1/applications"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        return {"error": "Failed to fetch application status"}

    data = response.json()
    applications = [
        {"application_name": app["metadata"]["name"], "status": app["status"]["sync"]["status"]}
        for app in data.get("items", [])
    ]

    return {"applications": applications}

@app.get("/api/v1/argocd/list_projects")
def list_projects():
    """Fetches the list of ArgoCD projects."""
    url = f"{ARGOCD_SERVER}/api/v1/projects"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        return {"error": "Failed to fetch projects"}

    data = response.json()
    projects = [
        {"project_name": proj["metadata"]["name"], "namespace": proj["metadata"]["namespace"]}
        for proj in data.get("items", [])
    ]

    return {"projects": projects}

