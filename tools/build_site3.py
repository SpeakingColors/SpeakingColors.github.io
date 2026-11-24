import json, os, html, re, sys, shutil, subprocess

S = sys.argv[1]; OUT = sys.argv[2]
BASE = "https://speakingcolors.github.io"
repos = {r["name"]: r for r in json.load(open(S + "/data/repos.json"))}
for _k, _v in {"SynthCookBook": "A patch recipe book for synths without patch memory: Behringer Pro-1, CAT, TD-3-MO and TD-3. It draws each front panel, keeps your recipes in the browser, and works offline."}.items():
    if _k in repos: repos[_k]["description"] = _v
exec(open(S + "/cats.py").read())   # defines CATS

e = html.escape
DESIGN = {"purrrvoicechannel"}
FXSTUDIO = {"catspacer","catcrusher-vst","FatCat","meowbass","Meowximizer","scaredy-cat"}
exec(open(S + "/art.py").read())
exec(open(S + "/copy_data.py").read())   # defines COPY
SLUGMAP = {"SynthCookBook": "synth-cook-book"}
DESCMAP = {"SynthCookBook": "A patch recipe book for synths without patch memory: Behringer Pro-1, CAT, TD-3-MO and TD-3. It draws each front panel, keeps your recipes in the browser, and works offline."}
def slug(n): n = SLUGMAP.get(n, n); return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
def short(x, n):
    x = x.strip()
    return x if len(x) <= n else x[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "..."
def dims(path):
    if shutil.which("sips"):
        o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True).stdout
        w = re.search(r"pixelWidth: (\d+)", o); h = re.search(r"pixelHeight: (\d+)", o)
        return (int(w.group(1)), int(h.group(1))) if w and h else (1200, 700)
    try:
        from PIL import Image
        return Image.open(path).size
    except Exception:
        return (1200, 700)

os.makedirs(OUT + "/img", exist_ok=True); os.makedirs(OUT + "/fonts", exist_ok=True)
for d in ("full", "thumb"):
    shutil.copytree(f"{S}/img/{d}", f"{OUT}/img/{d}", dirs_exist_ok=True)
for f in os.listdir(S + "/fonts"):
    if f.endswith(".woff2"): shutil.copy(f"{S}/fonts/{f}", f"{OUT}/fonts/{f}")
FONTCSS = open(S + "/fonts/fonts-local.css").read()
have = {f[:-4] for f in os.listdir(f"{OUT}/img/full")}
_ART_SLUGS = {"megasaw-xd","hypersaw-xd","hypersaw-drumlogue","super-duper-stuff","sawwiden-xd","whiskerwave-vst","provsmini-vst","mwave-fm1-linux-vst","cat-ui","claude-skills"}
have = {h for h in have if re.sub(r"[^a-z0-9]+","-",h.lower()).strip("-") not in _ART_SLUGS}   # repos without a real screenshot use our own artwork, not an illustrated card
TRY = json.load(open(S + "/try.json"))
AUDIO = json.load(open(S + "/audio.json"))
shutil.copytree(S + "/audio", OUT + "/audio", dirs_exist_ok=True)
shutil.copytree(S + "/try", OUT + "/try", dirs_exist_ok=True)
if os.path.isdir(S + "/guide"): shutil.copytree(S + "/guide", OUT + "/img/guide", dirs_exist_ok=True)

# short type label + accent per category
LABEL = {"synths": ("Synth", "pink"), "dynamics": ("Dynamics", "teal"), "tone": ("Tone", "yellow"), "space": ("Effect", "teal"),
         "dj-and-creative": ("Creative", "yellow"), "studio-tools": ("Tool", "pink"), "tv-apps": ("TV app", "pink"), "hardware-controllers": ("Controller", "teal"),
         "korg-units": ("Korg unit", "yellow"), "recipe-books": ("Recipe book", "yellow"), "developers": ("Developer", "pink")}

GHICON = '''<svg class="gh" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'''
LOGO = '''<svg class="logo" viewBox="0 0 48 48" aria-hidden="true"><path d="M8 40V10l9 8h14l9-8v30z" fill="none" stroke="#ff6aa5" stroke-width="3.5" stroke-linejoin="round"/><circle cx="18" cy="28" r="2.4" fill="#2dd4bf"/><circle cx="30" cy="28" r="2.4" fill="#2dd4bf"/><path d="M3 30l7 1M3 36l7-2M45 30l-7 1M45 36l-7-2" stroke="#2dd4bf" stroke-width="2.2" stroke-linecap="round"/></svg>'''

CSS = FONTCSS + """
:root{color-scheme:dark;--bg:#141618;--bg2:#1a1d20;--card:#202428;--line:#363b42;--fg:#f4efe6;--mut:#c4beb3;--pink:#ff6aa5;--pink-t:#ff6aa5;--on-pink:#2b0d1a;--teal:#2dd4bf;--yellow:#ffd23f}
@media (prefers-color-scheme: light){:root:not([data-theme=dark]){color-scheme:light;--bg:#f6efe3;--bg2:#efe5d4;--card:#fffaf1;--line:#d8c9b1;--fg:#1b1410;--mut:#5d4f43;--pink:#e0356f;--pink-t:#c4285f;--on-pink:#ffffff}}
:root[data-theme=light]{color-scheme:light;--bg:#f6efe3;--bg2:#efe5d4;--card:#fffaf1;--line:#d8c9b1;--fg:#1b1410;--mut:#5d4f43;--pink:#e0356f;--pink-t:#c4285f;--on-pink:#ffffff}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.65 'DM Sans',system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}img{max-width:100%}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px}
.hd,h2.sec{text-wrap:balance}
.hd{font-family:'Bricolage Grotesque','DM Sans',sans-serif;font-weight:800;letter-spacing:-0.04em;line-height:.95}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:84px;gap:12px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:25px;letter-spacing:-0.03em;white-space:nowrap}.logo{width:32px;height:32px}
.nav{display:flex;align-items:center;gap:30px;font-weight:700;font-size:16px}.nav a{text-decoration:none;white-space:nowrap}.nav a:hover{text-decoration:underline}
.pill{background:var(--fg);color:var(--bg);border-radius:999px;padding:11px 22px;text-decoration:none!important}
@media(max-width:820px){.nav a:not(.pill):not(.keep){display:none}.nav{gap:14px}.pill{padding:9px 16px}.brand{font-size:21px}.logo{width:26px;height:26px}.top .wrap{height:64px}}
@media(max-width:600px){.nav a.keep{display:none}.nav{gap:10px}.tog{padding:7px 11px;font-size:13px}.pill{padding:8px 14px}.brand{font-size:19px;gap:8px}.top .wrap{padding:0 16px}}
.tog{border:2px solid var(--line);background:transparent;color:var(--fg);border-radius:999px;padding:8px 14px;font:700 14px 'DM Sans',sans-serif;cursor:pointer;white-space:nowrap}.tog:hover{border-color:var(--fg)}
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:999px;font-weight:700;font-size:17px;padding:17px 30px;text-decoration:none;border:2px solid transparent;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}.btn.p{background:var(--pink);color:var(--on-pink)}.btn.o{border-color:var(--fg);color:var(--fg)}.btn.l{background:var(--fg);color:var(--bg)}.btn.t{background:var(--teal);color:#06221d}
@media(max-width:560px){.btn{width:100%;justify-content:center}}
.hero{padding:28px 0 52px}.hero h1{font-size:clamp(66px,12.5vw,148px);margin:0}.hero h1 em{font-style:normal;color:var(--pink-t)}
.hrow{display:flex;gap:40px;align-items:flex-end;justify-content:space-between;margin-top:34px;flex-wrap:wrap}
.hrow p{margin:0;max-width:520px;font-size:clamp(18px,2.2vw,22px);line-height:1.5;color:var(--mut)}.hbtn{display:flex;gap:14px;flex-wrap:wrap}
.bento{display:grid;grid-template-columns:1.5fr 1fr;gap:22px}@media(max-width:860px){.bento{grid-template-columns:1fr}}
.bcard{display:block;border-radius:28px;padding:18px;text-decoration:none;transition:transform .18s}.bcard:hover{transform:translateY(-4px)}
.bcard img{width:100%;height:auto;display:block;border-radius:16px}.bcard .bn{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-0.03em}
.bcard.big{background:var(--card);border:1px solid var(--line)}.bcard.big .row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;padding:16px 8px 4px}.bcard.big .bn{font-size:clamp(26px,3.4vw,34px)}.bcard.big span.s{color:var(--mut);font-size:16px}
.bcol{display:flex;flex-direction:column;gap:22px}.bcol .bcard{flex:1 1 0}.bcol .bcard img{aspect-ratio:16/10;object-fit:cover;object-position:top;border-radius:14px}.bcol .bn{font-size:26px;margin-top:12px}.bcol .s{display:block;font-size:16px}
.bcard.teal{background:var(--teal);color:#06221d}.bcard.yellow{background:var(--yellow);color:#2b2008}
.band{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;margin:88px 0 24px;border-top:3px solid var(--fg);padding-top:40px}@media(max-width:860px){.band{grid-template-columns:1fr}}
.band h2{font-size:clamp(40px,6vw,64px);margin:0}.band p{margin:18px 0 26px;font-size:20px;line-height:1.5;max-width:460px;color:var(--mut)}

@media(max-width:860px){.band img{height:260px}}
section{padding:24px 0}h2.sec{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(34px,5vw,52px);letter-spacing:-0.04em;margin:0 0 6px;line-height:1}.sub{color:var(--mut);margin:0 0 20px}
.bar{display:flex;flex-wrap:nowrap;gap:10px;align-items:center;margin:14px 0 24px;overflow-x:auto;padding-bottom:6px;scrollbar-width:thin}
@media(min-width:1000px){.bar{flex-wrap:wrap;overflow:visible}}
.chip{flex:none;white-space:nowrap;border:2px solid var(--fg);background:transparent;color:var(--fg);padding:10px 20px;border-radius:999px;font:700 16px 'DM Sans',sans-serif;cursor:pointer}
.chip[aria-pressed=true]{background:var(--pink);border-color:var(--pink);color:var(--on-pink)}
.search{flex:none;min-width:200px;margin-left:auto;background:var(--card);border:2px solid var(--line);color:var(--fg);padding:11px 16px;border-radius:999px;font:500 16px 'DM Sans',sans-serif}
.cat h3{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:28px;letter-spacing:-0.03em;margin:34px 0 2px}.cat p.sub{margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(256px,1fr));gap:18px}
.card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:22px;overflow:hidden;text-decoration:none;color:var(--fg);transition:transform .16s,border-color .16s}
.card:hover{transform:translateY(-4px);border-color:var(--pink)}
.card .im{aspect-ratio:16/10;background:var(--bg2);overflow:hidden}.card .im img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.card .tx{padding:16px 18px 20px}.card b{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:21px;letter-spacing:-0.02em;display:flex;align-items:center;gap:8px;flex-wrap:wrap;line-height:1.15}
.card span.d{display:block;color:var(--mut);font-size:15.5px;margin-top:6px;line-height:1.5}
.lab{font:700 12px 'DM Sans',sans-serif;letter-spacing:.02em;padding:3px 9px;border-radius:6px;color:#1b1410}.lab.pink{background:var(--pink)}.lab.teal{background:var(--teal)}.lab.yellow{background:var(--yellow)}
.badge{background:var(--yellow);border:0;color:#2b2008;border-radius:6px;padding:1px 8px;font:700 11px 'DM Sans',sans-serif;letter-spacing:.04em}
.tcard{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:16px;text-align:center;background:var(--card)}
.tcard b{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(22px,2.6vw,28px);letter-spacing:-0.03em;line-height:1.1;color:var(--pink-t)}.tcard small{color:var(--mut);font-size:14px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}.step{border:2px solid var(--fg);border-radius:22px;padding:22px}.step i{font:800 28px 'Bricolage Grotesque',sans-serif;font-style:normal;color:var(--pink-t)}.step b{display:block;font-size:20px;margin:4px 0}.step p{margin:0;color:var(--mut)}
.support{margin:80px 0 20px;background:var(--pink);color:var(--on-pink);border-radius:32px;padding:clamp(28px,5vw,56px);display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap}
.support .hd{font-size:clamp(34px,5vw,52px);line-height:1;max-width:640px}.support .btn{background:var(--bg);color:var(--fg)}
footer{margin-top:24px;padding:28px 0 48px;color:var(--mut);font-size:15px}.fcols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:22px;margin-bottom:22px}.fcols b{display:block;color:var(--fg);margin-bottom:6px}.fcols a{display:block;padding:2px 0}

.try{position:relative;border-radius:24px;overflow:hidden;border:1px solid var(--line);background:var(--card)}
.try>img{width:100%;height:100%;object-fit:cover;display:block}.try iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:#111}
.tbtn{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);border:0;background:var(--pink);color:var(--on-pink);border-radius:999px;padding:13px 24px;font:700 16px 'DM Sans',sans-serif;cursor:pointer;box-shadow:0 8px 28px rgba(0,0,0,.4);white-space:nowrap}
.tbtn:hover{transform:translateX(-50%) translateY(-2px)}.tnote{font-size:14.5px;color:var(--mut);margin:10px 4px 0}.tnote a{font-weight:700;color:var(--fg)}
.bcard.big{display:flex;flex-direction:column;padding:18px}.bcard.big .imgl{display:block}.bcard.big .more{margin-top:auto;padding:10px 8px 6px}
.bcard.big .more p{margin:0 0 14px;color:var(--mut);font-size:17px;line-height:1.55;max-width:60ch}.bcard.big .chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.bcard.big .chips span{border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:14px;color:var(--mut)}
.bcard.big .btns{display:flex;flex-wrap:wrap;gap:10px}.btn.s{padding:12px 22px;font-size:16px}
.gh{width:20px;height:20px;fill:currentColor;flex:none;vertical-align:-4px;margin-right:2px}

/* motion (only when JS is on and the visitor has not asked for reduced motion) */
.js .rv{opacity:0;transform:translateY(34px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0ms)}
.js .rv.in{opacity:1;transform:none}
.js .rv.card.in:hover,.js .rv.bcard.in:hover{transform:translateY(-4px)}
.par{translate:0 var(--py,0px);will-change:translate}
.pan{position:relative;overflow:hidden}.pan>img{position:absolute;left:0;top:0;width:100%;height:130%;object-fit:cover;object-position:top;border-radius:0;will-change:transform}
.pan.r16{aspect-ratio:16/10}.bcard .pan{border-radius:16px}.bcol .bcard .pan{border-radius:14px}
.card .im img{transition:transform .6s cubic-bezier(.2,.7,.2,1)}.card:hover .im img{transform:scale(1.07)}
.bar-p{position:fixed;left:0;top:0;height:4px;width:100%;background:var(--pink);transform-origin:0 50%;transform:scaleX(0);z-index:60;pointer-events:none}
.hero h1 .ln{display:block;overflow:hidden;padding-bottom:.06em}.hero h1 .ln>span{display:block}
.js .hero h1 .ln>span{transform:translateY(105%);animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}
.js .hero h1 .ln:nth-child(2)>span{animation-delay:.12s}.js .hero h1 .ln:nth-child(3)>span{animation-delay:.24s}
@keyframes up{to{transform:none}}
.js .hrow{opacity:0;animation:fade .9s .55s ease forwards}@keyframes fade{to{opacity:1}}
.marq{overflow:hidden;margin:6px -28px 44px;padding:14px 0;border-block:2px solid var(--fg);white-space:nowrap;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.marq .tr{display:inline-flex;gap:0;animation:mq 60s linear infinite;will-change:transform}.marq:hover .tr{animation-play-state:paused}
.marq span{font:800 clamp(26px,3.6vw,40px)/1 'Bricolage Grotesque',sans-serif;letter-spacing:-.03em;padding:0 22px;display:inline-flex;align-items:center;gap:44px}
.marq span:after{content:"";width:14px;height:14px;border-radius:50%;background:var(--pink);display:inline-block}.marq span:nth-child(3n):after{background:var(--teal)}.marq span:nth-child(3n+1):after{background:var(--yellow)}
@keyframes mq{to{transform:translateX(-50%)}}
.card.pop{animation:pop .45s cubic-bezier(.2,.8,.2,1)}@keyframes pop{from{opacity:0;transform:scale(.94) translateY(12px)}to{opacity:1;transform:none}}
.btn.p{position:relative;overflow:hidden}.btn.p:after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.35) 50%,transparent 70%);transform:translateX(-120%);transition:transform .7s}.btn.p:hover:after{transform:translateX(120%)}
@media(prefers-reduced-motion:reduce){.marq .tr{animation:none}.js .rv,.js .hero h1 .ln>span,.js .hrow{opacity:1!important;transform:none!important;animation:none!important}}

.prose{max-width:70ch}.prose h2{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-0.03em;font-size:clamp(26px,3.4vw,34px);line-height:1.1;margin:44px 0 10px}
.prose p,.prose li{color:var(--mut);font-size:19px;line-height:1.7}.prose p{margin:0 0 14px}.prose ul{padding-left:22px;margin:0 0 14px}.prose li{margin:6px 0}.prose a{color:var(--fg);font-weight:700}.prose strong{color:var(--fg)}
.pghero{padding:36px 0 8px}.pghero h1{font-size:clamp(54px,9vw,112px);margin:0 0 18px}.pghero .lead{font-size:clamp(19px,2.2vw,24px);line-height:1.5;color:var(--mut);max-width:60ch;margin:0 0 24px}
.upd{font-size:15px;color:var(--mut);margin-top:36px}
.cta{display:flex;flex-wrap:wrap;gap:14px;margin:22px 0 4px}

.art{position:relative;width:100%;height:100%;overflow:hidden;background:var(--card)}.art svg{position:absolute;inset:0;width:100%;height:100%}
.art .an{position:absolute;left:16px;bottom:30px;font:800 clamp(20px,2.4vw,26px)/1.05 'Bricolage Grotesque',sans-serif;letter-spacing:-.03em;color:var(--fg)}
.art small{position:absolute;left:16px;bottom:10px;color:var(--mut);font-size:13px}.art.big .an{font-size:clamp(28px,4vw,44px);left:26px;bottom:44px}.art.big small{left:26px;bottom:20px;font-size:15px}

.clips{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:14px}
.clip{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 18px}.clip b{font:800 20px 'Bricolage Grotesque',sans-serif;letter-spacing:-.02em}
.clip p{margin:4px 0 12px;color:var(--mut);font-size:15.5px;line-height:1.5}.clip audio{width:100%;height:40px}
.skip{position:absolute;left:-999px;top:8px;background:var(--teal);color:#06221d;padding:8px 14px;border-radius:8px;z-index:50;font-weight:700}.skip:focus{left:8px}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--yellow);outline-offset:3px;border-radius:8px}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
.crumbs{font-size:15px;color:var(--mut);padding:22px 0 8px}.crumbs a{color:var(--mut)}
.phero{display:grid;grid-template-columns:1.3fr 1fr;gap:40px;align-items:center;padding:12px 0 20px}@media(max-width:900px){.phero{grid-template-columns:1fr}}
.phero>*{min-width:0}.shot{width:100%;height:auto;border-radius:24px;border:1px solid var(--line);background:var(--card);display:block}
.noshot{aspect-ratio:16/10;border-radius:24px;border:1px solid var(--line);overflow:hidden}
.phero h1{font-size:clamp(44px,6vw,76px);margin:0 0 14px;overflow-wrap:anywhere}.phero .lead{font-size:20px;color:var(--mut);max-width:58ch;margin:0 0 22px;overflow-wrap:anywhere}
.meta{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 20px;margin:24px 0;font-size:16px;border-top:1px solid var(--line);padding-top:20px}.meta dt{color:var(--mut)}.meta dd{margin:0;overflow-wrap:anywhere}
.callout{margin-top:18px;padding:16px 18px;border:2px dashed var(--line);border-radius:16px;color:var(--mut);font-size:16px}.callout a{font-weight:700;color:var(--fg)}
.strip{display:grid;grid-template-columns:1.3fr 1fr;gap:40px;align-items:start;border-top:1px solid var(--line);padding:22px 0 8px;margin-top:8px}@media(max-width:900px){.strip{grid-template-columns:1fr;gap:18px}}
.strip .meta{margin:0;border-top:0;padding-top:0}.strip .callout{margin-top:0}
.about p{max-width:68ch;color:var(--mut)}.abt{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:clamp(20px,4vw,56px);align-items:start}.abt p{max-width:none}.abt .stat{font-size:14px;border-left:3px solid var(--pink,#ff6aa5);padding-left:12px}.ph{margin:0 0 10px;font-size:17px}.gfs{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:16px 0}.gf{margin:0}.gf img{width:100%;height:auto;border-radius:12px;border:1px solid var(--line);display:block}.gf figcaption{font-size:14px;color:var(--mut);margin-top:8px}.gd{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px;margin-top:16px}.gc{border:1px solid var(--line);border-radius:14px;padding:0 0 16px;overflow:hidden}.gc img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-bottom:1px solid var(--line);margin-bottom:14px}.gc b{display:block;margin:0 18px 6px;font-size:16px}.gc p{margin:0 18px;color:var(--mut);font-size:15px}.steps2{padding-left:22px;color:var(--mut);max-width:68ch}.steps2 li{margin:8px 0}.getit,.expect,.guide{margin-top:8px}#demo,#get{scroll-margin-top:84px}.pts{margin:0;padding-left:20px;color:var(--mut)}.pts li{margin:6px 0}
.minis{display:grid;grid-template-columns:repeat(var(--cols),minmax(0,1fr));gap:12px;margin-top:16px}.mini{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--card,transparent)}.mini .im{aspect-ratio:16/10;overflow:hidden}.mini .im img,.mini .im .art,.mini .im .tcard{width:100%;height:100%;object-fit:cover}.mini b{display:block;padding:8px 10px;font-size:13px;line-height:1.25}.mini:hover{border-color:var(--pink,#ff6aa5)}
@media(max-width:1100px){.minis{grid-template-columns:repeat(4,minmax(0,1fr))}}@media(max-width:820px){.abt{grid-template-columns:1fr}}@media(max-width:700px){.minis{grid-template-columns:repeat(2,minmax(0,1fr))}}.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:14px;color:var(--mut);margin:3px 5px 3px 0}
"""

TOG = """
(function(){var b=document.getElementById('tog');if(!b)return;var r=document.documentElement;
function cur(){var t=r.getAttribute('data-theme');if(t)return t;return window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'}
function label(){b.textContent=cur()==='dark'?'Light':'Dark'}
b.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('s87-theme',n)}catch(e){}label()});label()})();
"""


FXJS = """
(function(){var R=document.documentElement;if(!R.classList.contains('js'))return;
var vh=window.innerHeight;window.addEventListener('resize',function(){vh=window.innerHeight},{passive:true});
var bar=document.createElement('div');bar.className='bar-p';document.body.appendChild(bar);
/* reveal on scroll */
var sel='.card,.bcard,.step,.cat h3,.cat p.sub,section h2.sec,section p.sub,.band,.support,.phero>div,.about,.meta,.callout,.bar,.crumbs,.marq,.fcols';
var els=[].slice.call(document.querySelectorAll(sel));
els.forEach(function(el){if(el.closest('.hero'))return;el.classList.add('rv');var sib=el.parentNode?[].indexOf.call(el.parentNode.children,el):0;el.style.setProperty('--d',((sib%6)*70)+'ms')});
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)})}else{document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')})}
/* scroll-linked motion */
var pars=[].slice.call(document.querySelectorAll('.par')),pans=[].slice.call(document.querySelectorAll('.pan')),tick=false;
function frame(){tick=false;var y=window.scrollY||0,h=document.documentElement.scrollHeight-vh;bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
pars.forEach(function(el){var r=el.getBoundingClientRect();if(r.bottom<-200||r.top>vh+200)return;var f=parseFloat(el.getAttribute('data-par'))||0.06;el.style.setProperty('--py',((r.top+r.height/2-vh/2)*f)+'px')});
pans.forEach(function(el){var r=el.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var p=Math.max(0,Math.min(1,(vh-r.top)/(vh+r.height)));var img=el.firstElementChild;if(img)img.style.transform='translateY('+(-p*23.07).toFixed(2)+'%)'})}
function on(){if(!tick){tick=true;requestAnimationFrame(frame)}}
window.addEventListener('scroll',on,{passive:true});window.addEventListener('resize',on,{passive:true});frame();
/* filter pop-in */
var q=document.getElementById('q');function pop(){document.querySelectorAll('#all .card').forEach(function(c){if(c.style.display==='none')return;c.classList.remove('pop');void c.offsetWidth;c.classList.add('pop')})}
document.querySelectorAll('.chip').forEach(function(b){b.addEventListener('click',function(){setTimeout(pop,0)})});if(q)q.addEventListener('input',function(){setTimeout(pop,0)});
})();
"""
TRYJS = """\ndocument.addEventListener('play',function(e){[].forEach.call(document.querySelectorAll('audio'),function(a){if(a!==e.target)a.pause()})},true);
(function(){var w=document.querySelector('.try');if(!w)return;var b=w.querySelector('.tbtn');if(!b)return;var VW=1100;
b.addEventListener('click',function(){var poster=w.innerHTML;var f=document.createElement('iframe');f.src=w.getAttribute('data-src');f.title=w.getAttribute('data-title');
f.setAttribute('sandbox','allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox');
f.style.cssText='position:absolute;left:0;top:0;width:'+VW+'px;height:1400px;border:0;transform-origin:0 0;opacity:0;transition:opacity .4s';
b.textContent='Loading...';b.disabled=true;w.appendChild(f);var H=0;
function fit(){if(!H)return;var s=w.clientWidth/VW;f.style.height=H+'px';f.style.transform='scale('+s+')';w.style.aspectRatio=VW+' / '+H}
f.addEventListener('load',function(){var R=parseFloat(w.getAttribute('data-ratio')||0);if(R){H=Math.round(VW*R);[].slice.call(w.children).forEach(function(c){if(c!==f)w.removeChild(c)});fit();f.style.opacity=1;f.focus();if('ResizeObserver' in window)new ResizeObserver(fit).observe(w);return}var prev=-1,tries=0;
function measure(){var d=f.contentDocument,cw=f.contentWindow,bot=0;
var vh=cw.innerHeight;function fixedFull(el){var cs=cw.getComputedStyle(el),r=el.getBoundingClientRect();return cs.position==='fixed'&&r.height>=vh*0.97}
function skip(el){var cs=cw.getComputedStyle(el);return(cs.position==='fixed'&&!fixedFull(el))||cs.display==='none'||el.tagName==='SCRIPT'||el.tagName==='STYLE'}
function bottom(el,dep){var r=el.getBoundingClientRect();if(r.height>=vh*0.97&&dep<4&&el.children.length){var m=0,tp=1e9;[].forEach.call(el.children,function(c){if(!skip(c)){var cr=c.getBoundingClientRect();if(cr.height>2){m=Math.max(m,bottom(c,dep+1));tp=Math.min(tp,cr.top)}}});if(!m)return r.bottom;return cw.getComputedStyle(el).position==='fixed'?(m-tp):m}return r.bottom}
[].forEach.call(d.body.children,function(el){if(skip(el))return;var r=el.getBoundingClientRect();if(r.height>2)bot=Math.max(bot,bottom(el,0))});return Math.ceil(Math.max(300,bot+14))}
(function tick(){tries++;var h;try{h=measure()}catch(e){h=0}
if(h&&Math.abs(h-prev)<=3&&tries>=10||tries>=26){H=h||H||600;[].slice.call(w.children).forEach(function(c){if(c!==f)w.removeChild(c)});fit();f.style.opacity=1;f.focus();return}
prev=h;setTimeout(tick,400)})()});
if('ResizeObserver' in window)new ResizeObserver(fit).observe(w);window.addEventListener('resize',fit)})})();
"""
JS = """
(function(){var q=document.getElementById('q'),chips=[].slice.call(document.querySelectorAll('.chip')),cards=[].slice.call(document.querySelectorAll('#all .card')),cats=[].slice.call(document.querySelectorAll('#all .cat')),cat='all';
function run(){var t=(q&&q.value||'').toLowerCase();cards.forEach(function(c){var ok=(cat==='all'||c.dataset.grp===cat)&&(!t||c.dataset.s.indexOf(t)>-1);c.style.display=ok?'':'none'});
cats.forEach(function(s){var any=[].some.call(s.querySelectorAll('.card'),function(c){return c.style.display!=='none'});s.style.display=any?'':'none'})}
chips.forEach(function(b){b.addEventListener('click',function(){cat=b.dataset.cat;chips.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run()})});
if(q)q.addEventListener('input',run)})();
"""

HEADJS = """<script>try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("js")}catch(e){}</script><script>try{var m=localStorage.getItem("s87-theme");if(m==="light"||m==="dark")document.documentElement.setAttribute("data-theme",m)}catch(e){}</script>"""

def page(title, desc, path, body, ld=None, og=None, js=False):
    canon = BASE + path
    ldj = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    img = f'<meta property="og:image" content="{BASE}{og}"><meta name="twitter:card" content="summary_large_image">' if og else '<meta name="twitter:card" content="summary">'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}">
<meta name="theme-color" content="#141618" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#f6efe3" media="(prefers-color-scheme: light)">
{HEADJS}
<meta property="og:type" content="website"><meta property="og:site_name" content="Studio 87"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">{img}
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/BricolageGrotesque-800.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>{ldj}</head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="top"><div class="wrap"><a class="brand" href="/">{LOGO}STUDIO 87</a><nav class="nav"><a class="keep" href="/#all">Software</a><a href="/#synths">Synths</a><a href="/#dynamics">Effects</a><a href="/#hardware-controllers">Controllers</a><a href="/gearupdater/">Gear Updater</a><button class="tog" id="tog" type="button" aria-label="Switch between light and dark mode">Theme</button><a class="pill" href="https://ko-fi.com/studio87">Ko-fi</a></nav></div></div>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="fcols"><div><b>Studio 87</b>Free, open source music software, Linux first. Made by one person.</div><div><b>Browse</b><a href="/#synths">Synths</a><a href="/#dynamics">Compressors and EQ</a><a href="/#hardware-controllers">Hardware controllers</a><a href="/gearupdater/">Gear Updater</a></div><div><b>Links</b><a href="/support/">Support Studio 87</a><a href="/privacy/">Privacy</a><a href="https://github.com/SpeakingColors">GitHub</a><a href="https://www.youtube.com/@sonatural_" rel="me noopener">YouTube</a><a href="/llms.txt">Plain-text summary</a></div></div>Each project has its own open source license; see its page. To build on a project, fork it on GitHub.</div></footer>
<script>{TOG}</script><script>{TRYJS}</script><script>{FXJS}</script>{f'<script>{JS}</script>' if js else ''}</body></html>"""

SUPPORT = """<div class="support"><div class="hd">If it helps your music, buy me a coffee.</div><a class="btn" href="https://ko-fi.com/studio87">Support on Ko-fi</a></div>"""

def thumb(rn, dn="", kind=""):
    return (f'<img src="/img/thumb/{rn}.jpg" alt="{e(dn or rn)} screenshot" loading="lazy">' if rn in have
            else (f'<div class="art">{ART[slug(rn)]()}</div>' if slug(rn) in ART else f'<div class="tcard"><b>{e(dn or rn)}</b><small>{e(kind)}</small></div>'))

def is_test(rn): r = repos[rn]["release"]; return bool(r and r[2] == "true")

def card(rn, dn, cslug, kind, d, grp):
    d = COPY.get(rn, {}).get("tagline", d)
    lab, col = LABEL[cslug]
    s = (dn + " " + d + " " + lab + " " + " ".join(repos[rn]["topics"])).lower()
    return (f'<a class="card" href="/{slug(rn)}/" data-grp="{grp}" data-s="{e(s)}"><div class="im">{thumb(rn, dn, kind)}</div>'
            f'<div class="tx"><b>{e(dn)}<span class="lab {col}">{lab}</span>{"<span class=badge>MOCKUP</span>" if rn in DESIGN else ("<span class=badge>TEST</span>" if is_test(rn) else "")}</b><span class="d">{e(short(d, 100))}</span></div></a>')

GRP = {"synths": "synths", "dynamics": "effects", "tone": "effects", "space": "effects", "dj-and-creative": "creative",
       "studio-tools": "tools", "tv-apps": "tools", "recipe-books": "tools", "hardware-controllers": "controllers", "korg-units": "korg", "developers": "dev"}
urls = ["/"]


PLAYCSS = """
.play{position:fixed;inset:0;display:flex;flex-direction:column;background:var(--bg)}
.phd{display:flex;align-items:center;justify-content:space-between;gap:12px;height:64px;padding:0 20px;border-bottom:1px solid var(--line);flex:none}
.phd .pt{font:800 20px 'Bricolage Grotesque',sans-serif;letter-spacing:-.02em;text-align:center;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.phd .pt small{font:500 14px 'DM Sans',sans-serif;color:var(--mut);margin-left:8px}
.phd .pr{display:flex;align-items:center;gap:10px}.xbtn{display:inline-flex;align-items:center;gap:8px;border:2px solid var(--fg);color:var(--fg);border-radius:999px;padding:9px 18px;font:700 16px 'DM Sans',sans-serif;text-decoration:none;white-space:nowrap}.xbtn:hover{background:var(--fg);color:var(--bg)}
.play iframe{flex:1 1 auto;width:100%;border:0;background:#111;min-height:0}
@media(max-width:640px){.phd .pt{display:none}.phd{padding:0 12px}.xbtn{padding:8px 14px}}
"""
def playpage(rn, dn, back):
    path = f"/play/{slug(rn)}/"; os.makedirs(OUT + path, exist_ok=True)
    html_ = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(dn)}: interactive demo | Studio 87</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{back}">
<meta name="theme-color" content="#141618" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#f6efe3" media="(prefers-color-scheme: light)">
{HEADJS}<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<style>{CSS}{PLAYCSS}</style></head><body>
<div class="play"><header class="phd"><a class="brand" href="/">{LOGO}STUDIO 87</a><span class="pt">{e(dn)}<small>interactive demo</small></span>
<div class="pr"><button class="tog" id="tog" type="button" aria-label="Switch between light and dark mode">Theme</button><a class="xbtn" id="xb" href="{back}" aria-label="Close the demo and go back to {e(dn)}">&#10005; Close</a></div></header>
<iframe id="fr" src="/try/{TRY[rn]["file"]}" title="{e(dn)} interactive demo" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe></div>
<script>{TOG}
(function(){{var back=document.getElementById('xb').getAttribute('href');function esc(e){{if(e.key==='Escape')location.href=back}}document.addEventListener('keydown',esc);
var f=document.getElementById('fr');f.addEventListener('load',function(){{try{{f.contentWindow.addEventListener('keydown',esc)}}catch(e){{}}}})}})();</script></body></html>"""
    open(OUT + path + "index.html", "w").write(html_)

# ---- product pages
for cslug, ctitle, kind, blurb, items in CATS:
    for rn, dn in items:
        r = repos.get(rn)
        if not r: continue
        d = COPY.get(rn, {}).get("tagline") or (r["description"] or "").strip(); cp = COPY.get(rn, {}); rel = r["release"]; test = is_test(rn)
        dl = rel[1] if rel else f"https://github.com/SpeakingColors/{rn}"
        title = (f"{dn}: free open source tube channel strip (design mockup)" if rn in DESIGN else f"{dn}: free open source {kind}"); desc = short(d, 155)
        lab, col = LABEL[cslug]
        tags = "".join(f'<span class="tag">{e(t)}</span>' for t in r["topics"][:12])
        w, h = 1200, 750
        if rn in have:
            w, h = dims(f"{OUT}/img/full/{rn}.jpg")
            shot = f'<img class="shot" src="/img/full/{rn}.jpg" alt="{e(dn)} screenshot" width="{w}" height="{h}">'; og = f"/img/full/{rn}.jpg"
        else:
            shot = (f'<div class="noshot"><div class="art big">{ART[slug(rn)]()}</div></div>' if slug(rn) in ART else f'<div class="noshot"><div class="tcard"><b style="font-size:clamp(30px,4vw,44px)">{e(dn)}</b><small>{e(kind)}</small></div></div>'); og = None
        if rn in TRY:
            ratio_attr = (' data-ratio="' + str(TRY[rn]["ratio"]) + '"') if TRY[rn].get("ratio") else ""
            ar = "16 / 9" if TRY[rn].get("ratio") else (f"{w} / {h}" if rn in have else "16 / 10")
            inner = (f'<img src="/img/full/{rn}.jpg" alt="{e(dn)} screenshot" width="{w}" height="{h}">' if rn in have
                     else f'<div class="tcard"><b style="font-size:clamp(30px,4vw,44px)">{e(dn)}</b><small>{e(kind)}</small></div>')
            media = (f'<div class="try" id="demo" data-src="/try/{TRY[rn]["file"]}"{ratio_attr} data-title="{e(dn)} interactive mockup" style="aspect-ratio:{ar}">{inner}'
                     f'<button class="tbtn" type="button">&#9654; {"Open the recipe book" if rn == "SynthCookBook" else ("Open Cat FX Studio" if rn in FXSTUDIO else "Try the interface")}</button></div>'
                     f'<p class="tnote">{"This is the recipe book itself, running in your browser. Pick a synth, set the knobs, and your recipes are saved in this browser." if rn == "SynthCookBook" else ("This is Cat FX Studio, one test page with six Cat effects: Cat Crusher, Fat Cat, Cat Spacer, Meowbass, Meowximizer and Scaredy Cat. Pick one, press play and move the controls. It is a browser preview, not the compiled plugin." if rn in FXSTUDIO else ("Interactive mockup with sample content only: click it, then use the arrow keys, Enter and Escape, as you would with a TV remote. Sound starts after the first click." if rn == "StarDriftTVLauncher" else "Interactive mockup of the interface: click and drag the controls. The real plugin makes the sound."))} <a href="/play/{slug(rn)}/">Open full screen</a></p>')
        else:
            media = shot
        _sl = [(n2, d2) for n2, d2 in items if n2 != rn and n2 in repos]
        _rows = -(-len(_sl) // 8) if _sl else 1; _cols = -(-len(_sl) // _rows) if _sl else 1
        sib = "".join(f'<a class="mini" href="/{slug(n2)}/"><div class="im">{thumb(n2, d2, kind)}</div><b>{e(d2)}</b></a>' for n2, d2 in _sl)[:60000]
        meta = (f'<dt>Price</dt><dd>Free</dd><dt>License</dt><dd>{e(r["license"] if r["license"] not in ("", "Other") else "See the repository")}</dd>'
                f'<dt>Type</dt><dd>{e("Tube channel strip (VST3 planned)" if rn in DESIGN else kind[0].upper() + kind[1:])}</dd>'
                + f'<dt>Source</dt><dd><a href="https://github.com/SpeakingColors/{e(rn)}">{GHICON} github.com/SpeakingColors/{e(rn)}</a></dd>')
        hear = ""
        if rn in AUDIO and AUDIO[rn]:
            _items = "".join(f'<div class="clip"><b>{e(c["preset"])}</b><p>{e(c.get("description",""))}</p><audio controls preload="none" src="/audio/{slug(rn)}/{e(c["file"])}"></audio></div>' for c in AUDIO[rn])
            hear = f'<section><h2 class="sec">Hear it</h2><p class="sub">Short clips of factory presets. Press play.</p><div class="clips">{_items}</div></section>'
        status = ("Status: design mockup. The plugin is not built yet, but you can try the interface above in your browser." if rn in DESIGN else ("Status: test build. It installs and runs, but has not been checked on every machine yet." if test else ("Status: released." if rel else "Status: in development.")))
        pts = ('<div><h3 class="ph">What it does</h3><ul class="pts">' + "".join(f"<li>{e(x)}</li>" for x in cp["points"]) + "</ul></div>") if cp.get("points") else ""
        if cp.get("cta"): cta = f'<a class="btn p" href="{e(cp["cta"][1])}">{e(cp["cta"][0])}</a>'
        elif rel: cta = f'<a class="btn p" href="{e(dl)}">&#11015; Download {e(rel[0])}</a>'
        else: cta = f'<a class="btn p" href="{e(dl)}">Get it on GitHub</a>'
        trybtn = ' <a class="btn o" href="#demo">&#9654; Try it in your browser</a>' if rn in TRY else ""
        extra = ""
        if cp.get("guide"):
            _shots = "".join(f'<figure class="gf"><img src="/img/guide/{rn}/{f_}" alt="{e(c_)}" loading="lazy" width="1200" height="675"><figcaption>{e(c_)}</figcaption></figure>' for f_, c_ in cp.get("shots", []))
            extra += (f'<section class="guide"><h2 class="sec">How to use it</h2><p class="sub">{e(cp.get("guide_intro",""))}</p>' + (f'<p class="gl">' + " &middot; ".join(f'<a href="{e(u_)}">{e(l_)}</a>' for l_, u_ in cp.get("guide_links", [])) + '</p>' if cp.get("guide_links") else "") + '<div class="gd">'
                      + "".join((f'<div class="gc">' + (f'<img src="/img/guide/{rn}/{g_[2]}" alt="{e(g_[0])}: screenshot of the mockup" loading="lazy" width="1200" height="675">' if len(g_) > 2 else "") + f'<b>{e(g_[0])}</b><p>{e(g_[1])}</p></div>') for g_ in cp["guide"]) + "</div></section>")
        if cp.get("get"):
            extra += (f'<section class="getit" id="get"><h2 class="sec">{e(cp.get("get_title","Get it"))}</h2><p class="sub">{e(cp.get("get_intro",""))}</p><ol class="steps2">'
                      + "".join(f"<li>{e(s_)}</li>" for s_ in cp["get"]) + "</ol>"
                      + (f'<p><a href="{e(cp["get_link"][1])}">{e(cp["get_link"][0])}</a></p>' if cp.get("get_link") else "") + "</section>")
        if cp.get("expect"):
            extra += '<section class="expect"><h2 class="sec">What to expect</h2><ul class="pts">' + "".join(f"<li>{e(x_)}</li>" for x_ in cp["expect"]) + "</ul></section>"
        body = f"""<div class="wrap"><p class="crumbs"><a href="/">Studio 87</a> › <a href="/#{cslug}">{e(ctitle)}</a> › {e(dn)}</p>
<div class="phero"><div>{media}</div><div>
<div style="margin-bottom:12px"><span class="lab {col}">{lab}</span> {'<span class="badge">DESIGN MOCKUP</span>' if rn in DESIGN else ('<span class="badge">TEST BUILD</span>' if test else '')}</div>
<h1 class="hd">{e(dn)}</h1><p class="lead">{e(d)}</p>
{cta}{trybtn}</div></div>
<div class="strip"><dl class="meta">{meta}</dl>{('<div class="callout">Tip: the <a href="/gearupdater/">Gear Updater</a> app can browse, download and update Studio 87 software for you.</div>' if rn not in ("gearupdater", "StarDriftTVLauncher") else "")}</div>
{hear}<section class="about"><h2 class="sec">About {e(dn)}</h2><div class="abt"><div><p>{e(cp.get("about") or d)}</p><p class="stat">{e(status)}</p></div>{pts}</div><p>{tags}</p></section>
{extra}
{f'<section><h2 class="sec">More in {e(ctitle)}</h2><div class="minis" style="--cols:{_cols}">{sib}</div></section>' if sib else ''}
{SUPPORT}</div>"""
        ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": dn, "applicationCategory": "MultimediaApplication",
              "operatingSystem": "Linux, Windows, macOS", "description": d, "url": BASE + f"/{slug(rn)}/",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "author": {"@type": "Organization", "name": "Studio 87"}}
        if og: ld["image"] = BASE + og
        p = f"/{slug(rn)}/"; os.makedirs(OUT + p, exist_ok=True)
        open(OUT + p + "index.html", "w").write(page(title, desc, p, body, ld, og)); urls.append(p)
        if rn in TRY: playpage(rn, dn, p)


# ---- text pages: Support and Privacy
def textpage(path, title, desc, body):
    os.makedirs(OUT + path, exist_ok=True)
    open(OUT + path + "index.html", "w").write(page(title, desc, path, body)); urls.append(path)

textpage("/support/", "Support Studio 87: free and open source music software", "Why Studio 87 is free, what a coffee on Ko-fi does, and other ways to help.",
f"""<div class="wrap"><div class="pghero"><h1 class="hd">Support Studio 87.</h1>
<p class="lead">Everything here is free and open source, made by one person. If it helps your music, a coffee keeps it coming.</p>
<div class="cta"><a class="btn p" href="https://ko-fi.com/studio87">Support on Ko-fi</a><a class="btn o" href="/#all">Browse the software</a></div></div>
<div class="prose">
<h2>Why it's free</h2>
<p>I build these synths, effects and tools because I want them to exist, and because good music software shouldn't need a subscription. Studio 87 is Linux first, with Windows and macOS builds for many plugins, and everything is open source so you can see how it works.</p>
<h2>What a coffee does</h2>
<p>Studio 87 is one person's work. Support buys time: time to build the next plugin, to test the current ones on more machines, and to fix what doesn't work yet. There are no goals or tiers to unlock. A coffee simply makes more of this possible.</p>
<div class="cta"><a class="btn p" href="https://ko-fi.com/studio87">Buy a coffee on Ko-fi</a></div>
<h2>Other ways to help</h2>
<p>You don't have to give money to help. These all count:</p>
<ul><li><strong>Make music with it.</strong> That's the whole point.</li><li><strong>Tell another producer</strong> about a plugin you like.</li><li><strong>Star a project on GitHub.</strong> It helps other people find it.</li><li><strong>Fork it and build something.</strong> I don't manage issues or pull requests, so a fork is the best way to build on a project.</li></ul>
<h2>What you get either way</h2>
<p>Every plugin stays free. There are no ads on this site, no locked features and no account to download anything. Supporting is a thank-you, never a toll.</p>
<p class="upd">Thank you for using Studio 87.</p>
</div></div>""")

textpage("/privacy/", "Privacy: Studio 87", "What this website, the interactive demos and the Gear Updater do with your information, in plain words.",
f"""<div class="wrap"><div class="pghero"><h1 class="hd">Privacy.</h1>
<p class="lead">Short version: this site doesn't ask who you are, and I run no cookies, analytics or ads. It's hosted on GitHub, which has its own practices, explained below.</p></div>
<div class="prose">
<h2>This website</h2>
<p>I don't set any cookies, and I run no analytics, ads or tracking scripts of my own. When I checked, the pages, images, fonts and demos all came from this site itself, and the server sent no cookies.</p>
<h2>What GitHub may see</h2>
<p>This site is hosted on GitHub Pages, so GitHub's servers deliver every page. Like any web host, GitHub can see technical details of a visit, such as your IP address, and it may use logs or analytics for its own purposes. GitHub explains its practices in its <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">privacy statement</a>. I can't see or control any of that, and I don't receive visitor data from GitHub.</p>
<p>If you'd like extra protection, use whichever tools you trust: an ad or tracker blocker in your browser, a privacy-focused browser, or a network-level filter such as Pi-hole. Examples are uBlock Origin, Privacy Badger and Ghostery. They're only examples: I'm not affiliated with any of them, and this site works fine with or without them.</p>
<h2>What stays on your device</h2>
<p>If you pick light or dark mode with the switch at the top, the site remembers your choice in your browser's local storage. The interactive demos ("Try the interface") can save your own settings or presets in your browser the same way. The demos make no network requests. You can clear all of this at any time by clearing your browser's site data.</p>
<h2>The Gear Updater</h2>
<p>The Gear Updater app asks GitHub for the list of Studio 87 releases only when you open it or press "Check for updates". Those are read-only requests for public information, and it downloads a release file only when you choose one. It works offline and shows the list it saved last time. Signing in with GitHub is optional, only raises GitHub's request limit, and keeps its token in your system keychain. The <a href="https://github.com/SpeakingColors/gearupdater">README</a> has the details.</p>
<h2>The plugins</h2>
<p>The plugins run inside your music software, on your computer. Every one is open source, so anyone can read the code to see exactly what it does.</p>
<h2>Other sites</h2>
<p>This site links to GitHub, where the code and downloads live, and to Ko-fi, where you can support the project. Their own privacy policies apply once you are there. Ko-fi and its payment providers handle any payment, and I don't see your card or bank details.</p>
<h2>If this changes</h2>
<p>If anything here changes, I'll update this page.</p>
<p class="upd">Last updated 15 November 2026.</p>
</div></div>""")

# ---- home
n_proj = len(urls) - 1
GN = [("all", "All"), ("synths", "Synths"), ("effects", "Effects"), ("creative", "DJ and creative"), ("tools", "Tools and apps"), ("controllers", "Controllers"), ("korg", "Korg units")]
chips = "".join(f'<button class="chip" data-cat="{c}" aria-pressed="{"true" if c == "all" else "false"}">{t}</button>' for c, t in GN)
sections = ""
for cslug, ctitle, kind, blurb, items in CATS:
    cs = "".join(card(rn, dn, cslug, kind, repos[rn]["description"] or "", GRP[cslug]) for rn, dn in items if rn in repos)
    sections += f'<div class="cat" id="{cslug}"><h3>{e(ctitle)}</h3><p class="sub">{e(blurb)}</p><div class="grid">{cs}</div></div>'
steps = """<div class="steps"><div class="step"><i>01</i><b>Pick something</b><p>Browse the synths, effects and tools. Everything is free.</p></div>
<div class="step"><i>02</i><b>Download it</b><p>Grab the release zip from GitHub, or let the Gear Updater app do it for you.</p></div>
<div class="step"><i>03</i><b>Open it in your DAW</b><p>VST3 plugins show up after a plugin rescan. Many also run standalone.</p></div></div>"""
MARQ = "".join(f"<span>{e(dn)}</span>" for c in CATS for rn, dn in c[4] if rn in repos and c[0] not in ("developers",))
home = f"""<div class="wrap"><div class="hero"><h1 class="hd"><span class="ln"><span>Free</span></span><span class="ln"><span>plugins.</span></span><span class="ln"><span><em>Really.</em></span></span></h1>
<div class="hrow"><p>Synths, effects, DJ tools and controllers for hardware synths. All open source, all made by one person, Linux first.</p>
<div class="hbtn"><a class="btn p" href="#all">Browse {n_proj} projects</a><a class="btn o" href="/gearupdater/">Gear Updater</a></div></div></div>
<div class="marq" aria-hidden="true"><div class="tr">{MARQ}{MARQ}</div></div>
<div class="bento"><div class="bcard big"><a class="imgl" href="/supurrrsaw-vst/"><div class="pan r16"><img src="/img/full/SupurrrSaw-VST.jpg" alt="SupurrSaw synth plugin interface"></div></a><div class="row"><span class="bn">SupurrSaw</span><span class="s">Supersaw, hoover and acid synth</span></div>
<div class="more"><p>Three layers of supersaw, hoover and acid sounds, with built-in effects and presets. VST3 and standalone, built for Linux with Windows and macOS installers.</p><div class="chips"><span>supersaw</span><span>hoover</span><span>acid</span><span>trance</span><span>hardstyle</span></div><div class="btns"><a class="btn p s" href="/supurrrsaw-vst/">See SupurrSaw</a><a class="btn o s" href="https://github.com/SpeakingColors/SupurrrSaw-VST/releases">Download</a></div></div></div><div class="bcol"><a class="bcard teal par" data-par="0.06" href="/purrone/"><div class="pan r16"><img src="/img/full/PurrOne.jpg" alt="PurrOne synth interface"></div><div class="bn">PurrOne</div><span class="s">Thick mono synth for bass and lead.</span></a>
<a class="bcard yellow par" data-par="0.1" href="/kickkitten/"><div class="pan r16"><img src="/img/full/KickKitten.jpg" alt="Kick Kitten interface"></div><div class="bn">Kick Kitten</div><span class="s">A trance kick generator and maker.</span></a></div></div>
<div class="band"><div><h2 class="hd">One app for all of it.</h2><p>The Gear Updater browses, downloads, installs and updates every Studio 87 plugin, so you never dig through GitHub again.</p><a class="btn l" href="/gearupdater/">See the Gear Updater</a></div>
<div class="pan par" data-par="-0.05" style="aspect-ratio:16/11;border-radius:20px;border:3px solid var(--fg)"><img src="/img/full/gearupdater.jpg" alt="Gear Updater app listing available plugin updates" loading="lazy"></div></div>
<section id="all"><h2 class="sec">All software</h2><p class="sub">Filter by type, or search by name.</p>
<div class="bar">{chips}<input id="q" class="search" type="search" placeholder="Search plugins..." aria-label="Search plugins"></div>{sections}</section>
<section><h2 class="sec">How it works</h2><p class="sub">Three steps.</p>{steps}</section>
{SUPPORT}</div>"""
ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Studio 87", "url": BASE + "/", "sameAs": ["https://github.com/SpeakingColors", "https://ko-fi.com/studio87", "https://www.youtube.com/@sonatural_"]}
open(OUT + "/index.html", "w").write(page("Studio 87: free open source music software (VST3, Linux first)",
    "Free open source synths, effects, DJ tools and hardware controller plugins by Studio 87. VST3 and standalone, Linux first.", "/", home, ld, "/img/full/SupurrrSaw-VST.jpg", js=True))
open(OUT + "/404.html", "w").write(page("Page not found | Studio 87", "Page not found.", "/404.html", '<div class="wrap" style="padding:80px 28px"><h1 class="hd" style="font-size:72px">Page not found.</h1><p><a class="btn p" href="/">Back to Studio 87</a></p></div>'))
os.makedirs(OUT + "/cat-recipe-book", exist_ok=True)
open(OUT + "/cat-recipe-book/index.html", "w").write('<!doctype html><meta charset="utf-8"><title>Synth Cook Book</title><link rel="canonical" href="' + BASE + '/synth-cook-book/"><meta http-equiv="refresh" content="0; url=/synth-cook-book/"><meta name="robots" content="noindex"><a href="/synth-cook-book/">Synth Cook Book</a>')
# old addresses that moved (repo renames); keep them working
for _old, _new, _name in (("shimmerstuff", "purrrverb", "Purrrverb"), ("play/shimmerstuff", "play/purrrverb", "Purrrverb")):
    os.makedirs(OUT + "/" + _old, exist_ok=True)
    open(OUT + "/" + _old + "/index.html", "w").write('<!doctype html><meta charset="utf-8"><title>' + _name + '</title><link rel="canonical" href="' + BASE + '/' + _new.replace("play/", "") + '/"><meta http-equiv="refresh" content="0; url=/' + _new + '/"><meta name="robots" content="noindex"><a href="/' + _new + '/">' + _name + '</a>')
open(OUT + "/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(OUT + "/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(OUT + "/.nojekyll", "w").write("")
for f in ("favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
    shutil.copy(f"{S}/icons/{f}", f"{OUT}/{f}")
shutil.copy(f"{S}/icons/favicon-32.png", f"{OUT}/favicon.ico")
open(OUT + "/site.webmanifest", "w").write(json.dumps({"name": "Studio 87", "short_name": "Studio 87", "start_url": "/", "display": "browser", "background_color": "#141618", "theme_color": "#141618", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}))
L = ["# Studio 87", "", "> Studio 87 makes free, open source music production software: synth and effect plugins (VST3 and standalone), DJ tools, hardware synth controller plugins and Korg logue units. Linux first, with Windows and macOS builds for many. Built with JUCE and C++. Everything is free to use; to change or build on it, fork it on GitHub. Donations are welcome on Ko-fi.", "",
     "Website: " + BASE + "/", "Source code and releases: https://github.com/SpeakingColors", "Support: https://ko-fi.com/studio87", "YouTube: https://www.youtube.com/@sonatural_", "About supporting the project: "+BASE+"/support/", "Privacy: "+BASE+"/privacy/", ""]
for cslug, ctitle, kind, blurb, items in CATS:
    L += ["## " + ctitle, "", blurb, ""]
    for rn, dn in items:
        r = repos.get(rn)
        if not r: continue
        tb = " (test build)" if is_test(rn) else ""
        L.append(f"- [{dn}]({BASE}/{slug(rn)}/): {COPY.get(rn, {}).get('tagline') or short((r['description'] or '').strip(), 200)}{tb}")
    L.append("")
open(OUT + "/llms.txt", "w").write("\n".join(L))
print("pages:", len(urls))
