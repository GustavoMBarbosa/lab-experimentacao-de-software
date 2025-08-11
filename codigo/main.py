import requests
import json
import csv 
from datetime import datetime, timezone
import time

# confirugações
TOKEN = ("Token") # Token do GitHub não compartilhe publicamente
URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Query GraphQL
query = """
query ($cursor: String) {
  search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: 100, after: $cursor) {
    nodes {
      ... on Repository {
        name
        owner { login }
        stargazerCount
        updatedAt
        primaryLanguage { name }
        issues { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

def fetch_repositories(max_repos=1000):
    """
    Faz requisições paginadas à API GitHub GraphQL para coletar dados de repositórios.
    
    args:
        max_repos (int): número máximo de repositórios a coletar.
    """
    all_repos = []
    cursor = None

    while True:
        try:
            variables = {"cursor": cursor}
            response = requests.post(URL, json={"query": query, "variables": variables}, headers=HEADERS)

            if response.status_code != 200:
                raise Exception(f"Erro {response.status_code} ao buscar dados: {response.text}")

            data = response.json()["data"]["search"]
            all_repos.extend(data["nodes"])

            print(f"Coletados {len(all_repos)} repositórios até agora...")

            if not data["pageInfo"]["hasNextPage"] or len(all_repos) >= max_repos:
                break

            cursor = data["pageInfo"]["endCursor"]

            time.sleep(1)  # Espera 1 segundo para não saturar a API

        except Exception as e:
            print(f"Erro na requisição: {e}")
            print("Tentando novamente em 10 segundos...")
            time.sleep(10)
            # continua o loop para tentar de novo

    return all_repos[:max_repos]

def save_to_csv(repos, filename="repositorios_1000.csv"):
    """
    Salva os dados coletados em arquivo CSV.
    
    args:
        repos (list): lista de repositórios coletados.
    """
    now = datetime.now(timezone.utc)

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Cabeçalho
        writer.writerow([
            "Owner", "Name", "Stars", "DiasDesdeAtualizacao",
            "LinguagemPrincipal", "TotalIssues", "ClosedIssues", "PercentualIssuesFechadas"
        ])

        for r in repos:
            total_issues = r["issues"]["totalCount"]
            closed_issues = r["closedIssues"]["totalCount"]
            pct_closed = (closed_issues / total_issues * 100) if total_issues > 0 else 0

            updated_at = datetime.fromisoformat(r["updatedAt"].replace("Z", "+00:00"))
            delta_days = (now - updated_at).days

            writer.writerow([
                r["owner"]["login"],
                r["name"],
                r["stargazerCount"],
                delta_days,
                r["primaryLanguage"]["name"] if r["primaryLanguage"] else "N/A",
                total_issues,
                closed_issues,
                f"{pct_closed:.2f}"
            ])

def main():
    print("Iniciando coleta dos 1000 repositórios mais populares no GitHub...")
    repos = fetch_repositories(1000) # Quantidade de repositórios a coletar
    print(f"Coleta finalizada! Total de repositórios coletados: {len(repos)}")

    print("Salvando dados em CSV...")
    save_to_csv(repos)
    print("Arquivo 'repositorios_1000.csv' salvo com sucesso.")

if __name__ == "__main__":
    main()