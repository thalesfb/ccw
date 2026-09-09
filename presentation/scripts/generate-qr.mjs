import { mkdirSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { renderSVG } from 'uqr'

export const repositoryUrl = 'https://github.com/thalesfb/ccw'
export const outputPath = resolve(import.meta.dirname, '..', 'public', 'branding', 'ccw-repository-qr.svg')

mkdirSync(dirname(outputPath), { recursive: true })
writeFileSync(outputPath, renderSVG(repositoryUrl, { ecc: 'M', border: 4 }))
console.log(`Generated QR for ${repositoryUrl}: ${outputPath}`)
