# The Cheese Vault design system

## Overview

A cozy, premium farming dApp for people using Ethereum Sepolia wallets. The visual idea is a small golden hamster guarding a very real on-chain cheese vault. A cream canvas, chocolate ink, rounded display type and a custom 2.5D diorama carry the identity. Actual balances, actions and proof stay quieter and precise. The hero retains its illustrated headline and required tagline, followed by one sentence naming Sepolia staking and the 15% withdrawal fee. The redundant hero footnote is removed; the illustration and chain overview follow in normal flow.

`src/styles.css` is the token/style source of truth; `src/components.tsx` contains shared primitives. `src/App.tsx` composes the five pages. The home hero is a page-specific two-column composition, not a template to repeat above every tool page. Farm and Portfolio lead with positions and controls. One warm gold primary action competes with neutral secondary controls; the persistent wallet utility uses chocolate.

## Colors

The implementation uses hex primitives mapped to semantic CSS custom properties. Components use semantic roles where available; illustration colors and the three asset identities are deliberate artwork exceptions. There is one light theme.

| Semantic token | Exact value / primitive | Use |
| --- | --- | --- |
| `--color-bg-page` | `--cream-50: #faf7ef` | Main canvas |
| `--color-bg-surface` | `#fffcf5` | Pool/position/proof surfaces |
| `--color-bg-sunken` | `--cream-100: #f2ecdf` | Inputs, inactive controls, grouped panels |
| `--color-bg-raised` | `#fffdf8` | Dialogs and wallet popover |
| `--color-text-primary` | `--brown-950: #463321` | Headings, body, focus perimeter |
| `--color-text-secondary` | `--brown-500: #7a6650` | Captions, labels, supporting copy |
| `--color-text-inverse` | `--cream-50: #faf7ef` | Wallet utility text |
| `--color-text-disabled` | `#8b7c69` | Reserved disabled text role; native disabled controls also dim |
| `--color-border` | `--cream-300: #d7c8ae` | Field outline and strong separator |
| `--color-separator` | `--cream-200: #e6dcc7` | Rows, columns, fine structural divisions |
| `--color-accent-solid` | `--gold-400: #f2c65b` | Main action and illustration flourish |
| `--color-accent-solid-hover` | `--gold-500: #e9b843` | Main action hover |
| `--color-accent-subtle` | `--gold-100: #fff0bf` | Hover and instruction icon surface |
| `--color-accent-text` | `--gold-800: #795318` | Warm emphasis, decorative symbols |
| `--color-success-bg/text` | `#eaf0e1` / `#49623c` | Confirmed/earning status |
| `--color-warning-bg/text` | `#f8edcf` / `#795520` | Inactive rewards and blocked readiness |
| `--color-error-bg/text` | `#f9e8e2` / `#9c3d2f` | Failed or rejected operations |

Declared opaque foreground/background pairs were calculated, not visually estimated. Primary/page is 11.17:1; secondary/page 5.10:1; secondary/surface 5.33:1; secondary/sunken 4.64:1; primary/gold 7.41:1. Status pairs are above 5.6:1. Exact inputs/results are recorded in `artifacts/revision-validation.json`. These are source-pair measurements. The revision also measured the new proof evidence against its rendered surface: secondary text 5.332:1 and evidence link 11.672:1. Alpha-composited disabled controls and art overlays remain incompletely measured.

## Typography

Local `public/fonts/fredoka.ttf` (Fredoka variable 300–700) supplies headings and prominent numbers. Local `public/fonts/nunito.ttf` (Nunito Sans variable 200–900) supplies body, controls and labels. Both are preloaded, use `font-display: swap`, and fall back to `sans-serif`. No external font request is needed. The implemented weights are **400, 500 and 700**. `font-synthesis: none` preserves supplied styles. Prose does not require italic or small caps.

The six named scale tokens are `--text-small: .875rem` (14px), `--text-body: 1rem` (16px), `--text-medium: 1.25rem` (20px), `--text-heading: 1.75rem` (28px), `--text-large: 2.5rem` (40px), `--text-display: 5rem` (80px). At widths up to 1180px the hero uses 64px; at 950px and below it uses 56px. On phones the display token is 56px and tool page titles remain 40px. Decorative SVG art does not define UI sizes.

Headings use Fredoka 500, balanced wrapping, line-height 1.14; the short hero uses 1.04 and tighter tracking. Body uses 1.5; supporting text generally uses 1.55–1.6. Prose is limited to 65ch. Navigation and action text use Nunito Sans 700. Numeric data uses `font-variant-numeric: tabular-nums`. Addresses use system monospace at 14px with arbitrary wrapping; full addresses remain present and copyable. Form numbers use Fredoka at 28px, safely above iOS’s input zoom threshold.

`Amount` in `src/components.tsx` normally displays compact readable balances with an exact `title`. Its `exact` variant is required for consequential fee and approval values: all decimal digits are displayed and can wrap. Transaction construction always uses bigint, independent of the visual formatter.

## Layout

`content-width` is at most 1200px, centered with 48px desktop side margins; the header grows to 1352px. Repeated groups use 8/12/16/20/24/28/32px spacing, with larger section gaps of 40–64px. Content grows naturally; fixed heights are limited to decorative scenes, icons and minimum hit targets. Controls remain inset from viewport edges.

Implemented breakpoints:

- **1500px and up:** larger home hero breathing room.
- **1180px and down:** tighter navigation, smaller display type, compact surface padding.
- **950px and down:** navigation moves to a second header row; pool headers stack within three columns; proof rows become vertical; instructions become two columns.
- **640px and down:** hero, pools, portfolio and instructions become one column. The hero’s main action precedes its 240px illustration. Live stats form a 2×2 grid. Portfolio retains distinct per-asset fields. Proof statuses become a 2×2 grid. All navigation links remain accessible in a wrapping row. Dialogs become full-width bottom sheets with a 20px top clearance and safe-area bottom padding.
- **370px and down:** navigation wraps with explicit gaps, surfaces narrow, position fields stack and secondary arrows are removed to preserve button labels.

The hero artwork container clips decorative overflow so its oversized illustration cannot widen the viewport. Critical values and controls are never clipped. The first phone screen is designed to show the brand, product, explanatory line and “Explore Cheese Farm” before the illustration; **the final 390×844 screenshot confirms the primary CTA at y=459.25–509.25**. Chromium checked all five pages at 320, 390, 768, 1024 and 1440px without horizontal overflow. See `VALIDATION.md` for remaining browser limits.

## Elevation & Depth

Surfaces use `--shadow-surface`: a low-opacity 1px shadow ring plus a subtle 3px lift. Hover uses `--shadow-hover`, a slightly stronger ring and ambient lift. Cards do not pair a CSS border with a depth shadow. Borders divide rows/columns or outline fields. The primary action has a short caramel bottom shadow to feel tactile without a generic glowing DeFi style.

The native dialog top layer provides real background inertness and sits over a translucent chocolate scrim, with 5px backdrop blur. The persistent header is in normal document flow at z-index 20; the wallet utility popover is anchored to its control. There is no sticky header covering phone content.

## Shapes

`--radius-small: 10px` is for buttons and fields; `--radius: 18px` for cards; `--radius-large: 28px` for feature panels and desktop dialogs. Badges use a quiet 6px corner. Phone bottom sheets use 26px top corners. The segmented action switch uses a 12px outer shape, 4px inset and 9px active control. Asset circles and the hamster are illustration language, not alternate interaction controls.

## Components

| Pattern | Source | Behavior and reuse |
| --- | --- | --- |
| `.button` | `src/styles.css` | 48px minimum; primary gold, neutral pool action, quiet outlined secondary, chocolate wallet. Explicit hover/focus/disabled/pressed states. Press scale 0.96. |
| `Coin`, `Hamster` | `src/components.tsx` | Original local SVG illustrations. Decorative art is hidden from assistive technology. `Hamster bite` is used only after a matching confirmed withdrawal event. |
| `Badge` | `src/components.tsx` | Neutral/good/warning/error, with written status and a dot. Color alone never defines state. |
| `Amount` | `src/components.tsx` | Stable digits, optional symbol, unavailable dash, full precision through `exact`. Never use a formatted value to build a transaction. |
| `CopyAddress` | `src/components.tsx` | Full address, Etherscan link, named copy button and polite copied/error announcement. Copy failure retains selectable source text. |
| `Notice` | `src/components.tsx` | Inline info/warning/error explanation, adjacent to the relevant controls. |
| `Modal` | `src/components.tsx` | Native `dialog.showModal()`, labeled title, focus restoration, Escape/backdrop close and one close button. Transaction signing/pending phases hold the dialog open while their flow is unresolved. |
| `WalletControl`, `WalletSheet` | `src/wallet.tsx` | One header utility; discovered names/icons, Coinbase row, mobile app-browser links, pending/rejection and chain-switch states. |
| `PoolCard` | `src/App.tsx` | Consistent per-asset summary and actions. Current allocation/status are live; unavailable and unconfigured are distinct. |
| `TransactionModal`, `FeeBreakdown` | `src/TransactionModal.tsx` | Deposit/withdraw/claim, exact Max, approval, simulation, fee/gas review, signature, pending receipt, success/error and receipt retry. Amount and Max both lock during review; Edit amount clears it and requires fresh simulation. The nominal fee illustration never substitutes for the real quote. |
| `ReadStatus` | `src/App.tsx` | Linked read block, refresh, unavailable and stale-update copy. With `verifySources`, Refresh also retries all five independent source queries. |
| `SourceVerificationFact` | `src/App.tsx`, `src/contracts/verification.ts` | Existing Proof fact cell; checking, verified and unavailable states; direct Sourcify evidence link and UTC observation time. Source claims are distinct from deployment/configuration/activation. `.source-verification` stacks details with 5px gaps and wraps long text; fact grids align content to the start. |

Keyboard focus uses a 2px chocolate perimeter with 4px offset. A skip link focuses the current page’s main landmark without changing route. Hash navigation resets the scroll and focuses main. Native buttons/anchors/labels are used. Dynamic errors use `role="alert"`, pending and success use status announcements. The revision inspected the home CTA’s visible focus ring and exercised keyboard access to Edit amount plus dialog focus restoration in Chromium. Screen-reader sessions and native WebKit behavior remain unperformed.

The hero has a slow 7-second, 7px vertical motion; small decorative sparkles vary opacity/scale. The receipt-triggered nibble is a short finite sequence. `prefers-reduced-motion: reduce` disables all animation, transitions and press movement, retaining written state. Interactive color/opacity/transform transitions are named and last 150ms; there is no `transition: all`. No animation claims a completed transaction before confirmation.

## Do’s and Don’ts

- Start an additional page with `content-width inner-page`, `PageIntro`, and the existing section spacing; register its hash route and nav item together.
- Reuse semantic colors, the six type roles and the existing action hierarchy. Keep permanent brand art distinct from transaction state.
- Keep unavailable values distinct from zero. Label historical local activity and source-verification limits honestly.
- Keep assets separate. CHEESE rewards can share a denomination; ETH, CHEESE and sIMD principal cannot be added into an invented total.
- Show full transaction values with `Amount exact`; preserve complete copyable addresses and bigint construction.
- Do not add kicker labels, extra font families, all-caps prose, generic yield figures, owner controls, or a second primary action color.
- Use receipt events for completed bite visuals. Never let timer completion, a returned hash, a simulation, or a mocked test trigger a real success claim.

The design follows the pinned Better Interface guide across accessibility, layout, writing, typography, colors and UI. Coverage, source findings, fixes and unresolved testing limitations are recorded separately in `VALIDATION.md` and `artifacts/revision-validation.json`; the design document is an implementation description, not an independent certification.
