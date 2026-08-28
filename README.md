# Receitas e Comidas

Caderno de receitas publicado no GitHub Pages: **https://receitasecomidas.github.io/main/**

Cada receita é um arquivo Markdown em [`receitas/`](receitas/). Um script transforma a pasta
inteira em `dados/receitas.json`, e o `index.html` — página única, sem build, sem framework
instalado — lê esse JSON e monta o site.

## Como anotar uma receita nova

1. Crie um arquivo em `receitas/`, por exemplo `receitas/pao-de-forma.md`.
2. Copie o modelo abaixo e preencha.
3. Commit. O GitHub Actions regenera o índice e publica sozinho.

Dá para fazer tudo pelo navegador ou pelo celular, pela própria interface do GitHub —
não precisa clonar nada.

### Modelo

```markdown
---
titulo: Pão de forma
subtitulo: aquele de todo dia
colecao: Panificação
categoria: pao
cozinha: brasileira
fonte: Receita própria
rendimento: 2 formas
tempo: 4 h
tags: [pao, fermento, forno]
testada: true
---

Um parágrafo curto de apresentação — é ele que aparece no card da listagem.

## Ingredientes

- 500 g de farinha de trigo
- 300 g de água

## Modo de preparo

1. Misture tudo.
2. Deixe fermentar.

## Minhas notas

O que deu certo, o que ajustar da próxima vez.
```

### Campos do cabeçalho

| Campo | Obrigatório | Para que serve |
|---|---|---|
| `titulo` | sim | Nome da receita |
| `titulo_original` | não | Nome na língua de origem (ex: `だし`) |
| `subtitulo` | não | Tradução ou explicação curta |
| `colecao` | não | Agrupa receitas do mesmo caderno/curso. Vira um botão de filtro |
| `categoria` | não | Etiqueta colorida. Os valores conhecidos estão no `CATEGORIAS` do `index.html` |
| `cozinha` | não | Ex: `japonesa`, `brasileira` |
| `fonte` | não | **O crédito.** Aparece no card, na receita e no rodapé |
| `fonte_url` | não | Link da fonte, quando existir |
| `autor` | não | Quem assina a receita |
| `rendimento`, `tempo`, `dificuldade` | não | Aparecem na faixa de metadados |
| `idioma` | não | Use `en` se o conteúdo não estiver em português |
| `tags` | não | Lista: `[a, b, c]` |
| `testada` | não | `true` marca "Já fiz" e entra na aba correspondente |

Só `titulo` é obrigatório — todo o resto é opcional.

### Ligar uma receita a outra

Link com o nome do arquivo (sem `.md`) vira link interno:

```markdown
Usa o [molho para teriyaki](washoku-molho-teriyaki).
```

## Rodar localmente

```bash
python3 scripts/build_index.py   # gera dados/receitas.json
python3 -m http.server 8000      # abre em http://localhost:8000
```

Abrir o `index.html` com clique duplo não funciona: o navegador bloqueia a leitura do JSON
em `file://`. Precisa do servidor local.

O script não tem dependência nenhuma — roda com o Python que já vem no sistema.

## O que tem aqui

O site funciona como recorte de consulta: **só a formulação das receitas** — ingredientes e
modo de preparo — nunca o texto dos materiais de origem. Cada receita carrega a fonte de onde
veio, e o rodapé do site lista todas.

| Coleção | Receitas | Fonte |
|---|---|---|
| Ramen | 85 | *The Ramen_Lord Book of Ramen*, de Mike Satinover e Scott Satinover |
| Washoku | 9 | Apostila do curso Washoku — Culinária Japonesa (Aizome) |
| Sushi | 6 | Apostila do curso avançado de sushi (André) |

As receitas de ramen estão no inglês original (`idioma: en`) para não introduzir erro de
tradução nas medidas.

Se você é autor de alguma receita listada e quer correção de crédito ou remoção,
[abra uma issue](https://github.com/receitasecomidas/main/issues).

## Estrutura

```
index.html                    página única (React via CDN, sem build)
receitas/*.md                 uma receita por arquivo
scripts/build_index.py        lê receitas/ e gera dados/receitas.json
dados/receitas.json           gerado — não edite à mão
.github/workflows/pages.yml   regenera o índice e publica no Pages
```
