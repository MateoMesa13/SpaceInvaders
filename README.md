# SpaceInvaders

## Running tests

The test suite uses `pytest`. Ensure that `pygame` and `pytest` are installed in
your environment:

```bash
pip install pygame pytest
```

Then execute the tests from the repository root:

```bash
pytest
```

If running in a headless environment, set `SDL_VIDEODRIVER=dummy` to avoid
initializing a window.
