# 6. GitHub Actions CI — Step by Step

## What CI does here
Continuous Integration automatically tests code changes. TrustLayer's workflow is `.github/workflows/ci.yml`.

1. Trigger on pushes to `main`/`master`, pull requests targeting those branches, or manual dispatch.
2. Use a hosted Ubuntu runner.
3. Check out the repository.
4. Set up Python 3.12.
5. Install `requirements.txt`.
6. Run `pytest -v` with `src` on `PYTHONPATH`.

## Publish and verify
1. Create a public GitHub repository.
2. Push this project to `main`.
3. Open the repository's **Actions** tab.
4. Open **TrustLayer CI** and inspect the latest run.
5. Green means configured tests passed; red means inspect the failing step's log.
6. Make a small code change and push to see CI run again.

## Common failures
- `ModuleNotFoundError: trustlayer`: verify `PYTHONPATH: src` is set in the workflow.
- Missing dependency: add it to `requirements.txt`.
- YAML syntax issue: use spaces, not tabs; preserve indentation.
- Tests differ locally and in CI: check Python version, case-sensitive file paths, ignored/untracked files, and environmental assumptions.

## Security
Do not place passwords, tokens, or API keys in the workflow. The NYC API download does not require a secret for this basic public-data example.

Official guide: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
