# 时间离散
import pandas as pd
from django.db import connection

# 建立与数据库的连接
conn = connection


# DRY_STEP为没有降雨和没有积水时段径流计算的时间步长长度。
def write_dry_step(filename, dry_step):
    dry_step_key = 'DRY_STEP'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if dry_step_key in line:
                delete_lines = True
                file.write(f"{dry_step_key}          {dry_step}\n")
                delete_lines = False  # 在写入后重置 delete_lines
                continue

            if not delete_lines:
                file.write(line)
            if delete_lines:
                delete_lines = False


# WET_STEP为降雨时段或者当积水仍旧保留在地表时，计算子汇水面积径流的时间步长长度。
def write_wet_step(filename, wet_step):
    wet_step_key = 'WET_STEP'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if wet_step_key in line:
                delete_lines = True
                file.write(f"{wet_step_key}          {wet_step}\n")
                delete_lines = False  # 在写入后重置 delete_lines
                continue

            if not delete_lines:
                file.write(line)
            if delete_lines:
                delete_lines = False


# ROUTING_STEP为演算输送系统的流量和水质成分使用的时间步长长度，秒。
def write_routing_step(filename, routing_step):
    routing_step_key = 'ROUTING_STEP'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if routing_step_key in line:
                delete_lines = True
                file.write(f"{routing_step_key}      {routing_step}\n")
                delete_lines = False  # 在写入后重置 delete_lines
                continue

            if not delete_lines:
                file.write(line)

            if delete_lines:
                delete_lines = False
