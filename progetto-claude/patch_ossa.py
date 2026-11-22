# patch_ossa.py <cartella sito> : SCHELETRO2 (22.11.2026) - quando Zeta scheletro va KO le ossa schizzano e restano sparse a terra.
import sys, os
d = sys.argv[1]; p = d + '/index.html'; s = open(p, encoding='utf8').read()
if 'SCHELETRO2' in s: sys.exit('gia SCHELETRO2')
assert 'SCHELETRO1' in s

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

A = "// niente trasformazioni per i mostri: sono già la loro forma"
rep(A, r"""/*SCHELETRO2 (22.11.2026) - ordine dell'Avvocato: "quando perde le ossa si devono spargere". Al KO di Zeta scheletro
   le ossa (immagini ChatGPT osso1..osso10 del pacco) schizzano dal corpo, rimbalzano e restano a terra fino al round dopo. */
const OSSA=[];
function ossaSpargi(f){ const M=mostriSP.im&&mostriSP.im.zeta_scheletro; if(!M) return; const S=(196/128)*(f.def.size||1), dir=f.facing||1;
  const nomi=['osso1','osso2','osso3','osso4','osso5','osso6','osso7','osso8','osso9','osso10','osso11','osso1','osso3'];
  nomi.forEach((k,i)=>{ const im=M[k]; if(!im||!im.complete||!im.width) return; const a=-Math.PI/2+(Math.random()-0.5)*2.6;
    const v=7+Math.random()*9; OSSA.push({k,x:f.x+(Math.random()-0.5)*40*S,y:f.y-(30+Math.random()*90)*S,vx:Math.cos(a)*v-dir*1.5,vy:Math.sin(a)*v-3,
      r:Math.random()*6.28,vr:(Math.random()-0.5)*0.5,S:S*0.95,ferma:0,rimb:0}); });
  try{ G.shake=Math.max(G.shake||0,14); }catch(e){} }
function ossaStep(){ for(const o of OSSA){ if(o.ferma) continue; o.vy+=0.55; o.x+=o.vx; o.y+=o.vy; o.r+=o.vr;
    if(o.x<20){ o.x=20; o.vx=Math.abs(o.vx)*0.5; } if(o.x>W-20){ o.x=W-20; o.vx=-Math.abs(o.vx)*0.5; }
    if(o.y>GROUND-6){ o.y=GROUND-6; o.rimb++; if(Math.abs(o.vy)<2.2||o.rimb>3){ o.vy=0; o.vx*=0.6; o.vr*=0.5; if(Math.abs(o.vx)<0.3){ o.ferma=1; o.r=Math.round(o.r/Math.PI)*Math.PI+(o.r%0.5); } }
      else { o.vy=-o.vy*0.42; o.vx*=0.75; o.vr=-o.vr*0.7; } } } }
function drawOssa(){ if(!OSSA.length) return; const M=mostriSP.im&&mostriSP.im.zeta_scheletro; if(!M) return;
  ctx.save(); ctx.imageSmoothingEnabled=false;
  for(const o of OSSA){ const im=M[o.k]; if(!im||!im.width) continue; const w=im.width*o.S, h=im.height*o.S;
    ctx.save(); ctx.translate(o.x,o.y-(o.ferma?h*0.2:0)); ctx.rotate(o.r); ctx.drawImage(im,-w/2,-h/2,w,h); ctx.restore(); }
  ctx.restore(); }
{ const _stO=step; step=function(){ const r=_stO.apply(this,arguments); try{ for(const f of [G&&G.f1,G&&G.f2]){ if(!f||!f.def||f.def.base!=='Zeta scheletro') continue;
      if(f.state==='ko'&&!f._ossa){ f._ossa=1; ossaSpargi(f); } else if(f.state!=='ko') f._ossa=0; } ossaStep(); }catch(e){} return r; }; }
{ const _dfO=drawFighter; drawFighter=function(g,F){ const r=_dfO.apply(this,arguments); try{ if(g===ctx&&F&&F.def&&F.def.base==='Zeta scheletro'&&G&&(F===G.f1||F===G.f2)) drawOssa(); }catch(e){} return r; }; }
{ const _rrO=resetRound; resetRound=function(){ OSSA.length=0; return _rrO.apply(this,arguments); }; }
""" + A)
open(p, 'w', encoding='utf8').write(s); print('SCHELETRO2 ok')
