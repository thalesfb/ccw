import test from 'node:test'
import assert from 'node:assert/strict'
import { contrastRatio, deckValidationErrors, meetsWcagAA } from '../deck-standards.mjs'

test('calculates the WCAG contrast ratio for black and white', () => {
  assert.equal(contrastRatio('#000000', '#ffffff'), 21)
})

test('requires AA contrast for normal text and allows the large-text threshold', () => {
  assert.equal(meetsWcagAA('#ffffff', '#8a8a8a'), false)
  assert.equal(meetsWcagAA('#ffffff', '#8a8a8a', { largeText: true }), true)
  assert.equal(meetsWcagAA('#1f2a37', '#ffffff'), true)
})

test('accepts a complete, accessible deck contract', () => {
  const errors = deckValidationErrors({
    slides: [
      '<img src="./public/branding/ifc-campus-videira-horizontal.png" alt="Instituto Federal Catarinense — Campus Videira">',
      '<img src="./public/branding/ccw-repository-qr.svg" alt="QR code que abre o repositório público do projeto no GitHub">',
      'https://github.com/thalesfb/ccw',
    ].join('\n'),
    css: ":root { --ptc-ink: #1f2a37; } body { font-family: 'Barlow'; } h1 { font-family: 'Asap'; }",
    assetPaths: [
      'public/branding/ifc-campus-videira-horizontal.png',
      'public/branding/ccw-repository-qr.svg',
    ],
    repositoryUrl: 'https://github.com/thalesfb/ccw',
  })

  assert.deepEqual(errors, [])
})

test('reports missing identity, QR, typography, and decorative-font safeguards', () => {
  const errors = deckValidationErrors({
    slides: 'ifc-symbol',
    css: "body { font-family: 'Comic Sans MS'; }",
    assetPaths: [],
    repositoryUrl: 'https://github.com/thalesfb/ccw',
  })

  assert.equal(errors.some((error) => error.includes('official IFC Campus Videira logo')), true)
  assert.equal(errors.some((error) => error.includes('repository QR')), true)
  assert.equal(errors.some((error) => error.includes('Asap/Barlow')), true)
  assert.equal(errors.some((error) => error.includes('unapproved decorative typography')), true)
})
