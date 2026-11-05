import numpy as np, wave, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR=44100; DUR=20.0; N=int(SR*DUR)
rng=np.random.default_rng(42)
mixL=np.zeros(N); mixR=np.zeros(N); send=np.zeros(N)

def add(sig,t,g=1.0,pan=0.0,rev=0.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    l=g*np.sqrt((1-pan)/2); r=g*np.sqrt((1+pan)/2)
    mixL[i:i+n]+=sig[:n]*l; mixR[i:i+n]+=sig[:n]*r; send[i:i+n]+=sig[:n]*g*rev
def tt(d): return np.arange(int(d*SR))/SR
def band(x,lo,hi):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<lo)|(f>hi)]=0; return np.fft.irfft(X,len(x))
def sweep(f0,f1,d,shape='exp'):
    t=tt(d); f=f0*(f1/f0)**(t/d) if shape=='exp' else f0+(f1-f0)*t/d
    return np.sin(2*np.pi*np.cumsum(f)/SR)
def saw(f,d):
    t=tt(d); ph=(t*f)%1; return 2*ph-1
def sq(f,d,duty=.5):
    t=tt(d); return np.where((t*f)%1<duty,1.0,-1.0)
def env(d,a=.002,r=.2):
    t=tt(d); e=np.minimum(1,t/max(a,1e-4))*np.exp(-t/r); return e

# --- drums
def kick(g=1):
    d=.45; s=sweep(160,42,d)*np.exp(-tt(d)/.16); s[:60]+=np.linspace(.6,0,60); return np.tanh(s*1.6)*g
def clap():
    d=.25; n=band(rng.standard_normal(int(d*SR)),900,6000); e=np.exp(-tt(d)/.06)
    for o in (0.0,.011,.022): e+=np.where(tt(d)>o,np.exp(-(tt(d)-o)/.008),0)*.6*(o>0)
    return n*e*.5
def hat(open_=False):
    d=.18 if open_ else .05; n=band(rng.standard_normal(int(d*SR)),7000,16000); return n*np.exp(-tt(d)/(d/3))*.45
def boom(g=1):
    d=2.2; s=sweep(120,28,d)*np.exp(-tt(d)/.55); n=band(rng.standard_normal(int(d*SR)),40,4000)*np.exp(-tt(d)/.35)*.5
    return np.tanh((s+n)*1.8)*g
def crash():
    d=2.0; n=band(rng.standard_normal(int(d*SR)),3000,15000); return n*np.exp(-tt(d)/.6)*.35
def riser(d,f0=200,f1=4000):
    n=rng.standard_normal(int(d*SR)); t=tt(d); out=np.zeros_like(n); segs=12
    for k in range(segs):
        lo=f0*(f1/f0)**(k/segs); hi=lo*1.6; w=np.exp(-((t/d-k/segs)*segs/1.5)**2)
        out+=band(n,lo,hi)*w
    return out*(t/d)**2*.6
def whoosh(d=.4):
    return riser(d,300,6000)*1.2 + sweep(200,1200,d)*(tt(d)/d)**3*.15
def blip(f,d=.07,g=.25): return sq(f,d,.25)*env(d,.001,.03)*g
def click(): d=.012; return band(rng.standard_normal(int(d*SR)),2000,9000)*np.exp(-tt(d)/.003)*.5

BEAT=.5
# ---- intro 0-2.5
dr=tt(2.6); drone=(np.sin(2*np.pi*55*dr)+.5*np.sin(2*np.pi*55.4*dr*2)+.3*np.sin(2*np.pi*82.4*dr))*np.minimum(1,dr/.6)*.18
add(drone,0,1)
for i in range(26): add(click(),.2+i/34,.5,pan=rng.uniform(-.3,.3))
for i in range(27): add(click(),1.0+i/60,.4,pan=rng.uniform(-.3,.3))
for k in range(3): add(blip(880,.08,.3),1.5+k*.12)
for k in range(12): add(blip(440*2**(k/12),.03,.12),1.7+k*.05)
add(riser(1.0,150,6000),1.5,1.0)
for k in range(6): add(sq(110*(k+1),.03)*.08,2.2+k*.05)   # glitch stutter
add(boom(1.1),2.5,rev=.35); add(crash(),2.5,.9,rev=.4)

# ---- groove 2.5-17.5
chords=[(55.0,[220,261.6,329.6]),(43.65,[174.6,220,261.6]),(36.71,[146.8,174.6,220]),(41.2,[164.8,207.6,246.9])] # Am F Dm E
t=2.5
while t<17.5-1e-6:
    b=round((t-2.5)/BEAT)
    add(kick(),t,1.0)
    if b%2==1: add(clap(),t,.9,rev=.25)
    add(hat(),t+.25,.7,pan=.3)
    if t>=8.5: add(hat(),t+.125,.35,pan=-.3); add(hat(),t+.375,.35,pan=-.3)
    root,tri=chords[int(((t-2.5)/2))%4]
    for k in range(2):  # bass 8ths, sidechained
        d=.24; bs=(saw(root*2,d)*.6+np.sin(2*np.pi*root*tt(d)))*env(d,.03,.18)
        add(bs,t+k*.25+.02,.32 if k else .18)
    if t>=5.5:  # chip arp 16ths
        notes=[tri[0],tri[1],tri[2],tri[1]*2]
        for k in range(4): add(blip(notes[k]*2,.11,.07),t+k*.125,pan=-.2+.4*(k%2),rev=.3)
    t+=BEAT
# pad under groove
for bar in range(7):
    t0=2.5+bar*2; root,tri=chords[bar%4]; d=2.0
    pad=sum(saw(f,d)*.3+np.sin(2*np.pi*f*tt(d)) for f in tri)
    pad=band(pad,80,2200)*np.minimum(1,tt(d)/.3)*np.minimum(1,(d-tt(d))/.3)*.06
    add(pad,t0,1,rev=.5)

# impacts on slams
for ts,g in [(3.0,.6),(3.5,.6),(5.52,.7),(6.0,.7),(10.7,.6),(11.5,.5),(14.5,.5)]:
    add(boom(g),ts,rev=.25); add(crash(),ts,.35)
# whooshes into cuts
for c in [5.5,8.5,11.5,14.5]: add(whoosh(.45),c-.45,.9,rev=.2)
add(sweep(1500,200,.6)*np.exp(-tt(.6)/.2)*.08,3.3,rev=.4)
# SORCERER rows: small blips
for i,ts in enumerate([8.8,9.05,9.3,9.55,10.0]): add(blip(660+i*110,.06,.15),ts)
# tool pops
pent=[523.3,587.3,659.3,784,880]
for i in range(15): add(blip(pent[i%5]*(1 if i<5 else 2 if i<10 else 4)/1,.06,.16),11.8+i*.15,pan=(i%3-1)*.4)
# counter chatter
for k in range(30): add(blip(1200+rng.uniform(-200,600),.02,.05),14.8+k*.05,pan=rng.uniform(-.5,.5))
# lang bars
for i in range(4): add(sweep(300,900+i*200,.5)*env(.5,.01,.25)*.06,15.75+i*.15)

# ---- finale 17.5-20
d=1.0; add(riser(d,100,8000),17.5,1.3)
ch=sweep(80,900,d)*(tt(d)/d)**2; add(np.tanh(ch*2)*.25,17.5)
add(sweep(110,330,d)*.12,17.5,pan=-.6); add(sweep(130,390,d)*.12,17.5,pan=.6)  # blue / red hums
add(whoosh(.3),18.2,1.0)
add(boom(1.4),18.5,rev=.5); add(crash(),18.5,1.2,rev=.5)
d=1.5; t1=tt(d)
outpad=sum(np.sin(2*np.pi*f*t1)+.25*saw(f,d) for f in [110,220,261.6,329.6,440])*np.minimum(1,t1/.05)*np.exp(-t1/1.2)*.07
add(outpad,18.5,1,rev=.6)
for ts in [19.0,19.5]: add(kick(.8),ts)
add(clap(),19.0,.6,rev=.5)
for k in range(8): add(blip([440,523.3,659.3,880][k%4]*2,.1,.06),18.95+k*.125,rev=.5)

# ---- reverb (noise IR)
ir_d=1.6; ir=rng.standard_normal(int(ir_d*SR))*np.exp(-tt(ir_d)/.45); ir/=np.sqrt((ir**2).sum())
L=len(send)+len(ir); rv=np.fft.irfft(np.fft.rfft(send,L)*np.fft.rfft(ir,L),L)[:N]*1.2
mixL+=rv; mixR+=np.roll(rv,int(.013*SR))
# master: fade, soft clip, normalize
fade=np.ones(N); fl=int(.35*SR); fade[-fl:]=np.linspace(1,0,fl)**1.5
st=np.stack([mixL,mixR],1)*fade[:,None]
st=np.tanh(st*1.3); st/=np.abs(st).max()/0.89
with wave.open('audio.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
print('ok', st.shape)
