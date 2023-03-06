# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.3.0] - 2022-12-01
### Added:
- access historical quotes/trades endpoints
- filtering instruments updated since a specific point in time

## [1.2.0] - 2022-09-29
### Added:
- `auto_iter()` on list responses to automatically iterate through the pages of the response.This method respects by default the rate limits.


## [1.1.1] - 2022-08-24
### Added:
- "expires_at" used in create order call can accept strings in format "pXd"/"Xd" where X is a non-negative integer


## [1.1.0] - 2022-07-19
### Added:
- allow multiple order status query
- add live streaming support

### Changed:
- use env='live' rather than env='money', latter one is deprecated and will be removed in future SDK versions


## [1.0.5] - 2022-07-15
### Fixed
- lemon package is now available for python 3.7 again

## [1.0.4] - 2022-07-15
### Fixed
- urllib3 package version should be >=1.26.0

## [1.0.3] - 2022-06-22
### Changed
- filter out optional query parameters and optional payload attributes from queries

### Fixed
- updated README.md in market data part to add missing period params

## [1.0.2] - 2022-06-21
### Changed
- include README.md and CHANGELOG.md in package description

### Fixed
- fix license badge
- relax the requirements

## [1.0.0]  - 2022-06-21
### Added
- initial commit providing base SDK functionality
