# Laboratório 01 — Características de repositórios populares
## Introdução e hipóteses informais
- **RQ01 (Idade em meses):** espera-se mediana relativamente alta, indicando que repositórios populares tendem a ser maduros.
- **RQ02 (PRs/mês):** espera-se mediana > 0, sugerindo fluxo contínuo de contribuições externas.
- **RQ03 (Releases/mês):** espera-se uma mediana baixa porém positiva, pois muitos projetos fazem releases mensais ou trimestrais.
- **RQ04 (Dias desde última atualização):** espera-se mediana baixa, sinalizando atividade recente.
- **RQ05 (Linguagem primária):** espera-se concentração em algumas linguagens populares, como python.
- **RQ06 (% issues fechadas):** espera-se mediana alta, pois projetos populares tendem a fechar uma boa fração das issues.

## Metodologia
Coletamos 1.000 repositórios com mais estrelas no GitHub via GraphQL (consulta própria), capturando:
- `createdAt` (para idade em meses — RQ01),
- `pullRequests(states: MERGED) { totalCount }` (para PRs/mês — RQ02),
- `releases { totalCount }` (para Releases/mês — RQ03),
- `updatedAt` (para dias desde a última atualização — RQ04),
- `primaryLanguage` (para contagem por linguagem — RQ05),
- `issues` e `issues(states: CLOSED)` (para % de issues fechadas — RQ06).

Em RQ02 e RQ03, normalizamos por tempo (métricas por mês), dividindo totais pela idade em meses do repositório.

## Resultados (medianas globais)
Total de repositórios analisados: **1000**

| Métrica | Mediana |
|---|---:|
| RQ01 — Idade (meses) | 100.50 |
| RQ02 — PRs/mês | 8.32 |
| RQ03 — Releases/mês | 0.41 |
| RQ04 — Dias desde a última atualização | 0.00 |
| RQ06 — % issues fechadas | 85.41 |

### RQ05 — Contagem por linguagem (Top 10)
| Linguagem | Repositórios |
|---|---:|
| Python | 188 |
| TypeScript | 156 |
| JavaScript | 130 |
| N/A | 104 |
| Go | 73 |
| Java | 50 |
| C++ | 48 |
| Rust | 45 |
| C | 25 |
| Jupyter Notebook | 22 |

## Discussão
- **Maturidade (RQ01):** conforme esperado, grande parte dos repositórios analisados são maduros, passando de 80 ou até mesmo 100 meeses desde sua criação.
- **Contribuições externas (RQ02):** a quantidade de PRs/mês medianos é de aproximadamente 8.32, sinalizando participação ativa da comunidade.
- **Releases (RQ03):** a mediana é de fato baixa, porém postiva (0.41), já que, como teorizado, muitos projetos fazem releases mensais ou trimestrais.
- **Atividade (RQ04):** poucos dias desde a última atualização sustentam a ideia de manutenção contínua.
- **Linguagens (RQ05):** como esperado, python domina como a linguagem mais utilizada. Em geral, o resultado mostra que a maioria dos repositórios utiliza linguagens bem difundidas e conhecidas, o que confirmou as hipóteses prévias.
- **Gestão de issues (RQ06):** de fato, a mediana obtida foi alta. Uma mediana de 85% de issues fechadas sugere triagem ativa e boa governança.

---

## Bônus — RQ07 por linguagem
Comparamos PRs/mês, Releases/mês e dias desde a última atualização por linguagem, considerando as 10 linguagens com mais repositórios.

| Linguagem | PRs/mês (mediana) | Releases/mês (mediana) | Dias desde última atualização (mediana) |
|---|---:|---:|---:|
| Python | 10.59 | 0.42 | 0.00 |
| TypeScript | 29.66 | 1.85 | 0.00 |
| JavaScript | 4.22 | 0.29 | 0.00 |
| N/A | 1.48 | 0.00 | 0.00 |
| Go | 16.66 | 1.58 | 0.00 |
| Java | 6.58 | 0.32 | 0.00 |
| C++ | 11.55 | 0.57 | 0.00 |
| Rust | 38.04 | 0.83 | 0.00 |
| C | 0.96 | 0.30 | 0.00 |
| Jupyter Notebook | 1.71 | 0.00 | 0.00 |

**Discussão:** contrariando o que pensávamos, o número de PRs/mês, releases/mês e dias desde a última atualização não se distribui uniformemente de acordo com a popularidade das linguagens. Por exemplo, esperáva-mos que python, por ser a mais popular, seria a maior nas três categorias, e que o número de cada uma cairia proporcionalmente, mas observamos que é mais irregular do que o teorizado.