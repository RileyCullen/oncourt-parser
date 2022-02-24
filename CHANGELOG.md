# Change Log
## [v0.1.4] - 2022-02-23
Minor patch, issues 9 and 11 fixed
### Changed
* Special case for calculating point winner when the current frame is the frame after p2 had an advantage (A) and p1 scores (i.e. \[40-A\] -> \[40-40\])
* Point number counter only increments on actual point entries
## [v0.1.3] - 2022-02-21
Minor patch, issue number 7 fixed
### Changed
* PlayByPlayDriver now considers difference from current point score when compared to previous point score when determining the point winner
## [v0.1.2] - 2022-02-17
Minor patch, issue number 6 (where parser fails on certain inputs) fixed
### Changed
* End cases added to PlayParser and PlayByPlayDriver. For the PlayParser, end case no longer calls updateMatchScore
## [v0.1.1] - 2022-02-14
### Changed
* Issue number 5 (bug where square brackets are written to output file) fixed
## [v0.1.0] - 2022-02-11
### Added 
* PlayByPlay driver defined and implemented
### Changed
* PlayParser output format updated. Now writes "EndGame" when game is finished and "EndSet" when a set is finished
## [v0.0.3] - 2022-01-28
### Added
* Play-by-play parser integrated into system
## [v0.0.2] - 2022-01-26
### Added
* Progress bar type defined and implemented
### Changed
* Progress bar and other status output added
* Output format for parse_file cleaned
## [v0.0.1] - 2022-01-25
### Added
* Functions main, run, get_file_paths, and parse_file defined and partially implemented
* Function run implemented to call parse_file for each input file
* Function parse_file updated to read tournament, player names, date, and odds from input file
