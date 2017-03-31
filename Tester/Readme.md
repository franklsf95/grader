1. Run `npm install -g elm-test` if you haven't already.
2. `cd` into the project's root directory that has your `elm-package.json`.
3. Run `elm-test init`. It will create a `tests` directory inside this one,
   with some files in it.
4. Copy all the dependencies from `elm-package.json` into
   `tests/elm-package.json`. These dependencies need to stay in sync, so make
   sure whenever you change your dependencies in your current
   `elm-package.json`, you make the same change to `tests/elm-package.json`.
5. Run `elm-test`.
6. Edit `tests/Tests.elm` to introduce new tests.
