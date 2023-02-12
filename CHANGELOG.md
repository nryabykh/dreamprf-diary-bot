# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2002-02-13

## Fixed

- Global refactoring, change package structure. Separate layers from each other.

## [0.4.1] - 2022-02-09

## Fixed

- Add `isort` and `flake8`, fix their warnings.

## [0.4.0] - 2022-02-09

### Added

- Correct sheet name identification based on current date and course starting date.

## [0.3.1] - 2023-02-07

### Fixed

- Fix error when bot was unable to recognize a time of edited comment due to absence of leading zero in GSheets in times like 0:46.

## [0.3.0] - 2023-02-07

### Added

- Edit previously added comments via inline buttons (command `/last`)
- `start.sh` and `stop.sh` for easy starting and stopping the bot

### Fixed

- Fixed error if `user_sid.json` file didn't exist.

## [0.2.0] - 2023-02-03

### Added

- Register of night waking (commands `/night`, `/end`)
- Adding comments to the last night waking
- Storing spreadsheet ID in json-file for every user
- Extracting spreadsheet ID from the link to spreadsheet.

## [0.1.0] - 2023-02-01

### Added

- Init version
- Commands `/start`, `/help`
- Working with Google sheets: getting and updating data
