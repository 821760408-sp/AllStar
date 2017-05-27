from __future__ import print_function
from getpass import getpass
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from github import Github, AuthenticatedUser
from github.GithubException import UnknownObjectException
import sys
import argparse


FOLLOW_ALL = True
NUM_THREADS = 1


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError(
            'negative value {} is invalid'.format(value))
    return ivalue


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Star all repos from people you follow.')
    parser.add_argument(
        '--user',
        help='name of the user whose repos you wanna star.')
    parser.add_argument(
        '--threads',
        type=check_positive,
        default=NUM_THREADS,
        help='number of threads (default = 1)')
    return parser.parse_args()


def star_them_all(repos, user):
    assert isinstance(user, AuthenticatedUser.AuthenticatedUser)
    for repo in repos:
        # COMMENT OUT FOR SAVING API CALLS
        # if not user.has_in_starred(repo):
        # TODO: cache starred repo to guard agianst API rate limit
        print('staring repo: {}'.format(repo.full_name))
        user.add_to_starred(repo)


def main():
    args = get_arguments()
    n_threads = args.threads

    login_or_token = raw_input(
        'Enter your Github login or token: ')
    password = getpass()
    
    try:
        g = Github(login_or_token, password)

    except AssertionError as e:
        print(e)
        sys.exit(1)

    # Get user
    me = g.get_user()

    if args.user:
        whosname = args.user
        FOLLOW_ALL = False

    if FOLLOW_ALL:
        # Get user's followings
        following = me.get_following()

        # Get all public repos of all users
        repos_of_all = []
        for f in following:
            repos_of_all.append(f.get_repos())

        # Create partial method
        partial_star = partial(star_them_all, user=me)

        # Get the pool of workers
        pool = ThreadPool(n_threads)
        # Star all repos of all followings
        _ = pool.map(partial_star, repos_of_all)
        # Close the pool
        pool.close()
        pool.join()
    else:
        try:
            who = g.get_user(whosname)
            repos = who.get_repos()
            star_them_all(repos, me)
        except UnknownObjectException as e:
            print('The user you are trying to follow does not exist.')


if __name__ == '__main__':
    main()