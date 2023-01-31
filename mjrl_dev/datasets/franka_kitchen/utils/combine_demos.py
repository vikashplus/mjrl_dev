"""
Combine all the individually parsed demonstrations into
a single pickle file for easy downstream learning
"""

import os, pickle, click

DESC = '''
Script to combine (concatenate) all the demonstration data into a single file
    $ python combine_demos.py --demo_dir <path/to/kitchen_demos_multitask>\n
'''

@click.command(help=DESC)
@click.option('--demo_dir', type=str, help='path to the kitchen dataset directory', required=True)
def main(demo_dir):
    all_paths = concatenate_demos(demo_dir)
    pickle.dump(all_paths, open(demo_dir + '/kitchen-v3_all_parsed_paths.pkl', 'wb'))

def concatenate_demos(demo_dir):
    all_paths = []
    for task in os.listdir(demo_dir):
        demo_file = demo_dir + '/' + task + '/' + 'kitchen-v3_full_demos.pkl'
        print("Parsing file : " + demo_file)
        try:
            paths = pickle.load(open(demo_file, 'rb'))
        except:
            print("Unable to load data from " + task)
            paths = []
            pass
        all_paths = all_paths + paths
    return all_paths

if __name__ == '__main__':
    main()
