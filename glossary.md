# Glossary

**ARP** — Address Resolution Protocol.
On a local Ethernet segment, the way to
ask "who has this address?" — the network
layer below IP. Discovery on a segment
can rely on it because a machine on the
segment can't easily decline to answer
for itself.

**banner** — The greeting some services
send the moment a connection opens: a
line of text naming (or claiming) the
service and sometimes its version. The
NSE `banner` script fetches one verbatim.

**closed** — Port state: the host
answered and refused the connection —
nothing listens there. A fast, positive
"no" from the machine itself.

**connect scan (`-sT`)** — A scan that
asks the operating system to make
ordinary connections. Needs no
privileges, works anywhere, and is
logged by every service it reaches.

**filtered** — Port state: the knock got
no answer at all — typically because a
firewall dropped the packet or the
reply. Silence with several possible
authors; chapter 3 lists them.

**fingerprint (OS / service)** — The
pattern of a target's replies to
carefully chosen probes, matched against
nmap's databases to guess an operating
system or identify a service. A guess
with a database behind it, still a
guess.

**grepable output (`-oG`)** — The
one-line-per-host output format designed
to be processed by other text tools.
`-oA` writes it alongside the normal
and XML formats.

**handshake (TCP)** — The three-step
opening of every TCP connection: SYN,
SYN-ACK, ACK. A connect scan performs
it in full; a SYN scan stops after the
second step and resets.

**host discovery** — The preliminary
"is anything there?" step before port
scanning; `-sn` runs it alone. `-Pn`
skips it and treats every target as up.

**ICMP** — The network's own signalling
protocol: ping is an ICMP echo, and a
closed UDP port is betrayed by an ICMP
"port unreachable" from the host.

**latency** — In nmap's reports, how
long the target's answers took to come
back. A tenth of a millisecond means
"same machine"; large values mean a
long or congested path.

**NSE** — The Nmap Scripting Engine:
hundreds of Lua scripts shipped with
nmap that converse with open ports —
grabbing banners, reading web titles,
testing behaviours. Each carries
categories (`safe`, `vuln`, …) that
state its manners.

**open** — Port state: something
accepted the connection. Proves a
program listened, at that moment, for
that caller — not its identity, which
version detection investigates.

**open|filtered** — The combined state
UDP scans return when silence could
mean either a listening-but-quiet
service or a dropped packet. UDP's
honest shrug.

**port** — A numbered door on a machine:
65,535 possible TCP ports and the same
for UDP, each the address of at most
one listening program per protocol.

**probe (version)** — One of the
requests `-sV` sends to an open port —
an opener or a shaped oddity — to see
what the service does with it.
Replies, matched against fingerprints,
produce the VERSION column.

**raw socket** — The OS facility for
hand-built packets, needed by the SYN
and UDP scans and by OS detection.
Restricted to root or CAP_NET_RAW, and
withheld entirely by some sandboxes —
to all accounts alike.

**reason (`--reason`)** — The flag that
makes nmap print the evidence behind
each state: `syn-ack` for an open,
`conn-refused` for a closed,
`no-response` for a filtered.

**service column / phone book** — The
SERVICE name in a report comes from
nmap's table of customary tenants for a
port number, printed whether or not
anything listens. A first guess, never
a conclusion.

**SYN scan (`-sS`)** — The half-open
scan: a hand-built SYN, a verdict from
the reply, and a reset instead of a
completed connection. Quieter in the
target's logs; needs raw sockets.

**timing template (`-T0`…`-T5`)** —
Nmap's dial for how hard a scan leans:
parallelism, waits, retries. `-T3` is
the default, `-T4` the everyday
briskness, `-T0`/` -T1` the polite
crawl.

**UDP scan (`-sU`)** — Scanning UDP
ports with small datagrams and inferred
answers: a reply means open, an ICMP
unreachable means closed, silence means
`open|filtered`. Slow by nature; keep
its port lists short.
