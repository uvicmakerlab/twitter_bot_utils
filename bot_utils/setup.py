import logging
import argparse
from os import environ, path
from sys import stdout


def add_default_args(parser):
    parser.add_argument('-c', '--config', metavar='PATH', default=None, type=str, help='path to config file to parse (json or yaml)')

    parser.add_argument('--key', type=str, help='Twitter user key')
    parser.add_argument('--secret', type=str, help='Twitter user secret')
    parser.add_argument('--consumer-key', type=str, help='Twitter application consumer key')
    parser.add_argument('--consumer-secret', type=str, help='Twitter application consumer secret')

    parser.add_argument('--since-id-file', type=str, help='path of JSON file with since IDs')

    parser.add_argument('-n', '--dry-run', action='store_true', help="Don't tweet, just output to stdout")
    parser.add_argument('-v', '--verbose', action='store_true', help="Log to stdout")


def defaults(screen_name, args):
    '''Interpret default args, set up API'''
    logger = logging.getLogger(screen_name)

    if args.config:
        logger.info('Using custom config file: {0}'.format(args.config))
    else:
        logger.info('Trying to use a default config')

    if args.verbose:
        add_stdout_logger(screen_name)


def setup_args(botname, description):
    '''Set up an general argument parsing, logging'''
    add_logger(botname)

    parser = argparse.ArgumentParser(description=description)
    add_default_args(parser)

    return parser


def log_threshold():
    if environ.get('DEVELOPMENT', False) and not environ.get('production', False):
        # environment = 'development'
        threshold = logging.DEBUG
    else:
        # environment = 'production'
        threshold = logging.INFO

    return threshold


def add_logger(logger_name, log_path="bots/logs"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_threshold())

    log_file = path.join(path.expanduser('~'), log_path, logger_name + '.log')
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('%(asctime)s %(name)-13s line %(lineno)d %(levelname)-5s %(message)s'))

    logger.addHandler(fh)

    return logger


def add_stdout_logger(logger_name):
    logger = logging.getLogger(logger_name)

    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(filename)-10s %(lineno)-3d %(message)s'))

    logger.addHandler(ch)
