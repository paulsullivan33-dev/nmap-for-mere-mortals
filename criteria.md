# Writing Criteria

Every guide in this repo is written to the same
standard. If you're adding or editing a guide —
human or AI — hold it to these.

1. **Plain words, real ideas.** Simple language,
   never dumbed-down concepts. Explain jargon on
   first use; collect terms in the glossary.
2. **No hype.** No marketing adjectives, no
   "revolutionary," no promises about what
   something will do for the reader.
3. **Honest about limits.** Say what the thing
   *can't* do. State uncertainty instead of
   smoothing it over. Validation notes include
   what remains unverified.
4. **No invented numbers.** Benchmarks, defaults,
   and specs are either measured or qualified with
   "depends on your setup." If it wasn't tested,
   say so.
5. **Checkable.** Commands are meant to be run,
   with "Check:" blocks showing what success looks
   like. Sources are linked, not asserted.
6. **Respect the reader's setup.** Call out
   Windows/Mac/Linux differences. Don't assume a
   GPU, a budget, or prior experience.
7. **Safety isn't skipped.** Real risks get
   stated plainly, not buried.
8. **Scoped.** Each guide says what it covers and
   points elsewhere for the rest. No guide
   pretends to be the whole subject.
9. **Structure over prose.** Tables, before/after
   examples, symptom → fix. Scannable beats essay.

## Verification notes for this guide

Standard 3 and 4 applied to this guide,
specifically. The build machine ran Ubuntu
24.04 as root, with **Nmap 7.94SVN**
installed fresh for the build
(`apt-get install nmap`; the package
reported "7.94+git20230807"). Every quoted
output in the chapters is a capture from
that nmap, run against the shipped lab.
Working transcripts are kept with the
build (`nmap-lab/transcripts/`).

**The lab.** One shipped file,
`examples/lab_server.py`, stands up four
listeners: a web server on tcp/8080
(`LabHTTP/1.0`, one invented page), a
banner server on tcp/8022 that sends an
SSH-shaped greeting with no SSH behind
it, a chat greeter on tcp/8888, and a
UDP listener on udp/53535. tcp/59999
and udp/59998 are deliberately left
closed. The fixture was hardened during
the build after a real finding: its
first version let one abruptly-closed
connection kill the banner thread (a
client reset escaping its handler),
which showed up as an honest-looking
`closed` in a scan. The shipped version
shrugs off rude clients; the episode is
why the chapters say to check the lab
before doubting a scan.

**The sandbox, stated once.** The build
machine's runtime forbids sending raw
packets and UDP datagrams at the OS
level — reproduced independently of
nmap with a two-line Python program
(`sendto` → `Operation not permitted`)
and visible in nmap's own
`sendto in send_ip_packet_sd` errors.
Consequences, all captured rather than
hidden: the SYN scan cannot send its
knocks (its one-port attempt and a
full default scan both degrade to
`filtered` / errors), the UDP scan
receives nothing and cannot elicit an
ICMP unreachable, and OS detection's
probes never leave. Those three scan
types are therefore taught from their
real failure captures plus prose
descriptions of successful behaviour,
labelled as described wherever the
distinction matters. Version detection,
NSE scripts, host discovery, output
formats, and the firewall recipe are
unaffected — they ride ordinary
connections, and every one of their
captures is a success run.

**Verified by running, per chapter:**

- *Ch. 1:* `nmap --version` as printed
  by the freshly installed package;
  `lab_server.py --check` output as
  printed.
- *Ch. 2:* the default 1,000-port
  connect scan of localhost (three lab
  ports open, "997 closed" summarised);
  the four-port scan (59999 `closed` /
  `unknown`); the two closed ports
  wearing phone-book names (`22 ssh`,
  `80 http`) proving names are table
  lookups.
- *Ch. 3:* the `--reason` table
  (`syn-ack` ×3, `conn-refused`); the
  filtered state produced live — an
  iptables DROP rule on tcp/8888, the
  rescan (`filtered` / `no-response`,
  scan time 0.03s → 1.23s), the rule's
  removal, and the port's return to
  `open`; the UDP pair in
  `open|filtered` (from the ch. 6 run).
- *Ch. 4:* `--top-ports 10` finding
  none of the three running lab
  services; `-F` finding 8080 and 8888
  but not 8022 (8022 is not in the
  famous 100 — verified against the
  healthy lab, twice); the 8000-8100
  range (8022 and 8080 open, 99 closed
  summarised); `-p-` over all 65,535
  ports in 1.88s with the three lab
  ports open.
- *Ch. 5:* `-sn` on localhost;
  `-sn -n` over 127.0.0.0/24 reporting
  all 256 addresses up (the loopback
  stack answers for the whole range);
  `-sn` on the notional dead address
  127.0.0.99 reporting up for the same
  reason; `-Pn -sT -p 8080` on
  127.0.0.99 finding the lab web server
  (the fixture binds all local
  addresses); `-sn` on the machine's
  network address taking 13.00s.
- *Ch. 6:* connect-scan tables as
  cross-referenced; the SYN scan's
  failure captured twice (one port with
  `--reason`: sendto errors, then
  `filtered` / `no-response`; and the
  `-sV`-as-root run, where the implied
  SYN phase filtered all four lab
  ports); the UDP scan's two
  `open|filtered` verdicts with sendto
  errors; `-T4`'s table identical to
  the default template's on this
  target, in the same 0.03s.
- *Ch. 7:* `-sT -sV` over the lab:
  8022 upgraded to `ssh` "(protocol
  2.0)" with no product match, 8080's
  VERSION read as `LabHTTP/1.0` from
  its `Server:` header, 8888 as
  `sun-answerbook?`, three services
  "unrecognized despite returning
  data" with full SF fingerprints
  printed (the chapter quotes the
  table and characterises the blocks;
  the blocks themselves run to pages),
  total time 92.42s. `-sT -A` over
  8080+8022: version and script
  quarters worked (`http-server-header`
  among them), OS quarter printed its
  warnings and `No OS matches for
  host`, 98.63s total.
- *Ch. 8:* `--script-help banner`
  output (categories: discovery safe);
  `--script banner` returning both
  specimens' greetings and no line
  for the non-greeting web server;
  `--script http-title` returning
  "Lab Web - Specimen Page"; `-sC`
  running the default set, including
  `http-open-proxy`'s false-positive
  warning on the lab web server.
- *Ch. 9:* the `-oA` run leaving all
  three files; the `.gnmap` head
  including the command line in its
  header comment; the `.xml` head;
  `grep -c open` answering 1 (lines
  containing, not occurrences) and
  the awk field count answering 3.
- *Ch. 10:* the start/stop recipe —
  port 9000 `closed`, then a specimen
  web server started and `-sT -sV`
  reading `SimpleHTTPServer 0.6
  (Python 3.12.3)`, then the service
  stopped and 9000 `closed` again;
  the firewall recipe's four commands
  as printed in ch. 3's captures;
  the external-address scan reporting
  the lab ports open *and* 59999,
  443, and 12345 open (the sandbox
  fabric accepts every TCP connection
  to that interface — the chapter
  says so and builds the recipe on
  the disagreement).
- *Ch. 11:* every symptom from its
  chapter's capture: the firewall's
  selective `filtered`; the sendto
  wall behind a total one; the
  loopback census; the unprivileged
  SYN refusal printed by running
  nmap as user `nobody`
  ("You requested a scan type which
  requires root privileges.
  QUITTING!", exit 1); the `-O` run
  still retrying at 90 seconds and
  stopped by the harness timeout —
  the chapter says "stopped by hand,"
  which is what a timeout is.

**Capture hygiene (declared trims):**
scan headers (the "Starting Nmap"
line and report header) are cropped
from some later-chapter quotes where
the identical header appears earlier
in the guide, and the text says so or
shows the table only; the ch. 5 sweep
shows its first three reports and its
summary with the elision marked in
the text; sendto error blocks are
shown once in full-ish form (two
packets) and elsewhere cropped to one
line with "(further sendto errors
omitted)" or similar wording; the
`-sV` fingerprint blocks are
characterised, never retyped. No
output was completed, corrected, or
invented: where a capture surprised
the draft (the `-F` result, the
external address), the chapter was
rewritten to the capture.

**Documented-only (not run), and why:**

- *SYN, UDP, and OS detection
  succeeding.* The sandbox blocks the
  sends, so the successful tables
  cannot be captured here. Their
  behaviour is described from nmap's
  documentation and the failure
  captures' own contrast, and the
  chapters flag the joins.
- *A genuinely down host and
  `0 hosts up`.* Unproducible on
  loopback (the stack answers for
  every 127/8 address) and the only
  other local addresses are the
  sandbox fabric's, which are not the
  guide's to probe. Described, with
  the summary sentence quoted from
  nmap's documented output shape.
- *ARP-based discovery on a real
  LAN, and the home-LAN recipe's
  numbers.* The build machine has no
  Ethernet segment of neighbours.
  The recipe teaches the commands
  against the lab and tells the
  reader to substitute their own
  range; no neighbourhood was
  invented for it.
- *The combined states
  `unfiltered` and `closed|filtered`,*
  which belong to scan types outside
  the guide's scope; named with
  one-line meanings in ch. 3.
- *Timing templates `-T0`/`-T1`/
  `-T2`/`-T5`*, named with their
  designed delays; only `-T3`
  (default) and `-T4` were run —
  a `-T0` demonstration takes minutes
  per port by design, which is the
  point the chapter makes about it.
- *Windows and macOS nmap* are named
  (official builds exist; the
  connect family behaves the same);
  no non-Linux machine was available
  to the build.
- *Installation beyond the build
  machine's own* is the one command
  in ch. 1 — that one really was run,
  on a machine that an hour earlier
  had no nmap at all.

Specimen discipline, for the record:
every target scanned in this guide is
the machine the lab runs on —
localhost, its loopback range, and its
own network address. The sandbox
fabric's other endpoint was never
scanned, swept, or probed. The web
page, chat protocol, and banner are
inventions; the banner's SSH costume
is the guide's own specimen, disclosed
wherever it appears.
