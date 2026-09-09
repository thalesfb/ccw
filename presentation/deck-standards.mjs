const HEX_COLOR = /^#([0-9a-f]{6})$/i

function parseHexColor(color) {
  const match = HEX_COLOR.exec(color)
  if (!match) throw new Error(`Expected a six-digit hex color, received: ${color}`)

  return [0, 2, 4].map((offset) => Number.parseInt(match[1].slice(offset, offset + 2), 16) / 255)
}

function relativeLuminance(color) {
  return parseHexColor(color)
    .map((channel) => (channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4))
    .reduce((sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index], 0)
}

export function contrastRatio(foreground, background) {
  const foregroundLuminance = relativeLuminance(foreground)
  const backgroundLuminance = relativeLuminance(background)
  const lighter = Math.max(foregroundLuminance, backgroundLuminance)
  const darker = Math.min(foregroundLuminance, backgroundLuminance)
  return (lighter + 0.05) / (darker + 0.05)
}

export function meetsWcagAA(foreground, background, { largeText = false } = {}) {
  return contrastRatio(foreground, background) >= (largeText ? 3 : 4.5)
}

export function deckValidationErrors({ slides, css, assetPaths, repositoryUrl }) {
  const errors = []
  const assets = new Set(assetPaths)

  if (!slides.includes('./public/branding/ifc-campus-videira-horizontal.png')) {
    errors.push('The deck must use the official IFC Campus Videira logo asset.')
  }
  if (!assets.has('public/branding/ifc-campus-videira-horizontal.png')) {
    errors.push('The official IFC Campus Videira logo asset is missing.')
  }
  if (!slides.includes('./public/branding/ccw-repository-qr.svg')) {
    errors.push('The closing slide must include the repository QR asset.')
  }
  if (!assets.has('public/branding/ccw-repository-qr.svg')) {
    errors.push('The repository QR asset is missing.')
  }
  if (!slides.includes(repositoryUrl)) {
    errors.push('The closing slide must expose the canonical repository URL.')
  }
  if (!slides.includes('QR code que abre o repositório público')) {
    errors.push('The repository QR image must have an explanatory alternative text.')
  }
  if (!css.includes("'Asap'") || !css.includes("'Barlow'")) {
    errors.push('The deck must keep the Asap/Barlow typography defined by the supplied template.')
  }
  const hasDecorativeFontGuard = css.includes('.deck-font-guard') && css.includes("font-family: 'Asap', 'Barlow'")
  if (slides.includes('ifc-symbol') || (css.includes('Comic Sans MS') && !hasDecorativeFontGuard)) {
    errors.push('The deck must not recreate the IFC mark or use unapproved decorative typography.')
  }

  const requiredContrastPairs = [
    ['#1f2a37', '#ffffff', 'primary text on paper'],
    ['#4a4a4a', '#ffffff', 'secondary text on paper'],
    ['#ffffff', '#1f2a37', 'inverse text on dark cards'],
    ['#ffffff', '#315e9b', 'inverse text on blue accents'],
    ['#ffffff', '#8a5c1a', 'inverse text on amber badges'],
  ]
  for (const [foreground, background, label] of requiredContrastPairs) {
    if (!meetsWcagAA(foreground, background)) {
      errors.push(`Insufficient WCAG AA contrast for ${label}: ${foreground} on ${background}.`)
    }
  }

  return errors
}
