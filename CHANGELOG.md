# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [1.15.0](https://github.com/pablolmedorado/temat/compare/v1.14.1...v1.15.0) (2021-11-07)


### Features

* add colour and icon to Tags ([17a9291](https://github.com/pablolmedorado/temat/commit/17a9291ce4564135238eaabed2b54543bd380d7e))
* **scrum:** relax date field validations on sprint and user-story ([dd61002](https://github.com/pablolmedorado/temat/commit/dd61002b1c3e748d7be352e14e139ad0ef02977d))
* **sprints:** add filters and progress to deployment report ([b9db1a2](https://github.com/pablolmedorado/temat/commit/b9db1a2497f4a082fdd8c9e272176c0b674564c7))
* **user-stories:** add escape button to external resource field ([b950607](https://github.com/pablolmedorado/temat/commit/b95060722abab754656d4048fefbb4b9984b8c89))
* **user-stories:** show authorship info on user-story detail ([a0722b6](https://github.com/pablolmedorado/temat/commit/a0722b6e047ad82b9cd7d1efbe98ae01c5fc81cd))


### Bug Fixes

* **admin:** add UUIDWidget to avoid errors in imports/exports ([497a1fb](https://github.com/pablolmedorado/temat/commit/497a1fb54e4a441b5968236750a2a611f49638d4))
* **docker:** remove temat user ([c81bc3b](https://github.com/pablolmedorado/temat/commit/c81bc3bd5c82ebb488c0ecc67ee13cf530593379))
* **user-stories:** include tags in user story copies ([4be0a71](https://github.com/pablolmedorado/temat/commit/4be0a71479b985d7bc55a4636043278b058a38bd))
* **users:** make get_random_admin method truly random ([415eb51](https://github.com/pablolmedorado/temat/commit/415eb51003450b60444d164943c2bf41f3b1e8c9))

### [1.14.1](https://github.com/pablolmedorado/temat/compare/v1.14.0...v1.14.1) (2021-07-08)


### Bug Fixes

* **holidays:** fix queryset.union Oracle issue ([62553ef](https://github.com/pablolmedorado/temat/commit/62553ef35f462ea33ddcd1766afc42b3d04371bf))
* **notifications:** add missing notification model ([7a12408](https://github.com/pablolmedorado/temat/commit/7a124085f76b413190c835b21f67a5460b6827ba))

## [1.14.0](https://github.com/pablolmedorado/temat/compare/v1.13.0...v1.14.0) (2021-07-04)


### Features

* **user-stories:** add "all" filter to user-story index and apply it in indexes with context ([2391891](https://github.com/pablolmedorado/temat/commit/239189136a065c08ca3389698e5a8bd201af0f3d))


### Bug Fixes

* **effort:** user arg missing in canPerformAction function ([55d3bdf](https://github.com/pablolmedorado/temat/commit/55d3bdfbc7530d8098a37867c56734d9b09b6a3d))
* **frontend:** fix quick filter save warning ([73d80cd](https://github.com/pablolmedorado/temat/commit/73d80cda1fabfa38820341156c832a69a894d540))

## [1.13.0](https://github.com/pablolmedorado/temat/compare/v1.12.1...v1.13.0) (2021-06-28)


### Features

* **user-stories:** add links to epics and sprints ([6f0d8c1](https://github.com/pablolmedorado/temat/commit/6f0d8c1853203922457918640bd1946f18b9eb84))


### Bug Fixes

* **frontend:** add missing services after models refactor ([d4f4d32](https://github.com/pablolmedorado/temat/commit/d4f4d32cc66b3dfdb5f8a044dab94e7d98d8eb01))

### [1.12.1](https://github.com/pablolmedorado/temat/compare/v1.12.0...v1.12.1) (2021-06-27)


### Bug Fixes

* **routes:** provide fallback route to router guards ([f49f567](https://github.com/pablolmedorado/temat/commit/f49f567a8780393b7c7444fab340b842c6838c17))
* **user-stories:** hide action button when external resource is empty ([d6bda21](https://github.com/pablolmedorado/temat/commit/d6bda21605d1fca47fd26b65e7db3828f83b1fbc))
* **user-stories:** improve effort pie chart by adding a 10% error margin ([10c3cd3](https://github.com/pablolmedorado/temat/commit/10c3cd32144744eb10cb00489be7be40d0cff4bf))
* **user-stories:** update tab tables (task & effort) after changing the route ([c00943f](https://github.com/pablolmedorado/temat/commit/c00943f57c84a64e2b8a8a8e9249b05271db3f27))

## [1.12.0](https://github.com/pablolmedorado/temat/compare/v1.11.0...v1.12.0) (2021-06-21)


### Features

* **scrum:** add external resource field to user stories ([6840adb](https://github.com/pablolmedorado/temat/commit/6840adbc2c31dd5e86150630bc65af07b0080ee3))


### Bug Fixes

* **calendar:** fix event card v-menu width ([a00f502](https://github.com/pablolmedorado/temat/commit/a00f5024e40bf1a3521f7dc7558ae943541fdc19))
* **frontend:** show snackbar on network error ([bfc022a](https://github.com/pablolmedorado/temat/commit/bfc022ad75a90ad37d85227d0eb3674a354e78a3))
* **frontend:** use route path instead of route name as keep-alive key ([44356b6](https://github.com/pablolmedorado/temat/commit/44356b6805675760deea2b9f185da1ba5f4ca390))
* **holidays:** add holiday admins to holidays request notifications ([f9ee27a](https://github.com/pablolmedorado/temat/commit/f9ee27a0cab3198cb84bfaf08d4efc7fab472491))

## [1.11.0](https://github.com/pablolmedorado/temat/compare/v1.10.1...v1.11.0) (2021-06-13)


### Features

* use django permissions to allow/deny actions ([460d028](https://github.com/pablolmedorado/temat/commit/460d0288429d5c4cb04523a38552580f70b641ef))

### [1.10.1](https://github.com/pablolmedorado/temat/compare/v1.10.0...v1.10.1) (2021-06-10)


### Bug Fixes

* **frontend:** add css source maps to vue config ([9dab499](https://github.com/pablolmedorado/temat/commit/9dab4997fa574214bbb435f247fa4de2c4a6ded0))
* **frontend:** change navbar user menu and links visibility in small screens ([ddac69d](https://github.com/pablolmedorado/temat/commit/ddac69da9b65f22081fd0afc59dc285c5bf6d9f6))
* **frontend:** minor ui improvements ([ff06f93](https://github.com/pablolmedorado/temat/commit/ff06f931fe52dda8bc2599498a7ca20010e8597e))
* **holidays:** fix user holidays fetch after migrating to composition API ([b0c0f76](https://github.com/pablolmedorado/temat/commit/b0c0f76118db28a9da73d25d8dd4fe6f6617d1ac))

## [1.10.0](https://github.com/pablolmedorado/temat/compare/v1.9.3...v1.10.0) (2021-05-18)


### Features

* add links feature ([f50e6a8](https://github.com/pablolmedorado/temat/commit/f50e6a8881eac712aded9eb6a95842bf6c27fdaf))
* **breakfasts:** add copy to clipboard feature ([64de989](https://github.com/pablolmedorado/temat/commit/64de989c600b88a2c36521c3917d9a74f688ba5b))


### Bug Fixes

* **calendar:** debounce event fetching function to avoid unnecessary calls ([9aa9f59](https://github.com/pablolmedorado/temat/commit/9aa9f59791fcd6b48a52b2904aea0d401d5c194b))
* **frontend:** fix multiline v-data-table headers ([a65f67a](https://github.com/pablolmedorado/temat/commit/a65f67abc86a77cbba06478c3a3d9718815755d3))
* **frontend:** remove primary color from text buttons ([abcca73](https://github.com/pablolmedorado/temat/commit/abcca73e8025e593bd120161040fa4beaa0ed685))
* **holidays:** fetch used dates on holiday cancel ([8d67379](https://github.com/pablolmedorado/temat/commit/8d67379ac8ce1a998023afa8d8aa96dae5e63083))
* **scrum:** allow scroll in kanban view when fullscreen mode is active ([3cc2e42](https://github.com/pablolmedorado/temat/commit/3cc2e421477bada8274f9bf98136f786c94fa6db))
* **sprints:** fix sprint basic filters ([47431e5](https://github.com/pablolmedorado/temat/commit/47431e5d49cb8cc50a862df94a78c1f214708dd3))
* fix misc errors found during tests ([e5f0e19](https://github.com/pablolmedorado/temat/commit/e5f0e19a5e79287d13748990b9cd5920bca9b4c0))

### [1.9.3](https://github.com/pablolmedorado/temat/compare/v1.9.2...v1.9.3) (2021-04-11)


### Bug Fixes

* **user-stories:** add warning message when user tries to change tab without saving ([2c146b1](https://github.com/pablolmedorado/temat/commit/2c146b1ea2852220cbd8ec05af792fea375b9057))

### [1.9.2](https://github.com/pablolmedorado/temat/compare/v1.9.1...v1.9.2) (2021-03-23)


### Bug Fixes

* **user-stories:** fix epic & sprint ordering ([1a85ecd](https://github.com/pablolmedorado/temat/commit/1a85ecd6a10197ae54b31ce533d7ece7be68b41c))

### [1.9.1](https://github.com/pablolmedorado/temat/compare/v1.9.0...v1.9.1) (2021-02-10)


### Bug Fixes

* **calendar:** allow new lines in event details representation ([098e30f](https://github.com/pablolmedorado/temat/commit/098e30f7c76d3326bf8df8cfdb12fe795b983d26))
* **sprints:** fix duplicated developers issue in deployment report ([8d392d8](https://github.com/pablolmedorado/temat/commit/8d392d82a7def3945d06c571f3d8ff54871b2942))
* **user-stories:** fix issue with unsaved changes warning when validating a record ([505632d](https://github.com/pablolmedorado/temat/commit/505632dca518c6284797dc4e4f81097225ce8da5))

## [1.9.0](https://github.com/pablolmedorado/temat/compare/v1.8.0...v1.9.0) (2021-02-07)


### Features

* **sprints:** add deployment report view ([fa3c35b](https://github.com/pablolmedorado/temat/commit/fa3c35b410a5fa138e15403aec8546f544b05d09))
* **user-stories:** use mdi icon in user story priority field ([a7853f0](https://github.com/pablolmedorado/temat/commit/a7853f061b6ec63c650be117eaf0f66b364c083a))


### Bug Fixes

* **backend:** add missing user manager migration ([aae10d1](https://github.com/pablolmedorado/temat/commit/aae10d1c5172f193955b3a1a971ae6acefa5ddda))
* **frontend:** fix spacing after vuetify internal changes ([6b06578](https://github.com/pablolmedorado/temat/commit/6b065782b4a9b7726b5a07226b9d955f2a7aaaea))
* **frontend:** move/hide outer form field icons ([ff908b2](https://github.com/pablolmedorado/temat/commit/ff908b2e8758acfd35df7afc14ea79c76e994198))
* **frontend:** set keep-alive to false in sprint views ([f107fd6](https://github.com/pablolmedorado/temat/commit/f107fd677b62195cbaae3e46029083068e2341ef))
* **frontend:** use pre-wrap to allow new lines in truncated text ([b98d75c](https://github.com/pablolmedorado/temat/commit/b98d75c72cff70308ee9cd26c582670f301efff7))
* **notifications:** improve notifications readability adding "" to the notification target ([b8361db](https://github.com/pablolmedorado/temat/commit/b8361db4b5b8cc09aee039686b1571e769ef066b))
* **notifications:** mark notifications as read before navigate ([f7a9bee](https://github.com/pablolmedorado/temat/commit/f7a9bee8503ef495763ecd9e495a9bc5c6090f0c))
* **user-stories:** fix issue with unsaved changes warning on new records ([5feaa49](https://github.com/pablolmedorado/temat/commit/5feaa49198aa8da5e84739cbe97e9f33636bb89c))
* **users:** fix active/inactive user issues ([f54e25d](https://github.com/pablolmedorado/temat/commit/f54e25d979b426d9d76e88e9fad77747fce69d68))

## [1.8.0](https://github.com/pablolmedorado/temat/compare/v1.7.0...v1.8.0) (2021-01-31)


### Features

* **frontend:** include confirmation before leaving an unsaved form ([7377d60](https://github.com/pablolmedorado/temat/commit/7377d60b22e1504b42c8dff241ff740b7a6d5aa4))


### Bug Fixes

* **backend:** exclude inactive users ([5eea7e6](https://github.com/pablolmedorado/temat/commit/5eea7e6726f55845be690548bd19f2b6e7b1da90))
* **devcontainer:** fix typo in python language server setting ([9e1dd9c](https://github.com/pablolmedorado/temat/commit/9e1dd9c1fea3aaa7bc7acea21f0750c4b4e2c5d9))
* **frontend:** fix dark mode colours not working on app reload ([b7b343f](https://github.com/pablolmedorado/temat/commit/b7b343fa52da72f82267c477ba91e007c8949298))
* **sprints:** add user story counter on sprint kanban ([0d4d6a1](https://github.com/pablolmedorado/temat/commit/0d4d6a16277b7cd80080916001efd13b043d0cb3))

## [1.7.0](https://github.com/pablolmedorado/temat/compare/v1.6.2...v1.7.0) (2021-01-24)


### Features

* **frontend:** add new lopera sentence (Lopera vs Cuervas) ([ed0cf4d](https://github.com/pablolmedorado/temat/commit/ed0cf4d37bd7f4776ed9f08afae972aef7790519))
* **notifications:** add mark as read button in all notifications ([b80e3e4](https://github.com/pablolmedorado/temat/commit/b80e3e437d7c3e07d62f64cc8c52e3aaf1cb7bd3))


### Bug Fixes

* **frontend:** adapt clearable fields to new vuetify's behaviour ([2c94ebf](https://github.com/pablolmedorado/temat/commit/2c94ebf7ecf737c3b6ee621cf2e43a0bec275a9e))
* **frontend:** fix potential issue with xmas hat and long version numbers ([db5f3cd](https://github.com/pablolmedorado/temat/commit/db5f3cd5e0d57dfd48217d0151303a3d68bed05e))
* **frontend:** replace v-card-title by v-toolbar to improve readability in dark mode ([093b846](https://github.com/pablolmedorado/temat/commit/093b8466a1f03a5759f204b7c2213890f7ac464a))

### [1.6.2](https://github.com/pablolmedorado/temat/compare/v1.6.1...v1.6.2) (2020-12-03)


### Bug Fixes

* **login:** hide 'next' warning when the url is from the spa ([d0901cc](https://github.com/pablolmedorado/temat/commit/d0901cc03daffa225e493d6478cf705a1d8f0f1a))
* **urls:** remove fallback url to get 404 if an url does not exist ([043e716](https://github.com/pablolmedorado/temat/commit/043e71624deabe0d1f7654da00e83c5cd42ba9f1))

### [1.6.1](https://github.com/pablolmedorado/temat/compare/v1.6.0...v1.6.1) (2020-11-23)


### Bug Fixes

* **scrum:** fix lazy serializer imports after the reorganization ([445eadb](https://github.com/pablolmedorado/temat/commit/445eadb6e7eeffa1074a9b9fc450a1e2275caa6a))

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
