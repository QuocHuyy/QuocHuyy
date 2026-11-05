// usage: node render.js all  |  node render.js preview 1.2 3.4 ...
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const FPS=30,N=600,WORKERS=4;
(async()=>{
  process.chdir(__dirname);const mode=process.argv[2]||'all';const b=await chromium.launch();
  const open=async()=>{const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
    p.on('console',m=>console.log('[page]',m.text()));p.on('pageerror',e=>console.log('[err]',e.message));
    await p.goto('file://'+path.resolve('scene.html'));await p.evaluate(()=>window.ready);return p};
  const shot=async(p,t,file)=>{await p.evaluate(t=>renderAt(t),t);await p.locator('#c').screenshot({path:file})};
  if(mode==='preview'){fs.mkdirSync('preview',{recursive:true});const p=await open();
    for(const t of process.argv.slice(3).map(Number))await shot(p,t,`preview/t${t.toFixed(2)}.png`);}
  else{fs.mkdirSync('frames',{recursive:true});const t0=Date.now();
    await Promise.all([...Array(WORKERS)].map(async(_,w)=>{const p=await open();for(let i=w;i<N;i+=WORKERS)await shot(p,i/FPS,`frames/f${String(i).padStart(4,'0')}.png`)}));
    console.log('rendered',N,'frames in',(Date.now()-t0)/1000,'s');}
  await b.close();})();
