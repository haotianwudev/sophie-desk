# The Sophie work model, in plain English

You're running a one-person company with two AI workers. The whole design comes down to one
problem: you're the only person who can catch a bad decision, so the system's job is to make
sure your attention only goes where a bad decision is actually possible — and everything else
just runs.

## The three kinds of work

Everything you do splits into three buckets, and each one gets treated differently because
getting it wrong costs something different.

**Publishing** — articles, videos, the forum, tier system. This is the part that makes money
today and gets people to notice Sophie exists. If something here is wrong, you find out fast
(the page looks broken, a link is dead) and it's cheap to fix. Because of that, this work moves
fast and mostly doesn't need you.

**Research** — the SPX option backtests, the strategy studies. This is what might make money
later, either as something you sell or something you trade yourself. If something here is wrong
— a backtest that looks great but is secretly cheating (using information it shouldn't have had
yet) — you often *don't* find out. It just looks like a good result, and you build on top of a
lie. So this is the slow lane, and nothing here gets called "done" without you checking it against
a real bar first.

**Platform** — the data pipelines, the backfill, the plumbing that keeps everything else fed. If
this breaks, it usually breaks quietly — a table stops updating and nothing announces it. This
lane's whole job is to make silent failures loud.

You limit how many things are "in progress" in each bucket at once — a small number, like one or
two. Not because more work isn't available, but because past that point you stop being able to
hold it all in your head, and *you* become the bottleneck instead of the work being the
bottleneck.

## What a task actually is

Right now, some of your work-in-progress lives as long documents that describe a project and its
history — the SPX backfill notes, the write-conditions build. That's the right idea, but those
files never stop growing, because nothing ever tells them they're done. A 600-line file is what
happens when a "task" and a "reference doc" get mixed together with no separation.

So the fix is to give every task a small, fixed header at the top — what it's called, which
bucket it's in, whether it's moving or stuck, who's working on it, what the next step is — and
let everything else (the notes, the history, the gotchas) stay exactly as free-form as it already
is underneath. When the task is done, it moves to an archive folder, and anything genuinely worth
remembering long-term gets copied into the relevant permanent reference instead.

This matters because it's the difference between opening one file to see "what's going on," and
having to read 600 lines to find out.

## The part that keeps everyone honest: probes

Here's the thing that actually caused you real pain during the backfill: a status message told
you the download was "complete" when it wasn't, and separately, a "killed" notification arrived
for a process that was actually still running fine. Written status lies in both directions —
it says done when it isn't, and it says dead when it isn't.

So every task that involves something running gets a **probe** — a tiny script that checks the
real, physical evidence (how many files actually exist on disk, how recently a log file was
actually touched) and prints one of three words: it's fine, it's running, or it's actually stuck.
Never "I did five things and it went great" — just the measured truth. That one rule is what
makes it safe to trust a status list instead of re-reading the whole file every time.

## Who does the work

Three different workers, and the rule for who gets what is simple: **how fast would you find
out if this were done wrong, and how much would it cost you?**

- If a mistake is obvious immediately and cheap to fix — hand it to the cheaper, faster worker
  (agy). It's good at breadth: writing lots of similar articles, searching the web, building UI
  against a style guide you've already set.
- If a mistake would be invisible and expensive — that's yours, or the more careful worker's
  (Claude). Anything that touches the live database, anything that decides whether a research
  result is real, anything that spans multiple systems at once.
- There's also a free, local option (a small AI model running on your own machine, via Ollama)
  for anything where being wrong costs literally nothing — skimming a hundred research papers
  to find the handful worth a second look, for instance. It's worth being precise about what
  this actually is: not a third worker that claims its own tasks, but a plain question-answering
  tool that Claude or agy calls *while* working a task they hold — it has no way to read a file
  or act on its own. It runs over everything because it's free, and it never gets the final say
  on anything.

That routing decision gets written down once, when a task is created, so you're not re-deciding
it every time someone picks the work back up.

## Where all this actually lives

You don't need a new app for most of this.

- **Your computer is the center.** The code, the data, both AI workers — everything real happens
  here.
- **GitHub is just the mail system.** When a worker wants to claim a task, it edits that task's
  header and pushes — the push *is* the claim. If two workers somehow grab the same thing at the
  same time, git will refuse the second push instead of silently overwriting anyone, so you find
  out immediately rather than never.
- **Obsidian is where you look at it.** Since a task is just a small text file with a few labeled
  fields at the top, Obsidian can show you a live table of every task, sorted and filtered, with
  zero code written — it's a feature the note-taking app already has (called Dataview), not
  something you build. It works on your phone too, syncing through the same GitHub repo.
- **A small always-on helper does the busywork.** Something modeled on the restart script you
  already wrote for the backfill — it doesn't make judgment calls, it just checks on things
  regularly, writes down what it finds, and picks up unclaimed work that's safe to hand out
  automatically. If it's ever unclear what to do, it stops and marks the task as needing you,
  rather than guessing.
- **You can talk to that helper in plain sentences**, because you already have a chat agent
  built for Sophie (the one in `sophie_agent`) — teaching it to read and edit task files means
  you can just ask it things like "what's blocking the backfill" or "put the article audit on
  agy" instead of running commands.
- **A page on the Sophie website is the one piece that's genuinely optional**, and worth building
  last, if at all — mainly for the one thing none of the above can do: draw an actual chart of a
  backtest result. Everything else it might show, the vault already shows for free.

## What gets built first

Roughly in this order, cheapest and most valuable first:

1. **Stop waiting on the backfill.** It turns out the option research doesn't actually need it —
   the older data you already have is enough to build on. Decide what to do about the newer gap
   later; it's not blocking anything today.
2. **Turn the three long-running project files into proper tasks**, with the small header and a
   probe, so you can see their real status at a glance instead of re-reading them.
3. **Publish the backtest results you already have but never pushed.** Most of your finished
   research work is sitting unpublished — that's pure upside, no new building required.
4. **Build the small always-on helper**, and teach the chat agent to talk to it.
5. **Only after all that — if you still miss it — build the chart page on the website.**

## What could go wrong

The most likely failure isn't any of the above breaking. It's that building this system becomes
more fun than doing the actual work it's meant to support, and you spend weeks polishing a
dashboard nobody needed yet. The guard against that is simple: nothing above gets built unless
it removes an actual decision from your week. If it doesn't, it waits.
