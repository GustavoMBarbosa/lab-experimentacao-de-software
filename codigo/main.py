import requests
import json

TOKEN = ("TOKEN") # Token do github
URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Query GraphQL
query = """
{
  search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        owner {
          login
        }
        stargazerCount
        updatedAt
        primaryLanguage {
          name
        }
        issues {
          totalCount
        }
        closedIssues: issues(states: CLOSED) {
          totalCount
        }
      }
    }
  }
}
"""

def main():
    response = requests.post(URL, json={"query": query}, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        repos = data["data"]["search"]["nodes"]

        # Salvar dados para analise
        with open("repositorios_100.json", "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=2, ensure_ascii=False)

        # Mostrar resumo dos 5 primeiros repositórios
        for r in repos[:5]:
            total_issues = r["issues"]["totalCount"]
            closed_issues = r["closedIssues"]["totalCount"]
            pct_closed = (closed_issues / total_issues * 100) if total_issues > 0 else 0

            print(f"{r['owner']['login']}/{r['name']}")
            print(f"  Stars: {r['stargazerCount']}")
            print(f"  Última atualização (RQ4): {r['updatedAt']}")
            print(f"  Linguagem principal (RQ5): {r['primaryLanguage']['name'] if r['primaryLanguage'] else 'N/A'}")
            print(f"  % Issues Fechadas (RQ6): {pct_closed:.2f}%")
            print("-" * 50)

    else:
        print(f"Erro {response.status_code}: {response.text}")

if __name__ == "__main__":

    main()
