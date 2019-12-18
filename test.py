#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

sleep_time = 2
num_retries = 4

for x in range(0, num_retries):
  try:
    result = 'something'
  except:
    result = None
    print('Error: attempt {} of {}'.format(x, num_retries))
    pass
  if result is None:
    time.sleep(sleep_time)  # wait before trying to fetch the data again
    sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
  else:
    break
