# AI Usage

## AI Tool Used

- OpenAI Codex

## Prompts Given

- Asked Codex to read the Django hiring assignment from the uploaded DOCX file.
- Asked Codex to explain the requirements before coding.
- Approved implementation after reviewing the plan.
- Asked Codex to keep the solution simple, junior-friendly, and limited to Django, Django REST Framework, and SQLite.

## Output Accepted

- Project structure
- Django models
- Django admin setup
- Serializers
- API views and URL configuration
- Simple box recommendation logic
- Unit tests
- README.md
- requirements.txt
- TEST_OUTPUT.md
- ZIP packaging

## Output Rejected Or Modified

- The original plan included a possible `LEARNING.md` file. This was rejected because the assignment requires the candidate to write the learning answer personally.
- The recommendation logic was kept simple and was not changed into a complex packing or optimization algorithm.

## Mistakes Found

- Django REST Framework was not installed in the local environment, so it had to be installed into a local virtual environment.
- The virtual environment creation showed an `ensurepip` permission error, but pip was still usable afterward.

## Verification

- Ran Django system checks.
- Created migrations.
- Ran database migrations.
- Ran the full Django test suite.
- Reviewed code for unnecessary complexity.
- Packaged the final project into a ZIP file.
