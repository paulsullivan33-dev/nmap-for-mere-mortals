# Recipes

Four jobs, done end to end. Each is a
question from chapter 1 wearing work
clothes, and each was run exactly as
written against the lab.

## 1. Did my service actually start?

The log looks calm. The config is right.
Is the port open? Port 9000, before
anything is told to listen there:

```
$ nmap -sT -p 9000 127.0.0.1
PORT     STATE  SERVICE
9000/tcp closed cslistener
```

(The phone book calls 9000 `cslistener`.
The phone book calls everything
something.) Now start a specimen service
— Python's built-in web server — and ask
again, with version detection this time:

```
$ python3 -m http.server 9000 &
$ nmap -sT -sV -p 9000 127.0.0.1
PORT     STATE SERVICE VERSION
9000/tcp open  http    SimpleHTTPServer 0.6 (Python 3.12.3)
```

Open — and named, correctly this time,
because SimpleHTTPServer's replies match
a fingerprint nmap knows. Stop the
service and the port returns to `closed`
on the very next knock (verified exactly
that way for this page). The recipe's
point is the *order*: scan, change, scan
again. The two tables are the proof the
change did something; either one alone
is an anecdote.

## 2. Did the firewall change do what I meant?

Chapter 3 built this one. The task: the
chat service on 8888 should stop being
reachable. The rule goes in, the port is
rescanned with its reasons showing, the
verdict is read, and the rule comes back
out because this is a lab:

```
$ iptables -A INPUT -p tcp --dport 8888 -j DROP
$ nmap -sT -p 8888 --reason 127.0.0.1
8888/tcp filtered sun-answerbook no-response
$ iptables -D INPUT -p tcp --dport 8888 -j DROP
$ nmap -sT -p 8888 --reason 127.0.0.1
8888/tcp open  sun-answerbook syn-ack
```

(Full tables cropped to the row that
changed; the before rule and after scans
were run against all four lab ports, and
only 8888 moved.) Note the vocabulary gap
the recipe teaches you to expect: a DROP
rule doesn't make a port `closed` — it
makes it *silent*, `filtered`, because
refusals are also answers and the rule
forbids those too. If you'd wanted the
machine to keep saying no politely, the
rule would have been REJECT. Verify with
your eyes on the reason column, not on
your memory of the rule you typed.

## 3. What's answering on my network?

On your own LAN, this is a discovery
sweep followed by light scans of whatever
the census finds — and it is the recipe
this lab can only half-perform, so read
the label. The census step, exactly as
chapter 5 ran it against the one
neighbourhood the lab owns:

```
$ nmap -sn -n 127.0.0.0/24
... (256 reports, every address in the loopback range "up")
Nmap done: 256 IP addresses (256 hosts up) scanned in 0.01 seconds
```

That result is loopback's party trick,
not a network. On a real home LAN the
same command — with *your* network's
range, something like `192.168.1.0/24`,
which you know because it's yours —
returns a handful of reports, one per
device that answers: router, printer, the
computer under the desk, something you
don't recognise (that one gets the next
command). Then each address found gets
its light scan, `nmap -sT 192.168.1.50`
style, and the unrecognised thing is
usually identified by its open ports and
a `-sV` pass before you remember what it
is. Described rather than captured:
the build machine has no LAN of
neighbours, only a two-address sandbox
link it would be wrong to sweep, and a
guide that fakes a neighbourhood
teaches lying. The shape of the work is
the recipe; your network supplies the
numbers.

## 4. Scan yourself the way the network sees you

One machine, two doors. Chapter 2 scanned
the lab through localhost. Here is the
same box through its network address —
where the build machine's sandbox keeps
an intermediary that accepts every TCP
connection on its behalf:

```
$ nmap -sT -p 8080,8022,8888,59999 198.19.0.2
PORT      STATE SERVICE
8022/tcp  open  oa-system
8080/tcp  open  http-proxy
8888/tcp  open  sun-answerbook
59999/tcp open  unknown
```

Port 59999 — closed, verifiably, from
inside — reads `open` from the network
side, and random ports (443, 12345)
read open too, because something in
this sandbox answers every knock
addressed to that interface. On your own
infrastructure the intermediary would be
a NAT, a load balancer, a cloud
provider's fabric — different machinery,
same moral: **the inside view and the
network view of a machine are two
different reports, and the difference is
itself a finding.** When the two disagree
on your machines, something between the
doors is speaking for the box — know
what it is, because everyone scanning
from outside is talking to it, not to
you.
