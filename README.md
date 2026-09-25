# Quiver Launcher Community App Catalog

Official community-maintained app catalog for [Quiver Launcher](https://github.com/tgeorgiadis/quiver-launcher).

Fresh Quiver Launcher installs discover these lists automatically via the remote index. Your local `apps.json` is your library; use **App Catalog → Review** to add apps from a list deliberately.

## Remote index

Quiver Launcher loads this URL on startup:

`https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/index.json`

The index points to four brand lists:

| List | File |
|------|------|
| Nintendo | `community-app-catalog/Nintendo.json` |
| PlayStation | `community-app-catalog/PlayStation.json` |
| Xbox | `community-app-catalog/Xbox.json` |
| Other Platforms | `community-app-catalog/OtherPlatforms.json` |

Full base: `https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/community-app-catalog/`

## Repository layout

```
index.json                 # list registry (schema v2: GUIDs + remote URLs)
community-app-catalog/
  Nintendo.json
  PlayStation.json
  Xbox.json
  OtherPlatforms.json
README.md
```

## Index and list format

**Index (`index.json`, schema version 2)** — registry only. Each list entry has:

- `id` — stable GUID (do not change after publish)
- `remoteLocation` — raw GitHub URL to the list file

List metadata (`name`, `description`, `version`) lives in the list file, not the index.

**List files (`community-app-catalog/*.json`)** — each file has:

- `name` — display name shown in Quiver Launcher
- `description` — short summary of the list
- `version` — semver string; bump when the list changes
- `apps` — array of app entries

When adding a new list file, add a matching entry to `index.json` with a new GUID and `remoteLocation`. Set `name`, `description`, and initial `version` in the list file itself.

## Updating the catalog

1. Edit the relevant brand list under `community-app-catalog/` (Nintendo, PlayStation, Xbox, or Other Platforms).
2. Bump that list's `"version"` string (semver recommended).
3. Commit and push to `main`.

Quiver Launcher compares each list's `"version"` on refresh and shows **Review changes** when a list differs from the last acknowledged version.

Pull requests run JSON validation automatically. The check rejects invalid JSON, duplicate object keys, tabs, odd indentation, and trailing whitespace. Changed JSON files are also checked with Prettier.

To format JSON locally, run:

```sh
npx --yes prettier@3.5.3 --write index.json community-app-catalog/*.json
```

## Contributing

Open a pull request with your app entry in the appropriate brand list file and a version bump. Each app needs:

- `name` — display name
- `repository` — GitHub repo (`owner/name`)
- `folderName` — install folder under Quiver Launcher's Apps directory
- `appIconUrl` — icon URL (optional but recommended)
- `tags` — searchable tags in the order below (recommended)

Do not include user-local fields like `installPath`, `preferredVersion`, or `skippedUpdateVersion`.

## Naming conventions

### List files (`community-app-catalog/*.json`)

Each file is one catalog list, organized by brand:

| Pattern | Example |
|---------|---------|
| Brand list | `Nintendo.json`, `PlayStation.json`, `Xbox.json`, `OtherPlatforms.json` |

Rules:

- Use the brand display name in PascalCase (`Nintendo`, `PlayStation`, `Xbox`, `OtherPlatforms`).
- Filenames are case-sensitive in GitHub raw URLs — use the exact casing in `index.json` `remoteLocation` values.
- Do not rename `community-app-catalog/` itself; it is part of every remote list URL.

When adding a new list file, register it in `index.json` with a new GUID and `remoteLocation`, and set `name`, `description`, and `version` in the list file.

### App display `name`

Game title only:

```
{Title}
```

Examples:

- `Banjo-Kazooie`
- `Super Mario 64`

Do not put `(Decomp)`, `(Recomp)`, `(Recreation)`, or `(Port)` in `name`. Type is conveyed by tags.

For a recreation that is clearly a distinct take on the game (not a straight port/decomp), put the distinguishing label in square brackets:

```
{Title} [{Distinct recreation label}]
```

Example: `Super Mario 64 [Co-op DX]`, `The Legend of Zelda: Link's Awakening DX [HD Updated]`.

Do not use `[brackets]` for ordinary decomp/recomp project names — those belong in `project` (e.g. Ship of Harkinian, Lighthouse).

### App `project` (required)

Team, port, author, or product attribution. Place directly below `name`. Every app must set `project` — it feeds install folders:

```
{PascalCase(name)}-{PascalCase(project)}
```

Prefer a clear product or README title when one exists (`Ship of Harkinian`, `Unleashed Recompiled`, `Banjo: Recompiled`, `SS Anne`). Creator/org names are fine too if it is a better fit for the project.

Uniqueness across future alternate ports of the same game is not required up front — when a second port is added later, give *that* entry a distinct `project` (and `folderName`) then.

```json
{
  "name": "Super Mario 64",
  "project": "Ghostship",
  "repository": "harbourmasters/ghostship",
  "folderName": "SuperMario64-Ghostship"
}
```

Examples:

| `name` | `project` |
|--------|-----------|
| Banjo-Kazooie | Banjo: Recompiled |
| Banjo-Kazooie | Lighthouse |
| Bomberman 64 | Bomberman 64: Recompiled |
| Super Mario 64 | Ghostship |
| The Legend of Zelda: Ocarina of Time | Ship of Harkinian |
| Driver 2 | REDRIVER2 |

### App `tags`

Use this order (omit a slot when it does not apply):

1. **Type** — `recomp` | `decomp` | `recreation` (use `recreation` only once, at the start — there is no separate long form)
2. **Console acronym(s)** — one or more from the table below
3. **Project** — only if relevant (e.g. `harbour masters`)
4. **Series** — franchise/identity (e.g. `mario`, `zelda`, `sonic`)
5. **Brand** — `nintendo` | `playstation` | `xbox` (omit for Other Platforms when the console tag already covers it, e.g. `pc`)
6. **Full console name(s)** — lowercase long form matching each acronym (see table); omit when it would duplicate the acronym (`wii`, `pc`, `mobile`)
7. **Type long** — `recompilation` | `decompilation` only (not used for recreations)
8. Any other useful tags after that

Multiple console tags are allowed when the game spans platforms or a platform has alternate names (e.g. `gen` + `smd`, or `mobile` + `gen`). Put matching acronyms together after the type tag, and their full names together after brand (same order).

Console tags:

| Console | Acronym | Full name tag |
|---------|---------|---------------|
| Nintendo Entertainment System | `nes` | `nintendo entertainment system` |
| Super Nintendo Entertainment System | `snes` | `super nintendo entertainment system` |
| Nintendo 64 | `n64` | `nintendo 64` |
| GameCube | `gcn` | `gamecube` |
| Wii | `wii` | *(omit — same as acronym)* |
| Game Boy | `gb` | `game boy` |
| Game Boy Color | `gbc` | `game boy color` |
| Game Boy Advance | `gba` | `game boy advance` |
| PlayStation / PS1 | `ps1` | `playstation 1` |
| PlayStation 2 | `ps2` | `playstation 2` |
| Xbox | `xbox` | *(omit — same as acronym; use as brand)* |
| Xbox 360 | `x360` | `xbox 360` |
| Sega Mega Drive | `smd` | `sega mega drive` |
| Sega Genesis | `gen` | `sega genesis` |
| PC | `pc` | *(omit — same as acronym)* |

Do not use alternate console spellings (`psx`, `gc`, etc.) — stick to the acronym and full-name columns above.

Examples:

```text
recomp, n64, banjo, nintendo, nintendo 64, recompilation
decomp, n64, harbour masters, zelda, nintendo, nintendo 64, decompilation
decomp, ps1, crash, playstation, playstation 1, decompilation
recomp, x360, sonic, xbox, xbox 360, recompilation
decomp, pc, oddworld, decompilation
recreation, nes, mario, nintendo, nintendo entertainment system
decomp, mobile, gen, smd, sonic, sega genesis, sega mega drive, decompilation
```

### App `folderName`

Install folder under Quiver Launcher's Apps directory:

```
{PascalCase(name)}-{PascalCase(project)}
```

No `Recomp` / `Decomp` / `Recreation` / `Port` suffix — uniqueness comes from `project`.

PascalCase each side as follows:

1. Remove apostrophes (`Majora's` → `Majoras`).
2. Split on remaining non-alphanumeric characters (spaces, `:`, `-`, `.`, etc.).
3. Uppercase the first character of each token; preserve the rest of the token’s casing.
4. Concatenate tokens with no separators.

Examples:

| `name` | `project` | `folderName` |
|--------|-----------|--------------|
| Banjo-Kazooie | BanjoRecomp | `BanjoKazooie-BanjoRecomp` |
| Banjo-Kazooie | Lighthouse | `BanjoKazooie-Lighthouse` |
| Castlevania: Legacy of Darkness | fliperama86 | `CastlevaniaLegacyOfDarkness-Fliperama86` |
| Super Mario 64 | Ghostship | `SuperMario64-Ghostship` |
| The Legend of Zelda: Ocarina of Time | Ship of Harkinian | `TheLegendOfZeldaOcarinaOfTime-ShipOfHarkinian` |
| Pokemon Stadium | SS Anne | `PokemonStadium-SSAnne` |
| Driver 2 | REDRIVER2 | `Driver2-REDRIVER2` |
| Oddworld: Abe's Oddysee and Abe's Exoddus | R.E.L.I.V.E. | `OddworldAbesOddyseeAndAbesExoddus-RELIVE` |

Rules:

- Keep names filesystem-safe: letters and digits only in each segment; single `-` between name and project.
- Must be unique across the catalog.

### Choosing a list file

| App type | List file |
|----------|-----------|
| Nintendo platforms (N64, SNES, GB, GBA, GCN, Wii, NES, etc.) | `Nintendo.json` |
| PlayStation platforms (PSX, PS2, etc.) | `PlayStation.json` |
| Xbox platforms (Xbox 360, etc.) | `Xbox.json` |
| PC, Sega, mobile, and other non-brand lists | `OtherPlatforms.json` |


## Catalog release batches

App-addition PRs preserve list versions. After they merge, **Prepare catalog
release** opens or updates one **Release catalog updates** PR. Merge that PR
manually when the batch is ready; each changed list gets one patch bump, regardless
of how many apps were added. The release PR is intentionally refreshed while open,
so review its latest diff before merging. App proposal branches remain immutable.

`.github/catalog-release-state.json` records the contents last covered by a version.
The workflow updates that record in the release PR, never directly on main. It
ignores formatting-only changes and content already recorded by a release PR.
Avoid manual bumps: a legacy app PR that still bumps its version may receive one
additional bump in the next release, ensuring later app changes are signalled too.
Do not manually edit the release state. The initial state represents the catalogs
at setup time.

Catalog files on main still become publicly readable as soon as app PRs merge;
batching the version bump is an update signal, not a staging or access boundary.
The platform-metadata publisher continues running unchanged.

The release workflow uses only this repository's short-lived `GITHUB_TOKEN` with
contents/PR write access. It never uses either Discord GitHub App or their keys,
pushes main, approves PRs, or merges PRs. Enable **Allow GitHub Actions to create
and approve pull requests** in repository Actions settings to allow PR creation;
the workflow does not exercise approval permission. GitHub may ask you to approve
validation workflows on a bot-created release PR before checks can run.

Existing JSON validation allows app additions with unchanged versions. Release validation checks PRs
against current main for only the expected version bumps and release state. Update
a stale release by running **Prepare catalog release** on main again; do not merge
it with failing checks. Use branch protection requiring current checks if you want
GitHub to enforce that policy. Disabling this workflow stops release preparation;
`workflow_dispatch` on main retries a failed run. No new long-lived secrets are needed.

## Shared platform metadata

`platform-index.json` is generated browsing metadata for community catalogs. The
optional `platformMetadataUrl` in `index.json` lets newer launchers load platform
coverage in one request. Older launchers ignore it. App entries and catalog review
versions do not change when the index is refreshed.

The **Publish platform metadata** workflow runs on catalog edits, manual dispatch,
and at 00:17, 06:17, 12:17 and 18:17 UTC. It uses the repository-scoped GitHub Actions
token and the launcher generator pinned to a full commit SHA in the workflow.
Scheduled runs may be delayed or disabled by GitHub; timestamps describe the last
successful check, not a guaranteed service interval.

Do not hand-edit asset lists. Selection uses the launcher's Core release logic,
including preferred releases and fallback from assetless/auxiliary-only releases.
Entries include provider, normalized repository, preferred release, chosen tag,
asset names, validation time and selection revision. The launcher applies each
app's asset filter and platform policy; downloads resolve releases independently.

Failed individual checks retain their previous successful entries and are listed
in the workflow summary. Complete generation failures retain the previous file.
Publication is validated before an atomic Git commit and never force-pushes.
Missing metadata stays unverified in the launcher and can be checked explicitly.
A successfully checked release with no usable assets is a valid empty result.

To update the generator, validate its regression tests and generated output first,
then replace the pinned commit SHA. Publish an initial compatible index before
releasing a launcher that consumes a new format or selection revision.


### Website catalog identity

New website-generated proposals may include an optional `catalogId`, a stable ID
issued by the **production Quiver Launcher website**. It identifies this particular
catalog entry (not every game or port sharing a repository). Existing entries do
not need an ID; this change does not require a backfill.

Do not invent or copy IDs from a development deployment. Validation rejects test
IDs, duplicate IDs, and IDs whose production repository/provider/install-folder
binding differs from the proposed entry. Website entries remain drafts until their
catalog PR is manually merged and its contents verified.

The catalog validator checks that website-generated IDs use the production `qcat_`
UUID format and are unique across the catalog. Issuance and entry binding remain
owned by the production Convex website; the catalog workflow does not need website
credentials, an Actions variable, or a network lookup. Legacy entries without IDs
remain valid.
