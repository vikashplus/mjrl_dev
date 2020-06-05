"""Method to handle getting command line arguments.

Don't add additional dependencies here as ths is used by both job_script_mjrl.py
and train.py.
"""

import argparse

def get_args(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(
            # Show default value in the help doc.
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument('-c', '--config', nargs='*', default=['job_data_mjrl_0.txt'], help=(
        'Path to the job data config file(s). Multiple config files can be '
        'passed (space-separated list of paths). Globs (*) are supported. '
        'If a directory is given, any .txt file is read as a config.'
    ))
    parser.add_argument('-o', '--output_dir', default='.', help=(
        'Directory to output trained policies, logs, and plots. A subdirectory '
        'is created for each job.'
    ))
    parser.add_argument('-p', '--parallel', action='store_true', help=(
        'Whether to run the jobs in parallel.'
    ))
    parser.add_argument('--num_cpu', default=0, type=int, help=(
        'The number of CPUs to use in each job (for sampling rollouts in '
        'parallel). If not given, the number of CPUs to use is read from the '
        'job config.'
    ))
    parser.add_argument('--hardware', action='store_true', help=(
        'Run the jobs on the real hardware robot. This forces sequential job '
        'execution on 1 CPU.'
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
    parser.add_argument('--tensorboard', action='store_true', help=(
        'Output Tensorboard data. The data is saved to the "tensorboard" '
        'directory within the output folder.'
    ))
    parser.add_argument('--email', default=None, help=(
        'Send email about job progress and completion to provided address'
    ))
    parser.add_argument('--sms', default=None, help=(
        'Send sms about job progress and completion to provided sms gateway.\
         Find your SMS gateway here -- https://en.wikipedia.org/wiki/SMS_gateway'
    ))
    parser.add_argument('-i', '--include', type=str, default=None, help='task suite to import')
    
    return parser.parse_args()
