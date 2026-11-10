# AI merchant-support agent for Razorpay: teardown + PRD

A product case study by **Krupa Nirmal**. It looks at how Razorpay merchants get help today, what they complain about in public, and what an AI support agent should and shouldn't be allowed to do. It ends with a small eval on a local model.

Not affiliated with Razorpay, Cashfree or PayU. Public information only. Mockups are concepts with synthetic data.

**Read it:** [`Teardown_and_PRD.pdf`](Teardown_and_PRD.pdf) (12 pages) · [`Teardown_and_PRD.docx`](Teardown_and_PRD.docx)

## Numbers

| | |
|---|---|
| Public complaints tagged | 111 (65 X, 35 Play Store, 11 Reddit) |
| Written by merchants | 76 |
| Top merchant intents | Account suspended / funds withheld 22 · Activation & KYC 20 · Settlement delay 11 · Settlement on hold 9 |
| Merchant items mentioning a support problem | 35 of 76 |
| Hold / suspension items saying no reason was given | 16 of 31 |
| Support flows with steps counted | 5 |
| Eval scenarios | 26 (12 hand off, 9 resolve, 5 ask) |
| Eval pass rate, `qwen2.5-3b-instruct-q4_k_m` | 42.3% rule check · 19.2% strict (hand review of every auto-pass) |

The complaint counts rank pain points inside a self-selected sample. They are not estimates of ticket volume.

## What's here

```
Teardown_and_PRD.docx / .pdf   the write-up
data/complaints.csv            111 items: source, date, URL, role, intent, flags, excerpt, accessed date
teardown/screens/              screenshots of public support pages (headless Chromium, 11 Nov 2026)
eval/policy_prompt.md          the agent policy given to the model
eval/scenarios.py / .json      26 scripted merchant conversations with expected behaviour
eval/run_eval.py               runs them through a local GGUF model and scores them
eval/hand_review.py            second pass on every auto-passed reply
eval/results_*.json / .csv     replies, decisions, failures, timings
mockups/                       4 agent UI screens (HTML/CSS rendered to PNG)
scripts/                       screenshot and CSV build scripts
docs/build/                    builds the docx and the chart
```

## Method in brief

- **Complaints.** X posts from 4 keyword searches mentioning @Razorpay or @RazorpayCare (one item per author). The newest 1–2★ Play Store reviews of *Razorpay Payments for Business*. Reddit threads found via web search, because direct Reddit fetches were blocked. Each item has one primary intent, tagged by one person. Emails, phone numbers and merchant IDs are redacted in excerpts. Raw API pulls aren't published because they contain personal details.
- **Teardown.** Steps are counted from Razorpay's documented Dashboard flows. I didn't have a merchant login, so nothing was clicked through inside a Dashboard.
- **Eval.** Each scenario gives the model a synthetic Dashboard snapshot and one or two merchant turns. A reply passes if the behaviour label matches and the must and must-not regexes hold. Strict pass also needs a clean hand review. The refund cap and fee in the fixtures are test values, not recommendations.

## Re-run the eval

```bash
# needs llama-cpp-python and a GGUF model
cd eval
python scenarios.py                         # writes scenarios.json
python run_eval.py /path/to/model.gguf model-tag
```

Results here came from Qwen2.5-3B-Instruct Q4_K_M on CPU (temperature 0, seed 0). They are only for that model.

## Sources

Every source URL, with its access date, is listed in section 8 of the PDF and per row in `data/complaints.csv`.
