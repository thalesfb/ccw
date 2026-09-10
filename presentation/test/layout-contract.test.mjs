import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

const slides = await readFile(new URL('../slides.md', import.meta.url), 'utf8')
const css = await readFile(new URL('../styles/index.css', import.meta.url), 'utf8')

test('closing slide keeps its complete content on one explicit centered axis', () => {
  assert.match(slides, /<div class="closing-slide-content">[\s\S]*<h1>Obrigado<\/h1>[\s\S]*<\/div>/)
  assert.match(css, /\.closing-slide-content\s*\{[^}]*display:\s*flex;[^}]*width:\s*100%;[^}]*align-items:\s*center;[^}]*text-align:\s*center;/)
})

test('decorative mathematical drawings are hidden from assistive technology', () => {
  const decorativeBlocks = [...slides.matchAll(/<div class="cover-art [^"]+"([^>]*)>/g)]
  assert.ok(decorativeBlocks.length >= 8)
  assert.equal(decorativeBlocks.every(([, attributes]) => /aria-hidden="true"/.test(attributes)), true)
})

test('visual figures stay inside the presentation frame', () => {
  assert.match(css, /\.ptc-prisma-slide \.ptc-prisma-image\s*\{[^}]*transform:\s*none;/)
  assert.match(css, /\.slidev-layout\.cover-page \.cover-art-top\s*\{\s*top:\s*2\.2rem;/)
  assert.match(css, /\.slidev-layout\.cover-page \.cover-art-bottom\s*\{\s*bottom:\s*2\.1rem;/)
  assert.match(css, /\.cover-art-top\s*\{\s*top:\s*2\.2rem;/)
  assert.match(css, /\.cover-art-bottom\s*\{\s*bottom:\s*2\.1rem;/)
})

test('the objectives roadmap uses the available vertical stage', () => {
  assert.match(css, /\.slidev-layout\.ptc-objectives-slide\s*\{[^}]*display:\s*flex;[^}]*flex-direction:\s*column;[^}]*justify-content:\s*center;/)
})

test('remaining content slides fill a shared vertical stage without touching the exceptions', () => {
  assert.match(css, /\.slidev-layout\.content-slide:not\(\.ptc-objectives-slide\)\s*\{[^}]*display:\s*flex;[^}]*flex-direction:\s*column;/)
  assert.match(css, /\.slidev-layout\.content-slide:not\(\.ptc-objectives-slide\)\s*>\s*:is\([\s\S]*\.ptc-next-layout\s*\)\s*\{[\s\S]*flex:\s*1 1 auto;[\s\S]*min-height:\s*22rem;/)
  assert.doesNotMatch(css, /\.slidev-layout\.ptc-prisma-slide\s*\{[^}]*flex:\s*1 1 auto;/)
})
