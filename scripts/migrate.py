#!/usr/bin/env python3
"""Reapply the Universal Resume rebrand after an upstream sync."""
from pathlib import Path
import os, shutil

SKIP_DIRS = {'.git', '.github', 'scripts', 'node_modules'}
LICENSE = Path('LICENSE')

def newpath(s):
    return (s.replace('ReactiveResume', 'UniversalResume').replace('reactive-resume', 'universal-resume')
             .replace('Reactive-Resume', 'Universal-Resume'))

def sweep():
    pairs = [
        ('amruthpillai/reactive-resume', 'yashhasan570/universal-resume'),
        ('mailto:amruth@rxresu.me', 'https://t.me/johnconstantine570'),
        ('rxresu.me', 'universalresume.app'),
        ('Amruth', 'Universal'),
        ('RXRESUME', 'UNIVERSALRESUME'),
        ('rxresu', 'universalresume'),
        ('RXRESU', 'UNIVERSALRESUME'),
        ('Rxresu', 'Universalresume'),
        ('rxresume', 'universalresume'),
        ('RxResume', 'UniversalResume'),
        ('amruth', 'universalresume'),
        ('https://amruthpillai.com', 'https://github.com/yashhasan570/UniversalResume'),
        ('Amruth Pillai', 'Universal Resume'),
        ('amruth-pillai', 'universal-resume'),
        ('amruthpillai', 'yashhasan570'),
        ('AmruthPillai', 'yashhasan570'),
        ('amruth.cv', 'universalresume.cv'),
        ('reactiveresume', 'universalresume'),
        ('ReactiveResume', 'UniversalResume'),
        ('reactiveResume', 'universalResume'),
        ('reactive-resume', 'universal-resume'),
        ('reactive_resume', 'universal_resume'),
        ('REACTIVE_RESUME', 'UNIVERSAL_RESUME'),
        ('Reactive-Resume', 'Universal-Resume'),
        ('Reactive Resume', 'Universal Resume'),
        ('REACTIVE RESUME', 'UNIVERSAL RESUME'),
    ]
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = Path(root) / f
            if p == LICENSE or p.name == 'migrate.py': continue
            try: t = p.read_text(encoding='utf-8')
            except Exception: continue
            orig = t
            for old, new in pairs: t = t.replace(old, new)
            if t != orig: p.write_text(t)

def merge(src, dst):
    for child in list(src.iterdir()):
        ct = Path(newpath(str(child)))
        ct.parent.mkdir(parents=True, exist_ok=True)
        if ct.exists():
            if child.is_dir() and ct.is_dir():
                merge(child, ct)
                try: child.rmdir()
                except OSError: pass
            elif child.is_dir():
                shutil.rmtree(ct, ignore_errors=True)
                shutil.move(str(child), str(ct))
            else:
                if ct.is_dir(): shutil.rmtree(ct, ignore_errors=True)
                else: ct.unlink()
                shutil.move(str(child), str(ct))
        else:
            shutil.move(str(child), str(ct))
    try: src.rmdir()
    except OSError: pass

def renames():
    targets = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in dirs + files:
            if 'reactive' in name.lower():
                targets.append(Path(root) / name)
    targets.sort(key=lambda p: len(p.parts), reverse=True)
    for p in targets:
        if not p.exists(): continue
        tgt = Path(newpath(str(p)))
        if p == tgt: continue
        tgt.parent.mkdir(parents=True, exist_ok=True)
        if p.is_dir() and tgt.exists() and tgt.is_dir():
            merge(p, tgt)
        elif tgt.exists():
            if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
            else:
                if tgt.is_dir(): shutil.rmtree(tgt, ignore_errors=True)
                else: tgt.unlink()
                shutil.move(str(p), str(tgt))
        else:
            shutil.move(str(p), str(tgt))

def cleanup():
    for item in ['.github/FUNDING.yml', 'AGENTS.md', 'CLAUDE.md', 'CODING_STANDARDS.md', 'GLOSSARY.md', 'SECURITY.md', '.agents', '.claude-plugin', '.vscode', 'crowdin.yml', 'docs']:
        p = Path(item)
        if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
        elif p.exists(): p.unlink()

def readme():
    Path('README.md').write_text("""# Universal Resume

A free, open-source resume builder: pick a design template, fill in your details, and export a polished, ATS-friendly PDF. Self-hostable via Docker.

## Getting started

```
docker compose up -d
```

See `compose.yml` and `.env.example` for configuration.

## Contact

Telegram: [@johnconstantine570](https://t.me/johnconstantine570)
""")

if __name__ == '__main__':
    sweep(); renames(); cleanup(); readme()
    print('rebrand reapplied')
