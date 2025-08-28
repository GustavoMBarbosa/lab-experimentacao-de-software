import csv
import statistics as stats
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import math

# ==========================
# Configurações do relatório
# ==========================
INPUT_CSV = "repositorios_1000.csv"
SUMARIO_CSV = "sumario_metricas.csv"
RQ07_CSV = "rq07_por_linguagem.csv"
TOP_N_POP_LANGS = 10

# ==========================
# Leitura e tipos
# ==========================
@dataclass
class RepoRow:
    owner: str
    name: str
    stars: Optional[float]
    idade_meses: Optional[float]       # RQ01
    prs_mes: Optional[float]           # RQ02
    releases_mes: Optional[float]      # RQ03
    dias_desde_update: Optional[float] # RQ04
    linguagem: str                     # RQ05
    total_issues: Optional[float]
    closed_issues: Optional[float]
    pct_issues_fechadas: Optional[float]  # RQ06

def _to_float(x: str) -> Optional[float]:
    if x is None:
        return None
    x = str(x).strip().replace(",", ".")
    if x == "" or x.upper() == "N/A":
        return None
    try:
        return float(x)
    except ValueError:
        return None

def ler_csv(path: str) -> List[RepoRow]:
    rows: List[RepoRow] = []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for line in r:
            rows.append(
                RepoRow(
                    owner=line.get("Owner",""),
                    name=line.get("Name",""),
                    stars=_to_float(line.get("Stars")),
                    idade_meses=_to_float(line.get("IdadeMeses")),
                    prs_mes=_to_float(line.get("PRsMes")),
                    releases_mes=_to_float(line.get("ReleasesMes")),
                    dias_desde_update=_to_float(line.get("DiasDesdeAtualizacao")),
                    linguagem=(line.get("LinguagemPrincipal") or "N/A").strip() or "N/A",
                    total_issues=_to_float(line.get("TotalIssues")),
                    closed_issues=_to_float(line.get("ClosedIssues")),
                    pct_issues_fechadas=_to_float(line.get("PercentualIssuesFechadas")),
                )
            )
    return rows

# ==========================
# Estatísticas auxiliares
# ==========================
def mediana_suave(valores: List[Optional[float]]) -> Optional[float]:
    nums = [v for v in valores if v is not None and not math.isnan(v)]
    if not nums:
        return None
    return stats.median(nums)

def format_opt(x: Optional[float], fmt="{:.2f}"):
    return fmt.format(x) if x is not None else "N/A"

# ==========================
# Cálculos por RQ
# ==========================
def sumarizar_globais(repos: List[RepoRow]) -> Dict[str, Optional[float]]:
    return {
        "RQ01_IdadeMeses_mediana": mediana_suave([r.idade_meses for r in repos]),
        "RQ02_PRsMes_mediana": mediana_suave([r.prs_mes for r in repos]),
        "RQ03_ReleasesMes_mediana": mediana_suave([r.releases_mes for r in repos]),
        "RQ04_DiasDesdeAtualizacao_mediana": mediana_suave([r.dias_desde_update for r in repos]),
        "RQ06_PctIssuesFechadas_mediana": mediana_suave([r.pct_issues_fechadas for r in repos]),
    }

def contagem_linguagens(repos: List[RepoRow]) -> Counter:
    return Counter([r.linguagem for r in repos])

def rq07_por_linguagem(repos: List[RepoRow], top_n: int = TOP_N_POP_LANGS
                       ) -> Tuple[List[Tuple[str,int]], Dict[str,Dict[str,Optional[float]]]]:
    """
    Retorna:
      - lista de linguagens populares (top_n por contagem) [(linguagem, contagem), ...]
      - dicionário: linguagem -> { 'PRsMes_mediana', 'ReleasesMes_mediana', 'DiasDesdeAtualizacao_mediana' }
    """
    cont = contagem_linguagens(repos)
    populares = cont.most_common(top_n)

    por_linguagem: Dict[str, Dict[str, Optional[float]]] = {}
    grupos: Dict[str, List[RepoRow]] = defaultdict(list)
    for r in repos:
        grupos[r.linguagem].append(r)

    for lang, _ in populares:
        grp = grupos.get(lang, [])
        por_linguagem[lang] = {
            "PRsMes_mediana": mediana_suave([x.prs_mes for x in grp]),
            "ReleasesMes_mediana": mediana_suave([x.releases_mes for x in grp]),
            "DiasDesdeAtualizacao_mediana": mediana_suave([x.dias_desde_update for x in grp]),
        }

    return populares, por_linguagem

# ==========================
# Escrita de saídas (CSV/Markdown)
# ==========================
def salvar_sumario_csv(sumario: Dict[str, Optional[float]], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Métrica", "Mediana"])
        for k, v in sumario.items():
            w.writerow([k, format_opt(v)])

def salvar_rq07_csv(populares: List[Tuple[str,int]],
                    por_ling: Dict[str,Dict[str,Optional[float]]],
                    path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Linguagem", "Repos", "PRsMes_mediana", "ReleasesMes_mediana", "DiasDesdeAtualizacao_mediana"])
        for lang, count in populares:
            met = por_ling.get(lang, {})
            w.writerow([
                lang, count,
                format_opt(met.get("PRsMes_mediana")),
                format_opt(met.get("ReleasesMes_mediana")),
                format_opt(met.get("DiasDesdeAtualizacao_mediana")),
            ])

# ==========================
# Pipeline principal
# ==========================
def main():
    if not Path(INPUT_CSV).exists():
        raise SystemExit(f"Arquivo de entrada não encontrado: {INPUT_CSV}")

    repos = ler_csv(INPUT_CSV)

    # Medianas globais (RQ01–RQ04, RQ06)
    sumario = sumarizar_globais(repos)
    salvar_sumario_csv(sumario, SUMARIO_CSV)

    # RQ05 — contagem por linguagem
    cont = contagem_linguagens(repos)

    # RQ07 — por linguagem (Top-N populares por contagem)
    populares, por_ling = rq07_por_linguagem(repos, top_n=TOP_N_POP_LANGS)
    salvar_rq07_csv(populares, por_ling, RQ07_CSV)

    print(f"OK! Gerados:\n- {SUMARIO_CSV}\n- {RQ07_CSV}")

if __name__ == "__main__":
    main()
