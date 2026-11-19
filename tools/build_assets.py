"""Build original, script-free SVG profile graphics. Requires fonttools.
Run from anywhere. Generated outputs are included; running this is optional.
"""
from pathlib import Path
from html import escape
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/motion'
OUT.mkdir(parents=True,exist_ok=True)
FONT=Path('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf')
font=TTFont(FONT) if FONT.exists() else None
THEMES={
 'dark':dict(bg='#0B0D14',panel='#121520',fg='#F5F3EF',muted='#A3A9BD',line='#2A3041',a='#C2AFF5',b='#C6EF9A',soft='#1E2233'),
 'light':dict(bg='#F6F4F0',panel='#FFFFFF',fg='#202333',muted='#60697B',line='#D6D5DF',a='#7956AA',b='#50742E',soft='#E9E5F0')
}

def text(x,y,s,size=18,color=None,weight=400,mono=False,extra=''):
 return f'<text x="{x}" y="{y}" font-family="{("DejaVu Sans Mono,monospace" if mono else "Arial,Helvetica,sans-serif")}" font-size="{size}" font-weight="{weight}" fill="{color or "currentColor"}" {extra}>{escape(s)}</text>'

def namepath(s,x,y,size,color):
 if not font:return text(x,y,s,size,color,700,extra='letter-spacing="-3"')
 gs=font.getGlyphSet(); cmap=font.getBestCmap(); scale=size/font['head'].unitsPerEm; cursor=0; parts=[]
 for ch in s:
  n=cmap[ord(ch)];pen=SVGPathPen(gs);gs[n].draw(pen)
  parts.append(f'<path d="{pen.getCommands()}" transform="translate({cursor:.3f} 0)"/>')
  cursor+=gs[n].width-38
 return f'<g aria-label="{escape(s)}" fill="{color}" transform="translate({x} {y}) scale({scale} {-scale})">'+''.join(parts)+'</g>'

def shell(w,h,t,title,desc,body):
 c=THEMES[t]
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs>
 <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c['soft']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
 <linearGradient id="edge"><stop stop-color="{c['a']}"/><stop offset="1" stop-color="{c['b']}"/></linearGradient>
 <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['line']}" stroke-width=".6" opacity=".4"/></pattern>
</defs>
<style>
.orbit{{transform-box:fill-box;transform-origin:center;animation:spin 26s linear infinite}}
.orbit-reverse{{transform-box:fill-box;transform-origin:center;animation:spin 36s linear reverse infinite}}
.float{{animation:float 7s ease-in-out infinite}}
.signal{{stroke-dasharray:16 480;animation:signal 7s linear infinite}}
.pulse{{animation:pulse 4s ease-in-out infinite}}
.scan{{animation:scan 6s ease-in-out infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
@keyframes signal{{to{{stroke-dashoffset:-496}}}}
@keyframes pulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
@keyframes scan{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@media(prefers-reduced-motion:reduce){{.orbit,.orbit-reverse,.float,.signal,.pulse,.scan{{animation:none!important}}}}
</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="{c['bg']}" stroke="{c['line']}"/>
{body}
</svg>'''

def machinery(c,cx,cy,scale=1,phase=0):
 # The graphic represents software layers, not a measured production topology.
 a=c['a'];b=c['b'];line=c['line'];p=[]
 p.append(f'<g transform="translate({cx} {cy}) scale({scale})">')
 p.append(f'<circle r="186" fill="url(#grid)" stroke="{line}"/>')
 p.append(f'<circle r="163" fill="none" stroke="{line}" stroke-dasharray="2 11"/>')
 p.append(f'<path d="M-211 0H211M0-211V211" stroke="{line}" stroke-dasharray="3 8"/>')
 p.append(f'<g transform="rotate({phase*360:.3f})"><g class="orbit"><circle r="185" fill="none" stroke="{a}" stroke-dasharray="128 1035" stroke-width="2"/><circle cx="185" cy="0" r="5" fill="{a}"/><circle cx="-185" cy="0" r="3" fill="{b}"/></g></g>')
 p.append(f'<g transform="rotate({-phase*360:.3f})"><g class="orbit-reverse"><circle r="145" fill="none" stroke="{b}" stroke-dasharray="68 843" opacity=".8"/><circle cx="0" cy="-145" r="4" fill="{b}"/></g></g>')
 p.append(f'<g transform="translate(0 {-6*math.sin(phase*2*math.pi):.3f})"><g class="float">')
 for y,label,n in [(78,'DATA',3),(0,'API',2),(-78,'UI',1)]:
  p.append(f'<g transform="translate(0 {y})"><path d="M-99 0L0-48 99 0 0 48Z" fill="url(#surface)" stroke="{a}" stroke-opacity=".8"/><path d="M-99 0V15L0 63 99 15V0L0 48Z" fill="{c["panel"]}" stroke="{line}"/><path d="M0 48V63" stroke="{line}"/>{text(-17,6,label,14,c["fg"],700,True)}<circle cx="-65" cy="2" r="3" fill="{b}" class="pulse"/></g>')
 p.append('</g></g>')
 for x,y,label in [(-202,-125,'01'),(174,133,'03')]:
  p.append(f'<rect x="{x-15}" y="{y-15}" width="30" height="30" rx="6" fill="{c["bg"]}" stroke="{line}"/>{text(x,y+4,label,11,c["muted"],400,True,extra="text-anchor=\"middle\"")}')
 p.append('</g>');return ''.join(p)

def hero(theme,mobile=False,phase=0):
 c=THEMES[theme];fg=c['fg'];a=c['a'];m=c['muted'];b=c['b'];line=c['line']
 if not mobile:
  body=text(52,50,'SHON / SYSTEMS IN MOTION',15,m,400,True,extra='letter-spacing="2"')
  body+=f'<circle cx="1124" cy="44" r="4" fill="{b}" class="pulse"/>'+text(1108,49,'ENGINEERING JOURNAL',12,m,400,True,extra='text-anchor="end"')
  body+=namepath('Shantanu',50,183,105,fg)+namepath('Shahane.',50,291,105,a)
  body+=text(55,345,'Full-stack software. Applied AI.',25,fg)
  body+=text(55,383,'CO-FOUNDER @ ASTRIX TECHNOLOGIES',15,m,400,True)
  body+=f'<path d="M55 421H558" stroke="{line}"/><path class="signal" d="M55 421H558" stroke="{b}" stroke-width="2"/>'
  body+=machinery(c,906,256,.88,phase)
  body+=text(906,454,'SPEC / BUILD / DEPLOY',12,m,400,True,extra='text-anchor="middle" letter-spacing="2"')
  body+=f'<path d="M52 483H1148" stroke="{line}"/>'+text(55,515,'CSE / HONORS IN CLOUD COMPUTING',12,m,400,True)+text(1145,515,'CLASS OF 2027  /  INDIA',12,m,400,True,extra='text-anchor="end"')
  return shell(1200,542,theme,'Shantanu Shahane — Systems in Motion','Co-founder at Astrix Technologies. Full-stack software and applied AI. CSE with cloud computing honors, class of 2027. Animated orbital illustration of UI, API, and data layers.',body)
 body=text(36,47,'SHON / SYSTEMS IN MOTION',14,m,400,True,extra='letter-spacing="1.2"')
 body+=namepath('Shantanu',33,151,91,fg)+namepath('Shahane.',33,247,91,a)
 body+=text(38,297,'Full-stack software. Applied AI.',22,fg)
 body+=text(38,333,'CO-FOUNDER @ ASTRIX',16,m,400,True)
 body+=machinery(c,434,480,.59,phase)
 body+=text(38,432,'BUILDING',13,m,400,True)+text(38,474,'SaaS products',22,fg,700)+text(38,509,'AI workflows',22,fg,700)+text(38,544,'Cloud systems',22,a,700)
 body+=f'<path d="M38 615H602" stroke="{line}"/>'+text(38,650,'CSE / CLOUD HONORS',14,m,400,True)+text(602,650,'2027 / INDIA',14,m,400,True,extra='text-anchor="end"')
 return shell(640,682,theme,'Shantanu Shahane — Systems in Motion','Full-stack software, applied AI, co-founder at Astrix. Cloud honors, class of 2027.',body)

def cover(theme,kind):
 c=THEMES[theme];a=c['a'];b=c['b'];fg=c['fg'];m=c['muted'];line=c['line'];p=''
 if kind=='looply':
  label='01 / SAAS PRODUCT';title='Looply';sub='Loyalty. Engagement. Repeat.'
  # A conceptual loop; no invented customer counts or product screenshot.
  for r in [83,61,39]:p+=f'<circle cx="945" cy="126" r="{r}" fill="none" stroke="{line}" stroke-width="2"/>'
  p+=f'<g transform="translate(945 126)"><g class="orbit"><circle r="83" fill="none" stroke="{a}" stroke-width="3" stroke-dasharray="110 412"/><circle cx="83" cy="0" r="6" fill="{b}"/></g></g>'
  p+=f'<path d="M923 127l15 15 31-35" fill="none" stroke="{b}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
 elif kind=='ca-platform':
  label='02 / MULTI-TENANT SYSTEM';title='CA Firm Platform';sub='Operations, with an AI copilot.'
  for x,y in [(852,66),(1032,66),(852,164),(1032,164)]:
   p+=f'<path d="M945 125L{x} {y}" stroke="{line}" stroke-width="2"/><path class="signal" d="M945 125L{x} {y}" stroke="{a}" stroke-width="2"/>'
   p+=f'<rect x="{x-22}" y="{y-18}" width="44" height="36" rx="8" fill="{c["panel"]}" stroke="{a}"/><path d="M{x-10} {y}h20" stroke="{b}"/>'
  p+=f'<rect x="910" y="90" width="70" height="70" rx="20" fill="{c["soft"]}" stroke="{a}"/>'+text(945,132,'AI',21,fg,700,True,extra='text-anchor="middle"')
 else:
  label='03 / APPLIED MACHINE LEARNING';title='StockSense';sub='Financial news → sentiment signals.'
  for i,x in enumerate([828,854,880,906,932,958,984,1010,1036]):
   h=[30,50,75,46,90,64,104,82,116][i]
   p+=f'<rect class="scan" x="{x}" y="{190-h}" width="12" height="{h}" rx="4" fill="{a}" opacity=".55" style="animation-delay:{i*.3}s"/>'
  p+=f'<path d="M818 164L852 145 885 151 920 116 949 126 980 92 1016 101 1066 62" fill="none" stroke="{b}" stroke-width="3"/><circle class="pulse" cx="1066" cy="62" r="5" fill="{b}"/>'
 body=text(40,45,label,14,m,400,True,extra='letter-spacing="1.5"')+text(38,118,title,51,fg,700)+text(42,167,sub,22,a)
 body+=f'<path d="M42 204H620" stroke="{line}"/><path class="signal" d="M42 204H620" stroke="{a}" stroke-width="2"/>'+p
 return shell(1200,245,theme,title,sub+' Conceptual animated illustration; not a product screenshot or live data.',body)

def footer(theme):
 c=THEMES[theme]
 body=text(42,48,'NEXT / LET’S BUILD SOMETHING USEFUL.',17,c['muted'],400,True)
 body+=text(40,111,'From a good idea to working software.',36,c['fg'],700)
 body+=f'<path d="M42 146H1158" stroke="{c["line"]}"/><path class="signal" d="M42 146H1158" stroke="{c["a"]}" stroke-width="2"/>'
 return shell(1200,177,theme,'Let’s build something useful.','From a good idea to working software.',body)

def button(label,theme,width):
 c=THEMES[theme]
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="42" viewBox="0 0 {width} 42"><rect x="1" y="1" width="{width-2}" height="40" rx="10" fill="{c["soft"]}" stroke="{c["line"]}"/>{text(width/2,27,label,14,c["fg"],700,extra="text-anchor=\"middle\"")}</svg>'

for theme in THEMES:
 (OUT/f'hero-{theme}.svg').write_text(hero(theme))
 (OUT/f'hero-mobile-{theme}.svg').write_text(hero(theme,True))
 for kind in ['looply','ca-platform','stocksense']:(OUT/f'{kind}-{theme}.svg').write_text(cover(theme,kind))
 (OUT/f'footer-{theme}.svg').write_text(footer(theme))
 for slug,label,width in [('portfolio','Portfolio ↗',132),('looply-link','Looply ↗',116),('resume','Résumé ↓',120),('linkedin','LinkedIn ↗',130),('email','Email ↗',106)]:
  (OUT/f'{slug}-{theme}.svg').write_text(button(label,theme,width))

# A deterministic motion preview, rendered with the same vector geometry.
if __name__=='__main__':
 import sys
 if '--frames' in sys.argv:
  frames=ROOT/'preview/frames';frames.mkdir(exist_ok=True)
  for i in range(60):(frames/f'{i:03}.svg').write_text(hero('dark',phase=i/60))
 print('Wrote original theme-aware SVG assets to',OUT)
