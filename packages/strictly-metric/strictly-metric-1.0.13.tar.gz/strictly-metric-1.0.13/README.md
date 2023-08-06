# Player Metrics: 
This repository contains the source code for the <em>#StrictlyBytheNumbers</em> PlayerMetric module. The PlayerMetric module attempts to provide key player metrics that could be then leveraged in a variety ways for a multitude of downstream baskebtall applications. 

## open source, you can publish by
- 1.) Change the version number in setup.py then publish
- 2.) python setup.py sdist
- 3.) twine upload --skip-existing dist/*


## Installation:

- 1.) Install python package depedencies.
```shell
$ pip install strictly-metric -U
```

## Example Usage:

```python

# Import python package
from player_metric import player_metric

# Instantiate player object
player_object = player_metric.PlayerMetric(df_all=df_all, df_boxscore=df_boxscore)

# Calculate aggregate and per game metrics for the player, based on df_all and df_boxscore.

player_object.calculate_aggregate_metric()
player_object.calculate_per_game_metric()

# Examine transformed data 

player_object.df_all.head()
player_object.df_boxscore.head()
```
