
# Project Instructions

## Project Overview
This project is an asynchronous AI API client built using Python and HTTPX.

## Project Structure
- `src/ai_client/`: Application source code.
- `tests/`: Automated tests.
- `pyproject.toml`: Project configuration and dependencies.
- `.env`: Local environment variables.

## Coding Standards
- Use Python 3.11 or later.
- Follow PEP 8 conventions.
- Use type hints for functions and methods.
- Write asynchronous functions where appropriate.
- Keep code modular and reusable.
- Never hardcode API keys or secrets.

## Testing
- Use pytest and pytest-asyncio.
- Mock external HTTP requests using respx.
- All tests must pass before committing changes.

## Code Quality
- Use Ruff for linting and formatting.
- Keep functions small and readable.
- Handle HTTP errors and timeouts properly.
