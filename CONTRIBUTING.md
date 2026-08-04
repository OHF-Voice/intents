# Contributing

Our contributing guide lines can be found in [the Voice developer documentation](https://developers.home-assistant.io/docs/voice/intent-recognition/contributing).

## Restricted files

[`intents.yaml`](intents.yaml) declares the intents and slot combinations that
**every** language is validated against, so a change there affects all languages
at once. It may only be changed by [@OHF-Voice/admin](https://github.com/orgs/OHF-Voice/teams/admin)
and [@OHF-Voice/voice-ohf](https://github.com/orgs/OHF-Voice/teams/voice-ohf).
This is enforced by the `guard-core-files` check, which fails any pull request
that changes the file and is not authored by a member of those teams.

Language leaders own their own `sentences/`, `responses/`, `tests/`, `rules/`,
and `lists/` directories (see [CODEOWNERS](CODEOWNERS)) and do not need approval
to change them.

If a slot combination is missing, wrongly marked, or does not fit your language,
please open an issue describing what you need instead of editing `intents.yaml`
in your pull request.
