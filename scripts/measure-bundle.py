"""Measure a full-source Git bundle in disposable task scratch; never modify the assigned .git."""
from pathlib import Path
import shutil, subprocess, json

root = Path.cwd()
repo = root / 'test/scratch/budget-repo'
if repo.exists():
    shutil.rmtree(repo)
repo.mkdir(parents=True)
dirs = ['src', 'public', 'official', 'LICENSES', 'dist', 'test/unit', 'test/core', 'scripts', 'artifacts']
root_files = ['package.json', 'package-lock.json', 'index.html', 'tsconfig.json', 'vite.config.ts', 'vitest.config.ts', '.gitignore', 'README.md', 'DESIGN.md', 'VALIDATION.md']
paths = [root / name for name in root_files if (root / name).is_file()]
for name in dirs:
    paths.extend(p for p in (root / name).rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules', '.git', '.npm', '.cache']))
for path in paths:
    if path.is_symlink():
        raise RuntimeError('Required sources must not be external symlinks')
    rel = path.relative_to(root)
    dest = repo / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, dest)

def git(*args):
    return subprocess.run(['git', '-C', str(repo), '-c', 'core.hooksPath=/dev/null', *args], check=True, capture_output=True, text=True).stdout.strip()

git('init', '-q')
git('add', '--all')
git('-c', 'user.name=Export budget check', '-c', 'user.email=budget@example.invalid', 'commit', '-q', '-m', 'Disposable source budget measurement')
bundle = root / 'test/scratch/source-budget.bundle'
git('bundle', 'create', str(bundle), '--all')
size = bundle.stat().st_size
out = {'method': 'Complete required source/export copied to an isolated scratch Git repository; assigned .git untouched.', 'sourceFiles': len(paths), 'sourceBytes': sum(p.stat().st_size for p in paths), 'gitBundleBytes': size, 'providerLimitBytes': 8388608, 'fitsLocally': size <= 8388608, 'note': 'Local measurement does not guarantee provider network acceptance; the final service bundle can contain additional metadata.'}
(root / 'artifacts/bundle-budget.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
if size > 8388608:
    raise SystemExit(1)
