#! /usr/bin/python
# Copyright 2014 Tom Arnfeld
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collectd
import subprocess

PREFIX = "unbound"
STATS_CMD = ["/usr/sbin/unbound-control", "stats"]
VERBOSE_LOGGING = False


def configure_callback(conf):
    """Received configuration information"""

    global STATS_CMD, VERBOSE_LOGGING
    for node in conf.children:
        if node.key == 'StatsCmd':
            STATS_CMD = node.values[0].split(" ")
        elif node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            collectd.warning('unbound plugin: Unknown config key: %s.' % node.key)


def fetch_stats():
    proc = subprocess.Popen(STATS_CMD, stdout=subprocess.PIPE)
    return_code = proc.wait()

    if return_code > 0:
        collectd.error('ubnound plugin: Error code collecting stats %d' % return_code)
    else:
        for line in proc.stdout:
            yield parse_stat(line.rstrip())


def parse_stat(stat_line):
    return stat_line.split("=")


def dispatch_stat(key, value):
    val = collectd.Values(plugin='unbound')
    val.type = "gauge"
    val.type_instance = key.replace(".", "/")
    val.values = [value]
    val.dispatch()


def read_callback():
    log_verbose('Read callback called')

    stats = fetch_stats()
    for key, value in stats:
        dispatch_stat(key, value)


def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('mesos plugin [verbose]: %s' % msg)


collectd.register_config(configure_callback)
collectd.register_read(read_callback)
