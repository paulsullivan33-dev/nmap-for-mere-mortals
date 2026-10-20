# Port States, Honestly

Everything nmap concludes about a port fits
in one word in the STATE column. There are
six of those words, and mortals mostly meet
three. This chapter is about what each word
actually *proves* — which is always less
than it first sounds like — and about the
`--reason` flag, which makes nmap show its
working.

Add `--reason` to the lab scan and the table
grows a column: not just the verdict, but
the evidence it was reached from.

```
$ nmap -sT -p 8080,8022,8888,59999 --reason 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up, received localhost-response (0.00016s latency).

PORT      STATE  SERVICE        REASON
8022/tcp  open   oa-system      syn-ack
8080/tcp  open   http-proxy     syn-ack
8888/tcp  open   sun-answerbook syn-ack
59999/tcp closed unknown        conn-refused

Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds
```

## open — something said yes

Reason `syn-ack`: the port answered the
knock with the second step of TCP's opening
handshake, and (for a connect scan) the
connection completed. What that **proves**:
a program on that machine accepted a
connection on that port, at that moment,
from this machine. What it does **not**
prove: that the program is the service the
phone book names, that it will talk to you,
or that it would accept *you* specifically
from somewhere else. Open is a door
answering, not an identity — chapter 7 is
about asking who's behind it.

## closed — something said no, promptly

Reason `conn-refused`: the machine itself
answered, immediately, "nothing listens
here." A closed port is not an absence of
evidence; it is positive evidence of a live
machine with no listener on that port,
whose firewall (if any) lets the refusal
through. This is the lab's 59999, and it's
the friendliest no in networking: fast,
clear, and final.

## filtered — nobody said anything

Now make silence happen. The build machine's
firewall gets one temporary rule — *drop*
every packet to the chat port — and the same
scan runs again:

```
$ iptables -A INPUT -p tcp --dport 8888 -j DROP
$ nmap -sT -p 8080,8022,8888,59999 --reason 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up, received localhost-response (0.00028s latency).

PORT      STATE    SERVICE        REASON
8022/tcp  open     oa-system      syn-ack
8080/tcp  open     http-proxy     syn-ack
8888/tcp  filtered sun-answerbook no-response
59999/tcp closed   unknown        conn-refused

Nmap done: 1 IP address (1 host up) scanned in 1.23 seconds
```

The chat server never stopped running. But
its port now reads `filtered`, reason
`no-response`: nmap knocked, waited,
knocked again, and heard nothing at all —
and silence is genuinely ambiguous. It can
mean a firewall dropping packets (the truth
here), a machine that's off, a network
eating packets, or — chapter 11's case — a
scanner forbidden from knocking properly.
`filtered` never tells you which. It tells
you the knock went unanswered, full stop.
(Note also the scan took 1.23 seconds
instead of 0.03: waiting for answers that
never come is where scan time goes.)

Removing the rule restores the port to
`open` / `syn-ack` on the next scan —
chapter 10 builds a whole recipe on that
before-and-after.

## open|filtered — UDP's honest shrug

UDP has no handshake and no refusals from
the port itself, so a UDP scan (chapter 6)
often cannot distinguish "listening but
quiet" from "swallowed by a firewall":

```
PORT      STATE         SERVICE
53535/udp open|filtered unknown
59998/udp open|filtered unknown
```

That is the lab's UDP listener and the
lab's deliberately closed UDP port,
**indistinguishable** — on the build
machine the capture has an extra excuse
(the sandbox eats UDP outright; chapter 11),
but on any machine this pair of words is
UDP's standing warning: no reply is not a
reply of "no."

## The other three, named

Three combined states complete the set.
This guide doesn't produce them live — they
belong to scan types outside its scope — so
they are named from nmap's documentation,
not from captures:

- **unfiltered** — the port is reachable,
  but the scan type used (an ACK scan, for
  firewall mapping) cannot tell open from
  closed.
- **closed|filtered** — a UDP or IP-ID
  scan couldn't separate closed from
  filtered for this port.
- **open|filtered** above is the one of the
  three a mortal will actually meet.

The pattern to keep: a state word is a
report about *answers received*, and
`--reason` shows you the answer each word
was built from. When a report surprises
you, ask for the reasons before you believe
the words.
