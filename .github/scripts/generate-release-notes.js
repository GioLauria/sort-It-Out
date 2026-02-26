#!/usr/bin/env node
// Simple release notes generator used by CI.
// Prints release notes to stdout. When run inside GitHub Actions the
// workflow captures the output and stores it as the `body` output.

const { execSync } = require('child_process');

function getTag() {
  const ref = process.env.GITHUB_REF || '';
  const m = ref.match(/refs\/tags\/(.+)$/);
  return (m && m[1]) || process.env.GITHUB_REF_NAME || 'unknown';
}

function getRecentCommits(tag) {
  try {
    // list commits in the tag (if annotated) or since previous tag
    // fallback: show the last 20 commits
    const out = execSync('git --no-pager log -n 20 --pretty=format:"- %s (%h)"', { encoding: 'utf8' });
    return out.trim();
  } catch (err) {
    return '';
  }
}

function main() {
  const tag = getTag();
  const commits = getRecentCommits(tag);
  const notes = `# Release ${tag}\n\n${commits}\n`;
  process.stdout.write(notes);
}

main();
