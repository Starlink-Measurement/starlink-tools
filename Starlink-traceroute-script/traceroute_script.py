import os
from multiprocessing import Pool
# from socket import if_indextoname
# from requests import get
import pathlib
import time
import datetime 
import pytz
import sys
import glob

num_of_proc = 16

def executeCMD(cmd):
  os.system(cmd)

def starlinkToIps(index):
  global num_of_proc
  th_pool = Pool(num_of_proc)
  dir_list = ["as_ip", "eu_ip", "na_ip", "sa_ip", "af_ip"]

  as_ip_list = ["baidu.com", "bilibili.com", "qq.com", "163.com"]
  eu_ip_list = ["euronews.com", "rt.com", "spotify.ua", "vk.com"]
  na_ip_list = ["google.com", "youtube.com", "facebook.com", "amazon.com"]
  sa_ip_list = ["nic.ar", "cgi.br", "ix.br", "nic.do"]
  af_ip_list = ["whois.nic.ly", "whois.nic.dz", "cder.dz"]

  ip_list = [as_ip_list, eu_ip_list, na_ip_list, sa_ip_list, af_ip_list]

  s_to_ip_cmd = []
  work_path = str(pathlib.Path().resolve())
  for i in range(0, len(ip_list)):
    for ip in ip_list[i]:
      path_tcp = work_path + "/Starlink_to_IPs/tcp/" + dir_list[i] + "/" + ip + "/"
      # path_udp = work_path + "/Starlink_to_IPs/udp/" + dir_list[i] + "/" + ip + "/"
      if os.path.exists(path_tcp) == False:
        os.makedirs(path_tcp)
      # if (os.path.exists(path_udp) == False):
      #   os.makedirs(path_udp)
      s_to_ip_cmd.append("traceroute -T --back " + ip + " > " + '"' + path_tcp + ip + "." + str(index) + '''.txt"''')
      # s_to_ip_cmd.append("traceroute --back " + ip + " > " + path_udp + ip + "." + str(index) + ".txt")

  th_pool.map(executeCMD, s_to_ip_cmd)

  th_pool.close()
  th_pool.join()

if os.getuid() != 0:
  print("Sorry, need root user to run this script... (TCP traceroute)")
  exit()

# Find the max index in all log files, and use the max_index + 1 as the
# new index to name the new log file
max_index = 0
for filename in glob.iglob("Starlink_to_IPs/" + '**/*.txt', recursive=True):
  file_index = int(filename.split('.')[-2])
  if file_index > max_index:
    max_index = file_index
max_index += 1

PST = pytz.timezone('US/Pacific')
start_time = datetime.datetime.now().astimezone(PST)

while True:
  curr_date = datetime.datetime.now().astimezone(PST)
  if curr_date.minute in [0,1] and curr_date.hour in [2, 12, 21]:
    starlinkToIps(max_index)
    # serversToStarlink()
    max_index += 1
  elif curr_date.minute in [0,1]:
    time.sleep(60 * 60)
  else:
    time.sleep(60)

# def rootToAnotherUser(user_name, cmd):
#   return "runuser -l " + user_name + " -c '" + cmd + "'"

# def serversToStarlink():
#   global index
#   # global num_of_proc
#   # th_pool = Pool(num_of_proc)
#   instances = ["instance-1", "instance-finland", "instance-hongkong", "instance-london", "instance-santiago", \
#     "instance-southcarolina", "instance-sydney"]
#   external_ip = get('https://api.ipify.org').content.decode('utf8')

#   # The multi-threads has some potential problems. Temporarily discarded

#   # start_cmd = []
#   # end_cmd = []
#   # se_to_s_cmd = []
#   # scp_cmd = []
#   # rm_cmd = []

#   # for ins_name in instances:
#   #   path = "Servers_to_Starlink/" + ins_name + "/"
#   #   if(os.path.exists(path) == False):
#   #     os.makedirs(path)
#   #   gcloud_user = "zhy"   #depends on the who auth the gcloud

#   #   start_cmd.append(rootToAnotherUser(gcloud_user, 'gcloud compute instances start {}'.format(ins_name)))
#   #   se_to_s_cmd.append(rootToAnotherUser(gcloud_user, 'gcloud compute ssh {} --command="sudo traceroute -T --back {} > temp.txt"'.format(ins_name, str(external_ip))))
#   #   scp_cmd.append(rootToAnotherUser(gcloud_user, 'gcloud compute scp {}:~/temp.txt {}'.format(ins_name, path + str(external_ip) + "." + str(index) + ".txt")))
#   #   rm_cmd.append(rootToAnotherUser(gcloud_user, "gcloud compute ssh " + ins_name + ' --command="rm temp.txt"'))
#   #   end_cmd.append(rootToAnotherUser(gcloud_user, "gcloud compute instances stop " + ins_name))

#   # th_pool.map(executeCMD, start_cmd)
#   # th_pool.map(executeCMD, se_to_s_cmd)
#   # th_pool.map(executeCMD, scp_cmd)
#   # th_pool.map(executeCMD, rm_cmd)
#   # th_pool.map(executeCMD, end_cmd)

#   # th_pool.close()
#   # th_pool.join()

#   total_cmd = []
#   work_path = str(pathlib.Path().resolve())
#   for ins_name in instances:
#     path_tcp = work_path + "/Servers_to_Starlink/tcp/" + ins_name + "/"
#     path_udp = work_path + "/Servers_to_Starlink/udp/" + ins_name + "/"
#     if(os.path.exists(path_tcp) == False):
#       os.makedirs(path_tcp)
#     if(os.path.exists(path_udp) == False):
#       os.makedirs(path_udp)
#     gcloud_user = "ubuntu"   #depends on the who auth the gcloud
#     os.system(""" chown -R {} {}/Servers_to_Starlink/ """.format(gcloud_user, work_path))

#     total_cmd.append(""" runuser -l {} -c 'gcloud compute instances start {}' """.format(gcloud_user, ins_name))
#     total_cmd.append(""" runuser -l {} -c 'gcloud compute ssh {} --command="sudo traceroute -T --back {} > temp_tcp.txt"' """.format(gcloud_user, ins_name, str(external_ip)))
#     # total_cmd.append(""" runuser -l {} -c 'gcloud compute ssh {} --command="sudo traceroute --back {} > temp_udp.txt"' """.format(gcloud_user, ins_name, str(external_ip)))
#     total_cmd.append(""" runuser -l {} -c 'gcloud compute scp {}:~/temp_tcp.txt {}.{}.txt' """.format(gcloud_user, ins_name, path_tcp + str(external_ip), str(index)))
#     # total_cmd.append(""" runuser -l {} -c 'gcloud compute scp {}:~/temp_udp.txt {}.{}.txt' """.format(gcloud_user, ins_name, path_udp + str(external_ip), str(index)))
#     total_cmd.append(""" runuser -l {} -c 'gcloud compute ssh {} --command="rm temp_tcp.txt"' """.format(gcloud_user, ins_name))
#     # total_cmd.append(""" runuser -l {} -c 'gcloud compute ssh {} --command="rm temp_udp.txt"' """.format(gcloud_user, ins_name))
#     total_cmd.append(""" runuser -l {} -c 'gcloud compute instances stop {}' """.format(gcloud_user, ins_name))

#   for cmd in total_cmd:
#     executeCMD(cmd)
#     time.sleep(2)