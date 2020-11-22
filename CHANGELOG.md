# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [1.6.0](https://github.com/pablolmedorado/temat/compare/v1.5.0...v1.6.0) (2020-11-22)


### Features

* **frontend:** add Xmas icon to the navbar logo ([be96821](https://github.com/pablolmedorado/temat/commit/be968212804f0f4d2378f80c907b2f1c61b0c1f2))
* **index:** add pinned filters ([8b62960](https://github.com/pablolmedorado/temat/commit/8b629607a1b418e3d912245853106d060a2429f6))


### Bug Fixes

* **frontend:** use $route.name as keep-alive key to prevent the app from caching unnecesary views ([43d9621](https://github.com/pablolmedorado/temat/commit/43d96212e7d54d633b7548309fd1ce86ab83397b))
* **permissions:** replace is_staff by is_superuser to fit the real use case ([c0d99d2](https://github.com/pablolmedorado/temat/commit/c0d99d20b362ca11cf39cf8d9e4035dcb529fe25))
* **typo:** fix typo in v-spacer tag in event card toolbar ([697d3d8](https://github.com/pablolmedorado/temat/commit/697d3d8d889aa78ed1f6f8d3446e8469fd6d7257))

## [1.5.0](https://github.com/pablolmedorado/temat/compare/v1.4.0...v1.5.0) (2020-11-16)


### Features

* **holidays:** add "pending" filter ([616f9df](https://github.com/pablolmedorado/temat/commit/616f9df75edeb8c284b5a1bf7fe488ab559ced87))
* **holidays:** add multisort in team holidays table ([ff4d8ec](https://github.com/pablolmedorado/temat/commit/ff4d8ec801e1ca2ecb6f25b1ecb71cec70eac7d5))


### Bug Fixes

* **effort:** fix user filter in effort report ([9e20bcb](https://github.com/pablolmedorado/temat/commit/9e20bcbace07b0515405079e1626c9216dc5a8ad))
* **holidays:** fix reactive filters issue ([6cf22fc](https://github.com/pablolmedorado/temat/commit/6cf22fc485a01bd44990c70f967ebc89712e33a0))

## [1.4.0](https://github.com/pablolmedorado/temat/compare/v1.3.0...v1.4.0) (2020-11-15)


### Features

* **epics:** improve usability by adding a default filter ([0673618](https://github.com/pablolmedorado/temat/commit/06736188bf4a7720d1280107821d961d50bf532a))
* **filters:** add basic filters to advanced filters dialog ([7832a67](https://github.com/pablolmedorado/temat/commit/7832a67c0b7187f509a0765864f381479696fbec))
* **frontend:** add filters dropdown menu to the standard index component ([c725f35](https://github.com/pablolmedorado/temat/commit/c725f35a0f27b0eedc3c48ef50830aca881627de))
* **index:** add quick filters to index component ([59f1c05](https://github.com/pablolmedorado/temat/commit/59f1c0582b92e77ab1a77cfa6f9cbb8f5bb00116))


### Bug Fixes

* **filters:** show tooltip on year selector filter ([b77bdc9](https://github.com/pablolmedorado/temat/commit/b77bdc9c6923beaba6e2421359e72c7e72ce4c60))

## [1.3.0](https://github.com/pablolmedorado/temat/compare/v1.2.1...v1.3.0) (2020-11-11)


### Features

* **user-stories:** add progress date & validated date filters ([486fa78](https://github.com/pablolmedorado/temat/commit/486fa78c414c65ff950bd0f1f7da5e8dd647470d))
* **user-stories:** add style to status label in the index component ([b29a399](https://github.com/pablolmedorado/temat/commit/b29a3991c15d3551b8596049d0205671bdd6bddb))


### Bug Fixes

* **user-stories:** add navigation guard for 'new' route ([c79af50](https://github.com/pablolmedorado/temat/commit/c79af503908a445dd9342496cec423eb764ce0df))

### [1.2.1](https://github.com/pablolmedorado/temat/compare/v1.2.0...v1.2.1) (2020-10-24)


### Bug Fixes

* **frontend:** fix form validation error messages with params ([d1f85cb](https://github.com/pablolmedorado/temat/commit/d1f85cb6d2bc9908ad0fd2e3e5e56f0bb211cdb9))
* **frontend:** replace chevron async autocomplete icon ([83bbb3f](https://github.com/pablolmedorado/temat/commit/83bbb3f3986e7312588d1a26aaafa23dce48d487))
* **frontend:** use help/default cursors on TruncatedText component ([ad74010](https://github.com/pablolmedorado/temat/commit/ad74010fc3952aed134659388938b78f2ce039bd))
* **notifications:** remove useless "changes" notification when assigning users to user stories ([58b493d](https://github.com/pablolmedorado/temat/commit/58b493d03c5915680416b02077f316f93128fb75))

## [1.2.0](https://github.com/pablolmedorado/temat/compare/v1.1.0...v1.2.0) (2020-10-18)


### Features

* **sprints:** add current date indicator and navigation to the gantt chart ([96a862a](https://github.com/pablolmedorado/temat/commit/96a862a2de46478ded710d875bdd2e085116f073))


### Bug Fixes

* **breakfasts:** move main action (summary) to the fab button and add missing toolbar tooltip ([8732f4d](https://github.com/pablolmedorado/temat/commit/8732f4de3d39d665daedf1be62fb52a16ce31736))
* **charts:** set loading state while retrieving chart data and alert users if the request fails ([041429e](https://github.com/pablolmedorado/temat/commit/041429e242b9f0ff3914e7776e96ce406ec7e682))
* **sprints:** solve gantt chart shared tooltip issue ([30a5e31](https://github.com/pablolmedorado/temat/commit/30a5e31a1f08c22fcc9627b33f409daa6352beb0))

## [1.1.0](https://github.com/pablolmedorado/temat/compare/v1.0.1...v1.1.0) (2020-10-13)


### Features

* **sprints:** add gantt chart ([53ebd21](https://github.com/pablolmedorado/temat/commit/53ebd21d9d2821155aa4daa26dfeb09a6bf14dd8))


### Bug Fixes

* **effort:** remove text-decoration from user story links ([1aa8eb6](https://github.com/pablolmedorado/temat/commit/1aa8eb6482f51536e2f4ba0344b8fba034081560))
* **user-stories:** prevent sprint and date fields from being modified by non staff users ([ac954fb](https://github.com/pablolmedorado/temat/commit/ac954fbfc8ae1b2c948d262b8c7896d3d8ccca7c))

### [1.0.1](https://github.com/pablolmedorado/temat/compare/v1.0.0...v1.0.1) (2020-10-04)


### Bug Fixes

* **epics:** change index default ordering to asc ([e9ec14a](https://github.com/pablolmedorado/temat/commit/e9ec14a0abcf4f7a6c9c5a87ccf5efffa4eb72c3))
* **frontend:** avoid mutating options prop in table component ([2f4a56e](https://github.com/pablolmedorado/temat/commit/2f4a56e2b0dbb7a78283d2d1bb040e7e3b49dda9))
* **readme:** fix license link, which wasn't working ([27f1d1e](https://github.com/pablolmedorado/temat/commit/27f1d1e5d0b3848b1a1b3ce99771e6dbd7d3784a))
* **release:** downgrade frontend app version from 1.0.1 to 1.0.0 ([9e011bc](https://github.com/pablolmedorado/temat/commit/9e011bce6d519f600e5b6f0bd651efbaad2438fc))
* **release:** include project npm files in version bumping config ([efa5582](https://github.com/pablolmedorado/temat/commit/efa5582b48f4cf18c5fae16057f7e388a3f50224))

## 1.0.0 (2020-09-30)


### Features

* **general:** add support for Conventional Commits and standard-version
