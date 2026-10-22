import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

const workflow = await readFile(new URL('../.github/workflows/publish-reports.yml', import.meta.url), 'utf8')
const qualityWorkflow = await readFile(new URL('../.github/workflows/tcc-quality.yml', import.meta.url), 'utf8')

test('source validation checks the reproducibility manifest and optional templates', () => {
  assert.ok(qualityWorkflow.includes('tests/test_reproducibility_manifest.py'))
  assert.ok(qualityWorkflow.includes('tests/test_tcc_optional_frontmatter.py'))
  assert.ok(qualityWorkflow.includes('tests/test_protocol_consistency_current.py'))
  assert.ok(qualityWorkflow.includes('tests/test_tcc_readiness_regressions.py'))
})

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
