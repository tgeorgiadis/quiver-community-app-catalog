# Quiver Community App Catalog

Official community-maintained app catalog for [Quiver](https://github.com/tgeorgiadis/quiver).

Fresh Quiver installs discover these lists automatically via the remote index. Your local `apps.json` is your library; use **App Catalog → Review** to add apps from a list deliberately.

## Remote index

Quiver loads this URL on startup:

`https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/community-app-lists/index.json`

The index points to three topic lists:

| List | Raw URL |
|------|---------|
| N64 Recomp Games | `.../community-app-lists/n64-recomp.json` |
| Harbour Master Projects | `.../community-app-lists/harbour-master.json` |
| Community Apps | `.../community-app-lists/general.json` |

Full base: `https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/community-app-lists/`

## Repository layout

```
community-app-lists/
  index.json           # list registry (GUIDs + remote URLs)
  n64-recomp.json      # N64 recompilation ports
  harbour-master.json  # Harbour Masters decomp projects
  general.json         # other community apps
  README.md            # maintainer docs for this folder
```

See [`community-app-lists/README.md`](community-app-lists/README.md) for index format, list format, and version bump rules.

## Updating the catalog

1. Edit the relevant list file under `community-app-lists/`.
2. Bump that list's `"version"` string (semver recommended).
3. Update the matching `"listVersion"` in `index.json` if needed.
4. Commit and push to `main`.

Quiver compares list versions on refresh and shows **Review changes** when a list differs from the last acknowledged version.

## Contributing

Open a pull request with your app entry in the appropriate list file and a version bump. Each app needs:

- `name` — display name
- `repository` — GitHub repo (`owner/name`)
- `folderName` — install folder under Quiver's Apps directory
- `appIconUrl` — icon URL (optional but recommended)
- `tags` — searchable tags (optional)

Do not include user-local fields like `skippedUpdateVersion`.

## Legacy monolithic catalog

The old single-file catalog (`quiver-community-apps-catalog.json`) has been removed. If you subscribed to that URL manually, remove it in Quiver and rely on the default remote index flow instead.
