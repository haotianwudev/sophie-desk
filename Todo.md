# Todo

A scratch backlog — things you want done eventually but don't want to spend tokens/budget
formalizing into a real task right now. Not part of the Dataview board on purpose: these are
unformalized ideas, not tracked work, so nothing here has `status`, a probe, or a gate.

When you're ready to actually pick one up: turn it into a proper task per
[.claude/skills/sophie-desk/SKILL.md](.claude/skills/sophie-desk/SKILL.md) ("Creating a task")
and delete the line here. Don't let an item sit here *and* as a real task — pick one home.

---

- [ ] (add items below this line, one per line, oldest first)
- [ ] [2026-08-30] [platform] ETL: explore adding SPX futures (/ES) prices — gives insight into
      where SPX is heading while the US cash market is closed (overnight/pre-market). Would need
      a data source (ThetaData already has an integration in `spx-option-backfill`; check if it
      or another vendor covers futures too) and a new table alongside `prices`/`vol_regime_data`.
      Natural fit for the `vol-regime-etl` Cloud Run job if the read-after-write ordering allows
      it — see the "Automatic daily execution" section of the sophie-develop-guide skill.
