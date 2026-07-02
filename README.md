# Quiver Community App Catalog

Official community-maintained app catalog for [Quiver](https://github.com/tgeorgiadis/quiver).

Fresh Quiver installs subscribe to this list automatically as **Quiver Community App Catalog**. Your local `apps.json` is your library; use **App Catalog → Review** to add apps from this catalog deliberately.

## Catalog file

- **File:** [`quiver-community-apps-catalog.json`](quiver-community-apps-catalog.json)
- **Raw URL:** `https://raw.githubusercontent.com/tgeorgiadis/quiver-community-app-catalog/main/quiver-community-apps-catalog.json`

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

## Updating the catalog

1. Edit `quiver-community-apps-catalog.json`.
2. Bump the top-level **`version`** string whenever entries change (semver recommended).
3. Commit and push to `main`.

Quiver compares `version` on refresh and shows **Review changes** when it differs from the last acknowledged version.

## Contributing

Open a pull request with your app entry and a version bump. Each app needs:

- `name` — display name
- `repository` — GitHub repo (`owner/name`)
- `folderName` — install folder under Quiver's Apps directory
- `appIconUrl` — icon URL (optional but recommended)
- `tags` — searchable tags (optional)

Do not include user-local fields like `skippedUpdateVersion`.
