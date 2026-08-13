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
