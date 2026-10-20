# Scan Types

A scan type is a choice about *how to knock*.
The report table looks the same either way;
what changes is what happens on the wire,
what lands in the target's logs, and what
privileges you need. Nmap has many types.
A mortal needs two well, a third honestly,
and a sense of timing.

## -sT: the connect scan, an ordinary knock

`nmap -sT` asks the operating system to open
a connection — the full, ordinary TCP
handshake, exactly what any program does —
and reads the outcome: connected means
`open`, refused means `closed`, timeout
means `filtered`. Every capture in chapters
2–5 is a connect scan, and its results look
like this (chapter 3's reasons included):

```
PORT      STATE  SERVICE        REASON
8022/tcp  open   oa-system      syn-ack
59999/tcp closed unknown        conn-refused
```

Its virtues are universality: no special
privileges, works in containers and on
every platform, and it can go anywhere a
normal connection can go. Its cost is
visibility: a completed connection is the
thing servers log, so a connect scan writes
your name in the guest book of every open
port. On your own machines — this guide's
whole world — that is no cost at all.

## -sS: the SYN scan, half a handshake

The **SYN scan** (root's default) knocks
differently. Nmap itself crafts just the
first packet of the handshake — the SYN —
using **raw sockets**, the OS facility for
hand-built packets. If a SYN-ACK comes
back, the port is open, and nmap
immediately tears the attempt down with a
reset instead of completing the connection:
a "half-open" knock that many services
never log, because as far as they're
concerned nobody ever arrived. A reset in
reply means closed; silence, after
retries, means filtered. Same table,
quieter wire, less ink in the logs — which
is a property, not a virtue: it's why the
permission rule in chapter 1 doesn't care
which type you used.

It needs root (or the CAP_NET_RAW
capability) because ordinary users aren't
allowed to hand-build packets. And when
even root isn't allowed to *send* them,
the scan degenerates — the build machine
lives in a sandbox that forbids raw sends,
and its one-port SYN scan is this guide's
standing exhibit:

```
$ nmap -sS -p 8080 --reason 127.0.0.1
sendto in send_ip_packet_sd: sendto(3, packet, 44, 0, 127.0.0.1, 16) => Operation not permitted
... (further sendto errors omitted)
Nmap scan report for localhost (127.0.0.1)
Host is up, received localhost-response.

PORT     STATE    SERVICE    REASON
8080/tcp filtered http-proxy no-response

Nmap done: 1 IP address (1 host up) scanned in 2.06 seconds
```

Every knock failed to leave the building,
so the port — a healthy web server — reads
`filtered` / `no-response`. The scan didn't
lie about what it heard (nothing); it
couldn't have heard anything. Chapter 11
returns to this: a wall of `filtered` is
as often a statement about the scanner's
chair as about the target. On an
unrestricted machine the same command
prints the same table as the connect scan,
arrived at by the quieter road.

If you're *not* root, asking for `-sS`
ends the conversation, which chapter 11
also keeps. And `--unprivileged` is the
useful opposite switch: it forbids nmap
from using raw packets at all, forcing the
connect family even for root — the mode
that produced every clean capture in this
guide would have, had it needed naming.

## -sU: the UDP scan, knocking on fog

UDP has no handshake, no connection, and
no refusal from the port itself — a closed
UDP port is betrayed only by the *host*
sending an ICMP "port unreachable," and a
firewalled one by silence. So a UDP scan
sends a small datagram per port and
interprets: a reply means **open**, an
ICMP unreachable means **closed**, and
silence means **`open|filtered`** — the
shrug from chapter 3. Retries make it slow:
nmap must wait out each silence, sometimes
more than once, so mortal UDP scans name a
few ports with `-p` and budget patience.

The build machine's UDP is eaten by its
sandbox before any of that can happen —
both the lab's live UDP listener and its
deliberately closed port come back with
the identical shrug (the sendto errors
are cropped here; they're the same ones
as above):

```
$ nmap -sU -p 53535,59998 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up.

PORT      STATE         SERVICE
53535/udp open|filtered unknown
59998/udp open|filtered unknown

Nmap done: 1 IP address (1 host up) scanned in 3.17 seconds
```

On an ordinary machine those two ports
would separate — a reply from 53535
(`open`), an ICMP unreachable for 59998
(`closed`) — and that expected output is
described here rather than shown, because
the build machine cannot produce it. What
the capture *does* prove, on any machine:
when UDP gives you `open|filtered`, it is
not a maybe to be argued with. It is the
whole of the evidence.

## Timing templates: politeness as a dial

`-T0` through `-T5` set how hard nmap
leans: probe parallelism, waits between
knocks, retry counts. `-T3` is the
default; `-T4` ("aggressive") is the
everyday choice for your own networks —
same answers, less dawdling:

```
$ nmap -sT -T4 -p 8080,8022,8888,59999 127.0.0.1
PORT      STATE  SERVICE
8022/tcp  open   oa-system
8080/tcp  open   http-proxy
8888/tcp  open   sun-answerbook
59999/tcp closed unknown
Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds
```

(The header lines are cropped; the table
is identical to chapter 2's, which is
itself the first timing lesson — against
a fast, close target the templates barely
matter.) The low end is the interesting
end: `-T1` waits 15 seconds between
probes and `-T0` five minutes, by design,
for networks where knocking softly is the
whole point — IDS-dodging history aside,
on a fragile or busy production network a
slow scan is good manners with a flag.
They are named here, not run: a `-T0`
demonstration takes minutes per port,
which is precisely their character. `-T5`
("insane") trades accuracy for speed —
timeouts get read as filtered — and
belongs to networks you own and are in a
hurry on, which on a mortal's home lab is
rarely the honest description.
