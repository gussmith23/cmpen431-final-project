# cmpen431-final-project

[Here's the VPN setup info.](http://www.cse.psu.edu/~yul189/cmpsc431w/lab.html)

## Pipeline
### 1. Configuration Generator
* **Input:** Directory to place configuration files in.
* **Output:** SimpleScalar simulation configuration files.
  * TODO Files should be of a specific format, [something about the sim].cfg.

### 2. Simulation Runner
* **Input:** Directory containing configuration files, directory to place simulation output files.
* **Output:** SimpleScalar simulation output files.

### 3. Output Parser
* **Input:** Directory containing output files, directory to place parsed output files.
* **Output:** Parsed output files.
  * TODO decide what exactly gets included.
  * TODO decide format - .csv?

### 4. Data Analyzer
* **Input:** Directory containing parsed output files, TODO something to specify where output should go (a filename, maybe?).
* **Output:** TODO decide how we output. A single analysis file?




#Random Thoughts
If we can figure out the replacement policy for the btb cache, and it's a locality-based policy, I think increasing the associativity would be helpful. There would be more collisions by nature, but if we assume the most likely branch to encounter is one which was most recently encountered (seems reasonable), the increased associativity in combination with the replacement policy would lead to having more prediction information ready on encountered branches overall. 

The 2-level branch predictor seems to be the 'smartest' of the schemes, it supposedly 'learns' the branch patterns fairly quickly.


Is it fair to isolate some other settings as having a general trend/relation to performance?
    We can only have 4 total arrith. units. having an extra of one of any of the 4 types will make the instructions that use it run faster, but screw the ones that would use the type with 0 units. One might  
