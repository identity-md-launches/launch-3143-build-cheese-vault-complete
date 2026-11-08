# Validation and design review

## Revision results — 2026-11-08

This revision addresses the three supplied findings. The original contracts, ABIs, transaction construction, wallet connectors, artwork, fonts and tokens remain intact. The results below supersede the earlier run’s browser limitations. Evidence: [revision-validation.json](artifacts/revision-validation.json), [390px Home](artifacts/revision-home-390.jpg), [390px Proof](artifacts/revision-proof-390.jpg), and [.imd-responses.json](.imd-responses.json).

### Reproduction, corrections and rechecks

| Finding | Reproduced behavior | Final correction and evidence |
| --- | --- | --- |
| `0a35ddfa…` — Max invalidated the visible review | Unchanged production export, Chromium at 390×844 and 1440×900: after reviewing 1, Max displayed 100 CHEESE or 10,000 shares, while intercepted calldata still contained `1e18`. Both calls were rejected by an explicitly mocked EIP-6963 wallet; zero broadcasts. | `src/TransactionModal.tsx:562`: Max now shares the amount input’s review lock. Browser regressions verify 1 stays 1, unchanged fees/shares, and Edit amount → Max → new review signs the new units. JSDOM covers approval as well. Keyboard Tab reaches Edit amount and dialog dismissal restores focus. |
| `b518bad6…` — unconditional source verification | All five Source verified cells read Not checked before and after Refresh. No source query occurred. | `src/contracts/verification.ts:1`, `src/App.tsx:1230`: independent Sourcify v2 lookups validate the chain, address and runtime match, then display status, evidence link and UTC observation time. `src/App.tsx:181` refreshes the queries with protocol reads. Eight-second timeout, five-minute cache, explicit unavailable states, no inferred audit. Tests cover exact/runtime matches, incorrect identities, absent records, HTTP failures, invalid JSON, network failure, timeout and refresh. |
| `630b7202…` — stacked slogans | Original probe reported six matches, reproduced in the original 390px and 1440px screenshots. | `src/App.tsx:273`, `:390`, `:408`: required tagline/headline retained; direct staking/fee sentence; footnote removed; plain pool and fee copy. Final probe finds two slogan lines. Removing the footnote moves the phone illustration and chain overview up 38px naturally. |
| Proof layout during revision | The taller source-evidence cell stretched the neighboring Deployed label away from its value. Seen in mobile and desktop screenshots. | `src/styles.css:1396`: align each fact’s grid content to the start; measured label/value gaps are 5–6px at every tested width. New evidence uses existing small text and semantic colors. |

### Actual commands and results

The assigned `node_modules/` was not touched. The unchanged package manifest/lockfile, source, public assets and test/configuration files were copied into `test/scratch/revision-project`, then `npm ci --prefix test/scratch/revision-project --cache test/scratch/npm-cache --no-audit --no-fund` completed successfully with Node 24.21.0. The following package scripts ran in that source-identical copy. The final built `dist/` was copied back to the repository and checked again there.

| Check | Final result |
| --- | --- |
| `npm run typecheck` | Exit 0 after the final source change |
| `npm run test:core` | 33 passed, 0 failed |
| `npm run test:ui` | 40 passed, 0 failed: 28 UI cases and 12 verification cases |
| `npm run check:contracts` | Five unchanged official ABIs, 22 calldata round trips |
| `npm run build` | Exit 0; Vite 7.3.7; existing main-chunk warning now 731.45 kB / 210.04 kB gzip |
| `node scripts/check-export.mjs` | Exit 0 on final root export; 13 files, 3,709,701 bytes, relative assets, no failures |
| Pinned `taste.mjs --out test/scratch/taste` | Chromium rendered final export; 15/16 checks pass, compared with 14/16 before |
| Chromium transaction harness | Exit 0 before and after fix, 390×844 and 1440×900; mocked wallet/RPC, intercepted/rejected writes, zero broadcasts |
| Chromium layout harness | Exit 0; all five pages at 320, 390, 768, 1024 and 1440px; 25 route/width combinations without horizontal overflow, script errors or missing local assets |
| Bundle budget | [Measured complete source/export bundle](artifacts/bundle-budget.json); dependency/cache directories and scratch excluded, ignore file unchanged |

The browser harnesses served the actual root export under `/preview/`, not a development-only component. Playwright and browser downloads lived entirely in excluded scratch. The pinned probe was invoked with `PLAYWRIGHT_BROWSERS_PATH=test/scratch/pw-browsers` and `IMD_PLAYWRIGHT=test/scratch/browser-tools/node_modules/playwright/index.mjs`. Its final screenshots were inspected, including the complete first 390px screen. The primary CTA occupies x=20, y=459.25, width=204, height=50 in a 390×844 viewport. All required metadata is present; the remaining probe failure is its default-title regex matching **Home** in **Home · The Cheese Vault**, the same false positive identified by the reviewer. The title was preserved.

### Better Interface coverage for the revision

The pinned workflow and all six domains were read and applied to the changed surfaces. This is a scoped revision review, not a replacement of the accepted design.

| Domain | Checked and corrected | Limitations |
| --- | --- | --- |
| Accessibility | Native disabled amount/Max; keyboard path through review and Edit amount; focus restoration after dialog close; visible home CTA focus ring inspected; source status uses a stable status element and `aria-busy`; text accompanies status colors | No screen-reader session, native 200% zoom, physical touch device or WebKit verification |
| Layout | Five routes at five widths; 390px product/action visible; long evidence, dates and full addresses wrap; proof label/value stretching fixed and measured | Not every possible width or translated/RTL layout |
| Writing | Slogans 6 → 2; plain staking/15% fee explanation; exact required tagline retained; source unavailable explicitly differs from globally unverified; retry direction present | English only |
| Typography | Existing local fonts load in Chromium; scale retained; new evidence uses 14px role, full dates and normal casing; no clipped critical text in inspected proof cells | Native text-enlargement and other engines not checked |
| Colors | Existing tokens reused. Rendered proof secondary/surface ratio 5.332:1 and evidence-link/surface 11.672:1. Home probe passes measured contrast | Two home text boxes over art/gradients are excluded by the probe; disabled/alpha combinations not exhaustively measured |
| UI | Frozen transaction review, Edit amount refresh, checked/verified/unavailable source states, failed refresh clears positive status, source requests independent from protocol; native focus and pending controls; reduced-motion probe passes | Success-path wallets/verification are explicit fixtures; no real signatures, passkeys or transaction broadcasts |

### Live evidence and remaining limits

All five real Sourcify Contract Lookup requests on 2026-11-08 returned HTTP 404 with the correct Sepolia/address identity and `runtimeMatch: null` to the HTTP client; responses advertise CORS `*`. These dated observations are in the JSON evidence. In Chromium, the unmocked source requests instead failed with `net::ERR_EMPTY_RESPONSE`; the final Proof screenshot shows the resulting **Unavailable** state with its attempted observation time. Positive verification and successful refresh were tested with explicit response fixtures. Neither a missing Sourcify record nor a transport error means the source is unverified on Etherscan. The Etherscan token page returned HTTP 403 to the HTTP client and ERR_EMPTY_RESPONSE in Chromium, so its badge was not independently re-established here. The live API implementation follows [Sourcify’s documented Contract Lookup endpoint](https://docs.sourcify.dev/docs/api/).

The real browser page encountered external network errors; **zero script errors / missing local assets is not a claim of zero external request failures**. Layout checks explicitly simulated RPC outages; the transaction harness explicitly mocked wallet, protocol and source responses. Live chain readiness and signed Approve/Deposit/Withdraw/Claim remain unverified. WebKit was installed and launch attempted, but required system libraries including `libgtk-4.so.1` are absent. The task remains a static IPFS export with no credentials or backend; public pinning/CID assignment happens after submission.

The reproduced findings are fixed and the final source/export checks above passed. No `.git/`, `.github/`, environment files, assigned `node_modules/`, package manifests/lockfiles, or ignore files were changed. The earlier accepted-round record below is retained as history; its counts and browser limitations describe that earlier run, not this revision.

---

## Earlier accepted-round record

Date: 2026-11-08. This is the worker’s own evidence record, not an independent audit or network certification.

## Result and limits

The five-page dApp, source, lockfile, custom artwork and static IPFS export are implemented. Production build, TypeScript, integer/accounting tests, mocked UI interactions, official ABI integrity and relative export assets pass. **Rendered browser verification and real signed Sepolia transactions remain unperformed.** The public IPFS CID/URL is assigned by the delivery plane after submission, not by this worker.

Public RPC requests returned HTTP 403, with an independent Tenderly endpoint returning 429. All five supplied Etherscan pages returned 403. These responses say nothing about whether the contracts are deployed, verified, configured or activated. No live readiness, balances, Squeek height, mint totals, or receipt result was inferred from those failures. The app has live reads and honest loading/unavailable states; no mock data is included in the runtime.

The supplied browser tool was asked to open `https://imd-workspace.invalid/`; it failed before loading a page. An isolated Playwright installation and Chromium retry also exited before rendering. WebKit and Firefox could not be launched. No screenshot of the website, native browser observation, physical-device test or screen-reader session is claimed. The generated hero artwork itself was inspected locally; that is not a website screenshot.

## Commands and actual outcomes

| Check | Actual result |
| --- | --- |
| Node toolchain | `node --version`: v24.22.0 |
| Initial dependency installation | `npm install --no-audit --no-fund`: passed |
| Final lockfile/install consistency | `npm ci --dry-run --ignore-scripts ...`: exit 0; a dry run, not a new clean install |
| TypeScript | `npm run typecheck` / `tsc --noEmit`: exit 0 |
| Native core tests | `npm run test:core`: 33 passed, 0 failed; integer amounts, share offsets, fee caps/dust, readiness, calldata, simulation, gas and false-return approval |
| Frontend interactions | `npm run test:ui -- --reporter=verbose`: 24 passed, 0 failed; controlled JSDOM fixtures, not real transactions |
| Aggregate test entry | `npm test` runs core then UI; the final suites contain 57 cases total |
| Official ABI integrity | `npm run check:contracts`: exit 0; five unchanged ABIs; 22 calldata encode/decode round trips |
| Source provenance | All five ABI SHA-256 values separately matched raw files at official commit `69602c52b5d2edc4681c807a5b04517214d90241` |
| Production export | `npm run build`: exit 0; Vite 7.3.7 |
| Relative/static assets | `npm run check:export`: exit 0; 13 files, 3,707,888 bytes; required metadata present; all checked HTML/CSS local references resolve relatively |
| Source upload budget | `scripts/measure-bundle.py`: complete source/export measured in a disposable scratch Git repository; see `artifacts/bundle-budget.json` for exact final bytes and the 8,388,608-byte ceiling |
| Browser design probe | Exact pinned `taste.mjs --out test/scratch/taste` attempted; exit 2 before rendering; 0 measured checks and 0 screenshots. See `artifacts/taste-status.json` |
| Public evidence | Bounded requests to multiple independent public RPCs and all five Etherscan links; no chain evidence available. See `artifacts/network-status.json` |

The build’s remaining warning is a 729.39 kB main JavaScript chunk (209.28 kB gzip). It is a performance consideration, not a build failure. Assets, fonts, ABIs, wallet support and source have been retained. No dependency caches, npm archives, node_modules, source maps or submodules belong to the deliverable. The local bundle measurement does not guarantee provider network acceptance.

Earlier Vitest 3 runs completed assertions but stalled on worker shutdown. Upgrading to Vitest 5.1.0, declaring its test DOM dependency explicitly and cleaning mocks resolved that limitation; the final UI runner exits successfully. Core tests use Node’s native runner after compilation into disposable scratch. A forced-exit race was also caught and removed; the final harness waits for natural completion and fails unless all 33 expected core cases pass.

## Useful interaction coverage

`test/unit/ui.test.tsx` exercises:

- Home’s primary action navigating to Farm; all three pool controls and unconfigured sIMD state; all four How to Play steps; Portfolio with and without an account; proof job/source URLs, all five exact Sepolia contract links and six full-address copy controls.
- Named MetaMask and Rabby rows, generic injected-row suppression, Coinbase row, rejection/retry, wrong-network switching prompt, wallet popover Escape and focus restoration.
- Exact amount validation and Max shares, inactive rewards with permitted deposits, disabled unconfigured sIMD, exact approval before a separate deposit, native ETH calldata/value, claim recipient and shares-based withdrawals.
- Gross/fee/net preview, signature rejection, pending state before a receipt, successful and reverted receipts, completed bite only after a matching confirmed `Withdrawn` log, different-data replacement, and expired review rejection.

Fixtures supply connector lists, accounts, reads, wallet writes and receipts explicitly. No extension connection, passkey creation, private key, signature, transfer, live fork, or broadcast occurred. `test/core/` checks real source helpers and transaction plans with explicitly mocked RPC preflight where necessary. The live contract preview, not the test-side fee helper, supplies actual UI withdrawal amounts.

Transaction history is intentionally browser-local, scoped to account and Sepolia, with pending receipt reconciliation. Full cross-device history is linked on Etherscan. A replacement that happened while the page was closed may require checking that full history; the app does not invent a replacement result.

## Better Interface coverage across all six domains

| Domain | Checked evidence | Unperformed or not applicable |
| --- | --- | --- |
| Accessibility | Native buttons/anchors/labels, named copy/close controls, main landmark/skip link, alert/status text, amount-specific invalid state, native dialog implementation; JSDOM rejection, Escape and focus-restoration tests | Native focus trap/inert rendering, visible rings, screen reader, native 200% zoom, physical targets and real mobile sheets not verified |
| Layout | Source grids, shared edges, wrapping addresses/numbers, 1180/950/640/370px breakpoints; main phone action precedes art; decorative overflow clipped | 320/390/1440px screenshots, measured reflow/overlap, intermediate-width rendering and RTL mirror not verified |
| Writing | Action labels match methods; actual assets/shares are distinct; status and errors explain recovery; source verification separate; no APR/TVL fiction; explicit withdrawal fee and final-depositor exception | English only; localization not requested. First-screen rendered word count not measured |
| Typography | Two local variable fonts plus system code face; three used weights; six named size roles; tabular data, balanced headings, 65ch prose and 28px numeric input | Loaded font rendering, real wraps and native text enlargement not verified |
| Colors | Exact semantic tokens and nine declared opaque pairs calculated in `artifacts/declared-contrast.json`; all nine exceed 4.5:1 for normal text | Rendered/alpha/image/disabled pairs not measured. Dark theme not requested or implemented |
| UI | Shared surface/button/badge/state primitives; explicit 150ms transition properties; finite confirmed bite; reduced-motion rule disables animation; receipt and error states exercised in JSDOM | Native hover/pressed appearance, animation timing at 10% speed, reduced-motion rendering and native Safari not verified |

First screen at **390px**: the source puts the product name, four-word headline, plain description, wallet control and primary Explore Cheese Farm action before the 240px mobile illustration. This is implemented design intent, **not a screenshot-based pass**. Taste@1 has no measured score because its renderer could not launch. There are no fabricated screenshots or contrast claims.

## Findings fixed and rechecked

| Finding | Source location and initial issue | Correction and evidence |
| --- | --- | --- |
| HIGH: fee display lost precision | `src/components.tsx:190`, `src/TransactionModal.tsx:807`: compact formatting could hide low-order units in a consequential quote | Added `Amount exact` for fee/approval values and retained full bigint construction. Core precision/rounding cases and JSDOM fee/receipt cases pass |
| HIGH: different-data replacement could count as success | `src/TransactionModal.tsx:267`: a successful replacement receipt alone did not establish the original farm action | Separate repriced/replaced/cancelled handling; different-data replacement reports no original success and cannot play the bite. Explicit UI case passes |
| HIGH: bytecode truthiness | `src/contracts/read.ts:142`: an empty `0x` return must not mean deployed | Compare actual bytecode against `0x`, including undefined fallback. Source rechecked; live bytecode observation remains unavailable |
| MEDIUM: old review after wallet change | `src/TransactionModal.tsx:91`, `:213`: an asynchronous preflight could finish after identity changed | Reset unsigned review and check current address/chain before storing or sending it; preserve original submitted receipt watcher. Source reviewed; expired-review/wrong-chain cases pass; native account-change test remains unperformed |
| MEDIUM: refresh success copy overstated evidence | `src/TransactionModal.tsx:456`: receipt success does not guarantee the following RPC refresh succeeds | Neutral confirmation and instruction to check latest balances; real query invalidation remains after receipts. Confirmed/error UI paths pass |
| MEDIUM: decorative art could widen an intermediate viewport | `src/styles.css:494`: oversized hero art exceeded its column | Clip only its decorative container. Source fixed; actual intermediate viewport recheck remains unavailable |
| MEDIUM: generic errors marked the amount invalid | `src/TransactionModal.tsx:92`, `:579`: wallet rejection is not an invalid amount | Amount-specific invalid state and focus; rejection stays a recoverable transaction message. Precision/rejection tests pass |
| MEDIUM: wallet options lacked Escape dismissal | `src/wallet.tsx:52`: connected popover had no explicit keyboard dismissal | Escape and outside-pointer dismissal plus return focus. JSDOM keyboard/focus case passes |
| MEDIUM: false-return token approval | `src/contracts/transactions.ts:60`: an ERC20 can decline approval without reverting | Reject false simulation results before a signature; approval receipt copy describes the confirmed transaction and rechecks allowance for deposit. Dedicated native test passes |

`DESIGN.md` was written from final source tokens/components, with rendered limits stated. The Better Interface and Impeccable attribution/license texts are retained under `LICENSES/`.

## Completion

**Implementation and executable checks complete; rendered/live verification incomplete for the concrete tool/network reasons above.** Remaining manual checks are production rendering at phone/desktop widths, Chromium/WebKit console/resources and keyboard/zoom, real extension/mobile/Smart Wallet connections, and Approve/Deposit/Withdraw/Claim with actual Sepolia funds and confirmed receipts. No requirement needing a real wallet or public IPFS publication is represented by a mock or an invented URL.
