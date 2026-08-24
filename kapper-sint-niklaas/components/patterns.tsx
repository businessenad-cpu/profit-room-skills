/**
 * Handgecodeerde tatreez- en geometrie-SVG's (zie DESIGN.md §4).
 * Alles tekent in currentColor zodat kleur via CSS stuurbaar is.
 */

/** Eén kruissteek: twee kruisende lijntjes in een cel van 4×4. */
function stitchPath(x: number, y: number): string {
  return `M${x} ${y}l3 3M${x + 3} ${y}l-3 3`;
}

/**
 * Tatreez-band: zigzag-rand van kruissteken met basislijn,
 * geabstraheerd van klassieke Palestijnse randmotieven. Gebruik als <hr>.
 */
export function TatreezBand({ className = "" }: { className?: string }) {
  // zigzag: bergjes van 4 steken breed, plus onderliggende stiklijn
  const zigzag = [
    [0, 8], [4, 4], [8, 0], [12, 4], [16, 8], [20, 4], [24, 0], [28, 4],
  ]
    .map(([x, y]) => stitchPath(x, y))
    .join("");
  const base = [0, 8, 16, 24].map((x) => stitchPath(x, 13)).join("");
  return (
    <div
      aria-hidden
      className={`text-gold/60 ${className}`}
      role="presentation"
    >
      <svg width="100%" height="17" preserveAspectRatio="none" aria-hidden>
        <defs>
          <pattern
            id="tatreez"
            width="32"
            height="17"
            patternUnits="userSpaceOnUse"
          >
            <path
              d={zigzag + base}
              stroke="currentColor"
              strokeWidth="1.1"
              strokeLinecap="round"
              fill="none"
            />
          </pattern>
        </defs>
        <rect width="100%" height="17" fill="url(#tatreez)" />
      </svg>
    </div>
  );
}

/** Achtpuntige ster (khatam): twee vierkanten, 45° gedraaid. */
function starSquares(cx: number, cy: number, r: number) {
  const s = r * Math.SQRT1_2;
  return (
    <>
      <rect
        x={cx - s}
        y={cy - s}
        width={s * 2}
        height={s * 2}
        fill="none"
        stroke="currentColor"
      />
      <rect
        x={cx - s}
        y={cy - s}
        width={s * 2}
        height={s * 2}
        fill="none"
        stroke="currentColor"
        transform={`rotate(45 ${cx} ${cy})`}
      />
    </>
  );
}

/**
 * Sterrenveld-achtergrond op 3–4% opacity. Spaarzaam gebruiken:
 * alleen hero, Over mij en footer (DESIGN.md).
 */
export function StarField({ className = "" }: { className?: string }) {
  return (
    <div
      aria-hidden
      className={`pointer-events-none absolute inset-0 text-bone opacity-[0.04] ${className}`}
    >
      <svg width="100%" height="100%" aria-hidden>
        <defs>
          <pattern
            id="starfield"
            width="96"
            height="96"
            patternUnits="userSpaceOnUse"
          >
            <g strokeWidth="1">{starSquares(48, 48, 22)}</g>
            <circle cx="0" cy="0" r="1.5" fill="currentColor" />
            <circle cx="96" cy="0" r="1.5" fill="currentColor" />
            <circle cx="0" cy="96" r="1.5" fill="currentColor" />
            <circle cx="96" cy="96" r="1.5" fill="currentColor" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#starfield)" />
      </svg>
    </div>
  );
}

/**
 * Grote geometrische ster-tessellatie voor de hero: dicht raster van
 * khatam-sterren dat via CSS-mask naar transparant uitloopt.
 */
export function HeroGeo({ className = "" }: { className?: string }) {
  return (
    <div
      aria-hidden
      className={`pointer-events-none absolute inset-y-0 right-0 w-2/3 text-olive-deep ${className}`}
      style={{
        maskImage: "linear-gradient(to left, black 30%, transparent 95%)",
        WebkitMaskImage: "linear-gradient(to left, black 30%, transparent 95%)",
      }}
    >
      <svg width="100%" height="100%" aria-hidden>
        <defs>
          <pattern
            id="herogeo"
            width="120"
            height="120"
            patternUnits="userSpaceOnUse"
          >
            <g strokeWidth="1.5">{starSquares(60, 60, 34)}</g>
            <g strokeWidth="1">{starSquares(0, 0, 14)}</g>
            <g strokeWidth="1">{starSquares(120, 0, 14)}</g>
            <g strokeWidth="1">{starSquares(0, 120, 14)}</g>
            <g strokeWidth="1">{starSquares(120, 120, 14)}</g>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#herogeo)" opacity="0.5" />
      </svg>
    </div>
  );
}
