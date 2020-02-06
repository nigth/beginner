# -*- coding: utf-8 -*-
import re
import csv
import argparse
import datetime

parser = argparse.ArgumentParser(description='Filename for extracting IP (only TXT format')
parser.add_argument("-f", '--files', nargs='+', type=str, help='filenames, separated by space. DEFAULT is for_ip_parse.txt')

args = parser.parse_args()
if args.files == None:
    args.files = list()
    args.files.append('for_ip_parse.txt')

patt_ip = re.compile(ur'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
patt_range = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3})')

for fil in args.files:
    try:
        handle = open(fil, 'r')
    except:
        print 'File ' + fil + ' not found'
        continue
    print 'Extracting IPs ang ranges from ' + fil + ' ...'

    address = list()
    ranges = list()
    text = handle.read()
    words = text.split()
    for word in words:
        ip = re.findall(patt_ip, word)
        if len(ip) > 0 and ip[0] not in address:
            address.append(ip[0])
            rang = re.findall(patt_range, ip[0])
            if (rang[0]+'.0/24') not in ranges:
                ranges.append(rang[0]+'.0/24')
        
    address.sort()
    ranges.sort()

    now_time = datetime.datetime.now()
    now_format = now_time.strftime("%d-%m-%Y_%H:%M:%S")

    result_name_ip = fil + '(extr_' + str(len(address))+ '_IPs_'+ str(now_format) + ').txt'
    result_name_range = fil + '(extr_' + str(len(ranges))+ '_ranges_'+ str(now_format) + ').txt'
    result_file_ip = open(result_name_ip, 'w') 
    result_file_range = open(result_name_range, 'w') 
    
    for addr in address:
        result_file_ip.write(addr + '\n')
    result_file_ip.write('\n')

    for rang in ranges:
        result_file_range.write(rang + '\n')
    result_file_range.write('\n')

    result_file_ip.close()
    result_file_range.close()

print 'End'
