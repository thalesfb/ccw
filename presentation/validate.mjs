import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const presentationPath = resolve(import.meta.dirname, 'slides.md')
const summaryPath = resolve(import.meta.dirname, '..', 'research', 'exports', 'reports', 'summary.json')
const slides = readFileSync(presentationPath, 'utf8')
const summary = JSON.parse(readFileSync(summaryPath, 'utf8'))
const prisma = summary.statistics.prisma

const formatInteger = (value) => value.toLocaleString('pt-BR')
const requiredValues = [
  prisma.identification,
  prisma.duplicates_removed,
  prisma.screening,
  prisma.screening_excluded,
  prisma.eligibility,
  prisma.eligibility_excluded,
  prisma.included,
].map(formatInteger)

const requiredStatements = [
  ...requiredValues,
  '23 candidatos',
  '7 overrides manuais',
  '15 empíricos',
  '6921',
  'não equivalentes aos gates executados',
  'não foram gates obrigatórios',
  'Apoia um **relato transparente e completo**',
  'auditável e reconstruível',
  './public/images/prisma_flow.png',
  './public/images/selection_funnel.png',
  './public/images/database_coverage.png',
  './public/images/techniques_distribution.png',
  './public/images/papers_by_year.png',
  './public/images/relevance_distribution.png',
]

const staleClaims = [
  '9.431',
  '9,431',
  '2.517 duplicatas',
  '2,517 duplicatas',
  '6.914 estudos únicos',
  '6,914 estudos únicos',
  '1.883 elegíveis',
  '1,883 elegíveis',
  'Garante **rigor, transparência e reprodutibilidade**',
]

const missing = requiredStatements.filter((statement) => !slides.includes(statement))
const stale = staleClaims.filter((statement) => slides.includes(statement))

if (missing.length || stale.length) {
  if (missing.length) console.error(`Missing current presentation statements: ${missing.join(', ')}`)
  if (stale.length) console.error(`Stale presentation statements: ${stale.join(', ')}`)
  process.exit(1)
}

console.log(`PASS: presentation reconciled with summary.json (${formatInteger(prisma.included)} retained records).`)
