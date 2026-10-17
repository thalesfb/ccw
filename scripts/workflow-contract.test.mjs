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

test('Pages publishes every CSV linked by the current public evidence pages', async () => {
  const { existsSync } = await import('node:fs')
  const sourceFiles = ['index.html', 'research/index.html', 'scripts/generate-mmat-page.mjs']
  const linkedNames = new Set()
  for (const source of sourceFiles) {
    const text = await readFile(new URL(`../${source}`, import.meta.url), 'utf8')
    for (const match of text.matchAll(/(?:research\/)?data\/([a-z_]+\.csv)/g)) {
      linkedNames.add(match[1])
    }
  }
  assert.ok(linkedNames.size >= 5)
  for (const name of linkedNames) {
    assert.ok(existsSync(new URL(`../research/data/${name}`, import.meta.url)), `${name} must exist`)
    assert.ok(workflow.includes(`cp research/data/${name} _site/research/data/`), `${name} must be packaged`)
  }
})
