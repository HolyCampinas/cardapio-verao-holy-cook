# Como regenerar

1. Exportar as fichas para `fichas.json` (query em `cmv_produtos` + `cmv_fichas_ingredientes`, campos
   `nome, preco_venda, cmv_unitario, nome_insumo, quantidade, unidade, custo_unitario, ordem`, ordenado por nome e ordem).
2. Ajustar a lista `PROD` no topo de `build.py` (preço iFood/99, canais, pendências, foto).
3. `python3 gerador/build.py gerador/fichas.json index.html`
