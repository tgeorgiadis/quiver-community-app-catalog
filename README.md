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
| PC | `community-app-catalog/PC.json` |

Full base: `https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/community-app-catalog/`

## Repository layout

```
index.json                 # list registry (schema v2: GUIDs + remote URLs)
community-app-catalog/
  Nintendo.json
  PlayStation.json
  Xbox.json
  PC.json
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

1. Edit the relevant brand list under `community-app-catalog/` (Nintendo, PlayStation, Xbox, or PC).
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
| Brand list | `Nintendo.json`, `PlayStation.json`, `Xbox.json`, `PC.json` |

Rules:

- Use the brand display name in PascalCase (`Nintendo`, `PlayStation`, `Xbox`, `PC`).
- Filenames are case-sensitive in GitHub raw URLs — use the exact casing in `index.json` `remoteLocation` values.
- Do not rename `community-app-catalog/` itself; it is part of every remote list URL.

When adding a new list file, register it in `index.json` with a new GUID and `remoteLocation`, and set `name`, `description`, and `version` in the list file.

### App display `name`

Game title only (no type suffix, no project in brackets):

```
{Title}
```

Examples:

- `Banjo-Kazooie`
- `Super Mario 64`
- `Super Mario Bros. Remastered`

Do not put `(Decomp)`, `(Recomp)`, `(Recreation)`, or `(Port)` in `name`. Type is conveyed by tags.

### App `project` (required)

Team, port, author, or product attribution. Place directly below `name`. Every app must set `project` — it distinguishes ports of the same game and will drive future install folders:

```
{PascalCaseGameName}-{PascalCaseProject}
```

Example: `Bomberman64-RevoSucks` vs a second Bomberman 64 port under another creator.

```json
{
  "name": "Super Mario 64",
  "project": "Ghostship",
  "repository": "harbourmasters/ghostship",
  "folderName": "SuperMario64-Ghostship"
}
```

Choose `project` in this order:

1. **Distinct product / codename** that would not collide across forks of the same game (`Ship of Harkinian`, `Lighthouse`, `Unleashed Recompiled`, `SS Anne`, `REDRIVER2`).
2. **Owner / org / creator** when the README title is only `{Game}: Recompiled` (or similar) — e.g. `RevoSucks`, `Rainchus`, `sonicdcer`.
3. **Project-named org** when the org *is* the brand for that game (`BanjoRecomp`, `DinosaurPlanetRecomp`).

Avoid generic `{Game}: Recompiled` labels and repo slugs that only embed the game + `Recomp` (`BM64Recomp`, `MarioKart64Recomp`) — they are not unique if another port of the same game appears.

Examples:

| `name` | `project` |
|--------|-----------|
| Banjo-Kazooie | BanjoRecomp |
| Banjo-Kazooie | Lighthouse |
| Bomberman 64 | RevoSucks |
| Super Mario 64 | Ghostship |
| The Legend of Zelda: Ocarina of Time | Ship of Harkinian |
| Driver 2 | REDRIVER2 |

### App `tags`

Use this order (omit a slot when it does not apply):

1. **Type short** — `recomp` | `decomp` | `recreation`
2. **Console acronym** — see table below
3. **Project** — only if relevant (e.g. `harbour masters`)
4. **Series** — franchise/identity (e.g. `mario`, `zelda`, `sonic`)
5. **Brand** — `nintendo` | `playstation` | `xbox` (omit for PC; `pc` is already the console tag)
6. **Type long** — `recompilation` | `decompilation` | `recreation`
7. Any other useful tags after that

Console acronyms:

| Console | Tag |
|---------|-----|
| Nintendo Entertainment System | `nes` |
| Super Nintendo Entertainment System | `snes` |
| Nintendo 64 | `n64` |
| GameCube | `gcn` |
| Wii | `wii` |
| Game Boy | `gb` |
| Game Boy Color | `gbc` |
| Game Boy Advance | `gba` |
| PlayStation / PS1 | `ps1` |
| PlayStation 2 | `ps2` |
| Xbox | `xbox` |
| Xbox 360 | `x360` |
| PC | `pc` |

Do not also add long-form console aliases (`nintendo 64`, `playstation 1`, `gamecube`, `xbox 360`, `psx`, `gc`, etc.).

Examples:

```text
recomp, n64, banjo, nintendo, recompilation
decomp, n64, harbour masters, zelda, nintendo, decompilation
decomp, ps1, crash, playstation, decompilation
recomp, x360, sonic, xbox, recompilation
decomp, pc, oddworld, decompilation
recreation, nes, mario, nintendo, recreation
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
| PC | `PC.json` |
