# Fact check

Every rule in the guide was checked on 30 October 2026 against four sources:

- the voting platform, https://redbelly-governance.vercel.app (pages, the Details tab, the Wallet safety page, and the site's own API)
- Redbelly Access, https://access.redbelly.network (the verification flow and its FAQ)
- the Redbelly docs, https://vine.redbelly.network/identity/user-access/
- the Redbelly chain itself, through the public RPC at https://governors.mainnet.redbelly.network (chain ID 151)

This file lists each rule, where it comes from, and how to check it again. Every interface message the guide quotes was found word for word on the live platform on the same day.

## How to repeat the checks

The platform answers two public API calls that show exactly what the voting panel sees:

    curl "https://redbelly-governance.vercel.app/api/identity?address=<wallet>"
    curl "https://redbelly-governance.vercel.app/api/power?proposal=<proposal id>&voter=<wallet>"

Proposal data, including the snapshot block and the list of votes:

    curl "https://redbelly-governance.vercel.app/api/proposals/<proposal id>"

The proposal used as the example throughout is the Proposal Resubmission Policy, id `f832b2b9-18fd-4d65-967d-0a85b89a500e`.

## 01 Getting verified

| Rule in the guide | Source and evidence |
|---|---|
| Only verified wallets can vote. | New proposal form: "Only wallets holding a Receptor credential can vote, as Redbelly requires one for network access." The form publishes every proposal with `requireVerified` set to true on mainnet. The API shows `"require_verified": true` on every proposal published since the identity check went live. |
| You verify on Redbelly Access, not on the voting site, and it costs nothing. | Platform notice: "Complete identity verification and enable this wallet at access.redbelly.network". Access FAQ: "the accredited issuer that verifies your identity will cover any associated fees required to grant your network access." |
| Connect MetaMask or Coinbase Wallet. That address becomes your public address. | Access FAQ: "MetaMask and Coinbase Wallet can be used to get access." Access page: "the account(s) you use to connect will become your public address(es) on Redbelly Network." |
| Averer, the accredited issuer, checks you're a real person using your passport. | Access FAQ: "Your identity will be verified by an accredited issuer, Averer." Redbelly docs: a "valid photo identity document (passport) which is verified via biometric checks". Platform: "passport-backed identity check". |
| The wallet gets the Redbelly Network Access Credential, which the voting site calls a Receptor credential. | Access FAQ: "issuing your account the Redbelly Network Access Credential". Platform: a Receptor credential is the one "Redbelly requires for network access". Receptor is Redbelly's identity protocol (vine.redbelly.network/identity/receptor/). |
| You sign one transaction, and the issuer covers the fees. | Access: "Check your wallet to sign the transaction that will enable your account." Access: issuers "provide accounts with the funds required to enable them with network access." |
| You can link extra wallets to the same identity. A wallet belongs to one identity at a time. | Access FAQ: "you will be offered the option to add more accounts which will be connected to your identity." Access messages: "This wallet address is already linked to a different DID" and "Linking your wallet to this account will unlink it from its previously associated account". |

## 02 Casting a vote

| Rule in the guide | Source and evidence |
|---|---|
| Open a proposal under Active and select Connect wallet. A browser wallet or a phone wallet through WalletConnect both work. | Proposals page has an Active tab. In a browser without a wallet extension, Connect wallet opens a WalletConnect window: "Scan this QR Code with your phone". |
| The panel says Eligible to vote and shows your voting power. A reason is optional. | Voting panel text: "Eligible to vote", "Your voting power", "Reason (optional)". |
| Select Review and sign, then approve the signature. No gas. | Voting panel: "Review and sign", "Confirm the signature request in your wallet.", "Signing costs no gas. Your signature proves the vote is yours." |
| Your vote appears in the Votes list. An IPFS receipt follows, and the vote counts before it shows. | Voting panel: "Your signature was received. Recording your vote..." then the ballot is added to Votes. "IPFS receipt not available yet. Your vote is recorded." |
| While voting is open you can use Change vote. After it closes, no changes. | The vote button reads "Change vote" once you have voted. After the end time: "Voting has closed." |
| The message you sign is named Redbelly Governance and lists your address, the proposal, your choice as option numbers and your reason. No amount, no recipient. | Wallet safety page shows the signed structure: domain name "Redbelly Governance", chain ID 151, fields from, space, proposal, choice, reason, timestamp. The platform writes the choice as the option number, so Yes on a Yes/No/Abstain vote is signed as 1. |
| A real vote never asks for approve / permit, setApprovalForAll, transfer / send, or a gas fee. | Wallet safety page, "What this site will never ask for", with the same meanings the guide gives. |

## 03 Eligibility and the snapshot block

| Rule in the guide | Source and evidence |
|---|---|
| Every proposal has a snapshot block, shown on its Details tab. | Details tab, "Snapshot block". The Resubmission Policy shows 3208192, and the API returns `"snapshot_block": 3208192`. |
| The snapshot is recorded when the proposal is published, just before voting opens. | Block 3208192 has the chain timestamp 06:47:23 UTC on 30 September 2026, and the API shows voting opened at 06:49:45. A second proposal shows the same pattern: snapshot block 3163674 at 10:32:40 UTC on 2 September, voting opened at 10:35:01. Block times come from `eth_getBlockByNumber` on the RPC above. |
| Your wallet is judged at that block only. A wallet verified after the proposal opens can't vote on it, even if it is verified now. | Platform text: "Voting eligibility is determined at each proposal's snapshot" and "Eligibility is based on the proposal snapshot. Changes after that snapshot do not add voting power." Live test below. |
| RBNT that arrives mid-vote doesn't count. | Platform: "Voting power equals the native RBNT held at the snapshot block." |
| The panel messages and what they mean. | All four quoted messages appear on the platform word for word. The test below shows which one a late-verified wallet sees. |

### Live test: a wallet verified two minutes after voting opened

1. The platform checks wallets against the contract `0xcb385cD90ca6b219798F57B4a7958897e91A9163`, a proxy whose implementation exposes `isAllowed(address)`. Read its events from block 3208192 onward with `eth_getLogs`. The first wallet added after the snapshot appears in block 3208195, timestamp 06:51:55 UTC, about two minutes after voting opened.
2. Call `isAllowed` (selector `0xbabcc539`) for that wallet with `eth_call`. At block 3208192 it returns false. At block 3208195 and at the latest block it returns true.
3. `/api/identity` for that wallet returns `{"verified":true,"chainId":151}`.
4. `/api/power` for that wallet on the Resubmission Policy returns `{"power":0,"blocked":true,"unavailable":"This proposal is open to identity-verified wallets only. This address does not hold a Receptor credential on Redbelly."}`

So the wallet is verified today and still not eligible for a proposal whose snapshot came first, and the panel shows the Receptor credential message. That is why the guide explains that message the way it does.

## 04 Counting

| Rule in the guide | Source and evidence |
|---|---|
| The author picks the counting method, and it can't change once the proposal is live. | New proposal form: "a proposal cannot be edited once it is open". |
| The voting system shows under the title. The strategy is on the Details tab. | Proposal header, for example "Single choice · Verified wallets only". Details tab rows "Voting system" and "Strategy". |
| One verified address, one vote: every wallet verified at the snapshot gets one vote. | Platform: "Every identity-verified address gets exactly one vote regardless of holdings." `/api/power` on the Resubmission Policy for any wallet in its Votes list returns `{"power":1,"strategy":"verified-identity","snapshotBlock":3208192}`. |
| RBNT balance: power is the RBNT held at the snapshot block. | Platform: "Voting power equals the native RBNT held at the snapshot block." On the signalling vote `1a8c56fa-00f2-4454-aa5e-932f6299d662`, `/api/power` for a wallet in its Votes list returns the same figure the Votes list shows in its POWER column (319.07 for one of them). |
| A third strategy counts another token instead of RBNT. | New proposal form: "Voting power equals an ERC-20 balance at the snapshot block." |
| The voting systems and what each does. | New proposal form descriptions for Single choice, Approval, Weighted, Quadratic, Ranked choice, Copeland and "One verified address, one vote". |
| One identity can have up to 10 wallets in total. At 10, Access shows "Account allocation exhausted". | Redbelly Access, Accounts page ("Manage your Redbelly Network Accounts"). Once an identity has 10 accounts, the "Add another account" button is hidden and "Account allocation exhausted." is shown. In the portal's code the check is the account list length against `Number("10")`, in `/_next/static/chunks/pages/index-25986869981a8ae9.js`. The voting platform gives the same figure: "One credential currently enables up to about 10 addresses". |
| The platform counts verified addresses, not people, and doesn't merge linked wallets. | Platform: "Verified addresses are not necessarily unique people." and "Multiple addresses may belong to one person." |
| Quorum and identity quorum. Missing either closes the proposal as No quorum. | New proposal form: "Quorum (0 for none)", "Identity quorum (0 for none)", "Distinct verified voters who must take part, however much weight they carry." The results panel shows "No quorum" when either is missed, as on the High Council test election `0cd19281-a2f1-4eb5-9dc4-22f37ec1bf7c`. |
| Balance-weighted votes also show a one-per-address tally that decides nothing. | Results panel on balance-weighted, verified-only proposals: "Advisory, and decides nothing. Every verified address counts once here, regardless of holdings." |
| A wallet that isn't verified at all is refused. | `/api/power` on the Resubmission Policy for `0x000000000000000000000000000000000000dEaD` returns `"blocked":true` with the Receptor credential message, and `/api/identity` returns `"verified":false`. |

## 05 Known limits

| Limit in the guide | Source |
|---|---|
| A verified address isn't always a different person. | "Verified addresses are not necessarily unique people." and the 10-address figure above. |
| Late verification can't catch a live vote. | Live test in section 03. |
| Balances freeze at the snapshot. | "Changes after that snapshot do not add voting power." |
| One big holder can meet a power quorum alone. | New proposal form: "A power quorum can be met by one large holder alone; this cannot." The identity quorum is optional: "Identity quorum (0 for none)". |
| Live proposals can't be edited. | "a proposal cannot be edited once it is open". |
| Old results came from Snapshot. | Proposals marked imported carry a note that they came from the DAO's Snapshot space and were not signed on this portal. |

## Diagrams

Fig 1 and Fig 2, and their portrait versions for phones, show only the rules above. Both carry the date they were last verified. The block number in Fig 2 is the Resubmission Policy's real snapshot block.

## Not independently confirmed

- **The 10-wallet limit on chain.** The limit is confirmed in the Access portal and matches the voting platform's figure. The contract that grants network access has no published source, so the limit could not also be read from the chain.
- **The practice panel** in chapter 02 is modelled on the real voting panel and uses a past proposal as its example. Its status labels are part of the guide's design, not text from the platform.
