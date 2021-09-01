"""
Split demos into train/test split
"""

import os
import pickle
import click
import random

DESC = '''
Script to split parsed demos into train/test split
    $ python split_train_test.py --demo_dir <path/to/kitchen_demos_multitask> --train_split .8 \n
'''

@click.command(help=DESC)
@click.option('--demo_dir', type=str, help='path to the kitchen dataset sub-directory', required= True)
@click.option('--train_split', type=float, help='percentage to split into training set', default=.8)

def main(demo_dir, train_split):
    demo_file = demo_dir+'/kitchen-v3_full_demos.pkl'
    demos = pickle.load(open(demo_file, 'rb'))

    random.shuffle(demos)

    train_data = demos[:int(len(demos)*train_split)]    # takes train+test randomly according to split
    test_data = demos[int(len(demos)*train_split):]
    pickle.dump(train_data, open(demo_dir + '/train.pkl', 'wb'))
    pickle.dump(test_data, open(demo_dir + '/test.pkl', 'wb'))

if __name__ == '__main__':
    main()
