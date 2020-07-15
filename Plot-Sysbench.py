#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import argparse
import json
import re

import matplotlib.pyplot as plt
import pandas as pd

import logger_config

goodline = re.compile('\[\s+\d+\w\s+\]')
to_graph = ['thds',
            'tps',
            'qps',
            'latency',
            'errors']


def parse_args():
    epilog_example = ''' '''
    actiondoc = ''' '''

    parser = argparse.ArgumentParser(description='Plot tests ran on MySQL/MaxScale by sysbench',
                                     epilog=epilog_example, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', help='Add a file to scrape list',
                        action='append', dest='file_list', default=['oltp_read_only_direct'])
    args = parser.parse_args()
    args.file_list = list(set(args.file_list))
    return args


def render(metrics):
    tmpd = {}
    locs = {}
    for metric in to_graph:
        for test in metrics:
            for m in metrics[test]:
                if m == metric:
                    if m not in tmpd:
                        tmpd[m] = pd.DataFrame()
                        locs[m] = 0
                    j = []
                    for val in metrics[test][m]:
                        j.append(float(val))
                    tmpd[m].insert(column=test, value=j, loc=locs[m])
                    locs[m] += 1

    for df in tmpd:
        tmpd[df].plot()
        logger.info('Rendering %s.png' % df)
        plt.title(df)
        plt.savefig(df+'.png', dpi=300, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format='png',
                    transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)


def prepare(series_json):
    metrics = {}
    logger.info('Peparing series ...')
    for test_names in series_json:
        for serie in series_json[test_names]:
            if test_names not in metrics:
                metrics[test_names] = {}
            for key in list(serie.keys()):
                if key != 'time' and key not in metrics[test_names]:
                    metrics[test_names][key] = []
                if key != 'time':
                    metrics[test_names][key].append(serie[key])

    return metrics


def extract_from_file():
    '''
    that format:
      [ 1s ] thds: 4 tps: 515.04 qps: 8282.50 (r/w/o: 7248.44/0.00/1034.06) lat (ms,95%): 11.04 err/s: 0.00 reconn/s: 0.00
      [ 2s ] thds: 4 tps: 586.16 qps: 9378.54 (r/w/o: 8206.22/0.00/1172.32) lat (ms,95%): 9.39 err/s: 0.00 reconn/s: 0.00
      [ 3s ] thds: 4 tps: 563.93 qps: 9027.92 (r/w/o: 7900.05/0.00/1127.86) lat (ms,95%): 9.73 err/s: 0.00 reconn/s: 0.00
      [ 4s ] thds: 4 tps: 580.00 qps: 9274.03 (r/w/o: 8114.03/0.00/1160.00) lat (ms,95%): 9.73 err/s: 0.00 reconn/s: 0.00
      [ 5s ] thds: 4 tps: 587.98 qps: 9424.67 (r/w/o: 8248.71/0.00/1175.96) lat (ms,95%): 9.73 err/s: 0.00 reconn/s: 0.00
      [ 6s ] thds: 4 tps: 571.96 qps: 9126.39 (r/w/o: 7982.47/0.00/1143.92) lat (ms,95%): 10.46 err/s: 0.00 reconn/s: 0.00
      [ 7s ] thds: 4 tps: 564.12 qps: 9033.90 (r/w/o: 7905.66/0.00/1128.24) lat (ms,95%): 9.91 err/s: 0.00 reconn/s: 0.00
      [ 8s ] thds: 4 tps: 537.84 qps: 8580.38 (r/w/o: 7505.71/0.00/1074.67) lat (ms,95%): 10.27 err/s: 0.00 reconn/s: 0.00
      [ 9s ] thds: 4 tps: 621.04 qps: 9947.57 (r/w/o: 8704.50/0.00/1243.07) lat (ms,95%): 8.74 err/s: 0.00 reconn/s: 0.00
      [ 10s ] thds: 4 tps: 555.07 qps: 8894.07 (r/w/o: 7783.94/0.00/1110.13) lat (ms,95%): 10.65 err/s: 0.00 reconn/s: 0.00
    has to be converted to:
      {'time':'1s','thds':'4','tps':'435.22','qps':'7015.44'}
      {'time':'2s','thds':'4','tps':'444.05','qps':'7093.80'}
      {'time':'3s','thds':'4','tps':'438.94','qps':'7012.99'}
      {'time':'4s','thds':'4','tps':'457.08','qps':'7330.36'}
      {'time':'5s','thds':'4','tps':'453.02','qps':'7238.34'}
      {'time':'6s','thds':'4','tps':'442.01','qps':'7071.14'}
      {'time':'7s','thds':'4','tps':'425.87','qps':'6833.97'}
      {'time':'8s','thds':'4','tps':'436.12','qps':'6961.96'}
      {'time':'9s','thds':'4','tps':'438.90','qps':'7017.34'}
      {'time':'10s','thds':'4','tps':'449.10','qps':'7188.52'}
    '''
    out = {}
    for file in args.file_list:
        out[file] = []
        logger.debug('Processing conversion of %s' % file)
        try:
            f = open(file+'.txt')
            for line in f.readlines():
                if goodline.search(line):
                    time = line.split('[')[1].split(']')[0].strip(' ')
                    thds = line.split(']')[1].split('thds:')[
                        1].split('tps')[0].strip(' ')
                    tps = line.split('tps:')[1].split('qps')[0].strip(' ')
                    qps = line.split('qps:')[1].split('(r/w/o:')[0].strip(' ')
                    latency = line.split('lat (ms,95%):')[
                        1].split('err/s')[0].strip(' ')
                    errors = line.split(
                        'err/s:')[1].split('reconn/s')[0].strip(' ')
                    out[file].append({'time': time, 'thds': thds, 'tps': tps,
                                      'qps': qps, 'latency': latency, 'errors': errors})
            f.close()
        except:
            logger.error('Could not open %s' % file+'.txt', exc_info=True)
            pass
    return out


if __name__ == "__main__":
    args = parse_args()
    logger = logger_config.get_logger('plot-sysbench')
    logger.info('Kicking off graph preparation.')
    df = prepare(extract_from_file())
    render(df)
