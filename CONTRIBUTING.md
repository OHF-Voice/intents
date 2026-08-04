# Contributing

Our contributing guide lines can be found in [the Voice developer documentation](https://developers.home-assistant.io/docs/voice/intent-recognition/contributing).

## Restricted files

[`intents.yaml`](intents.yaml) declares the intents and slot combinations that
**every** language is validated against, so a change there affects all languages
at once. It may only be changed by repository admins and maintainers. This is
enforced by the `guard-core-files` check, which fails any pull request that
changes the file and is not authored by one of them.

Language leaders own their own `sentences/`, `responses/`, `tests/`, `rules/`,
and `lists/` directories (see [CODEOWNERS](CODEOWNERS)) and do not need approval
to change them.

If a slot combination is missing, wrongly marked, or does not fit your language,
please open an issue describing what you need instead of editing `intents.yaml`
in your pull request.
