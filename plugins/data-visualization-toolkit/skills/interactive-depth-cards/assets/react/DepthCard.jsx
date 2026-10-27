import React, { useEffect, useRef, useState } from 'react'
import useDepthMotion from './useDepthMotion.js'
import './DepthCard.css'

// Paths should point at bundled project-local art. Text remains live React content.
export default function DepthCard({ title, description = '', layers, back, children, sparkles = 0, finish = 'holographic', depth = 70, foil = true,
  autoRotate = false, exploded, flipped, onFlippedChange, onExplodedChange, instructionsId, focusRef }) {
  if (!Array.isArray(layers) || !layers.length || layers.some(layer => typeof layer?.src !== 'string' || !layer.src.trim() || (/^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(layer.src.trim()) && !/^data:image\/(?:png|jpeg|webp);base64,/i.test(layer.src.trim())))) {
    throw new Error('DepthCard requires project-local raster image paths or embedded PNG/JPEG/WebP data')
  }
  if (!Number.isInteger(sparkles) || sparkles < 0 || sparkles > 24) throw new Error('sparkles must be 0–24')
  const [ownFlipped, setOwnFlipped] = useState(false)
  const [ownExploded, setOwnExploded] = useState(false)
  const isExploded = exploded ?? ownExploded
  const isFlipped = !isExploded && (flipped ?? ownFlipped)
  const setFlipped = onFlippedChange ?? setOwnFlipped
  const setExploded = onExplodedChange ?? setOwnExploded
  const { hitRef, tiltRef, bind, reset, reducedMotion } = useDepthMotion({ depth, autoRotate, enabled: !isFlipped && !isExploded })
  useEffect(() => { if (focusRef) focusRef.current = hitRef.current; return () => { if (focusRef) focusRef.current = null } }, [focusRef, hitRef])
  const start = useRef(null)
  const dragged = useRef(false)
  const hasBack = Boolean(back)
  const changeFlip = () => { if (!hasBack) return; reset(); setExploded(false); setFlipped(!isFlipped) }
  const changeExploded = () => { reset(); setFlipped(false); setExploded(!isExploded) }
  const classes = ['depth-card', `finish-${finish}`, foil ? 'has-foil' : '', isFlipped ? 'flipped' : '', isExploded ? 'exploded' : ''].filter(Boolean).join(' ')
  const onKeyDown = event => {
    if (hasBack && (event.key === 'Enter' || event.key === ' ')) { event.preventDefault(); changeFlip() }
    else bind.onKeyDown(event)
  }
  return <div className="depth-card-shell">
    <div className={classes} ref={hitRef} tabIndex={0} role={hasBack ? 'button' : 'group'}
      aria-label={`${title} card. Arrow keys tilt; Home resets${hasBack ? '; Enter or Space flips' : ''}.`}
      aria-pressed={hasBack ? isFlipped : undefined} aria-describedby={instructionsId}
      onPointerDown={event => { start.current = { x: event.clientX, y: event.clientY, id: event.pointerId }; dragged.current = false; bind.onPointerDown(event) }}
      onPointerMove={event => { if (start.current?.id === event.pointerId && Math.hypot(event.clientX - start.current.x, event.clientY - start.current.y) > 8) dragged.current = true; bind.onPointerMove(event) }}
      onPointerUp={event => { start.current = null; bind.onPointerUp(event) }}
      onPointerCancel={event => { start.current = null; dragged.current = true; bind.onPointerCancel(event) }}
      onPointerLeave={bind.onPointerLeave} onBlur={bind.onBlur} onKeyDown={onKeyDown}
      onClick={event => { if (event.detail === 0 || !dragged.current) changeFlip(); dragged.current = false }}>
      <div className="depth-card-tilt" ref={tiltRef}><div className="depth-card-flipper">
        <div className="depth-card-face depth-card-front" aria-hidden={isFlipped}>
          <div className="depth-card-art">{layers.map((layer, index) => <img key={`${layer.src}-${index}`} src={layer.src}
            alt={layer.alt ?? ''} draggable="false" className={`depth-card-layer role-${layer.role ?? (index ? 'foreground' : 'background')}`}
            style={{ '--z': `${layer.depth ?? 0}px`, '--shift': `${layer.role === 'background' || (!layer.role && index === 0) ? -6 : (layer.depth ?? 0) * (layer.role === 'particles' ? .14 : .36)}px` }} />)}</div>
          {sparkles > 0 && <div className="depth-card-sparkles" aria-hidden="true">{Array.from({ length: sparkles }, (_, index) =>
            <i key={index} style={{ left: `${(index * 47 + 13) % 91}%`, top: `${(index * 31 + 17) % 87}%`, animationDelay: `${-index * .37}s` }} />)}</div>}
          <div className="depth-card-print"><strong>{title}</strong><p>{description}</p>{children}</div>
          <div className="depth-card-foil" aria-hidden="true" /><div className="depth-card-glare" aria-hidden="true" />
        </div>
        <div className="depth-card-face depth-card-back" aria-hidden={!isFlipped}>{hasBack && <div><strong>{back.title}</strong><p>{back.body}</p></div>}</div>
      </div></div>
    </div>
    <div className="depth-card-actions"><button type="button" aria-pressed={isExploded} onClick={changeExploded}>{isExploded ? 'Join layers' : 'Separate layers'}</button>
      {hasBack && <button type="button" aria-pressed={isFlipped} onClick={changeFlip}>{isFlipped ? 'Show front' : 'Show back'}</button>}
      <button type="button" onClick={reset}>Reset view</button></div>
    {reducedMotion && <p className="depth-card-note">Reduced motion is active; views change immediately.</p>}
  </div>
}
