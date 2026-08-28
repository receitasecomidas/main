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
| `testada` | não | `true` marca "Já fiz" e entra na aba correspondente. Também dá pra marcar/desmarcar direto no app, tocando na etiqueta na página da receita — mas isso fica só no navegador de quem tocou (ver abaixo) |

Só `titulo` é obrigatório — todo o resto é opcional.

### Ligar uma receita a outra

Link com o nome do arquivo (sem `.md`) vira link interno:

```markdown
Usa o [molho para teriyaki](washoku-molho-teriyaki).
```

## Calculadora de quantidades

Cada receita tem um seletor **½ receita / 1 receita / 2 receitas**, mais um campo livre para
qualquer multiplicador (`1,5`, `3`, `0,25`). As quantidades recalculadas aparecem em destaque,
e o rendimento acompanha.

A regra é escalar **só a quantidade que abre cada linha de ingrediente**, que é como as receitas
são escritas: `500 ml de água`, `99 g bread flour`. Isso é proposital — em
`1 pedaço de alga kombu de uns 5 cm`, dobrar a receita dobra o número de pedaços, não o tamanho
de cada um.

Por consequência, dois lugares **não** são recalculados:

- números no meio da linha, inclusive entre parênteses;
- o modo de preparo, porque tempo e temperatura não escalam junto com a quantidade.

O seletor avisa isso na tela quando o fator é diferente de 1.

A calculadora entende inteiro (`500`), decimal com ponto ou vírgula (`1.2`, `1,5`), fração
(`1/2`), fração unicode (`½`), mista (`1 ½`) e faixa (`2 a 3`, `3-4`). Na saída, só usa as
frações que se medem numa cozinha — ½ ⅓ ⅔ ¼ ¾ — e a partir de 10 passa a decimal, porque
`49,5 g` se pesa e `49½ g` não.

Como escala o número e não a palavra, a concordância pode ficar torta (`2 pedaço`). Preferi
isso a errar quantidade.

## Favoritos, "já fiz" e anotações — ficam só no seu navegador

O site não tem backend: publicado no GitHub Pages, não tem como um clique salvar nada de
volta no repositório. Três coisas usam `localStorage` do navegador em vez disso:

- **Favoritos** — o coração no card e na receita.
- **Já fiz** — a etiqueta na página da receita agora é um botão; tocar marca ou desmarca,
  sobrepondo o `testada` do `.md` só ali. O `.md` continua sendo o padrão de quem nunca tocou.
- **Anotações** — campo de texto livre no fim da receita, salvo sozinho (com um pequeno atraso
  enquanto você digita, pra não gravar a cada letra).

As três valem **por aparelho e por navegador** — não sincronizam entre celular e computador, e
somem se limpar os dados do site. Para uma nota ou marcação que todo mundo vê, e que sobrevive
a isso, edite o `.md` da receita no GitHub: `testada: true` no cabeçalho, ou uma seção
`## Minhas notas` no corpo.

O botão de WhatsApp manda a receita inteira — ingredientes e modo de preparo, já escalados se
você tiver ajustado a quantidade — não só o link.

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
veio.

As receitas de ramen estão no inglês original (`idioma: en`) para não introduzir erro de
tradução nas medidas.

Se você é autor de alguma receita listada e quer correção de crédito ou remoção,
[abra uma issue](https://github.com/receitasecomidas/main/issues).

## App Android (APK)

O mesmo site empacotado como app, via [Capacitor](https://capacitorjs.com/): o `index.html`
e o `dados/receitas.json` vão dentro do APK, então o app funciona **sem internet** — útil na
cozinha, onde o wifi nem sempre chega.

**Para gerar um APK:** na aba **Actions** deste repositório, abra **Gerar APK Android** →
**Run workflow**. Em alguns minutos o resultado fica disponível como *artifact* na página
da execução — baixe o `.zip`, extraia o `.apk` e abra no celular. O Android vai pedir
permissão para instalar de fora da Play Store; é esperado, é assim que qualquer APK fora
da loja se instala.

O gatilho é manual de propósito — não dispara sozinho a cada receita nova, porque um build
Android gasta minutos de Actions e a maioria dos commits aqui é só um `.md` novo. Rode de novo
sempre que quiser as receitas mais recentes no celular; o comentário no início do
`.github/workflows/android-apk.yml` mostra como trocar para automático, se preferir.

Os builds usam uma chave de debug fixa (`mobile/debug.keystore`, commitada de propósito —
chave de debug não é segredo) para que instalar um APK novo por cima do antigo funcione sem
precisar desinstalar primeiro.

Para trocar nome do app, ícone ou o identificador do pacote, edite dentro de `mobile/`
(`capacitor.config.json`, `mobile/android/app/src/main/res/mipmap-*`) — é um projeto Android
normal, abre no Android Studio se quiser ir além do que o workflow cobre.

## Estrutura

```
index.html                    página única (React via CDN, sem build)
receitas/*.md                 uma receita por arquivo
scripts/build_index.py        lê receitas/ e gera dados/receitas.json
dados/receitas.json           gerado — não edite à mão
.github/workflows/pages.yml   regenera o índice e publica no Pages
mobile/                       projeto Capacitor/Android — vira o APK
.github/workflows/android-apk.yml   builda o APK sob demanda
```
