# Service and OS Detection

Chapter 2's lesson was that the SERVICE
column is a phone book. **Version
detection** is nmap actually knocking and
asking who's home. Add `-sV` and — for
every open port — nmap opens a connection,
listens for a greeting, and then sends a
series of **probes**: polite nonsense,
protocol openers, requests shaped for
common services, watching what each port
does with them. The replies are matched
against nmap's fingerprint database and
the SERVICE column becomes a report
instead of a guess.

One spelling matters on the build machine:
`-sV` alone, as root, would still try to
*find* the open ports with a SYN scan and
die on the sandbox's raw-send ban (every
port "filtered," nothing left to
interrogate). The scan type is chosen
explicitly here — `-sT -sV` — and the flags
compose like that everywhere: the knock
from chapter 6, the interrogation from
this one.

```
$ nmap -sT -sV -p 8080,8022,8888,59999 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00015s latency).

PORT      STATE  SERVICE         VERSION
8022/tcp  open   ssh             (protocol 2.0)
8080/tcp  open   http-proxy      LabHTTP/1.0
8888/tcp  open   sun-answerbook?
59999/tcp closed unknown
3 services unrecognized despite returning data. ...
Nmap done: 1 IP address (1 host up) scanned in 92.42 seconds
```

(The fingerprint blocks nmap printed
between the table and the footer are
discussed below; the full capture runs to
several pages of them.)

Read the VERSION column as three different
outcomes wearing one coat:

- **8080 — read from the reply.**
  `LabHTTP/1.0` is the web server's own
  `Server:` header, lifted from its answer
  to nmap's first request. The service name
  still says `http-proxy` — the phone book
  doesn't update — but the version column
  now reports something the port itself
  said. Whatever serves you can name
  itself, truly or falsely.
- **8022 — the costume, half believed.**
  The banner server greets with an
  SSH-shaped line, and nmap upgrades the
  service from `oa-system` to `ssh` with
  version "(protocol 2.0)". Note what it
  could *not* do: name a product. A real
  OpenSSH banner carries a version nmap
  knows; this one's invented suffix
  matched no fingerprint, so nmap
  believed the protocol, declined the
  product, and filed the banner under
  "unrecognized" (below). A banner is
  testimony, and testimony can be a
  costume.
- **8888 — a guess, marked as one.**
  `sun-answerbook?` — the question mark is
  nmap's own. The chat server's greeting
  didn't match any known service, so the
  table's name stands with a `?` appended:
  *unverified*. When nmap is unsure, it
  prints its uncertainty in the table.
  Believe the punctuation.

Below the table, each unrecognized service
gets its full **service fingerprint**
printed — the exact bytes each probe
brought back, formatted for submission to
the nmap project's database. They are long
and mostly for the project's benefit, but
one line of the chat server's is worth
reading: probe after probe, its reply is
`you said: ...` followed by nmap's own
words coming back. The fingerprint is the
interrogation transcript, and even a
service nmap can't name has told it
plenty: it greets instantly, it echoes, it
answers everything with the same shape.
Unknown is not uninformative.

**The cost.** That scan took 92.42
seconds against four ports on the same
machine, where the connect scan took
0.03. Interrogation is conversation:
probes wait for replies, slow talkers hold
the floor, and silence must be waited out
again and again. Budget for it, aim it
with `-p`, and don't be surprised when
`-sV` is the difference between a scan
finishing and a scan being checked on
after lunch.

## -O and -A: the fingerprint guess

**OS detection** (`-O`) goes further: it
probes the target's TCP/IP stack itself —
how it sizes windows, orders options,
answers odd packets — and matches the
pattern against a database of known
systems. Two honesties belong with it.
First, it is a *guess*, and nmap grades
its own: it wants at least one open and
one closed port to work with, and prints
warnings when conditions aren't ideal.
Second, its probes are hand-built packets,
so it needs the raw sends this sandbox
forbids. It rides along in `-A`
("aggressive": version detection, OS
detection, the default scripts, and
traceroute in one flag — convenient, and
loud in all four ways at once). Here is
the `-A` run against the lab's two
talkingest ports, cropped to its OS
verdict:

```
$ nmap -sT -A -p 8080,8022 127.0.0.1
... (sendto errors: the OS probes could not be sent)
PORT     STATE SERVICE    VERSION
8022/tcp open  ssh        (protocol 2.0)
8080/tcp open  http-proxy LabHTTP/1.0
... (script output and fingerprints)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
No OS matches for host

Nmap done: 1 IP address (1 host up) scanned in 98.63 seconds
```

`No OS matches for host` is a real outcome
on healthy machines too — a stack the
database doesn't know, a middlebox
rewriting the evidence — and the honest
reading of "-A" on an unknown box is that
three of its four quarters did their work
and the fourth filed a shrug. When OS
detection *does* match, the report adds
lines naming the system family and
nmap's best specific guesses; those lines
are described here rather than quoted,
because the build machine's sandbox never
let its probes leave. Treat any OS line
you ever get as a lead, not a label: the
stack's manners suggest an origin, they
do not swear to one.
