import json, os, re, subprocess, sys, hashlib, shutil
S = sys.argv[1]
OUT = S + "/try"; FONT = OUT + "/fonts"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(FONT)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
M = {  # repo -> path of the single-file interactive mockup
 "PurrOne":"docs/mockup/purrone-mockup.html","multipawcompressor":"docs/mockup/MultiPaw.html","Apurrr2500":"docs/mockup/Apurrr2500.html",
 "LapCat2A":"docs/mockup/LapCat2A.html","Pawltec":"docs/mockup/Pawltec.html","FetlinePounce":"docs/mockup/FetlinePounce.html",
 "Furchild":"docs/mockup/Furchild.html","PunchPaw":"docs/mockup/PunchPaw.html","clawshaper":"docs/mockup/ClawShaper.html",
 "Clawpressor-vst":"docs/mockup/index.html","CatRack":"docs/mockup/CatRack.html","Purrrverb":"docs/mockup/shimmerstuff.html",
 "scratchcatfx-vst":"docs/mockup/scratchcatfx.html","scratchcatduo-vst":"docs/mockup/scratchcatduo.html","stretch-cat-vst":"docs/mockup/stretchcat.html",
 "copycat-vst":"docs/mockup/copycat.html","CATalog":"docs/mockup/catalog.html","purrfect-cut":"docs/mockup/purrfectcut.html",
 "whiskerscope":"docs/mockup/whisker-scope-mockup.html","Purrrstressor":"docs/mockups/Purrrstressor.html","Meowcorder":"docs/mockup/index.html",
 "hairball":"docs/mockups/Hairball.html","gearupdater":"docs/mockup/index.html","JPurrr-8000":"docs/mockups/JPurrr-8000-mockup-v3.12.html",
 "phasepaw":"docs/mockups/PhasePaw-mockup-v12.html","SynthCookBook":"docs/recipe-book.html","purrrvoicechannel":"docs/mockup/index.html","catspacer":"docs/mockups/Studio87-FX-test-page.html","linux-ultranova-controller":"docs/mockup/index.html","linux-peak-controller":"docs/mockup/index.html","minilogue-xd-controller":"docs/mockup/index.html","drumlogue-linux-controller":"docs/mockup/index.html","modxm-controller-vst":"docs/mockup/index.html","jt4000-vst":"docs/mockup/index.html","Cobalt8M-Controller-VST":"docs/mockup/index.html","mx400-vst-linux":"docs/mockup/index.html","whiskermix":"docs/mockup/index.html","SupurrrSaw-VST":"LOCAL:/private/tmp/claude-501/-Users-jyfjhfhj-Library-Application-Support-Claude-scratch-workspaces-cbacd2fe-dbea-4f2d-bb25-068d43c2fed0-56f4464d-554f-4874-92ad-713fb8143fbe-scratch-2026-11-14-a95345/07864805-ea39-422c-a8d5-09109e39def5/scratchpad/artifact-files/c45d4029-cfd0-4bc4-aba5-bb1a169455e4/index.html","KickKitten":"docs/mockups/KickKitten-v1.html"}

CLAIM = re.compile(r'\s*[^.<>"\n]{0,160}?(?:collects? nothing|no telemetry|nothing is sent anywhere|never uses the network|makes? no network calls?|no network calls?)[^.<>"\n]{0,120}\.', re.I)
def strip_claims(h):
    if not re.search(r'collects? nothing|no telemetry|nothing is sent anywhere|never uses the network|no network call', h, re.I): return h
    return CLAIM.sub('', h)


def localize_relative(h, repo, path):
    base = path.rsplit('/', 1)[0] if '/' in path else ''
    def rep(m):
        rel = m.group(1).strip('"\' ')
        if rel.startswith(('http', 'data:', '/', '#')): return m.group(0)
        url = f"https://raw.githubusercontent.com/SpeakingColors/{repo}/main/{base}/{rel}".replace('//main','/main')
        fn = hashlib.md5(url.encode()).hexdigest()[:10] + os.path.splitext(rel)[1]
        if not os.path.exists(f"{FONT}/{fn}"):
            subprocess.run(['curl','-sfL','-o',f"{FONT}/{fn}",url])
        return f"url(/try/fonts/{fn})" if os.path.exists(f"{FONT}/{fn}") else m.group(0)
    return re.sub(r'url\(([^)]+)\)', rep, h)


FONTPACK = ""
def fontpack():
    global FONTPACK
    if FONTPACK: return FONTPACK
    faces = [("Barlow Condensed",500,"barlow-condensed-latin-500-normal"),("Barlow Condensed",600,"barlow-condensed-latin-600-normal"),("Barlow Condensed",700,"barlow-condensed-latin-700-normal"),("JetBrains Mono",400,"jetbrains-mono-latin-400-normal"),("JetBrains Mono",500,"jetbrains-mono-latin-500-normal")]
    css = ""
    for fam, w, n in faces:
        dst = f"{FONT}/pack-{n}.woff2"
        if not os.path.exists(dst):
            subprocess.run(['curl','-sfL','-o',dst,f"https://raw.githubusercontent.com/SpeakingColors/purrrvoicechannel/main/docs/mockup/fonts/{n}.woff2"])
        if os.path.exists(dst): css += f'@font-face{{font-family:"{fam}";font-weight:{w};font-display:swap;src:url(/try/fonts/pack-{n}.woff2) format("woff2")}}'
    FONTPACK = "<style>" + css + "</style>"
    return FONTPACK
def ensure_fonts(h):
    if not re.search(r'Barlow Condensed|JetBrains Mono', h) or re.search(r'@font-face\s*\{[^}]*Barlow', h): return h
    st = fontpack()
    if '</head>' in h: return h.replace('</head>', st + '</head>', 1)
    if '<body>' in h: return h.replace('<body>', '<body>' + st, 1)
    return h

fontcache = {}
def localize(css):
    out = []
    for sub, block in re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S):
        if sub != 'latin': continue
        url = re.search(r'url\((https[^)]+)\)', block).group(1)
        if url not in fontcache:
            fn = hashlib.md5(url.encode()).hexdigest()[:10] + ".woff2"
            subprocess.run(['curl','-sfL','-o',f"{FONT}/{fn}",url]); fontcache[url] = fn
        out.append(re.sub(r'url\([^)]+\)', f'url(/try/fonts/{fontcache[url]})', block))
    return "\n".join(out)
done = {}
for repo, path in M.items():
    if repo not in ('catspacer',):
        _r = subprocess.run(['curl','-sfL',f"https://raw.githubusercontent.com/SpeakingColors/{repo}/main/docs/mockup/index.html"], capture_output=True)
        if _r.returncode == 0 and len(_r.stdout) > 2000:
            path = 'docs/mockup/index.html'
            h = _r.stdout.decode('utf-8', 'replace')
        elif path.startswith('LOCAL:'):
            h = open(path[6:], encoding='utf-8', errors='replace').read()
        else:
            _r = subprocess.run(['curl','-sfL',f"https://raw.githubusercontent.com/SpeakingColors/{repo}/main/{path}"], capture_output=True)
            if _r.returncode or not _r.stdout: print("FAIL", repo); continue
            h = _r.stdout.decode('utf-8', 'replace')
    elif path.startswith('LOCAL:'):
        h = open(path[6:], encoding='utf-8', errors='replace').read()
    else:
        r = subprocess.run(['curl','-sfL',f"https://raw.githubusercontent.com/SpeakingColors/{repo}/main/{path}"], capture_output=True)
        if r.returncode or not r.stdout: print("FAIL", repo); continue
        h = r.stdout.decode('utf-8', 'replace')
    css_links = re.findall(r'<link[^>]+href="(https://fonts\.googleapis\.com/css2[^"]+)"[^>]*>', h)
    local = ""
    for u in css_links:
        c = subprocess.run(['curl','-sfL','-A',UA,u.replace('&amp;','&')], capture_output=True, text=True).stdout
        local += localize(c)
    h = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>', '', h)
    if local: h = h.replace('</head>', f'<style>{local}</style></head>', 1)
    ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', h)
    ext = [x for x in ext if 'github.com' not in x and 'ko-fi' not in x and '${' not in x]
    if not path.startswith('LOCAL:'): h = localize_relative(h, repo, path)
    h = strip_claims(h)
    h = ensure_fonts(h)
    fn = ("cat-fx-studio.html" if repo == "catspacer" else re.sub(r'[^a-z0-9]+','-',repo.lower()).strip('-') + ".html")
    open(f"{OUT}/{fn}", "w").write(h)
    done[repo] = {"file": fn, "extern": ext[:4]}
for _a in ("catcrusher-vst","FatCat","meowbass","Meowximizer","scaredy-cat"):
    done[_a] = done["catspacer"]
# multi-file bundle: Stardrift (index.html fits a 1600x900 stage into the frame; needs its own template, runtime and audio files)
_bd = f"{OUT}/stardrift"; os.makedirs(_bd, exist_ok=True); _ok = True
for _f in ("index.html", "Main.dc.html", "support.js", "audio-asset.js"):
    _r = subprocess.run(f'gh api -H "Accept: application/vnd.github.raw" repos/SpeakingColors/StarDriftTVLauncher/contents/docs/mockup/{_f} > "{_bd}/{_f}"', shell=True)
    if _r.returncode != 0 or os.path.getsize(f"{_bd}/{_f}") < 500: _ok = False
if _ok: done["StarDriftTVLauncher"] = {"file": "stardrift/index.html", "extern": [], "ratio": 0.5625}
else: print("FAIL StarDriftTVLauncher")
json.dump(done, open(S + "/try.json", "w"), indent=1)
print(len(done), "mockups;", len(fontcache), "font files")
print({k:v["extern"] for k,v in done.items() if v["extern"]})
