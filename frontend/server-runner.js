const { spawn } = require('child_process');
const path = require('path');

const isDev = process.env.NODE_ENV !== 'production';
const cmd = 'npx.cmd';
const args = isDev ? ['next', 'dev', '-p', '3000'] : ['next', 'start', '-p', '3000'];

console.log(`Starting Next.js in ${isDev ? 'development' : 'production'} mode on port 3000...`);

const child = spawn(cmd, args, {
  cwd: __dirname,
  stdio: 'inherit',
  shell: true,
  env: { ...process.env, PORT: '3000' }
});

child.on('error', (err) => {
  console.error('Failed to start Next.js process:', err);
});

child.on('exit', (code, signal) => {
  console.log(`Next.js process exited with code ${code} signal ${signal}`);
});

process.on('SIGINT', () => child.kill('SIGINT'));
process.on('SIGTERM', () => child.kill('SIGTERM'));
