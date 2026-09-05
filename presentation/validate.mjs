import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const presentationPath = resolve(import.meta.dirname, 'slides.md')
const summaryPath = resolve(import.meta.dirname, '..', 'research', 'exports', 'reports', 'summary.json')
const slides = readFileSync(presentationPath, 'utf8')
const summaryText = readFileSync(summaryPath, 'utf8').replace(
  /:\s*(?:NaN|Infinity|-Infinity)(?=\s*[,}])/g,
  ': null',
)
const summary = JSON.parse(summaryText)
const prisma = summary.statistics.prisma
const techniques = summary.statistics.techniques

const formatInteger = (value) => value.toLocaleString('pt-BR')
const requiredStatements = [
  formatInteger(prisma.identification),
  formatInteger(prisma.duplicates_removed),
  formatInteger(prisma.screening),
  formatInteger(prisma.screening_excluded),
  formatInteger(prisma.eligibility),
  formatInteger(prisma.eligibility_excluded),
  formatInteger(prisma.included),
  formatInteger(techniques['Não especificado']),
  formatInteger(techniques['Assessment']),
  formatInteger(techniques['AI/Artificial Intelligence']),
  formatInteger(techniques['Machine Learning']),
  '17',
  '1',
  '2015–2026',
  '72',
  './public/images/prisma_flow.png',
  './public/images/selection_funnel.png',
  './public/images/database_coverage.png',
  './public/images/papers_by_year.png',
  './public/images/techniques_distribution.png',
  './public/images/relevance_distribution.png',
]

const forbiddenClaims = [
  '9.431',
  '9,431',
  '2.517',
  '2,517',
  '6.914',
  '6,914',
  '1.883',
  '1,883',
  '23 candidatos',
  '7 overrides',
  '6918',
  'nova rodada',
  'falsos positivos',
]

const missing = requiredStatements.filter((statement) => !slides.includes(statement))
const forbidden = forbiddenClaims.filter((statement) => slides.includes(statement))

if (missing.length || forbidden.length) {
  if (missing.length) console.error(`Missing current presentation statements: ${missing.join(', ')}`)
  if (forbidden.length) console.error(`Forbidden historical/internal claims: ${forbidden.join(', ')}`)
  process.exit(1)
}

console.log(`PASS: presentation reconciled with summary.json (${formatInteger(prisma.included)} retained records).`)
