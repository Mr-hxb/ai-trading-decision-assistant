# Project Agent Instructions

This project is an advisory-only stock analysis CLI. Keep all changes within that boundary.

- Do not store API keys, access tokens, credentials, or local machine paths in the repository.
- Do not implement or call broker execution, order placement, or automatic position-changing logic.
- Do not turn `decision_status` into trade commands or deterministic investment advice.
- Use `.env` for provider credentials and keep `.env.example` limited to placeholder variable names.
- Run the test suite before publishing or committing changes:

```bash
python -m pytest
```
