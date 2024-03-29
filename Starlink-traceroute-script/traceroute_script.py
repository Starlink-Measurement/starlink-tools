import os
from multiprocessing import Pool
import pathlib
import time
import datetime 
import pytz
import argparse
import pandas as pd
import numpy
# from socket import if_indextoname
# from requests import get
# import sys

def executeCMD(cmd):
  result = os.popen(cmd).read()
  return result, int(time.time())

def starlinkToIps(nThreads):
  dir_list = ["as_ip", "eu_ip", "na_ip", "sa_ip", "af_ip"]

  # as_ip_list = ["baidu.com", "bilibili.com", "qq.com", "163.com"]
  # eu_ip_list = ["euronews.com", "rt.com", "spotify.ua", "vk.com"]
  # na_ip_list = ["google.com", "youtube.com", "facebook.com", "amazon.com"]
  # sa_ip_list = ["nic.ar", "cgi.br", "ix.br", "nic.do"]
  # af_ip_list = ["whois.nic.ly", "whois.nic.dz", "cder.dz"]

  # ISP_na = [Google (California) T, Facebook (Seattle) T, Apple (California) T, Microsoft (Virginia) T, Amazon (Virginia) T]

  na_ip_list = ["74.125.142.94", "157.240.3.35", "17.253.144.10", "20.81.111.85", "107.170.145.187", "34.198.39.74"]
  as_ip_list = []
  eu_ip_list = []
  sa_ip_list = []
  af_ip_list = []

  ip_list = [as_ip_list, eu_ip_list, na_ip_list, sa_ip_list, af_ip_list]

  s_to_ip_cmd = []
  work_path = str(pathlib.Path().resolve())
  for ips in ip_list:
    for ip in ips:
      s_to_ip_cmd.append("traceroute -T --back " + ip)

  th_pool = Pool(nThreads)
  result = th_pool.map(executeCMD, s_to_ip_cmd)
  th_pool.close()
  th_pool.join()

  re_index = 0
  for i in range(0, len(ip_list)):
    for ip in ip_list[i]:
      path_tcp = work_path + "/Starlink_to_IPs/tcp/" + dir_list[i] + '/'
      if not os.path.exists(path_tcp):
        os.makedirs(path_tcp)
      if not os.path.exists(path_tcp + ip + ".csv"):
        start_id = 0
      else:
        csvFile = pd.read_csv(path_tcp + ip + ".csv")
        start_id = csvFile.iloc[-1]['id'] + 1
      trace_rs = list(filter(None, result[re_index][0].split('\n')))
      trace_df = pd.DataFrame({'id': numpy.full(len(trace_rs), start_id),
        'timestamp': numpy.full(len(trace_rs), result[re_index][1]),
        'trace_string': trace_rs})
      if start_id == 0:
        trace_df.to_csv(path_tcp + ip + ".csv", index=False)
      else:
        trace_df.to_csv(path_tcp + ip + ".csv", index=False, mode='a', header=False)
      re_index += 1

def main(args):
  if os.getuid() != 0:
    print("Sorry, need root user to run this script... (TCP traceroute)")
    exit()

  print("Script start...")
  PST = pytz.timezone('US/Pacific')

  while True:
    start_time = time.time()
    starlinkToIps(int(args.nThreads))
    print("""Last test finished at {}""".format(datetime.datetime.now().astimezone(PST).strftime("%Y/%m/%d %H:%M:%S")))
    time_to_sleep = int(args.timeInterval) * 60 - (time.time() - start_time)
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = "A large-scale Traceroute testing script.")
  parser.add_argument('-n', '--nThreads', default='4', help='Number of threads will be used.')
  parser.add_argument('-tI', '--timeInterval', default='30', help='Set the time interval for the test (Unit: mins). (default=30mins)')
  args = parser.parse_args()
  main(args)