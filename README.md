# soccer-sensor-data-analysis

## Data set: 
   http://www.orgs.ttu.edu/debs2013/index.php?goto=cfchallengedetails

## To change computation and output settings:

- Change output time intervals and associated file names in ```output_time_intervals.py```
- Metadata of the game is registered in ```metadata.py```
- Other parameters are registered in ```parameters.py```

## To run

- Seperate the big input file ```full-game``` into 2 input files, ```full-game-1st``` and ```full-game-1st```, for 2 halves of the game:
   
   ```python3 chop_input.py```
- Generate triples for the first half:
  
   ```python3 full-game-parser.py full-game-1st 1```
  
   and for the second half:
  
   ```python3 full-game-parser.py full-game-2nd 2```

- Contatenate sample output into one whole file:

   ```cat sample-data-* > whole-game-triples```

### Note: But don't commit/push/upload these huge bulk files onto the github repo!
