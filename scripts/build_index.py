#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le receitas/*.md e gera dados/receitas.json, que e o que o site consome.

Sem dependencia externa de proposito: roda com o Python puro que ja vem
no runner do GitHub Actions e na sua maquina.
"""
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_RECEITAS = os.path.join(RAIZ, "receitas")
SAIDA = os.path.join(RAIZ, "dados", "receitas.json")

# Campos que viram lista mesmo quando escritos como "tags: [a, b]"
LISTAS = {"tags"}
BOOLS = {"testada"}


def frontmatter(texto):
    """Separa o bloco --- ... --- do corpo. YAML de mentira, so o que a gente usa."""
    if not texto.startswith("---"):
        return {}, texto
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}, texto
    bruto = texto[3:fim].strip("\n")
    corpo = texto[fim + 4:].lstrip("\n")

    meta = {}
    for linha in bruto.split("\n"):
        linha = linha.rstrip()
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            continue
        chave, valor = linha.split(":", 1)
        chave = chave.strip()
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1].replace('\\"', '"')
        if chave in LISTAS:
            valor = valor.strip("[]")
            meta[chave] = [v.strip() for v in valor.split(",") if v.strip()]
        elif chave in BOOLS:
            meta[chave] = valor.lower() in ("true", "sim", "yes", "1")
        else:
            meta[chave] = valor
    return meta, corpo


def sem_acento(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def chave_ordem(s):
    """Ordena ignorando aspas e pontuacao inicial, senao \"Cement\" Ramen vem antes de tudo."""
    return re.sub(r'^[^0-9a-z]+', "", sem_acento(s))


def resumo(corpo, limite=180):
    """Primeiro paragrafo de texto corrido, para o card. Ignora titulos e listas."""
    for bloco in corpo.split("\n\n"):
        bloco = bloco.strip()
        if not bloco or bloco.startswith(("#", "-", "*", ">")) or re.match(r"^\d+\.", bloco):
            continue
        bloco = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", bloco)
        bloco = re.sub(r"[*_`]", "", bloco)
        bloco = re.sub(r"\s+", " ", bloco).strip()
        if len(bloco) > limite:
            bloco = bloco[:limite].rsplit(" ", 1)[0] + "..."
        return bloco
    return ""


def conta_ingredientes(corpo):
    dentro = False
    n = 0
    for linha in corpo.split("\n"):
        s = linha.strip()
        if s.startswith("## "):
            dentro = sem_acento(s[3:]).startswith("ingrediente")
            continue
        if dentro and s.startswith("- "):
            n += 1
    return n


def main():
    if not os.path.isdir(DIR_RECEITAS):
        sys.exit("nao achei a pasta receitas/")

    receitas = []
    problemas = []
    for nome in sorted(os.listdir(DIR_RECEITAS)):
        if not nome.endswith(".md"):
            continue
        caminho = os.path.join(DIR_RECEITAS, nome)
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        meta, corpo = frontmatter(texto)
        if not meta.get("titulo"):
            problemas.append(f"{nome}: sem 'titulo' no frontmatter")
            continue

        r = {
            "id": nome[:-3],
            "titulo": meta["titulo"],
            "corpo": corpo.rstrip() + "\n",
            "resumo": resumo(corpo),
            "n_ingredientes": conta_ingredientes(corpo),
        }
        for campo in ("titulo_original", "subtitulo", "colecao", "categoria", "cozinha",
                      "fonte", "fonte_url", "autor", "rendimento", "tempo",
                      "dificuldade", "idioma"):
            if meta.get(campo):
                r[campo] = meta[campo]
        r["tags"] = meta.get("tags", [])
        r["testada"] = bool(meta.get("testada", False))
        # campo de busca ja normalizado, pra nao normalizar no navegador a cada tecla
        r["busca"] = sem_acento(" ".join([
            r["titulo"], r.get("titulo_original", ""), r.get("subtitulo", ""),
            r.get("colecao", ""), r.get("categoria", ""), r.get("cozinha", ""),
            r.get("fonte", ""), " ".join(r["tags"]), corpo,
        ]))
        receitas.append(r)

    if problemas:
        for p in problemas:
            print("AVISO:", p, file=sys.stderr)

    receitas.sort(key=lambda r: chave_ordem(r["titulo"]))

    def valores(campo):
        return sorted({r[campo] for r in receitas if r.get(campo)}, key=sem_acento)

    saida = {
        "receitas": receitas,
        "colecoes": valores("colecao"),
        "categorias": valores("categoria"),
        "cozinhas": valores("cozinha"),
        "fontes": valores("fonte"),
        "total": len(receitas),
    }

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, separators=(",", ":"))

    print(f"{len(receitas)} receitas -> dados/receitas.json")
    for c in saida["colecoes"]:
        print(f"  {c}: {sum(1 for r in receitas if r.get('colecao') == c)}")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
