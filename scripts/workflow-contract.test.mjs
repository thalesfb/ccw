import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

const workflow = await readFile(new URL('../.github/workflows/publish-reports.yml', import.meta.url), 'utf8')

test('Pages waits for a successful TCC quality workflow on main', () => {
  assert.match(workflow, /workflow_run:\s*\n\s*workflows:\s*\n\s*- TCC quality/)
  assert.match(workflow, /types:\s*\n\s*- completed/)
  assert.match(workflow, /branches:\s*\n\s*- main/)
  assert.match(workflow, /github\.event\.workflow_run\.conclusion == 'success'/)
  assert.match(workflow, /ref:\s*\$\{\{[^}]*github\.event\.workflow_run\.head_sha/)
  assert.match(workflow, /deploy:\s*\n\s*needs:\s*build/)
})

test('canonical PDF gate and its guide require verification without repository writes', async () => {
  const quality = await readFile(new URL('../.github/workflows/tcc-quality.yml', import.meta.url), 'utf8')
  const guide = await readFile(new URL('../.github/workflows/README.md', import.meta.url), 'utf8')
  const canonical = quality.split('\n  canonical-pdf-sync:')[1]
  assert.ok(canonical, 'the canonical PDF provenance gate must remain present')
  assert.match(canonical, /contents:\s*read/)
  assert.match(canonical, /persist-credentials:\s*false/)
  assert.match(canonical, /python scripts\/check_canonical_pdf\.py/)
  assert.doesNotMatch(canonical, /(?:contents|actions):\s*write|git\s+(?:commit|push)|gh\s+workflow\s+run/)
  assert.match(guide, /scripts\/check_canonical_pdf\.py/)
  assert.doesNotMatch(guide, /pode atualizar o PDF compilado na branch/)
})
