#!/usr/bin/python3 -tt

import sys, os, time
import subprocess

def gettime(command):
    if command is None:
        return 0.0
    print('Running command:', command)
    starttime = time.time()
    subprocess.check_call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    endtime = time.time()
    return endtime - starttime

def measure():
    measurements = [
        ['meson', 'mkdir -p buildmeson && CC=gcc /home/jpakkane/workspace/meson/meson.py buildmeson', 'ninja -C buildmeson -j 4'],
        ['cmake-make', 'mkdir -p buildcmake && cd buildcmake && cmake -DCMAKE_BUILD_TYPE=debug ..', 'cd buildcmake && make -j 4'],
        ['cmake-ninja', 'mkdir -p buildcmakeninja && cd buildcmakeninja && cmake -DCMAKE_BUILD_TYPE=debug -G Ninja ..', 'cd buildcmakeninja && ninja -j 4'],
        ['scons', None, 'scons -j 4'],
        ['premake', '/home/jpakkane/premake-4.4-beta4/bin/release/premake4 gmake', 'cd buildpremake && make -j 4'],
        ['autotools', "rm -f *.o speedtest && autoreconf -vif && mkdir -p buildauto && cd buildauto && ../configure CFLAGS='-O0 -g'", 'cd buildauto && make -j 4'],
        ]
    results = []
    for m in measurements:
        cur = []
        results.append(cur)
        cur.append(m[0])
        conf = m[1]
        make = m[2]
        cur.append(gettime(conf))
        cur.append(gettime(make))
        cur.append(gettime(make))
    return results

def print_times(times):
    for t in times:
        print(t[0])
        print(" %.3f gen" % t[1])
        print(" %.3f build" % t[2])
        print(" %.3f empty build" % t[3])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0], '<output dir>')
    os.chdir(sys.argv[1])
    print_times(measure())
