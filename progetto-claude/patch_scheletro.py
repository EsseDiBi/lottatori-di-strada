# patch_scheletro.py <cartella sito> : SCHELETRO1 (22.11.2026) - Zeta scheletro, miniboss dell'Arcade nel cimitero scozzese.
import sys, shutil, os
d = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__)); p = d + '/index.html'; s = open(p, encoding='utf8').read()
if 'SCHELETRO1' in s: sys.exit('gia SCHELETRO1')
assert 'UOMOPESCE1' in s and 'drsteArcade' in s
shutil.copy(here + '/cimitero.png', d + '/img/arene/cimitero.png')
shutil.copy(here + '/mostri_zeta_scheletro.js', d + '/img/mostri_zeta_scheletro.js')
if os.path.exists(here + '/inc_zeta.jpg'): shutil.copy(here + '/inc_zeta.jpg', d + '/img/vignette/inc_zeta.jpg')

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

# 1) il mostro
A = "PROJ.melma={l:'Sputo Abissale',v:10,d:10}; PROJLBL.melma=PROJ.melma.l;"
rep(A, A + r"""
/*SCHELETRO1*/ MOSTRI['Zeta scheletro']={key:'lds-zetascheletro',pack:'zeta_scheletro',sk:'zeta',code:'scheletro-3e81d7',rk:'teschio',aura:0,msg:'ZETA SCHELETRO ora è un lottatore!',
  nomi:{rangedName:'Teschio da tre',spName:'Sfondamento d\'oltretomba',upName:'Stoppata dalla tomba',superName:'Schiacciata dei morti'},
  p:{base:'Zeta scheletro',size:1.16,special:'Sfondamento d\'oltretomba',superName:'Schiacciata dei morti',accent:'#7dff5a',suit:'#1a1a1f',legs:'#1a1a1f',
     bio:'In tournée in Scozia ha perso una partita a mezzanotte in un cimitero. Ha giocato la rivincita fino all\'alba ed è rimasto lì. Gli occhiali li ha tenuti. Il pallone no: adesso palleggia un teschio.'}};
PROJ.teschio={l:'Teschio da tre',v:9,d:9}; PROJLBL.teschio=PROJ.teschio.l;""")

# 2) tiro a parabola e disegno del teschio (immagine ChatGPT del pacco)
A = "// niente trasformazioni per i mostri: sono già la loro forma"
rep(A, r"""/*SCHELETRO1 teschio*/ { const _spS=spawnProj; spawnProj=function(f){ const n=P.length, r=_spS.apply(this,arguments); try{ for(let i=n;i<P.length;i++){ const q=P[i]; if(q&&q.kind==='teschio'){ q.x=f.x+f.facing*78; q.y=f.y-255; q.vy=-2; q.g=0.2; } } }catch(e){} return r; }; }
{ const _mpS=mostriProj; mostriProj=function(p){ if(p.kind==='teschio'){ const M=mostriSP.im&&mostriSP.im.zeta_scheletro, im=M&&M.teschio_volo; if(!im||!im.complete||!im.width) return false; if(p._t===undefined) p._t=0; p._t++;
      const d=Math.sign(p.vx)||1, w=60, h=im.height*w/im.width; ctx.save(); ctx.translate(p.x,p.y); ctx.scale(d,1); ctx.rotate(p._t*0.18); ctx.imageSmoothingEnabled=false; ctx.drawImage(im,-w/2,-h/2,w,h); ctx.restore();
      if(p._t%3===0) FX.push({x:p.x-d*14,y:p.y+(rnd()-.5)*14,vx:-d*1.5,vy:-0.4,life:12,c:rnd()<.5?'#7dff5a':'#c8ffb0'}); return true; }
    return _mpS.apply(this,arguments); }; }
""" + A)

# 3) arcade: miniboss prima di Marico Frankenstein, arena cimitero in Scozia
A = "// presentazione: la stessa forma con cui il miniboss entra in campo"
rep(A, r"""/*SCHELETRO1 (22.11.2026) - Zeta scheletro, miniboss dell'Arcade: cimitero spettrale in Scozia, si sblocca battendolo a Difficile */
try{ Object.assign(STAGES,{cimitero:'Ossa e Cornamuse'}); Object.assign(BGDATA,{cimitero:'img/arene/cimitero.png'});
  if(!BGIMG.cimitero){ const im=new Image(); im.onload=()=>{ if(curStage==='cimitero') buildBg('cimitero'); }; im.src=BGDATA.cimitero; BGIMG.cimitero=im; }
  [typeof TIFLAY!=='undefined'?TIFLAY:null,typeof TIFSPOT!=='undefined'?TIFSPOT:null,typeof CROWDR!=='undefined'?CROWDR:null,typeof FANSPOT!=='undefined'?FANSPOT:null,typeof CROWDM!=='undefined'?CROWDM:null,typeof FANK!=='undefined'?FANK:null].forEach(t=>{ if(t&&t.cimitero===undefined&&t.frankenlab!==undefined) t.cimitero=t.frankenlab; });
  if(typeof THEMES!=='undefined'&&!THEMES.cimitero&&THEMES.frankenlab) THEMES.cimitero=Object.assign({},THEMES.frankenlab,{seed:419});
  if(typeof PAINT!=='undefined'&&!PAINT.cimitero) PAINT.cimitero=g=>{ g.fillStyle='#0b1210'; g.fillRect(0,0,320,180); };
  HOMEB.cimitero=['dif',0.93,'Le ossa non sentono i colpi']; STLOCK.cimitero='lds-arcade'; TOR.home.scheletro='cimitero';
  ARC2.mb.zeta={base:'zeta',mon:'Zeta scheletro',home:'cimitero',pos:{w:[468,104],n:'Scozia'}}; TPOS.mb_zeta=ARC2.mb.zeta.pos;
  if(!ARC2.ordine.includes('zeta')){ const i=ARC2.ordine.indexOf('marico'); ARC2.ordine.splice(i>=0?i:ARC2.ordine.length,0,'zeta'); }
  ARC2.col.zeta='#7dff5a'; ARC2.mbTxt.zeta='Scozia, mezzanotte. Nebbia sulle lapidi, una cornamusa suona da sola. In mezzo al cimitero qualcuno palleggia. Il rimbalzo non è quello di un pallone.';
  ARC14FURTI.zeta='il pallone autografato'; { const im=new Image(); im.src='img/vignette/inc_zeta.jpg'; ARC14V2.inc_zeta=im; }
  try{ mostriLoad('zeta_scheletro'); }catch(e){} try{ buildArenas(); }catch(e){}
}catch(e){ console.error('SCHELETRO1 arcade',e); }
{ const _sbZ=arc14Sblocca; arc14Sblocca=function(b){ if(b==='zeta'&&typeof MOSTRI!=='undefined'&&MOSTRI['Zeta scheletro']){ try{ const m=MOSTRI['Zeta scheletro'], nuovo=localStorage.getItem(m.key)!=='1'; mostroSblocca(m); return nuovo?m.msg:''; }catch(e){ console.error('SCHELETRO1 sblocco',e); return ''; } } return _sbZ.apply(this,arguments); }; }
""" + A)
s = s.replace("'Quattordici sfide, nessuna rivincita.", "'Sedici sfide, nessuna rivincita.")
open(p, 'w', encoding='utf8').write(s); print('SCHELETRO1 ok')
