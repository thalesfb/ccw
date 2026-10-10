import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

test('Times typography is local and does not trigger CDN font imports', () => {
  const source = readFileSync(new URL('../slides.md', import.meta.url), 'utf8')
  const frontmatter = source.split(/^---\r?$/m)[1]
  assert.match(frontmatter, /^  sans: Times New Roman\r?$/m)
  assert.match(frontmatter, /^  serif: Times New Roman\r?$/m)
  assert.match(frontmatter, /^  provider: none\r?$/m)
})
