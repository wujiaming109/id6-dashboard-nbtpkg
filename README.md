# id6-dashboard-nbtpkg

An `.nbtpkg` for the [NBTApps](https://github.com/tom-pryor/nbtapps) agent that installs the four
iDrive plugin apps of [inotbarnacle/ID6_apps_prerelease](https://github.com/inotbarnacle/ID6_apps_prerelease)
(on a BMW NBT Evo / iDrive 6 head unit).

The archive is kept in this repository (`com.github.inotbarnacle.dashboard-1.0.0.nbtpkg`, raw URL
`https://github.com/wujiaming109/id6-dashboard-nbtpkg/raw/main/com.github.inotbarnacle.dashboard-1.0.0.nbtpkg`).
The record that lists it is submitted to
[tom-pryor/nbtapps-packages](https://github.com/tom-pryor/nbtapps-packages).

## Credit and attribution

**The four apps are not mine.** Every plugin binary, image archive, XML, `.manifest` and shared
library in this package was written and built by **inotbarnacle**, the author of
[inotbarnacle/ID6_apps_prerelease](https://github.com/inotbarnacle/ID6_apps_prerelease), and is
redistributed here unmodified, taken from that repository at commit
`79001aaab9847bc8bd2a8494e1516298ab9a4de4` (`packages/dashboard.zip`, 435,355 bytes).

| App | What it is upstream | Connector id | Upstream files | All by |
|---|---|---|---|---|
| `BoostDeck/` | Boost controller plugin | 100 (Etch) | 5 | inotbarnacle |
| `EngineCodes/` | fault code reader / clearer plugin | 102 (Etch) | 5 | inotbarnacle |
| `MhdMaps/` | MHD map slot writer plugin | 103 (Etch) | 6 | inotbarnacle |
| `ShiftDeck/` | shift / gearbox plugin | 104 (Etch) | 5 | inotbarnacle |

What this repository did add is packaging only: `manifest.json`, the `install.files` table that
gives each upstream file a destination and a mode, one `gateway-ip.txt` per app, `make-package.py`
and this README. No authorship is claimed over the app code itself, and none of it was rebuilt, patched
or recompiled — the files are byte for byte the upstream ones, with the upstream modes preserved (the
`*-qnx` programs are 0755; `libShiftDeck.so` is 0755 upstream and stays so; everything else 0644).

Questions and bug reports about how an app behaves belong upstream, in the
[issue tracker of `inotbarnacle/ID6_apps_prerelease`](https://github.com/inotbarnacle/ID6_apps_prerelease/issues).
Problems with the packaging — the manifest, the file layout under `${plugins}`, `gateway-ip.txt`,
signing — belong here.

Packaged for the NBTApps agent by [wujiaming109](https://github.com/wujiaming109). This packaging
is not made, reviewed or endorsed by the NBTApps project or by the upstream author.

## The archive

| | |
|---|---|
| id | `com.github.inotbarnacle.dashboard` |
| version | `1.0.0` |
| file | `com.github.inotbarnacle.dashboard-1.0.0.nbtpkg` |
| size | 606,442 bytes |
| SHA-256 | `138e24d22e973149cbf57cd93da5e684e2005b74b11642313011989a0efce59f` |
| manifest SHA-256 | `7cd4d834d5e37dd4e95f65a43d1529f6b284c6c1e24a69c2db3065bed5da4f07` |
| signing key | Ed25519, fingerprint `7e81 a1b3 e891 fe9f` |
| flags | `needs-reboot` |

It installs 25 files into `${plugins}`, in four folders: `BoostDeck/`, `ShiftDeck/`, `EngineCodes/`
and `MhdMaps/`. Each holds the plugin's `.manifest`, its `.xml`, its `_ALL_Images.zip`, its
`lib<Name>.so`, at least one `*-qnx` program, and one `gateway-ip.txt`. Connector ids 100, 102, 103
and 104 (Etch); no focus id. Nothing outside `${plugins}` is touched, and there are no hooks, no
`settings` and no `logs`.

## Provenance

Built from `inotbarnacle/ID6_apps_prerelease` at commit
`79001aaab9847bc8bd2a8494e1516298ab9a4de4`, file `packages/dashboard.zip` (435,355 bytes, its own
inner `SHA256SUMS` verified).

Nothing was rebuilt. The 21 files of the four app folders are byte for byte the upstream zip's,
and their modes are preserved. What this packaging adds is `manifest.json`, the `install.files`
entries that name a mode and a destination for each file, and one `gateway-ip.txt` per app — 4 files,
25 entries in total.

## Why `gateway-ip.txt` holds `192.0.2.1`

Each app's QNX program reaches the car over its own connection and reads the diagnostic gateway
address from `gateway-ip.txt` in its own folder. The upstream package does not ship that file; its
desktop installer writes it after installation, from the address it discovers.

An NBTApps package cannot do that. A hook sees `NBT_APP_DIR` (`${app}`), `NBT_DATA_DIR` (`${data}`)
and `NBT_TMP_DIR` (`${tmp}`) — there is no variable for `${plugins}`, so the address cannot be written
at install time. It has to be in the archive.

So the archive ships the RFC 5737 documentation address `192.0.2.1`. Nothing answers it, which is
the point: no app reaches the car before the value is set. To set it, put the car's real diagnostic
gateway address in all four files and build a new version — see below.

## Building a new version

The package is built and verified with the tools of the NBTApps repository, which needs python3 and
the `cryptography` module:

```
git clone --depth 1 https://github.com/tom-pryor/nbtapps
cd nbtapps/headunit

mkdir -p work/keys work/out
python3 tools/nbtpkg.py keygen dashboard work/keys/dashboard      # once; keep the .key out of any repo
python3 tools/nbtpkg.py build work/dashboard-pkg --key work/keys/dashboard.key -o work/out
python3 tools/nbtpkg.py verify work/out/com.github.inotbarnacle.dashboard-<version>.nbtpkg \
        --key work/keys/dashboard.pub
```

`work/dashboard-pkg/` holds `manifest.json` and `payload/`. `make-package.py` in this repository
generates both from an upstream `dashboard.zip`; set `GATEWAY` there to the real address.

A new version is a new version number and a new record. A published version never changes.

## The head unit it is for

The upstream programs were built for one reference firmware and framework combination, and only that
one. On another firmware they may not match, and the upstream `Check compatibility` step is not
available through this channel: an `.nbtpkg` install does not check firmware.

The apps talk to the DME, EGS and DSC over HSFZ with MOST as the fallback, read and clear fault
codes, write MHD map slots, drive the exhaust flap and run max cooling. xDrive Control switches AWD
and RWD and requires the engine to be off. This is a `needs-reboot` install: the head unit restarts
when it completes.

## Licence

Upstream declares no licence (`license: null`), which means the author reserves all rights: nothing
here grants you a licence to the app code, and the binaries are redistributed in this repository only
on the understanding that the author permits it. If the author objects, the archive, this repository
and the directory submission are withdrawn on request. Copyright in everything under the four app
folders stays with inotbarnacle.

The `manifest.json`, the `gateway-ip.txt` handling, `make-package.py` and the text written for this
packaging are this repository's own.

A package that installs an `.nbtpkg` receives full access to a car's head unit; read the upstream
documentation before you install it.
