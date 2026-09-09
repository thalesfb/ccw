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
