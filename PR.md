# Add com.github.inotbarnacle.dashboard 1.0.0

This adds one community package: the four iDrive plugin apps from
[inotbarnacle/ID6_apps_prerelease](https://github.com/inotbarnacle/ID6_apps_prerelease)
(`packages/dashboard.zip`) packaged as an `.nbtpkg`.

## What it adds

- `packages/com.github.inotbarnacle.dashboard/listing.json`
- `packages/com.github.inotbarnacle.dashboard/author.pub`
- `packages/com.github.inotbarnacle.dashboard/versions/1.0.0.json`

Archive: `com.github.inotbarnacle.dashboard-1.0.0.nbtpkg`, 606,442 bytes,
SHA-256 `138e24d22e973149cbf57cd93da5e684e2005b74b11642313011989a0efce59f`,
built from `inotbarnacle/ID6_apps_prerelease` at `79001aaab9847bc8bd2a8494e1516298ab9a4de4`.

## What it places on the head unit

24 files under `${plugins}`, in four app folders — `BoostDeck/`, `ShiftDeck/`,
`EngineCodes/`, `MhdMaps/`. Each holds the plugin's `.manifest`, its `.xml`, its
`_ALL_Images.zip`, its `lib<Name>.so`, at least one `*-qnx` program, and one
`gateway-ip.txt`. File modes match the upstream zip: the `*-qnx` programs are 0755,
everything else 0644. Nothing outside `${plugins}` is touched, and there are no
hooks, no `settings` and no `logs`.

`install.reboot` is `hmi-restart`.

## iDrive plugin ids

Connector id **100** (BoostDeck), **102** (EngineCodes), **103** (MhdMaps),
**104** (ShiftDeck), all `Etch`. The manifests declare no focus id.
`https://catalogue.nbtapps.com/v1/hmi-ids.json` lists 17, 200, 210, 211 as taken as
connectors and 32752, 32753, 32754 as taken as focus ids, so these four are free.

## gateway-ip.txt

Each app's QNX program reaches the car through its own connection and reads the
diagnostic gateway address from `gateway-ip.txt` in its own folder. The upstream
package does not ship that file; its desktop installer writes it after installation.
An NBTApps package cannot: a hook sees `${app}`, `${data}` and `${tmp}`, not
`${plugins}`, so the address cannot be written at install time.

So the archive ships one `gateway-ip.txt` per app with the RFC 5737 documentation
address `192.0.2.1`. It is a valid address that nothing answers, so no app reaches
the car before the value is set, and setting it is a matter of rebuilding the package
as a new version. Whoever publishes the next version sets the real address in all
four files first.

## Checks run before opening this

```
tools/check.py --nbtapps ../nbtapps/headunit --offline
  2 package(s): 0 error(s), 3 notice(s)     (the notices are the fetches left out)
nbtpkg.py verify com.github.inotbarnacle.dashboard-1.0.0.nbtpkg --key author.pub
  signature ok, key 7e81 a1b3 e891 fe9f, flags needs-reboot
```

`url` is the release asset address of the archive; it has to be live before this is
merged, and the record pins the SHA-256 above.

## For review

The binaries are upstream's prebuilt output, not rebuilt here, and they only match
the one reference firmware and framework combination the upstream README documents.
They talk to the DME, EGS and DSC over HSFZ with MOST as a fallback, read and clear
fault codes, write MHD map slots, drive the exhaust flap, and switch AWD and RWD
(engine off). On a car with other firmware they may not match, and the upstream
`Check compatibility` step is not available through this channel.

One thing to settle first: the upstream repository declares no licence (`license:
null`), so its binaries are redistributed here only with the author's permission —
please say if you want that permission recorded in the pull request before this is
merged.
