# Change Log
## [v1.0.0] - 2022-04-15
Major changes. Parser now supports writing to a database (in addition to writing to excel files). To account for this change, the parser's script arguments have been updated (see README.md)
## Added 
* GameStatus column added. This contains values like "In-progress", "EndGame", "EndSet", and "End"
* Screw up score added
* DBConnection type defined 
* Functions for populating database added
* Module pyodbc added to package
## Changed
* Command line arguments updated
* Score broken down into P1Score and P2Score
* clean_player_name in OnCourtDriver updated to remove multiple digits from player's name
* Function parse_play_dataframe updated to yield parse data instead of directly adding it to a DataFrame
## [v0.2.1] - 2022-03-07
### Added
* ServerVerifier type defined and implemented
### Changed
* PlayVerifier updated to use ServerVerifier type
## [v0.2.0] - 2022-02-28
Data verification module added
### Added
* AVerifier, PlayVerifier, PointVerifier, and VerificationStatus types defined and implemented
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
