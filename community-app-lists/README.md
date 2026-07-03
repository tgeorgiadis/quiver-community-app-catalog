# Community app lists

This folder is the published catalog for [Quiver](https://github.com/tgeorgiadis/quiver). Quiver fetches the remote index on startup and subscribes to each list automatically.

## Index (`index.json`)

The index tells Quiver which topic lists exist and where to download them.

```json
{
  "version": 1,
  "lists": [
    {
      "id": "b4e8c2a1-3f5d-4e9b-8c7a-1d2e3f4a5b6c",
      "name": "N64 Recomp Games",
      "description": "N64 recompilation ports",
      "remoteLocation": "https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/community-app-lists/n64-recomp.json",
      "listVersion": "1.0.0"
    }
  ]
}
```

- **`id`** — stable GUID; never change after a list is published.
- **`remoteLocation`** — raw GitHub URL for the list JSON (required; no bundled `location` field).
- **`listVersion`** — semver for the list contents; bump when that list's apps change.
- **`version`** (top-level) — bump when you add, remove, or reorder lists in the index.

## List files

Each topic list is a separate JSON file:

| File | Contents |
|------|----------|
| `n64-recomp.json` | N64 recompilation ports |
| `harbour-master.json` | Harbour Masters decomp projects |
| `general.json` | Other community apps (decomps, recreations, non-N64 recomps) |

Format:

```json
{
  "version": "1.0.0",
  "apps": [
    {
      "name": "Example App",
      "repository": "org/repo",
      "folderName": "ExampleApp",
      "installPath": null,
      "appIconUrl": "https://example.com/icon.png",
      "preferredVersion": null,
      "tags": ["example"]
    }
  ]
}
```

Bump the list file's **`version`** whenever you add, remove, or edit entries in that file. Update the matching **`listVersion`** in `index.json` when you publish the change.

## Adding a new list

1. Create a new list JSON file in this folder.
2. Generate a new GUID for the list `id`.
3. Add an entry to `index.json` with `name`, `description`, `remoteLocation`, and `listVersion`.
4. Bump the index top-level **`version`**.
5. Commit and push to `main`.

## Contributing

Edit the list file that matches your app (or open a PR). Do not include user-local fields like `skippedUpdateVersion`.

Each app entry needs:

- `name` — display name
- `repository` — GitHub repo (`owner/name`)
- `folderName` — install folder under Quiver's Apps directory
- `appIconUrl` — icon URL (optional but recommended)
- `tags` — searchable tags (optional)
