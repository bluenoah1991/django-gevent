#!/bin/bash

sed -i '1afrom gevent import monkey\nmonkey.patch_all()' manage.py
