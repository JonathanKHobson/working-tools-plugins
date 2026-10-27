import { useCallback, useEffect, useRef, useState } from 'react'

const clamp = (n, min, max) => Math.max(min, Math.min(max, n))
const zero = () => ({ x: 0, y: 0, lift: 0 })

// One motion owner writes already-scaled values; CSS applies fixed pixel distances.
export default function useDepthMotion({ depth = 70, autoRotate = false, enabled = true } = {}) {
  const hitRef = useRef(null)
  const tiltRef = useRef(null)
  const options = useRef({ depth, autoRotate, enabled })
  const engine = useRef(null)
  const [reducedMotion, setReducedMotion] = useState(() => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches)

  useEffect(() => {
    const preference = window.matchMedia('(prefers-reduced-motion: reduce)')
    let reduced = preference.matches, disposed = false, frame = 0, last = 0
    let current = zero(), target = zero(), hovered = false, keyed = false
    let touchId = null, captureNode = null, orbitStart = performance.now()
    const strength = () => options.current.enabled && !reduced ? clamp(Number(options.current.depth) || 0, 0, 100) / 100 : 0
    const paint = () => {
      const node = tiltRef.current
      if (!node) return
      const amount = strength(), x = current.x * amount, y = current.y * amount
      node.style.setProperty('--rx', `${(-y * 14).toFixed(3)}deg`)
      node.style.setProperty('--ry', `${(x * 14).toFixed(3)}deg`)
      node.style.setProperty('--px', x.toFixed(4))
      node.style.setProperty('--py', y.toFixed(4))
      node.style.setProperty('--mx', `${(50 + x * 50).toFixed(2)}%`)
      node.style.setProperty('--my', `${(50 + y * 50).toFixed(2)}%`)
      node.style.setProperty('--lift', (current.lift * amount).toFixed(4))
    }
    const stop = () => { if (frame) cancelAnimationFrame(frame); frame = 0; last = 0 }
    const schedule = () => { if (!frame && !disposed && !document.hidden && strength()) frame = requestAnimationFrame(tick) }
    function tick(time) {
      frame = 0
      if (!strength()) { reset(); return }
      const ambient = options.current.autoRotate && !hovered && !keyed
      if (ambient) target = { x: Math.sin((time - orbitStart) / 4200) * .42, y: Math.sin((time - orbitStart) / 5700) * .3, lift: .55 }
      const dt = last ? clamp(time - last, 0, 64) : 16.7
      last = time
      const blend = 1 - Math.exp(-dt / 85)
      let moving = false
      for (const axis of ['x', 'y', 'lift']) {
        current[axis] += (target[axis] - current[axis]) * blend
        if (Math.abs(target[axis] - current[axis]) < .0005) current[axis] = target[axis]
        else moving = true
      }
      paint()
      if (ambient || moving) schedule(); else last = 0
    }
    const release = () => {
      if (touchId !== null && captureNode) {
        try { if (captureNode.hasPointerCapture(touchId)) captureNode.releasePointerCapture(touchId) } catch { /* scroll may cancel capture */ }
      }
      touchId = null; captureNode = null
    }
    const reset = () => {
      release(); stop(); current = zero(); target = zero(); hovered = false; keyed = false
      orbitStart = performance.now(); paint(); if (options.current.autoRotate) schedule()
    }
    const rest = () => { hovered = false; keyed = false; target = zero(); schedule() }
    const pointerMove = event => {
      if (!strength() || (event.pointerType === 'touch' && event.pointerId !== touchId)) return
      const box = hitRef.current?.getBoundingClientRect() // stable, untransformed hit plane
      if (!box?.width || !box.height) return
      target = { x: clamp((event.clientX - box.left) / box.width * 2 - 1, -1, 1), y: clamp((event.clientY - box.top) / box.height * 2 - 1, -1, 1), lift: 1 }
      hovered = true; keyed = false; schedule()
    }
    const pointerDown = event => {
      if (event.isPrimary === false) return
      if (event.pointerType === 'touch') {
        touchId = event.pointerId; captureNode = event.currentTarget
        try { captureNode.setPointerCapture(touchId) } catch { /* capture is optional */ }
      }
      pointerMove(event)
    }
    const pointerUp = event => { if (event.pointerId === touchId) { release(); rest() } }
    const pointerCancel = () => { release(); rest() }
    const pointerLeave = event => { if (event.pointerType !== 'touch') rest() }
    const keyDown = event => {
      if (['Home', 'Escape', '0'].includes(event.key)) { event.preventDefault(); reset(); return }
      const step = { ArrowLeft: [-.2, 0], ArrowRight: [.2, 0], ArrowUp: [0, -.2], ArrowDown: [0, .2] }[event.key]
      if (!step || !strength()) return
      event.preventDefault(); keyed = true; hovered = false
      target = { x: clamp(target.x + step[0], -1, 1), y: clamp(target.y + step[1], -1, 1), lift: 1 }; schedule()
    }
    const refresh = () => { if (!strength()) reset(); else schedule() }
    const onPreference = event => { reduced = event.matches; setReducedMotion(reduced); refresh() }
    const onVisibility = () => { if (document.hidden) stop(); else refresh() }
    preference.addEventListener('change', onPreference)
    document.addEventListener('visibilitychange', onVisibility)
    engine.current = { pointerMove, pointerDown, pointerUp, pointerCancel, pointerLeave, keyDown, rest, reset, refresh }
    paint(); refresh()
    return () => { disposed = true; stop(); release(); preference.removeEventListener('change', onPreference); document.removeEventListener('visibilitychange', onVisibility); engine.current = null }
  }, [])
  useEffect(() => { options.current = { depth, autoRotate, enabled }; engine.current?.refresh() }, [depth, autoRotate, enabled])
  const call = name => event => engine.current?.[name](event)
  const reset = useCallback(() => engine.current?.reset(), [])
  return { hitRef, tiltRef, reducedMotion, reset, bind: {
    onPointerMove: call('pointerMove'), onPointerDown: call('pointerDown'), onPointerUp: call('pointerUp'),
    onPointerCancel: call('pointerCancel'), onPointerLeave: call('pointerLeave'),
    onKeyDown: call('keyDown'), onBlur: call('rest')
  } }
}
