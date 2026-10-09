# Before → after examples from the STANDCON 2026 deck

These come from "The Cat-and-Mouse Game of Chrome Credentials". "Hand edit" means Glendon changed the AI's text himself in PowerPoint. Weight those highest.

## Hand edits (strongest signal)

| AI wrote | He changed it to | Lesson |
|---|---|---|
| A stolen bearer cookie may be replayed while valid, subject to the site's checks. | A stolen bearer cookie may be replayed while valid. | Cut trailing caveats; the notes carry them. |
| `Local State` holds Chrome's wrapped AES key. Its master key is stored elsewhere. | `Local State` holds Chrome's wrapped AES key. | One-sentence lead lines. |
| Source: Microsoft DPAPI documentation. Covers the usual user-scoped case. | Source: Microsoft DPAPI documentation | Source lines just name the source. |
| Timeline divider with a bottom line ("Any app running as the user can still ask DPAPI to unlock the key.") | Bottom line removed on the first divider | Don't stack a takeaway on a slide that's already a map. |
| I am not a browser security expert | I am not a browser security expert. All credit goes to the original researchers. | Credit the researchers explicitly. |
| First love in web security, now exploring Windows internals | Started in web security, now exploring Windows | Plain over flourish on personal slides. |
| Suggested title "Chrome Session Theft: DPAPI, ABE, CDP and DBSC" | Kept "The Cat-and-Mouse Game of Chrome Credentials" | The submitted title stays, even if a style check flags it. |

## Accepted AI rewrites (patterns he approved)

| Before | After | Why it worked |
|---|---|---|
| Chrome 80 encrypted cookies with a DPAPI key | Chrome 80 protected its cookie key with DPAPI | Precise: DPAPI protects the key, not the cookies. |
| One DPAPI-wrapped key protected every cookie | One DPAPI-wrapped key protects cookie values | Drops the absolute. |
| On launch, Chrome unwraps the key once | On launch, Chrome unwraps the AES key | Drops the "once" overclaim and names the key. |
| Same-user access alone should no longer unlock ABE-protected data | Running as the same Windows user is no longer enough to read ABE-protected data | No metaphor ("unlock"), no vague "should". |
| The key goes through the service. Individual cookie values do not. | Only the AES key passes through the service; Chrome encrypts each cookie value itself. | One plain sentence instead of a two-beat contrast. |
| That file lives at `%APPDATA%\…` | (path moved to the appendix and narration) | Long paths and figures of speech come off the slide. |
| Admin access alone does not reveal the plaintext master key | Finding the master-key file is not the same as recovering the key inside it | States the real distinction. |
| Chrome has added four layers of cookie protection | Divider titles that move forward per section (past-tense findings) | No counting habit; the story moves forward. |

## Section template as built

```
[Divider] Chrome 127 bound the cookie key to the browser      (timeline, ABE card highlighted)
[Concept] App-Bound Encryption                                  (what it is, one lead line, 3–4 bullets)
[Concept] Chrome Elevation Service                              (who runs as what, privilege boundary diagram)
[Flow]    One app-bound key encrypts v20 cookie values          (encrypt path)
[Flow]    Why the service uses DPAPI twice                      (mechanism detail)
[Flow]    On launch, the service unwraps and checks the key     (decrypt path)
[Flow]    Chrome decrypts v20 cookie values locally
[Threat]  Google's threat model for ABE                         (verbatim quote, attributed)
[Table]   ABE workaround prerequisites
[Demo]    Demo: ABE with privileged access                      (build + privilege context on slide)
[Detect]  ABE: evidence and detection                           (event IDs, what must be enabled)
```
