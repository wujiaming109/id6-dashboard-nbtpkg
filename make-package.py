#!/usr/bin/env python3
"""Build the source folder of the NBTApps package from the upstream dashboard.zip.

    python3 make-package.py /path/to/nbtapps/headunit [--zip dashboard.zip] [--gateway 169.254.1.1]

It writes <out>/manifest.json and <out>/payload/<App>/... which `nbtpkg.py build` then takes.
Nothing is rebuilt: the plugin files are copied out of the zip with the modes it stores.
"""
import argparse
import json
import os
import shutil
import zipfile

APPS = ("BoostDeck", "EngineCodes", "MhdMaps", "ShiftDeck")
ID = "com.github.inotbarnacle.dashboard"
VERSION = "1.0.0"
NAME = "ID6 Dashboard (BoostDeck, ShiftDeck, EngineCodes, MhdMaps)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nbtapps", help="the headunit/ folder of a checkout of tom-pryor/nbtapps")
    ap.add_argument("--zip", default="dashboard.zip")
    ap.add_argument("--out", default="dashboard-pkg")
    ap.add_argument("--gateway", default="192.0.2.1",
                    help="the diagnostic gateway address put in each app's gateway-ip.txt")
    args = ap.parse_args()

    pay = os.path.join(args.out, "payload")
    shutil.rmtree(args.out, ignore_errors=True)
    os.makedirs(pay)

    files = []
    z = zipfile.ZipFile(args.zip)
    bad = z.testzip()
    if bad is not None:
        raise SystemExit("zip is corrupt at %s" % bad)

    for info in z.infolist():
        if not info.filename.startswith(tuple(a + "/" for a in APPS)):
            continue
        mode = (info.external_attr >> 16) & 0o777
        mode = 0o755 if mode == 0o755 else 0o644      # keep executables, normalise the rest
        dst = os.path.join(pay, info.filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with z.open(info) as f, open(dst, "wb") as g:
            g.write(f.read())
        os.chmod(dst, mode)
        files.append((info.filename, mode))

    # one gateway-ip.txt per app: a hook sees ${app}, ${data} and ${tmp}, never ${plugins},
    # so the address cannot be written at install time and has to be in the archive.
    for app in APPS:
        p = os.path.join(pay, app, "gateway-ip.txt")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(args.gateway + "\n")
        os.chmod(p, 0o644)
        files.append((app + "/gateway-ip.txt", 0o644))

    manifest = {
        "manifestVersion": 1,
        "id": ID,
        "name": NAME,
        "version": VERSION,
        "requires": {"agent": ">=1.2.0"},
        "install": {
            "files": [
                # "0644", not "644": the schema wants a leading zero
                {"src": "payload/" + rel, "dest": "${plugins}/" + rel, "mode": "%#05o" % mode}
                for rel, mode in sorted(files)
            ],
            "reboot": "hmi-restart",
        },
    }
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("%d files staged, %d install entries; gateway %s" %
          (len(files), len(manifest["install"]["files"]), args.gateway))


if __name__ == "__main__":
    main()
