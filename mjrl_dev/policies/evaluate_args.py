"""Method to handle getting command line arguments.

Don't add additional dependencies here as ths is used by both examine_policy.py
and evaluate.py.
"""

import argparse

DESCRIPTION = '''
Helper script to visualize a NPG policy.\n
USAGE:
    1. Visualize env with a random policy
        python examine_policy.py -e <name>
    2. Visualize env with the saved policy
        python examine_policy.py -e <name> -p "saved"
    3. Visualize env with the specific policy
        python examine_policy.py -e <name> -p <policy_with_path>
'''

def get_args(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(
            description=DESCRIPTION,
            # Show default value in the help doc.
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument('-e', '--env_name', required=True, help=(
        'The name of the environment to load. See the __init__.py files in '
        'the adept_envs module (e.g. "adept_envs/dclaw/__init__.py").'
    ))
    parser.add_argument('-p', '--policy', default='', help=(
        'The path of the policy (.pickle) to execute. "saved" will load '
        'best_policy.pickle in the adept_envs/mjrl/policies directory.'
    ))
    parser.add_argument('-m', '--mode', default='evaluation',
        choices=['exploration', 'evaluation'], help=(
        'Whether to run the policy in exploration or evaluation mode.'
    ))
    parser.add_argument('-n', '--num_episodes', default=10, type=int, help=(
        'The number of episodes the evaluate.'
    ))
    parser.add_argument('-s', '--num_samples', default=0, type=int, help=(
        'The number of samples to save.'
    ))
    parser.add_argument('-f', '--filename', default='newvideo', help=(
        'The name to save the rendered video as.'
    ))
    parser.add_argument('-r', '--render', default='onscreen',
        choices=['onscreen', 'offscreen'], help=(
        'Whether to render to a window onscreen, or headless offscreen.'
    ))
    parser.add_argument('--hardware', action='store_true', help=(
        'Run the evaluation on the real hardware robot.'
    ))
    parser.add_argument('--legacy', action='store_true', help=(
        'Uses the DynamixelSDK to communicate with the robot instead of DDS.'
    ))
    parser.add_argument('--device', help=(
        'The device path in /dev/ for the robot. Only needed in legacy mode.'
    ))
    parser.add_argument('--overlay', action='store_true', help=(
        'Show an window that renders the hardware joint positions.'
    ))
    parser.add_argument('--calibration_mode', action='store_true', help=(
        'Disengage the motors for calibration measurement.'
    ))
    parser.add_argument('-i', '--include', default='', help=(
        'task suite to import'
    ))
    parser.add_argument('-d', '--seed', default=123, type=int, help=(
        'random number seed'
    ))
    parser.add_argument('-l', '--log_std', default=0, type=float, help=(
        'log std of random policy or addional noise to add to provided policy'
    ))
    return parser.parse_args()
