#!/usr/bin/env node
import { mkdir, copyFile, writeFile, realpath, rm } from 'node:fs/promises';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';
import { spawn } from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const target = process.argv[2];
if (!target || !target.startsWith('/')) throw new Error('Usage: node scripts/setup.mjs /absolute/path/to/runtime (choose a mounted bulk-storage location)');
await mkdir(target, {recursive:true});
const runtime = await realpath(target);
await mkdir(join(runtime,'tmp'),{recursive:true});
for (const name of ['package.json','package-lock.json']) await copyFile(join(root,'runtime',name),join(runtime,name));
function run(cmd,args,env={}) { return new Promise((res,rej)=>{const p=spawn(cmd,args,{cwd:runtime,stdio:'inherit',env:{...process.env,TMPDIR:join(runtime,'tmp'),...env}});p.on('error',rej);p.on('exit',c=>c===0?res():rej(new Error(`${cmd} exited ${c}`)));}); }
await run('npm',['ci','--ignore-scripts','--no-fund','--no-audit','--cache',join(runtime,'npm-cache')]);
await run(process.execPath,[join(runtime,'node_modules/playwright/cli.js'),'install','chromium-headless-shell'],{PLAYWRIGHT_BROWSERS_PATH:join(runtime,'browsers')});
await rm(join(runtime,'npm-cache'),{recursive:true,force:true});
const config = join(homedir(),'.config/html-to-figma-clipboard');
await mkdir(config,{recursive:true});
await writeFile(join(config,'runtime.json'),JSON.stringify({runtime},null,2));
console.log(JSON.stringify({ready:true,runtime,converter:'@figit/dom-to-figma@0.2.4'}));
