# Output That Lasts

A scan on the screen is an answer. A scan
in a file is *evidence* — the thing you
diff against next month's scan, grep
during an incident, and wave at a
colleague when a port's story doesn't
match its documentation. Nmap writes
itself out in several shapes, because
different readers — you, a script, a
report tool — want different things.
`-oA` asks for all of them at once:

```
$ nmap -sT -p 8080,8022,8888,59999 -oA out/labscan 127.0.0.1
```

That one command leaves three files:
`labscan.nmap`, `labscan.gnmap`, and
`labscan.xml`. (The scan's own screen
output is unchanged — the files are
by-products, and the directory must
exist first.)

## The three shapes

**`.nmap`** is the screen report, frozen:
the same header, the same table, readable
by the same eyes. This is the file you
attach to a ticket.

**`.gnmap`** is the *grepable* format —
one line per host, every field labelled,
made to be fed to other tools:

```
$ head -3 out/labscan.gnmap
# Nmap 7.94SVN scan initiated Tue Oct 20 02:52:43 2026 as: nmap -sT -p 8080,8022,8888,59999 -oA out/labscan 127.0.0.1
Host: 127.0.0.1 (localhost)	Status: Up
Host: 127.0.0.1 (localhost)	Ports: 8022/open/tcp//oa-system///, 8080/open/tcp//http-proxy///, 8888/open/tcp//sun-answerbook///, 59999/closed/tcp/////
```

Notice the header comment keeps the whole
command line: a file that explains how it
was made. The `Ports:` line carries every
port in a fixed `port/state/protocol//service///`
shape — ugly to read, ideal to process.

**`.xml`** is the full structured record
— every probe detail nmap keeps, in the
format reporting tools and dashboards
import. Its head shows the discipline:
the command, the time, the scan type,
then host by host in nested elements:

```
$ head -12 out/labscan.xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<nmaprun scanner="nmap" args="nmap -sT -p 8080,8022,8888,59999 -oA out/labscan 127.0.0.1" ... version="7.94SVN" ...>
<scaninfo type="connect" protocol="tcp" numservices="4" services="8022,8080,8888,59999"/>
```

(xml-stylesheet and a few elements cropped
for the page.) Of the three shapes, only
the XML is the *complete* record; the
others are views of it.

Each format also has its own flag —
`-oN` (normal), `-oG` (grepable), `-oX`
(XML) — for when one shape is enough, and
`-oS` exists for a joke format nobody
needs. Mortal habit: `-oA` for audits you
mean to keep, `-oN` for quick notes.

## Feeding scans to the trio

The grepable file exists to be processed,
and the text-processing trio (the sibling
guide *Text Processing for Mere Mortals*
teaches all three properly) earns its
keep on exactly this shape. Watch one
old lesson fire on new material — how
many ports in the scan are open? `grep -c`
*counts lines, not matches*:

```
$ grep -c open out/labscan.gnmap
1
```

One *line* contains "open" — the whole
Ports line. The count of opens needs a
tool that counts occurrences; awk,
splitting on spaces and slashes and
counting fields that are exactly `open`,
answers correctly:

```
$ awk -F'[ /]' '/Ports:/{for(i=1;i<=NF;i++) if($i=="open") c++} END{print c+0}' out/labscan.gnmap
3
```

That pattern — scan to `-oA`, keep the
files, interrogate them later with
ordinary text tools — is how a monthly
port audit actually lives: this month's
`.gnmap` against last month's, and the
differences are your change report. Save
scans with dates in the filename, keep
the command in the habit of the header
comment (nmap puts it there for you), and
a year of a machine's doors fits in a
folder you can grep in a second.
