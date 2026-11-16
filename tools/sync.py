#!/usr/bin/env python3
"""Studio 87 site sync: refresh repo data, demos, clips and screenshots from GitHub, rebuild, report.
Usage: python3 -I sync.py <scratchpad> <site_repo_dir> [--publish]
Prints a short report. With --publish it commits and pushes only when the build passed its checks."""
import sys, os, json, subprocess, re, shutil, hashlib

S = sys.argv[1]; SITE = sys.argv[2]; PUBLISH = "--publish" in sys.argv
WORK = os.path.dirname(SITE)            # folder that holds studio87-build next to the site repo
BUILD = WORK + "/studio87-build"
EXCLUDE = {"SpeakingColors", ".github", "SpeakingColors.github.io"}

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def gh(args):
    r = sh(["gh", "api"] + args)
    return r.stdout if r.returncode == 0 else None

def tojpg(src, out, q, size):
    """Make a JPEG that fits in size x size. Uses sips on macOS, ImageMagick elsewhere."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if shutil.which("sips"):
        sh(["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(q), "-Z", str(size), src, "--out", out])
    else:
        from PIL import Image
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, (20, 22, 24)); bg.paste(im, mask=im.split()[3]); im = bg
        else: im = im.convert("RGB")
        im.thumbnail((size, size), Image.LANCZOS); im.save(out, "JPEG", quality=q, optimize=True)

for _d in ("shots", "img/full", "img/thumb", "audio"):
    os.makedirs(f"{S}/{_d}", exist_ok=True)

report = []

# ---------- 1. repo data ----------
lst = json.loads(sh(["gh", "repo", "list", "SpeakingColors", "--visibility", "public", "--limit", "300", "--json",
                     "name,description,repositoryTopics,licenseInfo,pushedAt"]).stdout)
old = {r["name"]: r for r in json.load(open(S + "/data/repos.json"))}
new = []
for r in lst:
    n = r["name"]
    if n in EXCLUDE: continue
    prev = old.get(n, {})
    rel = None
    out = gh([f"repos/SpeakingColors/{n}/releases", "--jq", ".[0]|[.tag_name,.html_url,.prerelease]|@tsv"])
    if out and out.strip() and out.strip() != "null": rel = out.strip().split("\t")
    shot = prev.get("shot", "")
    if shot and not gh([f"repos/SpeakingColors/{n}/contents/{shot}", "--jq", ".name"]): shot = ""   # the file was renamed or removed
    if not shot:
        for p in ["docs/screenshot.png", "docs/screenshot.jpg", "docs/home.png"]:
            if gh([f"repos/SpeakingColors/{n}/contents/{p}", "--jq", ".name"]): shot = p; break
    new.append({"name": n, "description": r["description"] or "", "topics": [t["name"] for t in (r["repositoryTopics"] or [])],
                "license": (r["licenseInfo"] or {}).get("name", "") if r.get("licenseInfo") else "", "pushed": r["pushedAt"],
                "release": rel, "shot": shot})
names_new = {r["name"] for r in new}; names_old = set(old)
if names_new - names_old: report.append("NEW public repos (not on the site until categorised): " + ", ".join(sorted(names_new - names_old)))
if names_old - names_new: report.append("repos gone or private now: " + ", ".join(sorted(names_old - names_new)))
json.dump(new, open(S + "/data/repos.json", "w"), indent=1)

# ---------- 2. screenshots ----------
n_sh = 0
for r in new:
    if not r["shot"]: continue
    nm = r["name"]; ext = r["shot"].rsplit(".", 1)[1]; dst = f"{S}/shots/{nm}.{ext}"
    if sh(["curl", "-sfL", "-o", dst + ".new", f"https://raw.githubusercontent.com/SpeakingColors/{nm}/main/{r['shot']}"]).returncode == 0 \
       and os.path.exists(dst + ".new") and os.path.getsize(dst + ".new") > 1000:
        same = os.path.exists(dst) and hashlib.md5(open(dst, "rb").read()).hexdigest() == hashlib.md5(open(dst + ".new", "rb").read()).hexdigest()
        os.replace(dst + ".new", dst)
        if not same or not os.path.exists(f"{S}/img/full/{nm}.jpg"):
            tojpg(dst, f"{S}/img/full/{nm}.jpg", 82, 1200)
            tojpg(dst, f"{S}/img/thumb/{nm}.jpg", 78, 640); n_sh += 1
    elif os.path.exists(dst + ".new"): os.remove(dst + ".new")
report.append(f"screenshots updated: {n_sh}")

# ---------- 3. mockups ----------
p = sh(["python3", "-I", S + "/prep_mock.py", S])
mk = re.findall(r"(\d+) mockups", p.stdout); fails = re.findall(r"FAIL (\S+)", p.stdout)
report.append(f"demos prepared: {mk[0] if mk else '?'}" + (f" (FAILED: {', '.join(fails)})" if fails else ""))

# ---------- 4. audio clips ----------
audio = {}; shutil.rmtree(S + "/audio", ignore_errors=True)
for repo in new:
    nm = repo["name"]
    j = sh(["curl", "-sfL", f"https://raw.githubusercontent.com/SpeakingColors/{nm}/main/docs/audio/clips.json"])
    if j.returncode != 0 or not j.stdout.strip().startswith("["): continue
    try: clips = json.loads(j.stdout)
    except Exception: continue
    slug = re.sub(r"[^a-z0-9]+", "-", nm.lower()).strip("-"); os.makedirs(f"{S}/audio/{slug}", exist_ok=True); keep = []
    for c in clips:
        f = c.get("file")
        if not f or "/" in f: continue
        if sh(["curl", "-sfL", "-o", f"{S}/audio/{slug}/{f}", f"https://raw.githubusercontent.com/SpeakingColors/{nm}/main/docs/audio/{f}"]).returncode == 0 \
           and os.path.getsize(f"{S}/audio/{slug}/{f}") > 1000: keep.append(c)
    if keep: audio[nm] = keep
os.makedirs(S + "/audio", exist_ok=True)
json.dump(audio, open(S + "/audio.json", "w"), indent=1)
report.append("clips: " + ", ".join(f"{k} {len(v)}" for k, v in audio.items()))

# ---------- 5. build ----------
shutil.rmtree(BUILD, ignore_errors=True)
b = sh(["python3", "-I", S + "/build_site3.py", S, BUILD])
if b.returncode != 0:
    print("BUILD FAILED:\n" + b.stderr[-800:]); sys.exit(2)
pages = int(re.findall(r"pages: (\d+)", b.stdout)[0]) if re.findall(r"pages: (\d+)", b.stdout) else 0

# ---------- 6. checks ----------
problems = []
old_pages = sum(1 for _ in open(SITE + "/sitemap.xml").read().split("<url>")) - 1 if os.path.exists(SITE + "/sitemap.xml") else 0
if pages < old_pages - 2: problems.append(f"page count dropped {old_pages} -> {pages}")
for must in ["index.html", "support/index.html", "privacy/index.html", "sitemap.xml", "llms.txt", "404.html"]:
    if not os.path.exists(f"{BUILD}/{must}"): problems.append("missing " + must)
bad = re.compile(r"collects? nothing|no telemetry|nothing is sent anywhere|never uses the network|no tracking", re.I)
hits = []
for root, _, files in os.walk(BUILD):
    for f in files:
        if f.endswith((".html", ".txt")) and "/fonts" not in root:
            t = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            if bad.search(t): hits.append(os.path.relpath(os.path.join(root, f), BUILD))
if hits: problems.append("privacy-claim wording found in: " + ", ".join(hits[:6]))
ext = re.compile(r'<(?:script|link|img|iframe)[^>]+(?:src|href)="https?://(?!speakingcolors\.github\.io|ko-fi\.com|github\.com)[^"]+', re.I)
exthits = [os.path.relpath(os.path.join(r, f), BUILD) for r, _, fs in os.walk(BUILD) for f in fs
           if f.endswith(".html") and ext.search(open(os.path.join(r, f), encoding="utf-8", errors="replace").read(2000000))]
if exthits: problems.append("outside requests in: " + ", ".join(exthits[:6]))
report.append(f"pages built: {pages}")

# ---------- 7. sync into the site repo ----------
subprocess.run(["rsync", "-a", "--delete", "--exclude", ".git", "--exclude", "/tools", "--exclude", "/.github", BUILD + "/", SITE + "/"])
st = sh(["git", "-C", SITE, "status", "--porcelain"]).stdout.strip().splitlines()
report.append(f"files changed in site: {len(st)}")
if problems:
    report.append("PROBLEMS (not published): " + " | ".join(problems))
elif PUBLISH and st:
    if os.environ.get("GITHUB_ACTIONS"):
        who, mail = "github-actions[bot]", "41898282+github-actions[bot]@users.noreply.github.com"
    else:
        uid = sh(["gh", "api", "user", "--jq", ".id"]).stdout.strip(); who, mail = "SpeakingColors", f"{uid}+SpeakingColors@users.noreply.github.com"
    sh(["git", "-C", SITE, "add", "-A"])
    c = sh(["git", "-C", SITE, "-c", f"user.name={who}", "-c", f"user.email={mail}", "commit", "-q", "-m",
           "Sync the site with the repos\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"])
    pr = sh(["git", "-C", SITE, "push", "-q", "origin", "main"])
    report.append("PUBLISHED" if pr.returncode == 0 else "PUSH FAILED: " + pr.stderr[-300:])
elif not st:
    report.append("nothing to publish")
print("\n".join(report))
