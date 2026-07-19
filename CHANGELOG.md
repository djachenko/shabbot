# CHANGELOG

<!-- version list -->

## v0.5.0 (2026-07-19)

### Bug Fixes

- Restructure generic error message formatting in error_handler
  ([`43b4502`](https://github.com/djachenko/shabbot/commit/43b450225cc0194cdf04c3fb2a0a6b7129bf8728))

### Chores

- Add _claude to .gitignore
  ([`3031ed5`](https://github.com/djachenko/shabbot/commit/3031ed5a2cb81960c1e86ab2747700b44d88e65b))

### Code Style

- Breathing in parse_update and _download_and_transcribe
  ([`03ece31`](https://github.com/djachenko/shabbot/commit/03ece31c68984086eb8767eeaa060d3a5b435cd2))

- Review fixes — breathing space, dedup cancel/gather, multiline create_files
  ([`0f38417`](https://github.com/djachenko/shabbot/commit/0f38417ed7615899083b3857c04577104b3f836f))

### Features

- Error handler + custom exceptions per module
  ([`83b76e1`](https://github.com/djachenko/shabbot/commit/83b76e1c9b15cacbc42883d212d73e24b9bc5e81))

### Refactoring

- Explicit if/else for description in create_task
  ([`c50f306`](https://github.com/djachenko/shabbot/commit/c50f306bba5e32eb8cff17fa1d2bce062930002a))

- Extract TranscriptionError messages as class constants
  ([`b1c533e`](https://github.com/djachenko/shabbot/commit/b1c533e4ff8071653fc4e0acac679c0e589f4e87))

### Testing

- Add create_files fixture to conftest, use in test_transcribe
  ([`f86a872`](https://github.com/djachenko/shabbot/commit/f86a8725c4e3251cb43c9ed27e4b6b707558952d))

- Assert specific TranscriptionError messages per failure path
  ([`08d03df`](https://github.com/djachenko/shabbot/commit/08d03df8decb3717bdae64b78a552cb6ec63df39))

- Update tests for exception-based error handling
  ([`fb353ac`](https://github.com/djachenko/shabbot/commit/fb353acfdcaba6dfbf7e81e73ba63dd9936202e5))


## v0.4.3 (2026-07-14)

### Bug Fixes

- Remove unused os import in test_config
  ([`a249dbe`](https://github.com/djachenko/shabbot/commit/a249dbe4086bea5c7f6f907135963009f8b76251))

- Skip chmod test on Windows
  ([`97668a5`](https://github.com/djachenko/shabbot/commit/97668a5d064839a183714fc9a930559bf8861a4e))

### Testing

- Add unit tests for all modules
  ([`aa709d5`](https://github.com/djachenko/shabbot/commit/aa709d5b98cdfb18b0fc5f6f2f42a5b9548e3b78))


## v0.4.2 (2026-07-11)

### Bug Fixes

- Assert message not None in VoiceMessageParserOutput._send
  ([`c6bfa6b`](https://github.com/djachenko/shabbot/commit/c6bfa6b87e0898f81b83b58de981a4c61a4815cf))

- Update test import after parser module rename
  ([`330adb2`](https://github.com/djachenko/shabbot/commit/330adb2d6764d8f38dae7d23e8e4b02746900d0f))

### Chores

- Add CLAUDE.local.md and _worktrees/ to .gitignore
  ([`f2a9124`](https://github.com/djachenko/shabbot/commit/f2a912430de26b8c323b1bfce679db05b5fa3be3))

### Refactoring

- Add Loggable mixin with cached_property logger
  ([`70dce8c`](https://github.com/djachenko/shabbot/commit/70dce8c553702ca06a8ddf1582a436d0706d00a6))

- Add message_parser layer with VoiceMessageParserOutput
  ([`84ef217`](https://github.com/djachenko/shabbot/commit/84ef217fffc5496d40bc793b4b425630487193bb))

- Add Processor as orchestration layer
  ([`22879dd`](https://github.com/djachenko/shabbot/commit/22879ddf6170e4f63fc76db9edb2bb692f13db2d))

- Consolidate Task and TaskParser into task_parser.py
  ([`e492ca3`](https://github.com/djachenko/shabbot/commit/e492ca32e5d92fee38b5c66a6c6db1c231c6f0ee))

- Extract TodoistClient class, remove todoist/ subpackage
  ([`d48c10e`](https://github.com/djachenko/shabbot/commit/d48c10eb3aa1ce6cf7649651615705ccfcf89394))

- Extract Transcriber — accepts Path, no Telegram deps
  ([`baa5bac`](https://github.com/djachenko/shabbot/commit/baa5bacfe3a242ddee9b130bcbfeb1b2a8a91085))

- Reduce bot.py to composition root
  ([`eddc7e7`](https://github.com/djachenko/shabbot/commit/eddc7e7129f1816c6aec224a85157b34a8deefb2))


## v0.4.1 (2026-07-11)

### Bug Fixes

- Add whisper timing logs
  ([`d6c3116`](https://github.com/djachenko/shabbot/commit/d6c311696efa953a55e77ca7f7a676317f7e1e24))

- Async subprocess for whisper + TodoistAPIAsync
  ([`8b71316`](https://github.com/djachenko/shabbot/commit/8b71316d4d0a73e7295d4ef346293fcd7f64ff98))

### Documentation

- Replace git clone with curl one-liners, fix Python version
  ([`02c7ee3`](https://github.com/djachenko/shabbot/commit/02c7ee38448467382b2bc6887c0359d53879b14d))


## v0.4.0 (2026-06-25)

### Chores

- [repokit] add .repokit to .gitignore
  ([`a358a9f`](https://github.com/djachenko/shabbot/commit/a358a9fa4750bf29369696ca956fb02d8db27c2e))

- [repokit] update ci workflows
  ([`dad486d`](https://github.com/djachenko/shabbot/commit/dad486d6375e42a6445e08c41b72c0e50caf4038))

- [repokit] update ci workflows
  ([`dea4727`](https://github.com/djachenko/shabbot/commit/dea472753128ff9285c9eea086e45c715ebc2798))

- Add Docker deployment files
  ([`2a6b6c1`](https://github.com/djachenko/shabbot/commit/2a6b6c1cffd70b2a12f697858df4bef226807dcc))

- Add Docker setup script
  ([`0d9707c`](https://github.com/djachenko/shabbot/commit/0d9707cff2ce352ae4b162715d0c60457e858f9d))

- Add uninstall script
  ([`920f16a`](https://github.com/djachenko/shabbot/commit/920f16a8f85766a4ac365c06420fd26b7efc00f2))

- Enable unbuffered Python output in compose
  ([`e0f59f4`](https://github.com/djachenko/shabbot/commit/e0f59f4dfdb27e9095bb4f66550a862bd20a126a))

- Remove old shabbot/ package root
  ([`230855d`](https://github.com/djachenko/shabbot/commit/230855d41fbca7fab26138f7de8df60ce95a732c))

### Documentation

- Actualize CLAUDE.md and README
  ([`d7f67af`](https://github.com/djachenko/shabbot/commit/d7f67af0ec69b7692eb9e52d558cf6f885917cc4))

- Add Docker as primary deployment path in README
  ([`6c01b92`](https://github.com/djachenko/shabbot/commit/6c01b9252782e369ccd0c48cf860cf2a6a55ddfd))

- Expand Docker setup instructions in README
  ([`632bf9b`](https://github.com/djachenko/shabbot/commit/632bf9b0ccbd5397eca510142a497e28f88b3420))

- Mention docker.sh in README setup section
  ([`22d50d6`](https://github.com/djachenko/shabbot/commit/22d50d6f2d3d6e4e01448e8aab1cd274115c7b3f))

- Move local requirements under local setup section
  ([`99e7a5b`](https://github.com/djachenko/shabbot/commit/99e7a5b6efced6c9fb5a9c117bb389452bc9a3f3))

- Update CLAUDE.md to reflect Docker as primary run method
  ([`0363375`](https://github.com/djachenko/shabbot/commit/0363375bbbd894e2aa601779a5a9f46579e3ee3a))

- Update README to reflect current setup flow and config location
  ([`dab7bf1`](https://github.com/djachenko/shabbot/commit/dab7bf1e55a865be04ad9156074b34497efc4c57))

### Features

- Add entrypoint that pre-warms Whisper model on container start
  ([`f3b1306`](https://github.com/djachenko/shabbot/commit/f3b13062883db58f292984fd9f638b5355b7d5ca))

### Refactoring

- Migrate config to dataclass, read whisper_model from config
  ([`feeca31`](https://github.com/djachenko/shabbot/commit/feeca313f93aec5d0e0bcd88e9b5dd4656525cda))


## v0.3.0 (2026-06-13)

### Bug Fixes

- Use config.todoist_token instead of dict access
  ([`ddf2d3a`](https://github.com/djachenko/shabbot/commit/ddf2d3aa607cf1dc310d0a4d57c9777fa1b03264))

### Chores

- Update memory index and backlog
  ([`7984ab3`](https://github.com/djachenko/shabbot/commit/7984ab3eabaaef692024ae3704c8de45ec09f642))

### Features

- Install wizard script
  ([`e158c54`](https://github.com/djachenko/shabbot/commit/e158c545b1897de69e7e5b7d5e5b4a765f2be551))

### Refactoring

- Pipeline via _make_handler and _catcher, invert handler dependencies
  ([`0713e56`](https://github.com/djachenko/shabbot/commit/0713e561842f316671affc04aec998f7a2fb57c0))

- Replace config dict with dataclass, move to XDG path
  ([`15b1954`](https://github.com/djachenko/shabbot/commit/15b19546945914b578bd8458abc58923d843601f))


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
