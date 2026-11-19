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
  assert.match(css, /\.tcc-prisma-slide \.tcc-prisma-image\s*\{[^}]*transform:\s*none;/)
  assert.match(css, /\.slidev-layout\.cover-page \.cover-art-top\s*\{\s*top:\s*2\.2rem;/)
  assert.match(css, /\.slidev-layout\.cover-page \.cover-art-bottom\s*\{\s*bottom:\s*2\.1rem;/)
  assert.match(css, /\.cover-art-top\s*\{\s*top:\s*2\.2rem;/)
  assert.match(css, /\.cover-art-bottom\s*\{\s*bottom:\s*2\.1rem;/)
})

test('the objectives roadmap uses the available vertical stage', () => {
  assert.match(css, /\.slidev-layout\.tcc-objectives-slide\s*\{[^}]*display:\s*flex;[^}]*flex-direction:\s*column;[^}]*justify-content:\s*center;/)
})

test('remaining content slides fill a shared vertical stage without touching the exceptions', () => {
  assert.match(css, /\.slidev-layout\.content-slide:not\(\.tcc-objectives-slide\)\s*\{[^}]*display:\s*flex;[^}]*flex-direction:\s*column;/)
  assert.match(css, /\.slidev-layout\.content-slide:not\(\.tcc-objectives-slide\)\s*>\s*:is\([\s\S]*\.tcc-next-layout\s*\)\s*\{[\s\S]*flex:\s*1 1 auto;[\s\S]*min-height:\s*22rem;/)
  assert.doesNotMatch(css, /\.slidev-layout\.tcc-prisma-slide\s*\{[^}]*flex:\s*1 1 auto;/)
})

test('key narrative slides use the shared inline SVG icon system', () => {
  assert.doesNotMatch(slides, /class="tcc-line-icon">[◎◷◈⌘]/)
  assert.doesNotMatch(slides, /class="tcc-source-icon">[⌘▤⛓⌑]/)
  assert.match(slides, /class="tcc-line-icon"[^>]*>[\s\S]*?<svg\s+viewBox="0 0 32 32"/)
  assert.match(slides, /class="tcc-source-icon"[^>]*>[\s\S]*?<svg\s+viewBox="0 0 32 32"/)
  assert.match(css, /\.tcc-line-icon svg[\s\S]*stroke-linecap:\s*round/)
  assert.match(css, /\.tcc-source-icon svg[\s\S]*stroke-linejoin:\s*round/)
})

test('the deck states the search cut-off date', () => {
  assert.match(slides, /busca até 31\/08\/2026/)
})

test('result slides are drawn in HTML, not as exported keyword-tag charts', () => {
  assert.doesNotMatch(slides, /techniques_distribution|relevance_distribution/)
  assert.match(slides, /class="tcc-typology-bars"/)
  assert.match(slides, /class="tcc-ct-grid"/)
  assert.match(css, /\.tcc-output-scale\s*\{[^}]*position:\s*relative;/)
})

test('research question is literal and the PRISMA flow is presented once', () => {
  assert.match(slides, /Como estruturar uma especificação técnica e pedagógica de protótipo para apoiar a interpretação docente da aprendizagem matemática a partir das evidências e técnicas computacionais identificadas na literatura\?/)
  assert.equal((slides.match(/src="\/images\/prisma_flow\.png"/g) || []).length, 1)
  assert.doesNotMatch(slides, /tcc-funnel-layout|O destino dos 18 registros/)
})

test('MMAT status slide keeps its caveats concise and category-specific', () => {
  const status = slides.match(/<div class="tcc-mmat-result">([\s\S]*?)<\/div>/)?.[1]
  assert.ok(status)
  assert.ok(status.length < 500, `MMAT status should stay concise; found ${status.length} characters`)
  assert.match(status, /Sokkhey/)
  assert.match(status, /métodos mistos/)
  assert.match(status, /Q1–Q5 variam por categoria/)
  assert.match(status, /sem escore agregado/)
})

test('architecture slide makes the seventh function explicit', () => {
  const architecture = slides.match(/<div class="slide-kicker">20 \/ ARQUITETURA E SAÍDA<\/div>([\s\S]*?)(?=\r?\n---\r?\n)/)?.[1]
  assert.ok(architecture)
  assert.match(architecture, /F07 · registro e exportação/)
  assert.match(architecture, /F01/)
  assert.match(architecture, /F06/)
})
