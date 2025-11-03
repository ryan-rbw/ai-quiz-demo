## 12. Feature to add during the demo

**Hints with penalty**
Prompt the assistant with this spec

* Add a `--hints` flag that enables one hint per question
* When a hint is used the correct answer is worth half points
* Update the summary to show how many hints were used
* Update README and docs with usage and example

Acceptance

* New flag appears in `--help` output
* Using a hint changes scoring and is reflected in the summary
* Unit tests cover hint scoring and limit of one per question