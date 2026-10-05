#!/usr/bin/env node
/**
 * Compile a LaTeX file containing TikZ and optionally render PNG.
 *
 * Usage:
 *   node compile_tikz.js solution.tex             # compile, print errors
 *   node compile_tikz.js solution.tex --png       # compile + render PNG
 *   node compile_tikz.js solution.tex -o outdir   # custom output dir
 *
 * Exit codes: 0 = compile OK, 1 = LaTeX errors, 2 = no TeX engine found.
 * Engines tried in order: pdflatex, tectonic, xelatex (first found on PATH).
 * No npm dependencies — uses Node.js built-ins only.
 */
'use strict';
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ENGINES = ['pdflatex', 'tectonic', 'xelatex'];

function which(exe) {
  const exts = process.platform === 'win32'
    ? (process.env.PATHEXT || '.EXE;.CMD;.BAT').split(';')
    : [''];
  const dirs = (process.env.PATH || '').split(path.delimiter).filter(Boolean);
  for (const dir of dirs) {
    for (const ext of exts) {
      const candidate = path.join(dir, exe + ext);
      try {
        fs.accessSync(candidate, fs.constants.X_OK);
        return candidate;
      } catch (_) { /* keep searching */ }
    }
  }
  return null;
}

function findEngine() {
  for (const exe of ENGINES) {
    const full = which(exe);
    if (full) return { name: exe, path: full };
  }
  return null;
}

function extractErrors(logText, maxErrors = 10) {
  const errors = [];
  const lines = logText.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('!')) {
      errors.push([lines[i], ...lines.slice(i + 1, i + 4)].join('\n'));
      if (errors.length >= maxErrors) break;
    }
  }
  return errors;
}

function compileTex(texPath, outDir, engine) {
  const base = texPath.replace(/\.(tex)$/i, '');
  const cmd = [engine.path];
  let args;
  if (engine.name === 'tectonic') {
    args = ['--keep-logs', '--outdir', outDir, texPath];
  } else {
    args = ['-interaction=nonstopmode', '-halt-on-error',
            '-output-directory', outDir, texPath];
  }
  const proc = spawnSync(cmd[0], args, { encoding: 'utf8', timeout: 180000 });
  const logFile = path.join(outDir, path.basename(base) + '.log');
  let log = '';
  try { log = fs.readFileSync(logFile, 'utf8'); } catch (_) { /* no log */ }
  const errors = extractErrors([proc.stdout, proc.stderr, log].filter(Boolean).join('\n'));
  const pdfPath = path.join(outDir, path.basename(base) + '.pdf');
  const ok = proc.status === 0 && fs.existsSync(pdfPath);
  return { ok, errors, pdfPath, logFile };
}

function renderPng(pdfPath, outDir) {
  const base = path.join(outDir, path.basename(pdfPath).replace(/\.pdf$/i, ''));
  const attempts = [
    { cmd: 'pdftoppm', args: ['-png', '-r', '200', '-singlefile', pdfPath, base] },
    { cmd: 'magick', args: ['-density', '200', pdfPath, base + '.png'] },
    { cmd: 'convert', args: ['-density', '200', pdfPath, base + '.png'] },
  ];
  for (const { cmd, args } of attempts) {
    const full = which(cmd);
    if (!full) continue;
    const proc = spawnSync(full, args, { encoding: 'utf8', timeout: 120000 });
    if (proc.status === 0) return base + '.png';
  }
  return null;
}

function main() {
  const argv = process.argv.slice(2);
  const flags = new Set(argv.filter(a => a.startsWith('-')));
  const positional = argv.filter(a => !a.startsWith('-'));
  const outIdx = argv.indexOf('-o') !== -1 ? argv.indexOf('-o')
    : argv.indexOf('--outdir');
  const outArg = outIdx !== -1 ? argv[outIdx + 1] : null;

  if (positional.length === 0) {
    console.error('Usage: node compile_tikz.js <file.tex> [--png] [-o outdir]');
    process.exit(2);
  }
  const texPath = path.resolve(positional[0]);
  if (!fs.existsSync(texPath)) {
    console.error(`ERROR: file not found: ${texPath}`);
    process.exit(2);
  }
  const outDir = path.resolve(outArg || path.dirname(texPath));
  fs.mkdirSync(outDir, { recursive: true });

  const engine = findEngine();
  if (!engine) {
    console.log('NO_ENGINE: no pdflatex/tectonic/xelatex found on PATH.');
    process.exit(2);
  }

  console.log(`Engine: ${engine.name}`);
  const { ok, errors, pdfPath, logFile } = compileTex(texPath, outDir, engine);
  if (!ok) {
    console.log('COMPILE_FAILED');
    if (errors.length) {
      errors.forEach(e => { console.log('---'); console.log(e); });
    } else {
      console.log('(no explicit \'!\' blocks; check the full log:', logFile, ')');
    }
    process.exit(1);
  }
  console.log(`COMPILE_OK: ${pdfPath}`);
  if (flags.has('--png')) {
    const png = renderPng(pdfPath, outDir);
    if (png) console.log(`PNG_OK: ${png}`);
    else console.log('PNG_SKIPPED: no pdftoppm/ImageMagick found; PDF is available.');
  }
  process.exit(0);
}

main();
