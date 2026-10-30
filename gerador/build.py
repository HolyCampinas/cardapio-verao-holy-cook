import json, sys, html
rows = json.load(open(sys.argv[1])); out = sys.argv[2]
# nome, ifood, canais, pendencias, grupo, foto
PROD = [
 ("Milk Shake Oreo", 41.90, "Loja · iFood · 99", [], "Bebidas", "milkshake-oreo.jpg"),
 ("Frozen Maracomanga", 26.90, "Loja · iFood · 99", ["Salt Cream feito na loja (lote R$ 13,68 rende ~586 g); sal ainda sem preço e creme de leite 35% a confirmar"], "Bebidas", "frozen-maracomanga.jpg"),
 ("Suco de Laranja com Morango", None, "Só na loja", ["Suco de laranja a R$ 13/L provisório — levantar preço real"], "Bebidas", "suco-laranja-morango.jpg"),
 ("Sorvete Pequeno", None, "Só na loja · 1 sabor", ["Servido no copo de café", "Sabor à escolha (Cookie com Nutella ou Red Velvet) — mesmo custo"], "Sorvetes", "sorvete.jpg"),
 ("Sorvete Grande", None, "Só na loja · 1 sabor", ["Pote de 200 g a R$ 0,32 provisório", "Confirmar se 150 g cabem no pote", "Sabor à escolha (Cookie com Nutella ou Red Velvet) — mesmo custo"], "Sorvetes", "sorvete.jpg"),
 ("Cookie Sandwich Nutella", 32.90, "Loja · iFood · 99", [], "Cookies", "cookie-sandwich-nutella.jpg"),
 ("Cookie Sandwich Red Velvet", 32.90, "Loja · iFood · 99", [], "Cookies", "cookie-sandwich-red-velvet.jpg"),
 ("Cookie Fries P", None, "Só na loja", [], "Cookies", "cookie-fries.jpg"),
 ("Cookie Fries G", None, "Só na loja", ["Confirmar se a caixinha comporta o dobro de palitos"], "Cookies", "cookie-fries.jpg"),
]
PEND_INS = { "Suco de Laranja Pasteurizado": "provisório", "Pote de Sorvete 200g": "provisório"}
by = {}
for r in rows:
    by.setdefault(r["nome"], {"preco": float(r["preco_venda"]), "cmv": float(r["cmv_unitario"]), "itens": []})["itens"].append(r)
def brl(v): return ("R$ " + f"{v:,.2f}").replace(",", "X").replace(".", ",").replace("X", ".")
def pct(v): return f"{v*100:.1f}%".replace(".", ",")
def qty(q, u): return (f"{q:.4f}").rstrip("0").rstrip(".").replace(".", ",") + " " + u
def sl(p, c): b = p*0.92; return b - b*0.04 - c
def si(p, c): b = p*0.62; return b - b*0.04 - c
def slug(s): return s.lower().replace(" ", "-")
def foto(f, nome, cls):
    if f: return f'<img class="{cls}" src="img/{f}" alt="{html.escape(nome)}" loading="lazy">'
    return f'<div class="{cls} sem-foto" aria-label="sem foto">sem foto</div>'

resumo, cards, g0, g1 = [], [], None, None
for nome, ifood, canais, pend, grupo, f in PROD:
    d = by[nome]; p, c = d["preco"], d["cmv"]
    tag = ' <span class="tag warn">pendente</span>' if any(("provisório" in x or "sem " in x) for x in pend) else ""
    if grupo != g0:
        resumo.append(f'<tr class="grp"><th colspan="8">{grupo}</th></tr>'); g0 = grupo
    ifc = (f'<td class="num gi gs" data-r="ipreco">{brl(ifood)}</td><td class="num gi" data-r="ipct">{pct(c/ifood)}</td><td class="num gi" data-r="isobra">{brl(si(ifood,c))}</td>'
           if ifood else '<td class="na gi gs" colspan="3">não vende</td>')
    resumo.append(f'<tr data-p="{slug(nome)}"><th scope="row"><a href="#{slug(nome)}" data-goto="fichas" class="prod">{foto(f, nome, "mini")}<span>{html.escape(nome)}{tag}</span></a></th>'
                  f'<td class="num gc gs"><b data-r="cmv">{brl(c)}</b></td><td class="num gl gs" data-r="lpreco">{brl(p)}</td><td class="num gl" data-r="lpct">{pct(c/p)}</td><td class="num gl" data-r="lsobra">{brl(sl(p,c))}</td>{ifc}</tr>')
    linhas = []
    for it in d["itens"]:
        q, cu = float(it["quantidade"]), float(it["custo_unitario"])
        t = PEND_INS.get(it["nome_insumo"]); t = f' <span class="tag warn">{t}</span>' if t else ""
        cus = f'{cu:.6f}'.rstrip("0")
        if len(cus.split(".")[1]) < 2: cus = f'{cu:.2f}'
        cus = cus.replace(".", ",")
        qs = (f"{q:.4f}").rstrip("0").rstrip(".").replace(".", ",")
        linhas.append(f'<tr class="ing"><td>{html.escape(it["nome_insumo"])}{t}</td>'
                      f'<td class="num"><span class="inp"><input inputmode="decimal" class="q" value="{qs}" data-orig="{qs}" aria-label="quantidade"><i>{it["unidade"]}</i></span></td>'
                      f'<td class="num"><span class="inp"><i>R$</i><input inputmode="decimal" class="u" value="{cus}" data-orig="{cus}" aria-label="preço por {it["unidade"]}"></span></td>'
                      f'<td class="num tot">{brl(q*cu)}</td></tr>')
    def ch(key, label, preco, sob, cls):
        ps = f"{preco:.2f}".replace(".", ","); cs = f"{c/preco*100:.1f}".replace(".", ",")
        return (f'<div class="kpi {cls}" data-ch="{key}"><span>{label}</span>'
                f'<label class="row">Preço <span class="inp big"><i>R$</i><input inputmode="decimal" class="preco" value="{ps}" data-orig="{ps}"></span></label>'
                f'<label class="row">CMV <span class="inp"><input inputmode="decimal" class="pct" value="{cs}"><i>%</i></span></label>'
                f'<small>sobra <b class="sobra">{brl(sob)}</b></small></div>')
    kp = f'<div class="kpi kc"><span>CMV</span><b data-k="cmv">{brl(c)}</b><small class="orig">sistema: {brl(c)}</small></div>'
    kp += ch("l", "Loja", p, sl(p,c), "kl")
    kp += (ch("i", "iFood / 99", ifood, si(ifood,c), "ki") if ifood else '<div class="kpi muted ki"><span>iFood / 99</span><b>—</b><small>não vende</small></div>')
    pend_html = ("<ul class='pend'>" + "".join(f"<li>{html.escape(x)}</li>" for x in pend) + "</ul>") if pend else ""
    sec = f'<h2 class="grp-t">{grupo}</h2>' if grupo != g1 else ""; g1 = grupo
    cards.append(f'''{sec}<article class="card" id="{slug(nome)}" data-p="{slug(nome)}">
 {foto(f, nome, "foto")}
 <div class="body"><header><h3>{html.escape(nome)} <span class="tag ed" hidden>simulando</span></h3><span class="canais">{canais}<button class="reset" type="button" hidden>restaurar</button></span></header>
 <div class="kpis">{kp}</div>
 <div class="tw"><table><thead><tr><th>Insumo</th><th class="num">Qtd</th><th class="num">Preço por unidade de medida</th><th class="num">Total</th></tr></thead>
 <tbody>{"".join(linhas)}</tbody><tfoot><tr><th colspan="3">CMV total</th><th class="num" data-k="cmv">{brl(c)}</th></tr></tfoot></table></div>
 {pend_html}</div></article>''')

T = {"l": "--c-cmv:#f1ece6;--c-loja:#e8f1e6;--c-loja-h:#2f6b2a;--c-if:#fbe9e7;--c-if-h:#b3261e;--sep:#c9b9a8;--bg:#faf7f2;--surface:#fff;--ink:#2b2118;--muted:#7a6a5c;--line:#eadfd3;--accent:#8a4b1f;--warn-bg:#fff1d6;--warn:#8a5a00;--grp:#f3ebe1",
     "d": "--c-cmv:#2a231c;--c-loja:#1c2a1b;--c-loja-h:#8fd18a;--c-if:#2e1c1a;--c-if-h:#f2a49c;--sep:#5a4a3b;--bg:#17120e;--surface:#211a14;--ink:#f1e8de;--muted:#b3a291;--line:#3a2f25;--accent:#e0a36f;--warn-bg:#3d2e10;--warn:#f0c46a;--grp:#2a2119"}
page = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cardápio de Verão Holy Cook</title>
<meta name="description" content="Fichas técnicas, CMV e preços propostos do cardápio de verão 2026/27.">
<style>
:root{{{T["l"]}}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{{T["d"]}}}}}
:root[data-theme="dark"]{{{T["d"]}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
main{{max-width:1040px;margin:0 auto;padding:28px 16px 64px}}
h1{{font-size:28px;margin:0 0 4px}} h3{{font-size:18px;margin:0}}
.grp-t{{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:28px 0 10px}}
.sub{{color:var(--muted);margin:0 0 18px}}
.tabs{{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-bottom:20px;position:sticky;top:0;background:var(--bg);z-index:2;padding-top:6px}}
.tabs button{{font:inherit;font-weight:600;background:none;border:0;border-bottom:3px solid transparent;color:var(--muted);padding:10px 14px;cursor:pointer}}
.tabs button[aria-selected="true"]{{color:var(--ink);border-bottom-color:var(--accent)}}
[role=tabpanel][hidden]{{display:none}}
.note{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;color:var(--muted);font-size:13.5px;margin-bottom:16px}}
.note b{{color:var(--ink)}}
.tw{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
table{{width:100%;border-collapse:collapse;background:var(--surface);font-size:14px}}
th,td{{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}}
thead th{{font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);font-weight:600}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.na{{text-align:center;color:var(--muted);font-style:italic}}
tr.grp th{{background:var(--grp);font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
tbody th{{font-weight:600}} a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
.resumo{{border:1px solid var(--line);border-radius:10px}}
.gs{{border-left:3px solid var(--sep)}}
td.gc,th.gc{{background:var(--c-cmv)}} td.gl,th.gl{{background:var(--c-loja)}} td.gi,th.gi{{background:var(--c-if)}}
th.band{{text-align:center;font-size:13px;letter-spacing:.06em;color:var(--ink)}}
th.band.gl{{color:var(--c-loja-h)}} th.band.gi{{color:var(--c-if-h)}}
tr.grp th{{border-left:0}}
.prod{{display:flex;align-items:center;gap:10px}}
.mini{{width:40px;height:40px;border-radius:8px;object-fit:cover;flex:none;background:var(--grp)}}
.tag{{display:inline-block;font-size:11px;font-weight:600;padding:1px 7px;border-radius:99px;margin-left:6px;vertical-align:1px}}
.warn{{background:var(--warn-bg);color:var(--warn)}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:grid;grid-template-columns:220px 1fr;margin-bottom:16px;scroll-margin-top:64px}}
.foto{{width:100%;height:100%;min-height:220px;object-fit:cover;background:var(--grp)}}
.sem-foto{{display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:13px}}
.mini.sem-foto{{font-size:9px;text-align:center}}
.body{{padding:16px;min-width:0}}
.card header{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;align-items:baseline;margin-bottom:12px}}
.canais{{color:var(--muted);font-size:13px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:12px}}
.kpi{{border:1px solid var(--line);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column}}
.kpi span{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}}
.kpi b{{font-size:20px;font-variant-numeric:tabular-nums}} .kpi small{{color:var(--muted);font-size:12.5px}}
.kpi.muted b{{color:var(--muted)}}
.card table{{border:1px solid var(--line)}}
tfoot th{{border-bottom:0}}
.inp{{display:inline-flex;align-items:center;gap:3px;border:1px solid var(--line);border-radius:6px;padding:2px 6px;background:var(--bg)}}
.inp:focus-within{{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 25%,transparent)}}
.inp input{{font:inherit;color:var(--ink);background:none;border:0;outline:0;width:64px;text-align:right;padding:2px 0;font-variant-numeric:tabular-nums}}
.inp i{{font-style:normal;color:var(--muted);font-size:12px}}
.inp.big input{{font-size:18px;font-weight:700;width:76px}}
.kpi .row{{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12.5px;color:var(--muted);margin-top:6px}}
.kpi.kl{{background:var(--c-loja)}} .kpi.ki{{background:var(--c-if)}} .kpi.kc{{background:var(--c-cmv)}}
.kpi .orig{{margin-top:auto}}
input.chg{{color:var(--accent);font-weight:700}}
.tag.ed{{background:var(--accent);color:var(--surface)}}
[hidden]{{display:none!important}}
.reset{{margin-left:8px;font:inherit;font-size:12.5px;background:none;border:1px solid var(--line);border-radius:6px;padding:1px 8px;color:var(--accent);cursor:pointer}}
.pend{{margin:12px 0 0;padding:10px 14px 10px 30px;background:var(--warn-bg);color:var(--warn);border-radius:8px;font-size:13.5px}}
@media (max-width:640px){{.card{{grid-template-columns:1fr}}.foto{{height:240px;min-height:0}}}}
footer{{margin-top:40px;color:var(--muted);font-size:12.5px}}
</style></head><body><main>
<h1>Cardápio de Verão</h1>
<p class="sub">Vendas de 06/11/2026 a fev/2027 · atualizado em 30/10/2026</p>
<div class="tabs" role="tablist">
 <button role="tab" id="t-fichas" aria-controls="fichas" aria-selected="true">Fichas técnicas</button>
 <button role="tab" id="t-resumo" aria-controls="resumo" aria-selected="false">Resumo</button>
</div>
<section role="tabpanel" id="fichas" aria-labelledby="t-fichas">
<div class="note"><b>Simulador:</b> quantidade, R$/un, preço e CMV % são editáveis. Mudou o preço, o CMV % acompanha; mudou o CMV %, o preço acompanha. As mudanças ficam só na sua tela, não alteram o sistema e somem ao recarregar a página.</div>
{"".join(cards)}
</section>
<section role="tabpanel" id="resumo" aria-labelledby="t-resumo" hidden>
<div class="note"><b>Sobra</b> = o que fica por unidade depois do CMV, 8% de imposto e 4% de royalties (sobre o valor já sem imposto e sem plataforma). No iFood/99 sai também a comissão de 30%.</div>
<div class="tw resumo"><table>
<thead><tr class="bands"><th rowspan="2" class="pcol">Produto</th><th class="band gc gs" rowspan="2">CMV</th><th class="band gl gs" colspan="3">Loja</th><th class="band gi gs" colspan="3">iFood / 99</th></tr>
<tr><th class="num gl gs">Preço</th><th class="num gl">CMV %</th><th class="num gl">Sobra</th><th class="num gi gs">Preço</th><th class="num gi">CMV %</th><th class="num gi">Sobra</th></tr></thead>
<tbody>{"".join(resumo)}</tbody></table></div>
</section>
<footer>Holy Cook · fichas do sistema em 30/10/2026. Fotos da ficha técnica da franquia.</footer>
</main>
<script>
const tabs=[...document.querySelectorAll('[role=tab]')];
function show(id,push){{tabs.forEach(t=>{{const on=t.getAttribute('aria-controls')===id;t.setAttribute('aria-selected',on);document.getElementById(t.getAttribute('aria-controls')).hidden=!on;}});
 if(push){{try{{history.replaceState(null,'','#'+id)}}catch(e){{}}}}}}
tabs.forEach(t=>t.addEventListener('click',()=>show(t.getAttribute('aria-controls'),true)));
document.querySelectorAll('[data-goto]').forEach(a=>a.addEventListener('click',()=>show('fichas',false)));
if(location.hash==='#resumo')show('resumo',false);
const num=v=>{{v=String(v).trim().replace(/[^0-9,.-]/g,'');if(v.includes(','))v=v.replace(/\./g,'').replace(',','.');const n=parseFloat(v);return isNaN(n)?0:n}};
const brl=v=>'R$ '+v.toLocaleString('pt-BR',{{minimumFractionDigits:2,maximumFractionDigits:2}});
const f2=v=>v.toLocaleString('pt-BR',{{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:false}});
const f1=v=>v.toLocaleString('pt-BR',{{minimumFractionDigits:1,maximumFractionDigits:1,useGrouping:false}});
const NET={{l:0.92*0.96,i:0.62*0.96}};
document.querySelectorAll('article.card').forEach(card=>{{
 const id=card.dataset.p, row=document.querySelector('#resumo tr[data-p="'+id+'"]');
 const set=(k,v)=>{{const e=row&&row.querySelector('[data-r="'+k+'"]');if(e)e.textContent=v}};
 let cmv=0;
 function calcCmv(){{cmv=0;card.querySelectorAll('tr.ing').forEach(tr=>{{const t=num(tr.querySelector('.q').value)*num(tr.querySelector('.u').value);cmv+=t;tr.querySelector('.tot').textContent=brl(t)}});
  card.querySelectorAll('[data-k="cmv"]').forEach(e=>e.textContent=brl(cmv));set('cmv',brl(cmv));}}
 function channel(ch,from){{const box=card.querySelector('[data-ch="'+ch+'"]');if(!box)return;const pi=box.querySelector('.preco'),ci=box.querySelector('.pct');
  let p=num(pi.value);
  if(from==='pct'){{const pc=num(ci.value);if(pc>0){{p=cmv/(pc/100);pi.value=f2(p)}}}}
  else if(document.activeElement!==ci){{ci.value=p>0?f1(cmv/p*100):''}}
  const s=p*NET[ch]-cmv;box.querySelector('.sobra').textContent=brl(s);
  set(ch+'preco',brl(p));set(ch+'pct',p>0?f1(cmv/p*100)+'%':'—');set(ch+'sobra',brl(s));}}
 function mark(){{let ed=false;card.querySelectorAll('input[data-orig]').forEach(i=>{{const c=num(i.value)!==num(i.dataset.orig);i.classList.toggle('chg',c);ed=ed||c}});
  card.querySelector('.tag.ed').hidden=!ed;card.querySelector('.reset').hidden=!ed;}}
 function all(from,ch){{calcCmv();['l','i'].forEach(c=>channel(c,c===ch?from:'preco'));mark()}}
 card.querySelectorAll('tr.ing input').forEach(i=>i.addEventListener('input',()=>all('preco')));
 card.querySelectorAll('[data-ch]').forEach(box=>{{const ch=box.dataset.ch;
  box.querySelector('.preco').addEventListener('input',()=>all('preco',ch));
  box.querySelector('.pct').addEventListener('input',()=>all('pct',ch));
  box.querySelector('.pct').addEventListener('blur',()=>all('preco',ch));}});
 card.querySelector('.reset').addEventListener('click',()=>{{card.querySelectorAll('input[data-orig]').forEach(i=>i.value=i.dataset.orig);all('preco')}});
 card.querySelectorAll('input').forEach(i=>i.addEventListener('focus',()=>i.select()));
}});
</script>
</body></html>'''
open(out, "w", encoding="utf-8").write(page); print("ok", len(page))
