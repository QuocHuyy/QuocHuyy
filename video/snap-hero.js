// Rasterize ../assets/hero.svg (skyline state, before the domain opens) to hero_city.png
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:840,height:320},deviceScaleFactor:1});
await p.goto('file://'+path.resolve(__dirname,'../assets/hero.svg'));await p.waitForTimeout(300);
await p.screenshot({path:path.join(__dirname,'hero_city.png')});await b.close();})();
