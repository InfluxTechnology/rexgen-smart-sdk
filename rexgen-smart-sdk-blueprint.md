# Rexgen Smart SDK Blueprint

## 1. Цел

Да се трансформира текущият Yocto/BSP stack около `influx-yocto-base` в официален, поддържан и използваем `Rexgen Smart SDK`, чрез който разработчик да може:

1. да разбере архитектурата на Rexgen Smart;
2. да подготви поддържана host среда;
3. да build-не официален image;
4. да flash-не устройство безопасно;
5. да инсталира SDK/toolchain;
6. да build-не и пусне пример;
7. да разработва Linux-side приложение чрез документирани API;
8. да знае какво е поддържано и какво не.

## 2. Какво НЕ е достатъчно

Текущият Yocto release не е SDK, защото в момента покрива главно:

- repo manifests;
- layer composition;
- machine configuration;
- image build;
- platform engineering setup.

Това е добра основа за BSP, но не е завършен developer product.

## 3. Целеви резултат

`Rexgen Smart SDK` трябва да бъде официалният developer package за Linux-side разработка върху Rexgen Smart.

Той трябва да съдържа:

- официален entry-point repository;
- документация за архитектурата и supported flow;
- API boundary;
- SDK/eSDK или еквивалентен developer artifact;
- примери и templates;
- tooling за build, flash и debug;
- release process;
- security и support policy.

## 4. Кардинални промени

### A. Промяна на продуктния модел

Трябва да се разделят ясно три неща:

1. `Platform/BSP`
   Това е Yocto основата, layers, machine config, image recipes, boot artifacts.
2. `SDK`
   Това е developer-facing пакетът за писане на приложения върху Rexgen Smart.
3. `Product image / production release`
   Това е release image за устройство с production security posture.

Без това разделение всичко остава смесено и объркващо.

### B. Нов публичен entry point

Трябва да има нов repo:

`rexgen-smart-sdk`

Той не трябва просто да бъде rename на `influx-yocto-base`, а продуктово подреден вход към цялото решение.

### C. От BSP към developer experience

Текущият flow е BSP-centric:

- `repo init`
- `repo sync`
- `source ...`
- `bitbake ...`

Целевият flow трябва да е developer-centric:

- clone
- setup host
- build image
- build SDK
- flash
- run example
- start app development

### D. Формален SDK artifact

Трябва да има ясен инсталируем или архивируем artifact, например:

- `rexgen-smart-sdk-<version>.sh`
- `rexgen-smart-esdk-<version>.sh`
- `rexgen-smart-image-dev-<version>.wic.zst`
- `rexgen-smart-image-production-<version>.wic.zst`
- checksums
- SBOM
- release notes

### E. Публична API граница

Трябва да се дефинира кои интерфейси са официални за Linux-side development:

- комуникация с Rexgen Core;
- CAN send/receive;
- status/state APIs;
- configuration APIs;
- logging and diagnostics;
- application lifecycle hooks;
- error model.

### F. Security by design

SDK и production image не могат да разчитат на:

- известни root пароли;
- passwordless users;
- лични credentials в public README;
- mutating setup scripts с неясни side effects.

### G. Release engineering като продуктова дисциплина

Всяка версия трябва да има:

- version tag;
- release notes;
- compatibility matrix;
- checksums;
- SBOM;
- known limitations;
- support statement.

## 5. Целева структура на решението

```text
rexgen-smart-sdk/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── SECURITY.md
├── SUPPORT.md
├── COMPATIBILITY_MATRIX.md
├── docs/
├── api/
├── examples/
├── templates/
├── tools/
└── platform/
    └── yocto/
```

### Примерно съдържание

`docs/`

- `overview.md`
- `hardware-architecture.md`
- `rexgen-core-integration.md`
- `rexgenlibrary-positioning.md`
- `getting-started.md`
- `host-setup.md`
- `yocto-build.md`
- `sdk-install.md`
- `flashing.md`
- `mender-update.md`
- `api-reference.md`
- `troubleshooting.md`

`api/`

- public headers;
- user-space library;
- optional bindings;
- API versioning notes.

`examples/`

- `hello-rexgen-smart`
- `core-status`
- `can-send-receive`
- `socketcan-example`
- `lte-status`
- `wifi-status`
- `mqtt-publisher`

`tools/`

- `setup-env.sh`
- `build-image.sh`
- `build-sdk.sh`
- `flash-device.sh`
- `collect-debug-info.sh`

## 6. Задължителни workstreams

### Workstream 1: Product Definition

Цел:
Да се фиксира какво точно е Rexgen Smart SDK и за кого е.

Deliverables:

- one-page product definition;
- supported audience definition;
- supported use cases;
- non-goals;
- naming and positioning rules.

Acceptance:

- няма противоречие между marketing, CTO и engineering;
- еднаква терминология навсякъде.

### Workstream 2: Architecture & Boundaries

Цел:
Да се документират Rexgen Smart, Rexgen Core, RexgenLibrary и Linux host integration.

Deliverables:

- architecture diagram;
- component responsibilities;
- data flow over USB;
- dependency map;
- public/internal boundary.

Acceptance:

- нов инженер може да разбере системата без устно обяснение.

### Workstream 3: Repository & Layout

Цел:
Да се изгради SDK repo моделът.

Deliverables:

- `rexgen-smart-sdk` repo;
- folder structure;
- README;
- docs skeleton;
- examples skeleton;
- tooling skeleton.

Acceptance:

- repo-то изглежда като SDK още от първия екран.

### Workstream 4: Yocto/BSP Cleanup

Цел:
Да се изчисти BSP основата, така че да бъде стабилен backend за SDK.

Deliverables:

- премахване на runtime mutation на upstream layers;
- `.bbappend`/patch discipline;
- clean image recipes;
- image split по профили;
- machine config cleanup;
- deploy flow cleanup.

Acceptance:

- clean build от fresh checkout;
- reproducible build behavior;
- без manual patching след sync.

### Workstream 5: Security Hardening

Цел:
Да се отстранят всички release-blocking security слабости.

Deliverables:

- премахнати default passwords;
- премахнати passwordless users;
- премахнати credential leaks от docs;
- secure provisioning policy;
- dev vs production security separation.

Acceptance:

- няма shared credentials в release paths;
- SDK docs не изискват персонални токени по неподходящ начин.

### Workstream 6: API & Runtime Contract

Цел:
Да има реален и стабилен developer contract.

Deliverables:

- public headers/interfaces;
- API reference;
- error handling model;
- versioning policy;
- deprecation policy.

Acceptance:

- разработчик може да пише app без reverse engineering на pipes и scripts.

### Workstream 7: Examples & Templates

Цел:
Да има working starting point за нови разработчици.

Deliverables:

- минимум 5-7 runnable examples;
- application template project;
- example README files;
- expected outputs and validation steps.

Acceptance:

- примерите build-ват и работят на поддържан hardware revision.

### Workstream 8: SDK Artifact Generation

Цел:
Да има формален SDK deliverable.

Deliverables:

- Yocto SDK/eSDK generation или одобрен алтернативен формат;
- install guide;
- versioned artifact naming;
- host compatibility notes.

Acceptance:

- developer може да инсталира SDK и да build-не app без да разбира целия BSP internals.

### Workstream 9: Release Engineering

Цел:
Да се въведе release discipline.

Deliverables:

- tagging strategy;
- changelog process;
- release notes template;
- checksum publishing;
- SBOM generation;
- artifact retention policy.

Acceptance:

- всеки release е проследим и възпроизводим.

### Workstream 10: CI, QA and Hardware Validation

Цел:
Да има обективна увереност, че SDK е usable.

Deliverables:

- parse/build smoke checks;
- packaging QA;
- example build tests;
- hardware validation checklist;
- first-run success checklist.

Acceptance:

- release кандидат минава автоматични проверки и ръчна hardware валидация.

## 7. Последователност на изпълнение

### Phase 0: Definition

- фиксиране на scope;
- naming;
- audience;
- supported hardware revisions;
- release model.

### Phase 1: Cleanup

- security cleanup;
- Yocto metadata cleanup;
- image split;
- deploy/tooling cleanup.

### Phase 2: SDK Foundation

- нов repo;
- docs skeleton;
- tools skeleton;
- API boundary draft;
- first examples.

### Phase 3: Formalization

- SDK/eSDK artifact generation;
- support/security policies;
- compatibility matrix;
- release notes and SBOM.

### Phase 4: Validation

- clean host onboarding test;
- hardware validation;
- partner dry run;
- first public/partner release candidate.

## 8. Минимален acceptance gate за версия 1.0

SDK 1.0 не трябва да се обявява преди да са изпълнени всички точки:

1. Има `rexgen-smart-sdk` repo с продуктово README.
2. Има официална архитектурна документация.
3. Има дефиниран public API boundary.
4. Има поне един formal SDK artifact.
5. Има dev image и production image с отделен security posture.
6. Има working flash flow.
7. Има working examples.
8. Има support policy.
9. Има release notes, checksums и SBOM.
10. Нов разработчик може да мине first-run flow без вътрешна помощ.

## 9. Конкретни кардинални решения, които трябва да вземем

Това са решенията, без които проектът ще остане "полу-SDK":

1. Дали `rexgen-smart-sdk` ще е manifest repo или umbrella repo с submodules/subtrees/referenced repos.
2. Дали официалният developer artifact ще е Yocto SDK, eSDK или custom packaged toolchain/sysroot.
3. Кой е официалният public API слой: директно `rexgen-linux-stream`, нов wrapper library или изцяло нов API library.
4. Дали `RexgenLibrary` остава отделен продукт или части от него влизат като reference/integration layer в Smart SDK.
5. Кои hardware revisions ще са официално supported за SDK 1.0.
6. Каква е границата между dev convenience и production security.
7. Какви примери са задължителни за първия release.

## 10. Най-важният принцип

Не трябва да се опитваме да "преименуваме BSP-то на SDK".

Трябва да направим продуктова трансформация:

- от build environment;
- към developer platform;
- с ясно обещание;
- ясни граници;
- ясни артефакти;
- и възпроизводим first-run успех.
