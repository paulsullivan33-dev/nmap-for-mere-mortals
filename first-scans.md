# First Scans

Start the lab (chapter 1), open a second
terminal, and scan the machine you're sitting
on. `127.0.0.1` is the address every machine
has for itself — **localhost** — and it is
the one target on earth you always have
permission to scan.

One piece of spelling first. This command
says `-sT`, which asks for a **connect scan**:
nmap asks the operating system to make an
ordinary connection to each port, the same
way a browser or any other program would.
It is the scan type any user can run, it
works everywhere, and chapter 6 explains what
the alternatives do differently and why this
guide's captures are mostly connect scans.
For now, read reports, not mechanics.

## The first scan

With no port options, nmap scans the 1,000
most common ports — the ones real services
usually live on:

```
$ nmap -sT 127.0.0.1
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-10-20 02:42 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00011s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8022/tcp open  oa-system
8080/tcp open  http-proxy
8888/tcp open  sun-answerbook

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
```

Read it top to bottom, once, slowly:

- **`Nmap scan report for localhost
  (127.0.0.1)`** — the target, with the name
  nmap found for it by looking the address up
  backwards. On your machine this machine
  calls itself localhost; on a network it
  would be whatever your naming says.
- **`Host is up (0.00011s latency).`** — the
  target answered, and **latency** is how
  long its answers took: a tenth of a
  millisecond, because the target is the same
  box. Across a real network this number is
  your first clue about distance and
  congestion, and chapter 5 is about hosts
  nmap decides are *not* up.
- **`Not shown: 997 closed tcp ports
  (conn-refused)`** — the compression. Three
  ports earned rows in the table; the other
  997 all said the same thing ("refused"),
  so nmap summarises them in one line rather
  than printing 997 rows. The number in
  parentheses is the summary's *reason* —
  chapter 3 is about reasons.
- **The table.** `PORT` is the port number
  and protocol. `STATE` is what the knock
  concluded — here, `open`: something
  accepted the connection. `SERVICE` is a
  name — and here is your first lesson in
  not fooling yourself.

## The service column is a phone book, not a witness

The lab's web server is on 8080, and the
table calls it **http-proxy**. The banner
server on 8022 is called **oa-system**; the
chat server on 8888 is **sun-answerbook**.
None of those names came from the ports.
Nmap carries a table — port number in,
customary service out — and prints whatever
the table says, for open ports and closed
ones alike:

```
$ nmap -sT -p 80,22 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000091s latency).

PORT   STATE  SERVICE
22/tcp closed ssh
80/tcp closed http
```

Port 22 is `ssh` and port 80 is `http`
whether or not anything has ever listened
there — it is the port's *usual* tenant, from
the phone book. That makes the column a good
first guess and a terrible conclusion.
Chapter 7 asks the ports themselves, and
8080 turns out to be a web server after all,
while 8022's costume comes partly off.

## Naming the ports yourself

Usually you know which doors you care about.
`-p` takes a list, and the report shrinks to
exactly your question — this is the shape of
most scans in this guide:

```
$ nmap -sT -p 8080,8022,8888,59999 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00041s latency).

PORT      STATE  SERVICE
8022/tcp  open   oa-system
8080/tcp  open   http-proxy
8888/tcp  open   sun-answerbook
59999/tcp closed unknown

Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds
```

The fourth port is the lab's deliberately
closed one, and it earns two new words:
state `closed` (chapter 3 takes the states
apart properly) and service `unknown` — the
phone book has no entry at all for 59999, so
nmap prints the honest word instead of
inventing one.

Check: with the lab running, that scan shows
three `open` rows and one `closed`. If 8080
shows `closed` for you, the lab isn't
running — start it in its own terminal and
knock again.
