# Nmap for Mere Mortals

**Nmap** is the command line's way of
asking a machine what it's listening to:
one tool, thirty years old and free, that
knocks on ports and reports — carefully,
and with its evidence showing if you ask —
what answered, what refused, and what
stayed silent. It answers the four
questions every mortal with a server asks
sooner or later: what's on my network,
what is this machine exposing, did my
service actually start, and is the
firewall doing what I think it is.

The rule of this guide is stated in its
first chapter and repeated until it's
reflex: **only scan machines and networks
you own, or that you have explicit
permission to scan.** Everything here is
practised on a lab — four small specimen
listeners in `examples/lab_server.py` that
you stand up on your own machine — so the
rule costs nothing to keep. One specimen
wears a costume (an SSH banner with no
SSH behind it), one is a web server with
an invented page, one is a chat greeter
no phone book knows, and two ports are
deliberately left closed, because a
genuine "closed" is a lesson too.

A note on how this guide was verified.
Nmap 7.94SVN was installed fresh on the
build machine (`apt-get install nmap`)
and every scan quoted was run against
the lab above and captured: the report
tables, the reasons, the firewall
before-and-after, the 256-host loopback
census, version detection taking the
costume half off, and the scripts. The
build machine lives in a restrictive
sandbox, and the guide keeps the
receipts: the sandbox refuses to send
raw packets or UDP at all, so the
privileged scan types — SYN, UDP, OS
detection — appear here as their real
failure modes (the error text, the wall
of `filtered`, the `open|filtered`
shrug), with their successful behaviour
described and labelled as described.
That turns out to be a feature: each of
those failures is one a mortal will meet
in containers and locked-down
environments, and chapter 11 is built
from them. `criteria.md` keeps the full
ledger of what was run and what was
only described.

## What this guide covers

- [**What nmap is**](what-nmap-is.md) —
  the four questions, the permission rule,
  what nmap is not, and the lab
- [**First scans**](first-scans.md) —
  the connect scan, reading a report line
  by line, and why the service column is
  a phone book
- [**Port states, honestly**](port-states.md) —
  open, closed, filtered, and the combined
  states; what each one proves, and
  `--reason` as the evidence column
- [**Choosing ports**](choosing-ports.md) —
  lists, ranges, the famous 1,000,
  `--top-ports`, `-F`, and all 65,535
- [**Host discovery**](host-discovery.md) —
  the census, `-sn`, the sweep that found
  256 computers on one machine, and `-Pn`
  used honestly
- [**Scan types**](scan-types.md) —
  connect versus SYN (what differs on the
  wire and in the logs), UDP's fog and its
  timing, and timing templates as manners
- [**Service and OS detection**](service-and-os-detection.md) —
  `-sV` asking the ports themselves,
  fingerprints for the unrecognized, and
  `-O`/`-A` with their honesty warnings
- [**Scripts**](scripts-nse.md) — the NSE,
  categories as the safety story, `banner`
  and `http-title` on the lab, and `-sC`
- [**Output that lasts**](output-that-lasts.md) —
  `-oA`'s three shapes, and feeding scans
  to grep and awk
- [**Recipes**](recipes.md) — did it
  start, did the firewall rule work,
  what's on my network, and scanning
  yourself from the network side
- [**Troubleshooting**](troubleshooting.md) —
  everything filtered, the down host that
  isn't, privilege errors, slow scans, and
  UDP's identical shrug
- [**Glossary**](glossary.md) — the terms,
  collected in one place

## What it doesn't cover

Scanning other people's networks — not a
technique gap, the whole point of the
rule. The remaining scan types (ACK,
window, idle, FTP bounce) beyond naming
the states they produce; evasion and
spoofing (`-D`, `-S`, fragmentation),
which exist to mislead and belong to
another shelf; Zenmap and other front
ends; writing NSE scripts (using them is
chapter 8's whole job); and IPv6 beyond
a mention — the lab is IPv4, and the
build machine's IPv6 story is its
sandbox's, not yours.

## How to use this guide

Read chapter 1, start the lab
(`python3 examples/lab_server.py`,
in its own terminal), and keep a second
terminal open from chapter 2 on — every
scan is aimed at the machine you're
sitting on. Keep the lab afterwards:
a server whose answers you *know* is a
standing rehearsal for the day a real
one's scan comes back strange.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Netcat for Mere Mortals](https://paulsullivan33-dev.github.io/netcat-for-mere-mortals/)
- [tcpdump for Mere Mortals](https://paulsullivan33-dev.github.io/tcpdump-for-mere-mortals/)
- [Wireshark for Mere Mortals](https://paulsullivan33-dev.github.io/wireshark-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/nmap-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/nmap-for-mere-mortals/blob/main/LICENSE-CODE).
