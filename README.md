# The Cheese Vault

A React/TypeScript farming dApp for **Ethereum Sepolia (11155111)**. Custom hamster artwork, five hash-routed pages, real contract reads, EIP-6963 browser wallet discovery, mobile wallet links and Coinbase Wallet/Smart Wallet support. No API keys or backend are required.

**Tagline:** Stake Your Cheese. Let the Hamsters Work.

## Install, preview and rebuild

Use Node.js 22.12+ (Node 24 was used for this build).

```sh
npm ci
npm run dev
```

For the finished export:

```sh
npm run typecheck
npm run test:core
npm run test:ui
npm run check:contracts
npm run build
npm run check:export
npm run preview
```

`npm run preview` prints the local preview address. The app uses Vite `base: './'`, local fonts/images and `#/home`, `#/farm`, `#/portfolio`, `#/how-to-play`, `#/proof` routes. It works at an IPFS gateway subpath without server rewrites. Serve `dist/` over HTTP(S); opening `index.html` with `file://` does not support wallet and module behavior reliably.

The provided worker preview is `https://imd-workspace.invalid/`, a private preview of the current export, **not a public hosting URL**. Its supplied browser launcher failed before rendering during this run. See [actual validation results](VALIDATION.md), including the browser and network limitations.

## Checked delivery

- `npm run typecheck` and `npm run build` passed with exit 0.
- 33 native core tests and 24 JSDOM interaction tests passed. All five page routes, exact contract links, wallet rejection, approval, native deposit, share withdrawal, claim, fees and receipt-gated animation are covered with explicit fixtures. **These are not real transactions.**
- `npm run check:contracts` passed: five unchanged official ABIs and 22 calldata round trips. `npm run check:export` passed: 13 runtime files, 3,707,888 bytes, local assets and required metadata.
- `npm ci --dry-run --ignore-scripts` passed; package manifest and lockfile dependency sets match. The complete local source bundle is below 8 MiB; exact final measurement is in the named review artifacts.

The supplied and isolated browsers failed before rendering, so mobile screenshots, native focus/zoom and Chromium/WebKit behavior remain unverified. Public RPC/explorer requests returned 403/429; live readiness and signed wallet transactions could not be verified. UI status never substitutes fixtures or guesses for missing reads. The build emits a 729.39 kB main-chunk warning (209.28 kB gzip).

See [VALIDATION.md](VALIDATION.md) for all six design-review domains, findings/fixes, test scope and limits. Additional machine-readable review evidence is delivered under `artifacts/`.

## Delivery and IPFS

`dist/index.html` and all required runtime assets are included alongside complete source, lockfile, tests and documentation. The IdentityMD delivery plane pins the submitted export to IPFS and assigns the public preview URL after submission. No public CID or live public URL was issued inside this worker session; none is fabricated here.

To pin independently later, add the **contents of `dist/` as one directory** to your chosen IPFS pinning service or IPFS Desktop and retain its root directory CID. Pin that root recursively. Open its HTTPS gateway URL, retaining the final slash before hash routes. The production export is self-contained for UI assets; live chain reads and wallet services still require network access. See [IPFS’s static website guide](https://docs.ipfs.tech/how-to/websites-on-ipfs/single-page-website/).

## Connect a custom domain

After the published CID is available, use a domain you control:

1. Create a TXT record at `_dnslink.YOUR_DOMAIN` whose value is `dnslink=/ipfs/YOUR_PUBLISHED_DIRECTORY_CID`. These are instructions to replace with the actual domain and issued CID, not application configuration values.
2. Configure a DNSLink-capable HTTPS gateway or a host that supports your domain. Add the gateway/host’s prescribed CNAME or A/AAAA record and TLS configuration. DNSLink alone does not provision HTTPS or make an arbitrary gateway accept your hostname.
3. Verify the site and each hash route through the custom domain. Use an isolated HTTPS origin for wallet permissions and storage. Retest mobile “Open in” links on that origin.
4. For updates, keep the previous CID pinned for rollback, pin the new directory, then update the TXT record. Update `og:image` to an absolute HTTPS URL in `index.html` once the canonical domain exists and rebuild for the most reliable social unfurling.

Follow [IPFS’s current custom domains and DNSLink guide](https://docs.ipfs.tech/how-to/websites-on-ipfs/custom-domains/) for the DNS and gateway setup. No domain purchase or contract deployment is part of this source.

## Official deployment

| Contract | Sepolia address |
| --- | --- |
| CHEESE | `0x33a41a4093b1aadcce2f9e0dda53211ed91c3521` |
| Controller | `0xe06748177ad22d422e49cdb0982a5f932e46ee7d` |
| CHEESE Pool | `0xd460157324fe20eeb83f8255aca5d2f09f387f21` |
| ETH Pool | `0x8ab46e3c9d16c4ca3ee8a28648c5809142c48faa` |
| sIMD Pool | `0x222f1a83afc0e1abd9b37f004bed792e7c027d88` |

[Official Swarm job](https://explorer.imd.fun/jobs/3c7de646-4d13-45f5-ba32-3c57c559d8e8) · [Official source and ABIs](https://github.com/identity-md-launches/launch-3140-cheese-v2-official)

`src/contracts/abi/` contains the unmodified official JSON ABIs. `official/provenance.json` records the exact source commit and SHA-256 hashes, independently compared against the commit URLs during implementation. The Solidity files in `official/` are read-only source references for the frontend’s accounting choices, not a separate deployment project. No owner-only transactions are exposed.

## Contract behavior and readiness

- Public reads use viem with bounded fallback across the public Sepolia RPCs in `src/contracts/config.ts`. The chain ID is checked. Protocol values are read at a specific block, linked on the page; each pool and position is also read at a pinned block. Missing values are `—`, not fabricated zeros. Reads refresh every 30 seconds and after receipts. Retry controls are available.
- `controller.token`, token emission authority, pool controller, registration, allocation, activation, pause flags, completion, pending checkpoint and real sIMD `asset()` are inspected. Deployed code, source verification, configuration and activation are shown separately. Source verification says **Not checked** with direct Etherscan links; this static client does not guess explorer verification or imply an audit.
- Official source permits unregistered CHEESE/ETH deposits before activation. Those deposits are available when their real preconditions permit them, with a clear warning that they are not earning yet. Unconfigured sIMD deposits are **Coming soon**. Paused or unsynchronized deposits are blocked. Exit and claim availability is checked separately.
- The Home page reads `SqueekCore.state().blockHeight` from the address reported by the controller. Farm emission progress uses `fundedBlocks()`. Scheduled emission for the next farm block is `issued(b + 1) - issued(b)` at the last farm checkpoint, across all allocation points; it is not a promised pool payout or APR. The launch bonus is included by that function.
- Lifetime minted (`totalMinted`) is separate from circulating supply. Burns do not reopen the 2.1B lifetime mint cap. The initial tokenomics are 210M premint and 1.89B mining, with launch allocations 40/20/20/20. Current allocation uses live values; the Future Reserve stays unminted.

## Wallet and transaction flows

- MetaMask, Rabby and other EIP-1193 extensions are discovered by EIP-6963 and listed by name/icon. A generic “Browser wallet” row is shown only when no named extension is discovered. Mobile browsers without injection receive app-browser links. Coinbase Wallet/Smart Wallet uses its SDK. No WalletConnect relay/project ID, seed phrase or private key is requested.
- Wagmi handles reconnection, account changes and Sepolia switching/add-chain through the chain definition in viem. The connected control exposes Disconnect.
- Exact decimal parsing uses `bigint`. Excess decimal places are rejected before viem can round them. No floating point participates in approval, deposit or share calculations.
- ERC20 approval grants only the entered amount to that specific pool. Approval and deposit are separately reviewed and signed. ETH deposits call payable `deposit()` with native value and **no amount argument**. ETH Max reserves an estimated gas ceiling and is validated again before signing.
- Withdraw inputs are explicitly denominated in **internal shares**, with exact Max. The contract’s `previewWithdraw(shares)` supplies gross, net, retained and Treasury amounts in the actual asset. These are displayed at full precision. Withdrawals burn shares; reward claims call `claim(connectedAccount)` separately.
- The nominal bite is 15%: 85% user, up to 14% retained and at least 1% Treasury. Retention is capped by remaining stake. The final depositor sends the full fee plus residual virtual-offset dust to Treasury. Contract preview and receipt amounts take precedence over the illustrated nominal split.
- A preflight simulation and gas estimate precede wallet confirmation. The padded call gas ceiling is an estimate, with a 60-second review expiry; smart wallet overhead and the final fee are shown by the wallet. The withdrawal quote is checked again before signing. Chain state can still change before mining; these contracts have no minimum-payout parameter.
- A hash first means pending. Success requires a confirmed successful receipt; errors, rejection, timeout, cancellation and different-data replacement have distinct handling. Only a matching `Withdrawn` event on a confirmed successful receipt triggers the completed bite, using **receipt** amounts. Repricing is followed; a different-data replacement cannot count as the requested action.
- Portfolio keeps each asset separate. Transaction history covers submissions made in this browser, scoped to wallet and Sepolia, with local storage capped at 100 entries and reconciliation of pending receipts. Full, cross-device history is linked on Etherscan; this site does not pretend local history is a global index.

## Source map

- `src/App.tsx`: five pages, hash navigation, pool cards, portfolio and proof.
- `src/components.tsx`, `src/styles.css`: shared controls, modal, icons and design tokens.
- `src/wallet.tsx`, `src/wallet-config.ts`: wallet picker, deep links and wagmi setup.
- `src/contracts/`: addresses, exact ABIs, reads, transaction plans and integer helpers.
- `src/TransactionModal.tsx`, `src/history.ts`: review, signing, receipt flow and local history.
- `public/`: bundled original hero art, custom SVG artwork, wallet marks and fonts.
- `test/unit/` and `test/core/`: explicit mocked frontend tests and native Node integer/accounting tests. These do not broadcast.
- `DESIGN.md`, `VALIDATION.md`: implemented design and actual checks/limitations.

## Submission budget

The explicit `.gitignore` path budget excludes only `**/node_modules/`, `/test/scratch/`, `/.cache/`, `**/.npm/` and `**/*.tsbuildinfo`. These are generated dependency, test, cache or incremental compiler paths. `dist/` is deliberately **included**. There are no submodules, dependency archives, vendored registries or source maps in the production export. The local size check is recorded in validation; it does not guarantee the provider’s final network upload acceptance.

## Attribution

Hero art was generated specifically for this website. The logo, token illustrations, hamster and bite SVGs are original source artwork. Fredoka and Nunito Sans are bundled under the SIL Open Font License. Mobile wallet marks come from RainbowKit (MIT); Coinbase’s mark follows the pinned wallet guide. Lucide icons are used through the installed package. Design/review guidance is adapted from Jakub Krehel’s Better Interface (MIT) and Paul Bakaus’s Impeccable documentation guide (Apache-2.0), at the commits recorded in `LICENSES/NOTICE.md`. Required license texts are in `LICENSES/`.
