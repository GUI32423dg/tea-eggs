# -*- coding: utf-8 -*-
'''
	desc: 更新用户密码模块
	author：miguitian
	date：2020-04-10
'''

import pathlib
import sys
import os
import yaml
from ansible.playbook import Playbook
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
_project_root = str(pathlib.Path(__file__).resolve().parents[2])
sys.path.append(_project_root)
from ansibleService import playbook
from config import config

YAML_PATH = config['change_user_password']['yaml_path']
BECOME_PASS = config['change_user_password']['become_pass']
HOST = config['change_user_password']['host']
USERNAME = config['change_user_password']['username']
PASSWORD = config['change_user_password']['password']


yaml_template = """
- hosts: params_host
  become: yes
  become_user: root
  gather_facts: F #开启debug模式
  vars:
    username: params_username
    password: params_password
  tasks:
  - name: ping the machine
    ping:
  - name: change user password
    user:
      name: '{{username}}'
      password: '{{password | password_hash("sha512")}}'
      shell: /bin/bash
      update_password: always
"""

class TaskInfo:
    host = ""
    username = ""
    password = ""

def run_task_yaml(task_info_obj  , yaml_save_path):
    data = yaml.safe_load(yaml_template)
    data[0]['hosts'] = task_info_obj.host
    data[0]['vars']['username'] = task_info_obj.username
    data[0]['vars']['password'] = task_info_obj.password
    with open(yaml_save_path, 'w') as yaml_file:
        documents = yaml.dump(data, yaml_file)
#        print(documents)
    become_pass=BECOME_PASS
    #os.path.abspath(yaml_save_path)
    playbook.run_palybook(os.path.abspath(yaml_save_path),become_pass)
    return True # todo 根据事情情况判断执行是否成功，返回的数据也不是单纯的True或者False


def run_task():
    playbook.playbook_run()
    Playbook.load()

if __name__ == "__main__":
    task_info_obj = TaskInfo()
    task_info_obj.host = HOST
    task_info_obj.username = USERNAME
    task_info_obj.password = PASSWORD
    yaml_save_path = YAML_PATH
    run_task_yaml(task_info_obj, yaml_save_path)
    pass
