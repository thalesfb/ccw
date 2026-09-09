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
  formatInteger(summary.statistics.databases.semantic_scholar),
  formatInteger(summary.statistics.databases.openalex),
  formatInteger(summary.statistics.databases.crossref),
  formatInteger(summary.statistics.databases.core),
  '17',
  '1',
  '2015–2026',
  '72',
  './public/images/prisma_flow.png',
  './public/images/selection_funnel.png',
  './public/images/papers_by_year.png',
  './public/images/techniques_distribution.png',
  './public/images/relevance_distribution.png',
]

const requiredTemplateMarkers = [
  'ptc-challenge-layout',
  'ptc-objective-layout',
  'ptc-question-grid',
  'ptc-mission-layout',
  'ptc-objective-roadmap',
  'ptc-search-layout',
  'ptc-source-grid',
  'ptc-funnel-layout',
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
const missingTemplateMarkers = requiredTemplateMarkers.filter((marker) => !slides.includes(marker))
const forbidden = forbiddenClaims.filter((statement) => slides.includes(statement))

if (missing.length || missingTemplateMarkers.length || forbidden.length) {
  if (missing.length) console.error(`Missing current presentation statements: ${missing.join(', ')}`)
  if (missingTemplateMarkers.length) console.error(`Missing PTC template structures: ${missingTemplateMarkers.join(', ')}`)
  if (forbidden.length) console.error(`Forbidden historical/internal claims: ${forbidden.join(', ')}`)
  process.exit(1)
}

console.log(`PASS: presentation reconciled with summary.json (${formatInteger(prisma.included)} retained records).`)
