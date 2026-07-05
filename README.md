# Quiver Community App Catalog

Official community-maintained app catalog for [Quiver](https://github.com/tgeorgiadis/quiver).

Fresh Quiver installs discover these lists automatically via the remote index. Your local `apps.json` is your library; use **App Catalog → Review** to add apps from a list deliberately.

## Remote index

Quiver loads this URL on startup:

`https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/index.json`

The index points to nine topic lists:

| List | File |
|------|------|
| N64 Recomps | `community-app-catalog/N64-Recomps.json` |
| N64 Decomps (Harbour Masters) | `community-app-catalog/N64-Decomps-HarbourMasters.json` |
| N64 Decomps | `community-app-catalog/N64-Decomps.json` |
| SNES Decomps | `community-app-catalog/SNES-Decomps.json` |
| GBA Decomps | `community-app-catalog/GBA-Decomps.json` |
| GCN Decomps | `community-app-catalog/GCN-Decomps.json` |
| PSX Decomps | `community-app-catalog/PSX-Decomps.json` |
| X360 Recomps | `community-app-catalog/X360-Recomps.json` |
| General Game Recreations | `community-app-catalog/General-Game-Recreations.json` |

Full base: `https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/community-app-catalog/`

## Repository layout

```
index.json                 # list registry (schema v2: GUIDs + remote URLs)
community-app-catalog/
  N64-Recomps.json
  N64-Decomps-HarbourMasters.json
  N64-Decomps.json
  SNES-Decomps.json
  GBA-Decomps.json
  GCN-Decomps.json
  PSX-Decomps.json
  X360-Recomps.json
  General-Game-Recreations.json
README.md
```

## Index and list format

**Index (`index.json`, schema version 2)** — registry only. Each list entry has:

- `id` — stable GUID (do not change after publish)
- `remoteLocation` — raw GitHub URL to the list file

List metadata (`name`, `description`, `version`) lives in the list file, not the index.

**List files (`community-app-catalog/*.json`)** — each file has:

- `name` — display name shown in Quiver
- `description` — short summary of the list
- `version` — semver string; bump when the list changes
- `apps` — array of app entries

When adding a new list file, add a matching entry to `index.json` with a new GUID and `remoteLocation`. Set `name`, `description`, and initial `version` in the list file itself.

## Updating the catalog

1. Edit the relevant list file under `community-app-catalog/` (pick the platform or topic that matches the app; use `General-Game-Recreations.json` for cross-platform recreations).
2. Bump that list's `"version"` string (semver recommended).
3. Commit and push to `main`.

Quiver compares each list's `"version"` on refresh and shows **Review changes** when a list differs from the last acknowledged version.

## Contributing

Open a pull request with your app entry in the appropriate list file and a version bump. Each app needs:

- `name` — display name
- `repository` — GitHub repo (`owner/name`)
- `folderName` — install folder under Quiver's Apps directory
- `appIconUrl` — icon URL (optional but recommended)
- `tags` — searchable tags (optional)

Do not include user-local fields like `installPath`, `preferredVersion`, or `skippedUpdateVersion`.

## Naming conventions

### List files (`community-app-catalog/*.json`)

Each file is one catalog list. Use PascalCase segments separated by hyphens:

```
{PlatformOrTopic}-{Recomps|Decomps|...}.json
```

| Pattern | Example |
|---------|---------|
| Platform recomp list | `N64-Recomps.json`, `X360-Recomps.json` |
| Platform decomp list | `SNES-Decomps.json`, `PSX-Decomps.json`, `GCN-Decomps.json` |
| Platform decomp with qualifier | `N64-Decomps-HarbourMasters.json` |
| Cross-platform / topic list | `General-Game-Recreations.json` |

Rules:

- Use platform shorthand with no spaces (`N64`, `SNES`, `GBA`, `PSX`, `GCN`, `X360`).
- Match the suffix to the list content (`Recomps` vs `Decomps`).
- Filenames are case-sensitive in GitHub raw URLs — use the exact casing in `index.json` `remoteLocation` values.
- Do not rename `community-app-catalog/` itself; it is part of every remote list URL.

When adding a new list file, register it in `index.json` with a new GUID and `remoteLocation`, and set `name`, `description`, and `version` in the list file.

### App display `name`

Human-readable title shown in Quiver:

```
{Title} [{Optional project name}] ({Recomp|Decomp|Recreation})
```

Examples:

- `Banjo-Kazooie (Recomp)`
- `Super Mario 64 [Ghostship] (Decomp)`
- `Super Mario Bros. Remastered (Recreation)`

### App `folderName`

Install folder under Quiver's Apps directory. Use PascalCase with no spaces:

```
{GameTitle}[-{VariantOrProjectName}]-{Recomp|Decomp|Recreation}
```

Examples:

| `name` | `folderName` |
|--------|--------------|
| Banjo-Kazooie (Recomp) | `BanjoKazooie-Recomp` |
| Super Mario 64 [Ghostship] (Decomp) | `SuperMario64-Ghostship-Decomp` |
| The Legend of Zelda: Ocarina of Time [Ship of Harkinian] (Decomp) | `LegendOfZeldaOcarinaOfTime-ShipOfHarkinian-Decomp` |
| Super Mario Bros. Remastered (Recreation) | `SuperMarioBrosRemastered-Recreation` |

Rules:

- Strip punctuation from the title portion (no `:`, `'`, `.`, or `-` inside the title).
- Suffix reflects the project type (`Recomp`, `Decomp`, or `Recreation`), not necessarily the list filename.
- Add a middle segment when the display name includes a project in `[brackets]` (e.g. `[REDRIVER2]` → `-REDRIVER2`).
- Keep names filesystem-safe: no spaces or slashes.

### Choosing a list file

| App type | List file |
|----------|-----------|
| N64 recompilation | `N64-Recomps.json` |
| N64 decomp (Harbour Masters) | `N64-Decomps-HarbourMasters.json` |
| N64 decomp (other) | `N64-Decomps.json` |
| Other platform decomp/recomp | matching `{Platform}-Decomps.json` or `{Platform}-Recomps.json` |
| Cross-platform recreation | `General-Game-Recreations.json` |