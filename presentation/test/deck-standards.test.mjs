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
      'S1 Há perguntas de pesquisa claras?',
      'S2 Os dados coletados permitem responder às perguntas de pesquisa?',
      'Y = Sim N = Não CT = Não é possível concluir',
    ].join('\n'),
    css: ":root { --tcc-ink: #1f2a37; } body { font-family: 'Times New Roman', 'Nimbus Roman'; } h1 { font-family: 'Times New Roman'; }",
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
  assert.equal(errors.some((error) => error.includes('Times-compatible')), true)
  assert.equal(errors.some((error) => error.includes('unapproved decorative typography')), true)
})

test('requires the MMAT screening questions and current response legend in the deck', () => {
  const errors = deckValidationErrors({
    slides: [
      '<img src="./public/branding/ifc-campus-videira-horizontal.png">',
      '<img src="./public/branding/ccw-repository-qr.svg" alt="QR code que abre o repositório público">',
      'https://github.com/thalesfb/ccw',
      'S1',
      'S2',
      'Há perguntas de pesquisa claras?',
      'Os dados coletados permitem responder às perguntas de pesquisa?',
      'Y = Sim',
      'N = Não',
      'CT = Não é possível concluir',
    ].join('\n'),
    css: "body { font-family: 'Times New Roman'; } .deck-font-guard { font-family: 'Times New Roman', 'Nimbus Roman'; }",
    assetPaths: [
      'public/branding/ifc-campus-videira-horizontal.png',
      'public/branding/ccw-repository-qr.svg',
    ],
    repositoryUrl: 'https://github.com/thalesfb/ccw',
  })

  assert.deepEqual(errors, [])
})

test('reports an MMAT deck that hides S1/S2 or uses an ambiguous legend', () => {
  const errors = deckValidationErrors({
    slides: 'MMAT preliminar; S/N/ND',
    css: "body { font-family: 'Times New Roman'; } .deck-font-guard { font-family: 'Times New Roman', 'Nimbus Roman'; }",
    assetPaths: [],
    repositoryUrl: 'https://github.com/thalesfb/ccw',
  })

  assert.equal(errors.some((error) => error.includes('S1 and S2')), true)
  assert.equal(errors.some((error) => error.includes('Y/N/CT')), true)
})
