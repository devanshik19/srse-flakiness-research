#!/usr/bin/env bash
# screen.sh <zenodo_url> [topN] — rank every class in a project by generatability
set -u
URL="${1:?zenodo url}"; TOP="${2:-5}"; export URL
cd "$HOME/srse-java" || exit 1
Z=$(basename "$URL"); [ -f "$Z" ] || wget -q -O "$Z" "$URL" || { echo "download failed"; exit 1; }
D="$PWD/${Z%.zip}.dir"; [ -d "$D" ] || { mkdir -p "$D"; unzip -q "$Z" -d "$D"; }
P=$(find "$D" -maxdepth 4 -name pom.xml | grep -m1 Flaky || find "$D" -maxdepth 4 -name pom.xml | head -1)
[ -z "$P" ] && { echo "no pom"; exit 1; }
cd "$(dirname "$P")" || exit 1
python3 - "$TOP" <<'PY'
import re,sys,glob,os
TOP=int(sys.argv[1])
SIMPLE=re.compile(r'^(int|long|double|float|boolean|char|byte|short|String|Object|CharSequence|Number|'
                  r'List|Map|Set|Collection|Integer|Long|Double|Boolean|Date|BigDecimal|BigInteger)'
                  r'(<[^>]*>)?(\[\])?$')
METH=re.compile(r'^\s*public\s+(?!class|interface|enum|static\s+final)([\w<>\[\],.\s]+?)\s+(\w+)\s*\(([^)]*)\)')
ACC=re.compile(r'^(get|set|is|has)[A-Z]')
def simple_params(p):
    p=p.strip()
    if not p: return True
    for a in p.split(','):
        a=a.strip().split()
        if len(a)<2: return False
        if not SIMPLE.match(a[0].split('.')[-1]): return False
    return True
rows=[]
for f in glob.glob('src/main/java/**/*.java',recursive=True):
    src=open(f,errors='ignore').read()
    if re.search(r'\b(abstract class|interface )\w',src): continue
    pub=acc=good=0
    for line in src.splitlines():
        m=METH.match(line)
        if not m: continue
        pub+=1; name=m.group(2)
        if ACC.match(name): acc+=1; continue
        if simple_params(m.group(3)): good+=1
    if pub==0 or pub>80 or acc>=pub or good==0: continue
    rows.append((good,pub,f[len('src/main/java/'):-5].replace('/','.')))
rows.sort(reverse=True)
if not rows: print("NO VIABLE CLASS")
else:
    print(f"{'good':>4} {'pub':>4}  class")
    for g,p,fq in rows[:TOP]: print(f"{g:>4} {p:>4}  {fq}")
    print("\nqueue lines:")
    for g,p,fq in rows[:TOP]: print(f"{os.environ.get('URL','')}\t{fq}")
PY
