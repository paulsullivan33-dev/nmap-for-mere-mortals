# What Nmap Is

**Nmap** ("Network Mapper") is a command-line
tool that asks machines what's listening. You
name a machine — usually your own — and a set
of **ports**, and nmap knocks on each one and
reports what happened: something answered and
welcomed a connection, something answered and
refused, or nothing answered at all. From those
three outcomes it builds the map most system
problems actually need: *what is exposed, where,
and under what name.*

It has been free and open source since 1997,
which is why it is everywhere: installable from
nearly every Linux package manager, present on
most admin workstations, and quietly built into
a generation of other tools.

A mortal asks it four questions, over and over:

1. **What's on my network?** Which machines are
   up, and what is each of them offering?
2. **What is this machine listening on?** The
   audit you run on your own server before
   someone else runs it for you.
3. **Did my service actually start?** You
   launched it, the log looks calm — is the port
   open, from the outside as well as inside?
4. **Is the firewall doing what I think?** You
   wrote a rule. Did the port's answer change
   the way the rule says it should have?

Every chapter of this guide is one of those
questions being answered against machines we
own.

## The rule, before anything else

**Only scan machines and networks you own, or
that you have explicit permission to scan.**
Scanning is knocking on doors; on your own house
that's maintenance, on someone else's it can be
a crime, a terms-of-service violation, or the
start of an incident response — sometimes all
three, and "I was just curious" is not a
defence anyone accepts. This guide is built so
the rule costs you nothing: every target in it
is a lab running on the same machine as the
scan. Your own network at home, your own
servers, your own lab — that is a career's worth
of legitimate scanning, and it starts in
chapter 2.

## What nmap is not

- **Not an oracle.** Nmap reports what came
  back over the wire. A service can lie in its
  banner, a middlebox can answer on a machine's
  behalf, and silence can mean several different
  things. Chapters 3 and 6 are largely about
  not fooling yourself with a clean-looking
  table.
- **Not, by itself, a vulnerability scanner.**
  It finds doors and reads nameplates. Some of
  its scripts (chapter 8) probe for known
  problems, but nmap's core job is the map, not
  the verdict.
- **Not quiet.** A scan is traffic: connections
  in logs, alerts in monitoring. On your own
  lab, that's a lesson. Elsewhere, it's that
  permission rule again.

## Have you got it?

```
$ nmap --version
Nmap version 7.94SVN ( https://nmap.org )
Platform: x86_64-pc-linux-gnu
Compiled with: liblua-5.4.6 openssl-3.0.13 libssh2-1.11.0 libz-1.3 libpcre2-10.42 libpcap-1.10.4 nmap-libdnet-1.12 ipv6
```

That capture is from the machine this guide
was built on: **Nmap 7.94SVN** on Linux,
installed fresh for the purpose
(`apt-get install nmap` — the package is
called `nmap` in essentially every
distribution, and there are official builds
for Windows and macOS as well; those two
platforms are named in this guide, not
exercised). Every scan quoted in these
chapters was run by root on that machine,
against the lab below — and where being root
wasn't enough, the chapters say so and show
you the failure. Chapter 11 collects them.

## The lab

One file, `examples/lab_server.py`, stands up
four small listeners on your machine:

```
$ python3 examples/lab_server.py --check
would listen: tcp/8080 (web), tcp/8022 (banner), tcp/8888 (chat), udp/53535 (udp)
deliberately closed: tcp/59999, udp/59998
```

- **tcp/8080** — a tiny web server wearing a
  name tag that reads `LabHTTP/1.0`, serving
  one invented page.
- **tcp/8022** — a socket that greets every
  connection with an SSH-style banner. There
  is no SSH behind it. It is a costume, and
  chapters 7 and 8 enjoy taking it off.
- **tcp/8888** — a chat greeter with no
  standard service attached, so nmap's
  guesses about it are visibly guesses.
- **udp/53535** — a listener that answers any
  datagram, for the UDP chapter.
- **tcp/59999 and udp/59998** — nothing at
  all. A genuinely closed port is a lesson,
  so two are reserved by doing nothing.

Start it with `python3 examples/lab_server.py`
and leave it running in its own terminal;
Ctrl-C stops it. `examples/lab-notes.txt`
describes each specimen. Keep the lab —
every chapter from here on scans it.
