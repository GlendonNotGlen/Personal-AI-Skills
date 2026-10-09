---
name: talk-deck-style
description: Glendon's preferences for building, editing, reviewing and fact-checking conference and technical-talk slide decks (PowerPoint .pptx, the Claude PowerPoint add-in, or any slide outline). Use this whenever he asks to create, restructure, reword, fact-check, humanize, or review slides, a talk flow, timeline/divider slides, demo slides, or detection slides — even if he only says "fix this slide", "suggest wording", "add a slide after X" or pastes feedback to apply. Also use it when planning a talk's section order or slide budget.
metadata:
  version: "1.0.0"
---

# Talk deck style

These preferences come from how Glendon has steered several AI tools while building a 45-minute conference talk, and from the edits he made by hand afterwards. His hand edits are the strongest signal: when the AI's version and his differ, his version wins.

## 1. Shape of the talk

**Budget.** About 45 minutes of talking, including about 15 minutes of demos, plus Q&A. Allow 1–1.5 minutes per content slide and a few seconds per divider. That works out to roughly **22–26 main slides**. Count slides before adding more. If a request would push the deck over budget, say so and suggest what to merge.

**Opening.** Start with a situation the audience recognises, such as how a login and cookie work, before any acronym. Then add a short "why this matters" slide from the attacker's point of view (attackers take the easiest route). Introduce terms only once people care about the problem.

**One organising idea.** Pick one thread, such as a timeline of protections, and come back to it. A roadmap or timeline slide shows every stage. Reuse it as the divider before each section, with that stage's card highlighted and the others greyed out. Divider titles should move the story forward: a past-tense finding per stage, for example "Chrome 127 bound the cookie key to the browser".

**Same shape for every section.** Readers learn the pattern, so keep it identical across sections:

1. A divider: the timeline with the current stage highlighted.
2. A concept intro, 1–2 slides: what it is, who runs it, and what privilege it runs under.
3. Flow diagrams: one for the write or encrypt path and one for the read or decrypt path. Use as many slides as the mechanism needs, with one step-change per slide.
4. The threat model: what changed for attackers. A short quote from the vendor works well here.
5. A demo slide.
6. An "evidence and detection" slide.

If a later section breaks this shape (for example, a missing detection slide or a concept slide placed after its diagrams), flag it.

**Framing: purple team.** Every section pairs the attacker's technique with what defenders can see and do. Don't sanitise it into a neutral version history, and don't drop the attack side. Credit the original researchers by name. Keep the submitted talk title as he wrote it, even if a style check flags it.

**Close.** A side-by-side summary of every stage (control, what it protects, where to investigate), plus two or three takeaways someone could repeat to a colleague. Put appendix slides and references after Questions.

## 2. Slide content rules

- **One new concept per slide.** If a slide needs two new terms, split it.
- **Draw it before you explain it.** Prefer simple boxes and arrows that build step by step over bullets or tables. Give the box the slide is about a blue border so the eye lands there. When he shares a reference diagram from a blog, adapt it to the deck's style rather than pasting it in.
- **Caveats go in the speaker notes, not on the slide.** Qualifiers on the slide make the talk sound unsure. He has repeatedly cut trailing caveats by hand, for example "…while valid, subject to the site's checks" became "…while valid." Make the claim narrower so it's true without a hedge, then put the nuance in the notes.
- **Precise rather than absolute.** Avoid "every", "all", "once", "never" and "skip every check" unless they are literally true. Use "Recovering that AES key decrypts the cookie values encrypted with it", not "…decrypts every stored cookie." Precision and directness both matter: be precise by narrowing the claim, not by adding hedges.
- **Keep keys and data distinct.** For example: DPAPI protects Chrome's key, and Chrome's key encrypts the cookie values. Say what protects what.
- **Use one term per concept for the whole deck.** For example, don't drift between "session token", "authentication cookie" and "bearer cookie". Define each acronym once in full, at first use.
- **Code formatting.** Put API names, files, flags, registry paths and event IDs in a monospace font (Consolas), slightly smaller than the surrounding text. On slides, prefer short relative paths (`<Profile Path>\Network\Cookies`). Long full paths go in an appendix slide or the narration.
- **Sources.** Each technical slide gets a small source line that just names the source ("Source: Chromium, Windows OSCrypt implementation"), linked to the exact versioned primary source, such as a Chromium file at the version tag the demo uses. Don't add qualifiers to the source line; he deletes them.
- **Demo slides.** Each demo has one thing to notice. Show the build and privilege context on the slide ("Pre-ABE browser build", "Assumed privileged access"). Say the takeaway before and after the demo, and keep a recorded backup. Don't claim the demo shows more than it does. If the PoC is a model or fixture, say so.
- **Detection slides.** Name concrete telemetry (event IDs, log channels, Sysmon event numbers, server-side logs) and state what must be enabled for it to exist. Frame the bullets as investigation leads, not proof.

## 3. Wording voice

Glendon runs `humanizer` and `writing-tropes` on nearly every slide. Apply both whenever you write slide text, and run them if they're installed. What he consistently wants:

- **Short, plain declarative sentences.** A lead line is one sentence; he deletes second sentences. For example, "`Local State` holds Chrome's wrapped AES key. Its master key is stored elsewhere." became just the first sentence.
- **Titles state the finding.** Sentence case, one line, no full stop, and clear of the QR code in the top-right corner. Shorten rather than wrap.
- **No figures of speech for locations or actions** ("lives at", "sits elsewhere", "disk keeps it for later"), no stock phrases ("path of least resistance"), no slogans or quotable closers, no "not X but Y" contrasts, no forced groups of three, no dashes, no "four layers of…" counting.
- **The bottom line on a slide** is one plain claim that leads into the next slide.
- **Personal slides stay in his voice.** "About me" and disclaimers are terse and personal ("Pentesting, Purple Teaming @ CSA", "First time speaker @ conference"). Don't polish them into marketing copy. Prefer plain over flourish: he changed "First love in web security" to "Started in web security".
- When a quote is verbatim, keep it verbatim and attribute it (author, outlet, date).

## 4. Visual style (only when asked)

He usually says "focus on contents, I'll fix design later". Don't restyle unless asked. When matching or extending the existing look:

- Near-black background `#111418`, off-white text `#F2F4F5`, one electric-blue accent `#4C8DFF`, greys for everything else. Use red only for a single emphasis word on the attacker's side (for example, "easier").
- Bold titles in Aptos Display, about 36pt (48pt on the cover). A monospace font (Consolas) for section labels, footers and code. Body text 18–21pt.
- The QR code linking to the slides sits top-right on every slide, with a footer label and a **live** slide number from the layout, never typed by hand.
- Diagram cards are dark grey with a subtle border. Dimmed timeline cards must stay legible from the back of the room.

## 5. How to work on his decks

1. **Find the master copy and check for his edits first.** He edits in PowerPoint between AI sessions. Before changing anything, compare the file with what you last saw and keep his manual wording. Never overwrite a phrase he changed by hand just to restore your own.
2. **Make the edits he asked for, and refine them.** When he pastes feedback from another reviewer, apply it but improve it for clarity and accuracy. If you deviate from the feedback, say why in one line.
3. **Fact-check technical claims** against primary sources: Microsoft Learn, Chromium source at the relevant tag, the vendor's security blog, the original researcher's write-up. Distinguish what a source states from what you infer. If something is unverified (rollout dates, version numbers), say so instead of smoothing it over.
4. **Do structural changes before text changes**: add, delete, reorder, then reword. Then check the rendered slides for overflow, and check that titles clear the QR code.
5. **Report back briefly, per slide**: what changed (before → after when it's wording), what you deliberately left alone, and anything you noticed but didn't touch. Don't change speaker notes or demos unless asked. If notes now contradict a slide, flag it.
6. When he's brainstorming ("is it better if…"), give a recommendation with a short reason and one or two alternatives. Don't build anything until he picks.

See `references/examples.md` for before-and-after pairs taken from his deck.
