## How to get the parsed dataset?

**TODO:** Add download link to goal-relabeled dataset here once ready.

Follow the steps below if you would like to re-parse the demos.

1. Download the raw dataset. This will be in the form of a zip file. Unzip the file to get a directory named `kitchen_demos_multitask`. Place the directory in here, i.e. `mjrl_dev/franka_kitchen/kitchen_demos_multitask`.
```
$ wget https://github.com/google-research/relay-policy-learning/raw/master/kitchen_demos_multitask.zip
$ unzip kitchen_demos_multitask.zip
```
NOTE: In case the above download link doesnt work, you can get the data from the team google drive: [link](https://drive.google.com/file/d/1FY-zP6PrJ5QnqWFo6jNaSHNxCsOHxEpU/view?usp=sharing)

2. The directory will contain multiple sub-directories, each corresponding to different sub-task sequences in the environment.

3. An example to parse one of the above task combinations is provided in `demo_parsing_example.sh`, which will also perform playback rendering to provide a visual description. This file is for illustration, you don't have to run it for getting the final dataset.

5. Run the script `parse_all_demos.sh` which will parse all the demonstrations across all the task combinations, and will provide a concatenated pickle file containing the demonstrations: `kitchen_demos_multitask/kitchen-v3_all_parsed_paths.pkl`

6. You can visualize the parsed demonstrations for final checking with:
```
python utils/visualize_demos.py --env kitchen-v3 --data kitchen_demos_multitask/kitchen-v3_all_parsed_paths.pkl
```

## Goal Relabeling

The raw human data is not goal directed and is play data. As a result, the goal fields are not populated (they contain default values of 0). In order to populate the goal fields for goal-conditioned BC, we can relabel the goals using the state of the objects at some point in the future (called `shift_window`). A script to do this is provided and can be used as:

```
python utils/basic_goal_relabeling.py --shift_window_lower 30 -- shift_window_upper 30 --data <path/to/file.pkl>
```

The shift window is a hyper-parameter and heuristic. We do not want to pick it too small, since we may not see any variation in the object (goal) positions. If we pick it too large, then multiple goals may have been accomplished in the shift_window. An intermediate sweet spot for the kitchen environment seems to be around 30.

The above script allows the option to relabel shift windows from a lower bound to an upper bound by granularity (i.e. we can relabel a dataset from a shift window of 10 through a shift window of 30 (producing corresponding saved .pkl files) in granularity of 2).

```
python utils/basic_goal_relabeling.py --shift_window_lower 10 -- shift_window_upper 50 --granularity 2 --data <path/to/file.pkl>
```