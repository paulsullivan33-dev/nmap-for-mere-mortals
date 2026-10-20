# Choosing Ports

A scan asks about the ports you name, and
only those. Nmap's defaults are sensible,
but the difference between a scan that
answers your question and one that answers
a stranger's is usually the port list.
There are 65,535 TCP ports (and the same
again for UDP); these are the ways mortals
choose among them.

## The default: the famous 1,000

With no `-p`, nmap scans the 1,000 ports its
statistics say services most often live on.
Chapter 2's first scan is one: three lab
ports found, 997 closed ports summarised.
The default is a fine "what's this machine
about" — and a poor audit, because anything
unusual lives exactly where the famous
1,000 aren't.

## Lists and ranges

`-p` accepts names for the job directly:

- **A list** — `-p 8080,8022,8888,59999`:
  exactly these, no others. Most scans in
  this guide are lists, because most real
  questions are lists ("are *my* services
  up?").
- **A range** — `-p 8000-8100`: every port
  from 8000 to 8100. Ranges are how you
  cover a service family's neighbourhood:

```
$ nmap -sT -p 8000-8100 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00014s latency).
Not shown: 99 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8022/tcp open  oa-system
8080/tcp open  http-proxy
```

Ninety-nine closed ports compressed into
the *Not shown* line, and the two lab
services that live in the 8000s in the
table. (8888 is outside the range; a range
answers for its own span and nothing
else.)

- **Mixing** — lists and ranges combine:
  `-p 22,80,8000-8100` is one option, read
  left to right.

## Fame, ranked: --top-ports and -F

`--top-ports N` scans the N most common
ports only. It has a trap in it, and the
lab springs it cleanly:

```
$ nmap -sT --top-ports 10 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000091s latency).

PORT     STATE  SERVICE
21/tcp   closed ftp
22/tcp   closed ssh
23/tcp   closed telnet
25/tcp   closed smtp
80/tcp   closed http
110/tcp  closed pop3
139/tcp  closed netbios-ssn
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
```

All three lab services were up — and the
scan found **none of them**, because not
one lab port is among the world's ten most
common. `--top-ports` answers "does this
machine run the usual things," and a clean
result says nothing about anything
unusual. `-F` ("fast") is the same idea at
100 ports: the lab scan with `-F` found
8080 and 8888 but walked straight past
8022, which isn't in the famous 100
either. Fame is a sampling strategy, not
a census.

## Everything: -p-

`-p-` scans all 65,535 ports. On localhost,
with connect scans, that is startlingly
cheap — this is chapter 2's machine
answering for every door it has:

```
$ nmap -sT -p- 127.0.0.1
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000065s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8022/tcp open  oa-system
8080/tcp open  http-proxy
8888/tcp open  sun-answerbook

Nmap done: 1 IP address (1 host up) scanned in 1.88 seconds
```

Sixty-five thousand refusals arrive
quickly when the target is the same box
and says no instantly. Across a network,
against ports that filter silently,
`-p-` is a different proposition — every
silent port costs retries and waiting, and
chapter 6's timing templates become
manners, not just speed. The mortal's
habit: `-p-` for audits of your own
machines, lists and ranges for questions,
fame-ranked scans only when fame is the
question.
