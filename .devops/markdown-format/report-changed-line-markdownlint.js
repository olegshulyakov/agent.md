const fs = require('fs');
const { execFileSync } = require('child_process');

function parseMarkdownlintResults(rawResults) {
  const trimmedResults = rawResults.trim();
  if (!trimmedResults) {
    return [];
  }

  const jsonStart = trimmedResults.search(/[\[{]/);
  if (jsonStart === -1) {
    return [];
  }

  return JSON.parse(trimmedResults.slice(jsonStart));
}

const baseRefName = process.env.BASE_REF_NAME;

if (!baseRefName) {
  throw new Error('BASE_REF_NAME is required');
}

const baseRef = `origin/${baseRefName}`;
const files = fs.readFileSync('changed-markdown-files.txt', 'utf8')
  .split(/\r?\n/)
  .filter(Boolean);
const changedLinesByFile = new Map();

for (const file of files) {
  const diff = execFileSync(
    'git',
    ['diff', '--unified=0', `${baseRef}...HEAD`, '--', file],
    { encoding: 'utf8' }
  );
  const changedLines = new Set();

  for (const line of diff.split(/\r?\n/)) {
    const match = line.match(/^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@/);
    if (!match) {
      continue;
    }

    const start = Number(match[1]);
    const count = match[2] === undefined ? 1 : Number(match[2]);
    for (let offset = 0; offset < count; offset += 1) {
      changedLines.add(start + offset);
    }
  }

  changedLinesByFile.set(file, changedLines);
}

const rawResults = fs.readFileSync('markdownlint-results.json', 'utf8');
const results = parseMarkdownlintResults(rawResults);
const failures = [];

for (const result of results) {
  const file = result.fileName.replace(`${process.cwd()}/`, '');
  const line = result.lineNumber;
  const changedLines = changedLinesByFile.get(file);

  if (!changedLines || !changedLines.has(line)) {
    continue;
  }

  failures.push({ ...result, fileName: file });
  const rule = [result.ruleNames?.[0], result.ruleDescription].filter(Boolean).join(' ');
  const detail = result.errorDetail ? `: ${result.errorDetail}` : '';
  const context = result.errorContext ? ` (${result.errorContext})` : '';
  console.log(`::error file=${file},line=${line},title=${result.ruleNames?.[0] || 'markdownlint'}::${rule}${detail}${context}`);
}

if (failures.length > 0) {
  console.error(`Found ${failures.length} Markdown formatting issue(s) on changed lines.`);
  process.exit(1);
}

console.log('No Markdown formatting issues found on changed lines.');
