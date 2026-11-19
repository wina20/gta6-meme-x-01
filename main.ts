// Entry program for make.fun's gta6-meme-x-01 bounty ("Post a GTA 6 meme on X").
//
// The entry itself is the post on X: my agent drew the meme (see make_meme.py),
// the post goes up from a public account, and POST.json in this repository
// names that post's address. All this program has to do is hand POST.json to
// the grader: copy it from the repository root into the output directory.
// Node standard library only -- no network, no clock, nothing outside the repo.
//
// Run it the way the grader does, with the two directories pointed locally:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(repoDir, 'POST.json');
const target = join(outDir, 'POST.json');

mkdirSync(outDir, { recursive: true });

try {
  copyFileSync(source, target);
} catch (err) {
  console.error(`failed to copy POST.json out of ${repoDir}: ${(err as Error).message}`);
  process.exit(1);
}

// The copy is the whole job; if it is not sitting in the output afterwards,
// something is deeply wrong, so say so loudly instead of exiting quietly.
if (!existsSync(target)) {
  console.error(`POST.json copy missing from ${outDir} after copying`);
  process.exit(1);
}
