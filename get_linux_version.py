#!/usr/bin/env python3
import os
from sys import argv
from os import path
from panda import Panda, blocking, ffi
from panda.x86.helper import * # XXX omg these are 32-bit names
from subprocess import Popen
import docker

arch = "x86_64" if len(argv) <= 1 else argv[1]
panda = Panda(arch=arch, qcow="/home/luke/workspace/qcows/bionic-server-cloudimg-amd64.qcow2", extra_args="-nographic", expect_prompt=rb"root@ubuntu.*#",mem="1G")

interesting_file_name = b"fakefile"

panda.set_os_name("linux-64-ubuntu")
panda.load_plugin("callstack_instr", args={"stack_type": "asid"})
panda.require("syscalls2")


@blocking
def mycmd():
    panda.revert_sync("root")
    global kernel_version
    kernel_version = panda.run_serial_cmd("uname -r")
    #print("GUEST RUNNING COMMAND:\n\n# cat fakefile\n" + panda.run_serial_cmd("cat fakefile"))
    #panda.revert_sync("strace")
    #print(panda.run_serial_cmd("strace -v cat fakefile"))
    panda.end_analysis()

panda.queue_async(mycmd)
panda.run()
print(kernel_version)
client = docker.from_env()
cmd = "apt-get install --download-only -y --allow-unauthenticated linux-image-"+kernel_version+"-dbgsym"
client.containers.run("panda-limage-downloader", cmd.split(), volumes={os.getcwd()+"/dbgsym": {'bind': '/var/cache/apt/archives/', 'mode': 'rw'}})

