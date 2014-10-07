
collectd-unbound
================

Collectd [Python plugin](http://collectd.org/documentation/manpages/collectd-python.5.shtml) for gathering metrics from [unbound](unbound.net).

This plugin is based heavily on the [Elasticsearch Collectd Python plugin](https://github.com/phobos182/collectd-elasticsearch) written by [phobos182](https://github.com/phobos182).

Install
-------
 1. Place unbound.py in collectd'opt/collectd/lib/collectd/plugins/python (assuming you have collectd installed to /opt/collectd).
 2. Configure the plugin (see below).
 3. Restart collectd.

Configuration
-------------
 * See unbound.conf

Requirements
------------
 * collectd 4.9+
