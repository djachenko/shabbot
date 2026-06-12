# CHANGELOG

<!-- version list -->

## v0.2.0 (2026-06-12)

### Bug Fixes

- Remove unused os import
  ([`eee7c4e`](https://github.com/djachenko/shabbot/commit/eee7c4e0911b73ba0a558da9bd07f6000b75d734))

### Features

- Add config module with .env loading and interactive setup
  ([`2fdcb2f`](https://github.com/djachenko/shabbot/commit/2fdcb2fc18e574e34ae1955d5fa30dd7776bd945))

### Refactoring

- Hardcode whisper model and bin instead of reading from env
  ([`06538e7`](https://github.com/djachenko/shabbot/commit/06538e764448116d3ff8a24707b794602ab16cdc))

- Replace direct env access with config module
  ([`aef1595`](https://github.com/djachenko/shabbot/commit/aef159515fad5c8d84df598a4372d87b87516535))


## v0.1.1 (2026-06-09)

### Bug Fixes

- Detect release by tag diff instead of PSR --print
  ([`0ec03d1`](https://github.com/djachenko/shabbot/commit/0ec03d1e431e5aca99288421e802ac713c7a0bb6))

### Continuous Integration

- Add [skip ci] to PSR version bump commit message
  ([`b063988`](https://github.com/djachenko/shabbot/commit/b0639882238acf1831b6bf9ac415b10d3b7145a3))

- Skip release workflow on PSR version bump commit
  ([`03020df`](https://github.com/djachenko/shabbot/commit/03020dfa4ea4cc080c007ae0bc977a175df84263))

- Trigger CI
  ([`b26034c`](https://github.com/djachenko/shabbot/commit/b26034c5df6595e0f294383cd0ec44fad9a82140))


## v0.1.0 (2026-06-09)

### Bug Fixes

- Add shell: bash to pytest step for Windows compatibility
  ([`500a8f0`](https://github.com/djachenko/shabbot/commit/500a8f070b8e0f6d72fea4c24d19d431f54c875c))

- Add test extras and fix mypy path in CI
  ([`738e924`](https://github.com/djachenko/shabbot/commit/738e9244d8bc0660c2941ce0db9c6e5e41e89793))

- Configure git identity before merge in integration workflow
  ([`013f6a0`](https://github.com/djachenko/shabbot/commit/013f6a0757b398b99f30a5557825bdeefb6e9c0c))

- Disable major bump on 0.x in semantic release config
  ([`66764a3`](https://github.com/djachenko/shabbot/commit/66764a37c1fa052185767cb1e2707ab80f630f75))

- Handle --help in main via argparse for smoke test
  ([`196e1ff`](https://github.com/djachenko/shabbot/commit/196e1ff6e707b1dc5df7ba26552c494fe4da839f))

- Lower requires-python to 3.10, add release extras, add parser tests
  ([`561b660`](https://github.com/djachenko/shabbot/commit/561b66084295a6f6f4bb591c8e0a7f53c4305f34))

- Resolve mypy type errors in bot and todoist client
  ([`52067da`](https://github.com/djachenko/shabbot/commit/52067dacf08ba8cc188063bdea1ab702648e035a))

- Retry voice file download on TimedOut
  ([`75e5344`](https://github.com/djachenko/shabbot/commit/75e5344a548d9f16f84f7b97bfc4a4dc476d3575))

- Set whisper transcription language to ru
  ([`4974d03`](https://github.com/djachenko/shabbot/commit/4974d03c049132cbbb4f4a2d2fc23d170aeef59a))

- Simplify CI matrix, remove windows and python 3.10
  ([`da9beaa`](https://github.com/djachenko/shabbot/commit/da9beaaea90ba64a38659f3ca5c58d27cde0c6ad))

- Use bot identity for git merge in integration workflow
  ([`ce516ae`](https://github.com/djachenko/shabbot/commit/ce516aef09ba01d3a9e1e99850dedda023c3bdd7))

### Chores

- Add session memory
  ([`6b45358`](https://github.com/djachenko/shabbot/commit/6b45358dffc9e9870f5a3d2ddedcc2bdf0cec557))

- Project config
  ([`41f5b14`](https://github.com/djachenko/shabbot/commit/41f5b14dd1ce92be042f336d7a15cbfd9c6a93e1))

- Repokit setup
  ([`f9d2e10`](https://github.com/djachenko/shabbot/commit/f9d2e10a735b100cd7ef4df242f99bbd1deca1e9))

- Reset version to 0.0.0 for PSR baseline
  ([`8a3189c`](https://github.com/djachenko/shabbot/commit/8a3189c1036781233f6d69773258041a14381e5b))

- Update project memory and claude context
  ([`f20db20`](https://github.com/djachenko/shabbot/commit/f20db20d8e4dd0d8401668036d4e25a8196133d4))

### Continuous Integration

- Configure release pipeline with GitHub App auth
  ([`a086762`](https://github.com/djachenko/shabbot/commit/a0867624dd4b23a5e04b06056dfb816ce30a9f07))

- Switch release to direct PSR CLI, allow zero versions
  ([`6149dd3`](https://github.com/djachenko/shabbot/commit/6149dd3fc03c5ada22a55705f5e6b246d3399a48))

### Documentation

- Add README
  ([`725b885`](https://github.com/djachenko/shabbot/commit/725b885bf17e05fccfa9e67524df57e393f83094))

- Add whisper install and model pre-download to README
  ([`7285e11`](https://github.com/djachenko/shabbot/commit/7285e110f30957e122b1f4eb41fc77309326f559))


## v1.0.0 (2026-06-09)

- Initial Release
