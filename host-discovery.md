# Host Discovery

Before scanning ports, nmap answers a prior
question: is anything there at all? This
preliminary step is **host discovery** — a
few light probes whose only job is "up or
not." It matters because the default
behaviour leans on it: hosts discovery calls
down are skipped entirely, ports and all.
`-sn` runs discovery alone — the old "ping
scan" — and prints the census without
touching a single port:

```
$ nmap -sn 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up.
Nmap done: 1 IP address (1 host up) scanned in 0.00 seconds
```

## A sweep that found 256 computers on one machine

Discovery earns its keep over ranges. Watch
what it does with the whole localhost
neighbourhood (`-n` turns off name lookups,
which otherwise tax every address a DNS
round-trip):

```
$ nmap -sn -n 127.0.0.0/24
Nmap scan report for 127.0.0.0
Host is up.
Nmap scan report for 127.0.0.1
Host is up.
Nmap scan report for 127.0.0.2
Host is up.
... (253 further reports, every one "Host is up.")
Nmap done: 256 IP addresses (256 hosts up) scanned in 0.01 seconds
```

Two hundred fifty-six hosts, all up, on a
machine that is alone in the room. Not a
bug: the entire 127.0.0.0/8 range is
loopback — every one of those addresses is
this same machine wearing a different
number, so the machine's own network stack
answers every probe. The lesson generalises
past the joke: **"host is up" means
something answered**, and knowing *what*
answered is your job. On a real network the
answerer is the machine; in loopback land
it's always you.

That same fact springs the chapter's
second trap. 127.0.0.99 runs nothing and
belongs to nobody — and discovery refuses
to call it down, because the stack answers
for it:

```
$ nmap -sn -n 127.0.0.99
Nmap scan report for 127.0.0.99
Host is up.
```

…which is also why a `0 hosts up` result
cannot be produced inside this lab at all,
and this guide won't fake one: on a real
network it looks like the same report with
the summary changed — `0 hosts up` — and
no per-host table at all.

## Why a live host can look down

Discovery's default probes are an ICMP echo
(the classic ping) plus, with privileges, a
couple of bare TCP knocks on common ports.
Real machines defeat them innocently all
the time:

- Many systems and most firewalls **drop
  ICMP echo** by policy while serving TCP
  happily — the host is up and answering
  customers; it just doesn't answer *that*.
- A host behind a packet filter may drop
  discovery's TCP probes on ports it doesn't
  serve, looking down from nmap's chair
  while serving its real port.
- On a local Ethernet segment, discovery
  can use **ARP** — asking the segment
  itself "who has this address?" — which a
  machine on the segment cannot politely
  decline. This is why LAN sweeps are
  reliable in a way routed sweeps aren't:
  the ARP answer comes from the network
  layer below all that policy. (Named from
  nmap's documentation — the build machine
  has no Ethernet segment of neighbours to
  demonstrate against; its only segment is
  a two-address sandbox link.)

## -Pn: skip the census, knock anyway

`-Pn` tells nmap to treat every target as
up and go straight to the ports. Used
honestly, it is exactly the fix for the
host above that's alive but won't answer
discovery: you *know* the machine exists
(it's yours), so the census is ceremony.
Used lazily — pointed at a whole range on
the *hope* something's there — it makes
nmap knock on every port of every empty
address, slowly, and produce pages of
filtered nothing. The honest rule: `-Pn`
for hosts you already know, discovery for
hosts you're counting.

On the lab, `-Pn` plus a port scan aimed at
the nobody-home address underlines the
loopback lesson one last time — it "finds"
the lab web server at 127.0.0.99, because
the lab binds every local address, and on
loopback every local address is home:

```
$ nmap -Pn -sT -p 8080 127.0.0.99
Nmap scan report for 127.0.0.99
Host is up (0.00020s latency).

PORT     STATE SERVICE
8080/tcp open  http-proxy
```

Your own machine's second door behaves
more like a network target: discovery of
the build machine at its network address
took its time (the sandbox fabric answers
when it feels like it), a reminder that
even one host can cost seconds once a real
path is involved:

```
$ nmap -sn 198.19.0.2
Nmap scan report for 198.19.0.2
Host is up.
Nmap done: 1 IP address (1 host up) scanned in 13.00 seconds
```
