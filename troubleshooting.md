# Troubleshooting

Five symptoms, each reproduced on the
build machine while this guide was being
written, with the cause each turned out
to have. Several are the same symptom —
that is rather the point of the chapter.

## Everything is filtered

A wall of `filtered` says knocking isn't
producing answers. It has at least three
causes, and the scan alone can't rank
them:

- **A firewall is dropping.** Real and
  common — chapter 3 made one on purpose:
  one iptables DROP rule turned exactly
  the chat port `filtered` / `no-response`
  while its neighbours stayed open. The
  signature of an honest firewall is
  selectivity: *some* ports answer.
- **The scanner can't send.** When a
  privileged scan type's packets are
  forbidden by the environment — a
  container without CAP_NET_RAW, a
  sandbox like the build machine's —
  nmap prints `sendto ... Operation not
  permitted` warnings and then reports
  *everything* filtered, open ports
  included, because nothing it sent ever
  left. The signature: the errors
  themselves, plus a healthy service
  reading `filtered`. Chapter 6 has the
  capture. The fix in such a chair is
  chapter 6's other scan: `-sT` goes
  through the ordinary connection path
  and gets ordinary answers.
- **The target is gone or the path is.**
  Everything filtered *including* ports
  that were open an hour ago, on a host
  discovery also calls down, is usually
  a machine off, unplugged, or
  renumbered — check the boring layer
  before the clever one.

## The host that's "down" isn't — or the up one isn't a host

Discovery said nothing's there; the
service disagrees. Usual truth: the host
drops discovery's probes (ICMP by
policy, or a filter on its side) while
serving its real ports. If the machine is
yours and you *know* it's there, `-Pn`
skips the census and knocks — chapter 5.
The mirror-image trap lives in the same
chapter: on loopback, *everything* is
"up," 256 addresses of it, because your
own stack answers for the whole range.
An "up" from an address nobody owns, on
a network you don't recognise, deserves
the same scepticism: ask what answered.

## "You requested a scan type which requires root privileges"

In full, captured from an unprivileged
account (the build ran it as the `nobody`
user) asking for the SYN scan:

```
$ nmap -sS -p 8080 127.0.0.1
You requested a scan type which requires root privileges.
QUITTING!
```

No scan happened; exit, stage left. The
fixes are the ones the message implies:
run the privileged types with sudo, or
ask for the types that need nothing —
`-sT` and `-sn` (unprivileged discovery
uses plain connections) work from any
account, and `--unprivileged` tells nmap
to stay in that lane even when you're
root. The build machine adds a wrinkle
worth knowing by sight: there, even root
hits `Operation not permitted` on raw
sends — root is a property of the
account, packet injection is a property
of the environment, and sandboxes can
withhold the second from the first.

## The scan that takes forever

Time in a scan is mostly *waiting*:
for silences to ripen into `filtered`
(chapter 3's one rule added 1.2 seconds
to a four-port scan), for slow services
to finish answering version probes
(chapter 7's interrogation: 92 seconds
for four ports), for paths through
middlemen (the build machine's network
address answered everything, eventually —
13 seconds a scan). And one scan in this
guide simply never finished: OS
detection, retrying raw probes the
sandbox would never let leave, was
stopped by hand after 90 seconds.
Practical order of operations: narrow
`-p` before widening `-T`; run `-sV`
only at ports already known open; put
`--host-timeout` on sweeps of ranges
you don't know; and when a scan crawls,
suspect a silent port before a slow
network — silence is what nmap spends
its life waiting out.

## UDP says everything is open|filtered

Chapter 6's shrug, returned as a
symptom. Causes, in order of likelihood
on a normal network: the ports are
listening but don't answer empty
datagrams (most UDP services), a
firewall is dropping, or the host's ICMP
unreachables are being rate-limited or
filtered on the path — in which case
even closed ports look ambiguous. On
the build machine it's simpler and total:
the sandbox eats UDP itself, so live and
closed lab ports wear the same
`open|filtered`. The honest tools for
UDP are patience, short port lists, and
`-sV`'s protocol-shaped probes (which
give real services something worth
answering) — and the honest conclusion,
often, is chapter 3's: no reply is not a
reply of "no."
