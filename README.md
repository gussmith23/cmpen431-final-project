# cmpen431-final-project

[Here's the VPN setup info.](http://www.cse.psu.edu/~yul189/cmpsc431w/lab.html)

## Pipeline
### 1. Configuration Generator
**Input:** Directory to place configuration files in.
**Output:** SimpleScalar simulation configuration files.
  * TODO Files should be of a specific format, [something about the sim].cfg.

### 2. Simulation Runner
**Input:** Directory containing configuration files, directory to place simulation output files.
**Output:** SimpleScalar simulation output files.

### 3. Output Parser
**Input:** Directory containing output files, directory to place parsed output files.
**Output:** Parsed output files.
  * TODO decide what exactly gets included.
  * TODO decide format - .csv?

### 4. Data Analyzer
**Input:** Directory containing parsed output files, TODO something to specify where output should go (a filename, maybe?).
**Output:** TODO decide how we output. A single analysis file?
