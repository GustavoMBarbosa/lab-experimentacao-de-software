import csv
from collections import Counter
import matplotlib.pyplot as plt

# arquivo CSV
filename = "repositorios_1000.csv"

# listas para armazenar os dados
idades = []
prs_mes = []
releases_mes = []
dias_desde_update = []
languages = []
pct_issues_fechadas = []

# ler CSV aqui
with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # RQ01 - Idade em meses
        try:
            idades.append(float(row["IdadeMeses"]))
        except:
            pass

        # RQ02 - Pull requests por mes
        try:
            prs_mes.append(float(row["PRsMes"]))
        except:
            pass

        # RQ03 - Releases por mes
        try:
            releases_mes.append(float(row["ReleasesMes"]))
        except:
            pass

        # RQ04 - Dias desde ultima atualização
        try:
            dias_desde_update.append(float(row["DiasDesdeAtualizacao"]))
        except:
            pass

        # RQ05 - Linguagem principal
        lang = row.get("LinguagemPrincipal", "").strip()
        if lang and lang != "N/A":
            languages.append(lang)

        # RQ06 - Percentual de issues fechadas
        try:
            pct_issues_fechadas.append(float(row["PercentualIssuesFechadas"]))
        except:
            pass

def _save_hist(data, bins, title, xlabel, ylabel, outfile, color=None):
    if not data:
        print(f"[aviso] sem dados para {title}, gráfico não gerado.")
        return
    plt.figure(figsize=(8, 5))
    if color:
        plt.hist(data, bins=bins, edgecolor='black', color=color)
    else:
        plt.hist(data, bins=bins, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close()
    print(f"[ok] salvo: {outfile}")

# RQ01 - Idade do repositório
_ = _save_hist(
    idades, bins=20,
    title="RQ01 — Idade dos repositórios (meses)",
    xlabel="Meses", ylabel="Quantidade de repositórios",
    outfile="rq01_idade_hist.png", color="skyblue"
)

# RQ02 - Pull requests aceitas por mes
_ = _save_hist(
    prs_mes, bins=20,
    title="RQ02 — Pull Requests aceitas por mês",
    xlabel="PRs/mês", ylabel="Quantidade de repositórios",
    outfile="rq02_prs_mes_hist.png", color="green"
)

# RQ03 - Releases por mes
_ = _save_hist(
    releases_mes, bins=20,
    title="RQ03 — Releases por mês",
    xlabel="Releases/mês", ylabel="Quantidade de repositórios",
    outfile="rq03_releases_mes_hist.png", color="orange"
)

# RQ04 - Dias desde ultima atualização
_ = _save_hist(
    dias_desde_update, bins=20,
    title="RQ04 — Dias desde a última atualização",
    xlabel="Dias", ylabel="Quantidade de repositórios",
    outfile="rq04_dias_desde_update_hist.png", color="purple"
)

# RQ05 - Linguagens mais populares (Top 5)
language_counts = Counter(languages)
top5 = language_counts.most_common(5)
if top5:
    langs = [item[0] for item in top5]
    counts = [item[1] for item in top5]

    plt.figure(figsize=(8, 5))
    plt.bar(langs, counts, color='blue')
    plt.title("RQ05 — Top 5 Linguagens Mais Usadas")
    plt.xlabel("Linguagens")
    plt.ylabel("Quantidade de repositórios")
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    plt.savefig("rq05_top5_linguagens.png", dpi=150)
    plt.close()
    print("[ok] salvo: rq05_top5_linguagens.png")
else:
    print("[aviso] sem dados de linguagem para RQ05.")

# RQ06 - Percentual de issues fechadas
_ = _save_hist(
    pct_issues_fechadas, bins=20,
    title="RQ06 — Percentual de issues fechadas",
    xlabel="% de issues fechadas", ylabel="Quantidade de repositórios",
    outfile="rq06_pct_issues_fechadas_hist.png", color="red"
)

# RQ07 - Dois gráficos separados:
# 1 PRs/mes x Releases/mes
# 2 Dias desde atualização
top_languages = [item[0] for item in language_counts.most_common(5)]
if top_languages:
    # calcular as medias por linguagem:
    medias = {} 
    for lang in top_languages:
        lang_prs, lang_rel, lang_dias = [], [], []
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("LinguagemPrincipal", "").strip() == lang:
                    try:
                        lang_prs.append(float(row["PRsMes"]))
                    except:
                        pass
                    try:
                        lang_rel.append(float(row["ReleasesMes"]))
                    except:
                        pass
                    try:
                        lang_dias.append(float(row["DiasDesdeAtualizacao"]))
                    except:
                        pass
        avg_prs = sum(lang_prs)/len(lang_prs) if lang_prs else 0.0
        avg_rel = sum(lang_rel)/len(lang_rel) if lang_rel else 0.0
        avg_dias = sum(lang_dias)/len(lang_dias) if lang_dias else 0.0
        medias[lang] = (avg_prs, avg_rel, avg_dias)

    # ordenar por PRs/mes médio 
    ordenado = sorted(medias.items(), key=lambda kv: kv[1][0], reverse=True)
    langs_ord = [k for k, _ in ordenado]
    prs_ord = [v[0] for _, v in ordenado]
    rel_ord = [v[1] for _, v in ordenado]
    dias_ord = [v[2] for _, v in ordenado]

    # Grafico 1: PRs e Releases 
    idx = list(range(len(langs_ord)))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - width/2 for i in idx], prs_ord, width=width, label="PRs/mês", color="green")
    plt.bar([i + width/2 for i in idx], rel_ord, width=width, label="Releases/mês", color="orange")

    plt.title("RQ07 — PRs e Releases por linguagem (Top 5)")
    plt.xlabel("Linguagens")
    plt.ylabel("Valores médios")
    plt.xticks(idx, langs_ord, rotation=25, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig("rq07_prs_releases.png", dpi=150)
    plt.close()
    print("[ok] salvo: rq07_prs_releases.png")

    # Grafico 2: Dias desde ultima atualização
    plt.figure(figsize=(8, 5))
    plt.bar(langs_ord, dias_ord, color="purple")
    plt.title("RQ07 — Dias desde última atualização (média por linguagem)")
    plt.xlabel("Linguagens")
    plt.ylabel("Dias (média)")
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    plt.savefig("rq07_dias_desde_update.png", dpi=150)
    plt.close()
    print("[ok] salvo: rq07_dias_desde_update.png")
else:
    print("[aviso] sem linguagens para RQ07.")
