# Scripts: The Nmap Scripting Engine

Ports answer knocks. But some questions
need conversation: *what does this service
say when it connects? what is this web
page called? is this thing behaving like
the proxy it claims to be?* The **Nmap
Scripting Engine** (NSE) is nmap's answer —
hundreds of small programs, shipped with
nmap and written in Lua, that run against
the open ports a scan finds and report
back in the table, on lines beginning
with `|`.

Every script carries **categories**, and
the categories are the safety story:
`safe` (won't crash or meaningfully
disturb the service), `intrusive` (might),
`discovery`, `auth`, `brute`, `exploit`,
and — the one to read twice — `vuln`,
scripts that check for known
vulnerabilities. Running a `vuln` script
at a machine is testing that machine for
holes. On your own machines: a chore. On
anyone else's, without explicit permission:
the crime chapter 1 mentioned. This guide
runs `safe` and `discovery` scripts
against the lab, and names the rest.

You can read any script's own description
before trusting it:

```
$ nmap --script-help banner
banner
Categories: discovery safe
https://nmap.org/nsedoc/scripts/banner.html
  A simple banner grabber which connects to an open TCP port and prints out anything sent by the listening service within five seconds.
```

## Two scripts against the lab

**banner** takes whatever a service says
first — the same greeting version
detection listens for, printed raw:

```
$ nmap -sT --script banner -p 8022,8888,8080 127.0.0.1
PORT     STATE SERVICE
8022/tcp open  oa-system
|_banner: SSH-2.0-OpenSSH_9.6p1 LabSSH
8080/tcp open  http-proxy
8888/tcp open  sun-answerbook
|_banner: LABCHAT 1.0 ready - say something
```

Two lines of pure profit. The banner
server's costume, quoted verbatim — and
note that *this* evidence doesn't claim
SSH at all; it just shows you the bytes,
and the claiming is yours to do. The web
server gets no `|_banner` line: it doesn't
greet, it waits to be asked, so there was
nothing to grab. A missing script line is
a result too — the service said nothing
first.

**http-title** asks a web port for its
page and reports the `<title>`:

```
$ nmap -sT --script http-title -p 8080 127.0.0.1
PORT     STATE SERVICE
8080/tcp open  http-proxy
|_http-title: Lab Web - Specimen Page
```

Small, and constantly useful on your own
network: the difference between "something
web-ish on 8080" and "ah, *that* page."

## -sC: the default set

`-sC` runs the scripts in the `default`
category — the ones nmap's maintainers
judge useful, quick, and polite enough to
be a default. Point it at the lab and it
answers with the title above, plus one
line that teaches the chapter's last
lesson:

```
$ nmap -sT -sC -p 8080,8022,8888 127.0.0.1
PORT     STATE SERVICE
8022/tcp open  oa-system
8080/tcp open  http-proxy
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Lab Web - Specimen Page
8888/tcp open  sun-answerbook
```

`http-open-proxy` tested whether the web
server would fetch pages for strangers —
because the phone book calls 8080
"http-proxy," that test made sense to
run. Its verdict ("might be redirecting")
is a false positive on a specimen: the
lab server returns the same page for
every path, which looks, to a proxy test,
like fetching. Both halves matter.
Scripts act on the table's guesses as
well as on facts, and a script's warning
is a lead to check, not a verdict —
especially against a service you built
from string and sealing wax in chapter 1.

Choosing scripts deliberately is the
grown-up form: `--script banner,http-title`
names exactly the two you mean, `--script
"http-*"` takes a family, and the nsedoc
site linked from every `--script-help`
keeps the full catalogue with each
script's categories printed at the top.
Read the category before the description.
On your own lab, curiosity is cheap; on
anything else, the categories *are* the
permission conversation, in miniature.
