import test from 'node:test'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

test('initializes the Slidev desktop tooltip plugin without console errors', () => {
  // Resolve through Slidev's client, not an unrelated top-level installation.
  // Characterize the real plugin registration; mounting and layout still need
  // a browser check. Import before adding the desktop event surface so Vue does
  // not mistake this unmounted Node probe for a complete browser DOM.
  const probe = `
    import assert from 'node:assert/strict'
    import { createRequire } from 'node:module'
    import { pathToFileURL } from 'node:url'

    const cliRequire = createRequire(import.meta.resolve('@slidev/cli'))
    const clientRequire = createRequire(cliRequire.resolve('@slidev/client/package.json'))
    const { createApp } = await import(pathToFileURL(clientRequire.resolve('vue')).href)
    const { default: TwoslashFloatingVue } = await import(
      pathToFileURL(clientRequire.resolve('@shikijs/vitepress-twoslash/client')).href
    )

    globalThis.window = new EventTarget()
    const app = createApp({})
    app.use(TwoslashFloatingVue, { container: '#twoslash-container' })
    assert.ok(app.component('VMenu'), 'The tooltip menu must be registered')
    assert.ok(app.directive('tooltip'), 'The tooltip directive must be registered')
  `
  const result = spawnSync(process.execPath, ['--input-type=module', '-e', probe], {
    cwd: fileURLToPath(new URL('..', import.meta.url)),
    encoding: 'utf8',
    timeout: 30_000,
  })

  assert.ifError(result.error)
  assert.equal(result.status, 0, result.stderr)
  // Twoslash catches incompatible VMenu internals and logs instead of throwing.
  assert.equal(result.stderr, '', 'Tooltip initialization must not log errors or warnings')
})
