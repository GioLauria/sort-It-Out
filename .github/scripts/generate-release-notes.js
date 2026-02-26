const fs = require('fs');
const { execSync } = require('child_process');

function extractFromChangelog(changelog, headerMatch) {
  const idx = changelog.indexOf(headerMatch);
  if (idx === -1) return [];
  const nextIdx = changelog.indexOf('\n## [', idx + headerMatch.length);
  const section = (nextIdx === -1) ? changelog.slice(idx) : changelog.slice(idx, nextIdx);
  return section.split(/\r?\n/)
    .map(l => l.trim())
    .filter(Boolean)
    .filter(l => l.startsWith('-'))
    .map(l => l.replace(/^[-\s]+/, ''));
}

function writeOutput(body) {
  const outPath = process.env.GITHUB_OUTPUT;
  if (outPath) {
    const marker = 'END_OF_RELEASE_BODY';
    const safeBody = body.replace(new RegExp(marker, 'g'), marker + '_REPLACED');
    fs.appendFileSync(outPath, `body<<${marker}\n${safeBody}\n${marker}\n`);
  } else {
    // Fallback to stdout
    console.log(body);
  }
}

async function main() {
  // Determine tag
  const ref = process.env.GITHUB_REF || process.env.GITHUB_REF_NAME || '';
  const tag = ref && ref.startsWith('refs/tags/') ? ref.replace('refs/tags/', '') : ref;
  const ver = tag && tag.startsWith('v') ? tag.slice(1) : tag;

  let entries = [];
  try {
    const changelog = fs.readFileSync('CHANGELOG.md', 'utf8');
    if (ver) entries = extractFromChangelog(changelog, `## [${ver}]`);
    if (!entries.length) entries = extractFromChangelog(changelog, '## [Unreleased]');
  } catch (e) {
    // ignore
  }

  if (!entries.length) {
    try {
      // Find tags sorted by creation date (newest first)
      const tagsOutput = execSync('git for-each-ref --sort=-creatordate --format="%(refname:short)" refs/tags', { encoding: 'utf8' }).trim();
      const tags = tagsOutput ? tagsOutput.split(/\r?\n/).map(t => t.trim()).filter(Boolean) : [];

      // Determine the previous tag relative to the current tag (if any)
      let prevTag = '';
      if (tag) {
        const idx = tags.indexOf(tag);
        if (idx !== -1) prevTag = tags[idx + 1] || '';
        else prevTag = tags[0] || '';
      } else {
        prevTag = tags[0] || '';
      }

      let cmd;
      // If we have a previous tag and a current tag, list commits between them
      if (prevTag && tag && prevTag !== tag) {
        cmd = `git log ${prevTag}..${tag} --pretty=format:'- %s (%an)'`;
      } else if (tag) {
        // No previous tag found (or tag not in list) -- show commits reachable from the tag
        cmd = `git log ${tag} --pretty=format:'- %s (%an)'`;
      } else if (prevTag) {
        // No current tag (untagged run) but tags exist: show commits since latest tag
        cmd = `git log ${prevTag}..HEAD --pretty=format:'- %s (%an)'`;
      } else {
        // No tags at all: show full history
        cmd = `git log --pretty=format:'- %s (%an)'`;
      }

      const out = execSync(cmd, { encoding: 'utf8' });
      entries = out.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    } catch (e) {
      entries = ['No release notes available.'];
    }
  }

  const categories = { Added: [], Changed: [], Fixed: [], Docs: [], CI: [], Other: [] };
  for (const e of entries) {
    const low = e.toLowerCase();
    if (/\b(feat|add|added|new)\b/.test(low)) categories.Added.push(e);
    else if (/\b(fix|bug|fixes|patched?)\b/.test(low)) categories.Fixed.push(e);
    else if (/\b(doc|docs|documentation)\b/.test(low)) categories.Docs.push(e);
    else if (/\b(ci|workflow|actions|github)\b/.test(low)) categories.CI.push(e);
    else if (/\b(refactor|change|changed|upgrade|update|improve)\b/.test(low)) categories.Changed.push(e);
    else categories.Other.push(e);
  }

  let date = new Date().toISOString().slice(0, 10);
  try {
    if (tag) {
      const dt = execSync(`git log -1 --format=%cd ${tag}`, { encoding: 'utf8' }).trim();
      if (dt) date = new Date(dt).toISOString().slice(0, 10);
    }
  } catch (e) {
    // ignore
  }

  const lines = [];
  lines.push(`## ${tag || 'untagged'} — ${date}`);
  lines.push('');

  const first = entries.find(Boolean) || '';
  if (first) {
    lines.push('### Highlights');
    lines.push(`- ${first}`);
    lines.push('');
  }

  for (const [name, list] of Object.entries(categories)) {
    if (!list.length) continue;
    lines.push(`### ${name}`);
    for (const item of list) lines.push(`- ${item}`);
    lines.push('');
  }

  lines.push('---');
  const repo = process.env.GITHUB_REPOSITORY || '';
  lines.push(`Full changelog: https://github.com/${repo}/blob/master/CHANGELOG.md`);

  const body = lines.join('\n');
  writeOutput(body);
}

main().catch(err => { console.error(err); process.exit(1); });
