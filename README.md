# sabren/sixthdev

> A grab-bag archive of sabren's pre-2011 programming life: 822 files
> spanning DOS-era Turbo Pascal hobby code, the Python web-app frameworks
> and apps of the Cornerhost era, a piano-teaching program, a personal
> finance toolkit, and a shelf of projects marked `@dead` and `@gone`.
> Repo: https://github.com/sabren/sixthdev — 822 files, git history in
> this clone 2007-05-02 → 2011-03-03 (file contents reach back further:
> CVS `$Id$` tags from 2002–2006). **Keep.**

## What it is

`sixthdev` is not one project — it is the attic. The name itself is
unexplained in the repo (flagged as unverified below), and the tree reads
like several CVS checkouts swept into one git repo in 2007–2009, with a
final round of cleanups in 2011 (including a 2to3 pass, per the last
commit message "misc old changes (2to3, etc)").

The two biggest blocks:

- **pascal/** (~208 files) — DOS-era Turbo Pascal: `progs/` holds over a
  hundred small programs (`3D-THING.PAS`, `DRAGON.PAS`, `DOTH.PAS`,
  `DVORAK.PAS`, `FRCTL1.PAS`, `MUDSTUFF`-era experiments), `units/`
  holds reusable units (`GRAFX.PAS`, `SPRITES.PAS`, `MODEM.PAS`,
  `MUDSTUFF.PAS`, `SNDSTUFF.PAS`, `BGIFONT.PAS` — BGI graphics, modem
  and sound code), plus `inc/` and a `crap/` directory. This is hobby
  code from the pre-web era, preserved whole.
- **@dead/ and @gone/** — two shelves of retired work. `@gone/` holds the
  sabren Python web libraries: `weblib`, `strongbox`, `sixthday`,
  `zebra`, `platonic`, `arlo`, `pytypes`, `storage`, `sdunit`, `handy`
  — the stack the Cornerhost-era apps were built on (see
  `rantelope/INSTALL.txt`, which lists exactly these as prerequisites).
  `@dead/` holds retired applications: `zikeshop` (a shop, with admin,
  public, spec and test dirs), `zikebase`, `hotspring`, `zdc`,
  `lecter`, `payment`, `generic` (adminapp/userapp templates),
  `blogdrive`, `shipment`, `tourney`, `py3d`. Whether `@dead` vs
  `@gone` meant anything different is not recorded in the repo
  (flagged as unverified).

The standalone projects still standing in the tree:

- **turcanator/** — a piano-teaching program: takes a MIDI file, shows a
  piano roll, and gives visual feedback on whether you are playing the
  notes correctly. Python 2.4 + pygame, with a bundled MIDI module and a
  Win32 `pypm` module; "The main code is (c) 2006 Michal J Wallace.
  License: BSD style." Short one-voice MIDI files recommended.
- **planaconda/** and **crappyconda/** — two generations of the same
  idea. `planaconda/design.txt` ("PLANACONDA 1.0 DESIGN DOC") describes
  a node-based project outliner: a flat list of project nodes on the
  front page, node pages with children and history, add/edit and split
  pages. `crappyconda/` is the implementation attempt (`.app` files,
  `PlanSession.py`, `PlanacondaTest.py`, a `gui/` dir, an Xcode project,
  and `stories.txt` — a work log referencing `webappworkshop.com` docs
  and a `sixthdev.versionhost.com` CVS viewer).
- **rantelope/** — a blog engine on the sabren stack (arlo, pytypes,
  strongbox, weblib, storage, handy, sixthday, zebra): `blog.app`,
  `rantelope.app`, `search.app`, author/category/channel/story forms,
  RSS/Atom templates (`rss.zb`, `atom.zb`), and `rantelope.sql`.
- **ledger/** — personal finance tooling: QIF/OFX parsing
  (`parseqif.py`, `parseqfx.py`, `txt2qif.py`, `qif2led.py`),
  bank converters (`amex.py`, `bofaconvert.py`, `bankview.py`),
  reconciliation (`reconcile.el`, `ledger-entries.el`, `summary.py`,
  `unreconciled.py`), and a `cleared` directory.
- **gameworld/** — a multiplayer-game skeleton: `Actor.py`,
  `Avatar.py`, `Game.py`, `Map.py`, `Observable.py`, an `event.py`
  system, a `server/` dir, and `spec/` tests.
- **spingdom/** — a diagram-drawing library: `canvas.py`,
  `diagram.py`, `divided.py`, `drawn.py`, `lines.py`, `bmpshape.py`,
  `composit.py`, plus `wxdemo.py` and OpenGL helpers (`oglmisc.py`).
  (What "sping" means is not recorded in the repo — flagged as
  unverified.)
- **trailblazer/** — a small XML-driven document tool, documented in
  `bigpicture.txt`: "You take an xml file, turn it into a dom. If it
  says import, then you import that file too. Then you walk the tree,
  and you build a grove of output streams" declared with `<stream>`
  tags. Also `methodology.txt`, `benefits.txt`, `tribalhistory.txt`.
  (Note: this is a different "trailblazer" from the Team Trailblazer
  game team in `sabren/blaze` — the repo does not state any
  connection, and none is assumed here.)
- **buggernaut/** — a task tracker (`TrackerApp.py`, `Task.py`,
  `Area.py`, `tracker.app`, `buggernaut.sql`). The same project name
  appears as the standalone repo `sabren/buggernaut` (documented
  separately); the repo does not say which copy is canonical.
- **cvssh/** — a CVS-over-SSH helper (`cvssh.py`, `fake_client.py`,
  `fake_pserver.py`, `stub.py`); its `doc/changes.txt` runs
  0.1 → 0.2 in January 2002.
- **seismq/** — "sei's messaging queue": a simple SQLite-backed
  message queue (`seismq.py`, spec + test dirs). The spec says
  "sei's messaging queue" without expanding "sei" (flagged as
  unverified — same open question as in `sei-bin`).
- **timesheet/**, **ensemble/**, **scroller/**, **openeeg/** —
  smaller pieces: a timesheet app (`.app`/`.zb`/`.sql`), an
  ensemble test harness with Perl and Python child tests
  (`ensemble.py`, `ensemble.pl`, `PerlChildTest.pm`,
  `PythonChildTest.py`), a tiny scroller demo (`scroller.py` plus
  three sprite GIFs), and an openEEG biofeedback prototype
  (`proto.py`: "python prototype of a mind-mirror style biofeedback
  machine… this version still only graphs fake data").

## Tech stack

Mostly Python 2 (2.2–2.4 era: `print` statements, `Numeric`,
`pysqlite`/`MySQLdb`), plus Turbo Pascal, Perl, Emacs Lisp, and SQL.
Templating is the sabren `.zb`/`.app` system (zebra/weblib). Tests
exist in places (`spec/` dirs, `PlanacondaTest.py`) but there is no
single test runner or build — this is an archive, not a runnable
project.

## Inventory (highlights)

| Path | Contents |
|------|----------|
| `pascal/progs/`, `pascal/units/`, `pascal/inc/` | DOS-era Turbo Pascal programs and units (graphics, sound, modem, MUD) |
| `@gone/weblib`, `@gone/strongbox`, `@gone/sixthday`, `@gone/zebra`, `@gone/platonic`, `@gone/arlo`, `@gone/pytypes`, `@gone/storage` | The sabren Python web stack, retired |
| `@dead/zikeshop`, `@dead/zikebase`, `@dead/hotspring`, `@dead/zdc`, `@dead/lecter`, `@dead/payment`, `@dead/generic` | Retired applications |
| `turcanator/` | MIDI piano-roll piano teacher (Python/pygame, ©2006, BSD) |
| `planaconda/`, `crappyconda/` | Node-based project outliner: design doc + implementation attempt |
| `rantelope/` | Blog engine on the sabren stack (RSS/Atom, search) |
| `ledger/` | QIF/OFX parsing, bank converters, reconciliation |
| `gameworld/` | Multiplayer game skeleton (Actor/Avatar/Map/server) |
| `spingdom/` | Diagram-drawing library (canvas/diagram, wx + OpenGL demo) |
| `trailblazer/` | XML → output-streams document tool |
| `buggernaut/` | Task tracker (also exists as standalone repo `sabren/buggernaut`) |
| `cvssh/` | CVS-over-SSH helper (2002) |
| `seismq/` | SQLite message queue ("sei's messaging queue") |
| `timesheet/`, `ensemble/`, `scroller/`, `openeeg/` | Timesheet app, test harness, scroller demo, EEG biofeedback prototype |

## Surprising / notable

- **The whole sabren stack in one place:** `@gone/` is the library
  layer and `@dead/` the app layer of the same era — together with
  `cornerops-svn` (the Cornerhost control panel) and `sei-bin` (the
  sysadmin scripts), this repo completes the picture of how the
  Cornerhost-era operation was built.
- **turcanator is the most complete artifact here:** a working
  program with a README, a license note, and a clear purpose — the
  piano-roll idea predates the modern "learn piano by falling notes"
  apps by years.
- **ledger/ is personal infrastructure, not a product:** bank
  converters plus Emacs Lisp reconciliation is the same "automate my
  own life" instinct visible across the sabren repos.
- **No single README:** there is no top-level README at all. The
  per-project notes (`planaconda/design.txt`,
  `trailblazer/bigpicture.txt`, `turcanator/README.txt`,
  `rantelope/INSTALL.txt`, `seismq/spec/seismq.txt`) are the only
  maps, and several directories have none.
- No linked streams or videos found in the repo.

## Verdict

Keep. An archive of record: the DOS hobby code, the sabren web stack,
and the personal tools are all worth preserving as-is. Nothing here
needs to run again, but `turcanator/`, `ledger/`, and the
`@gone/` libraries are reference material, and the repo as a whole is
the backstory for the Cornerhost-era work documented in
`cornerops-svn.md` and `sei-bin.md`.

(Flagged as unverified: what "sixthdev" means, what distinguishes
`@dead` from `@gone`, what "sping" means, and what "sei" stands for
— none of these are explained anywhere in the repo.)
