#!/usr/bin/env python

import os, sys
import commands
import time
import utils

FILEPATH = os.path.dirname(os.path.realpath(__file__))
SERVER_NAME = utils.get_machines_from_file('execs.backend')
VERIFIER_NAME = utils.get_machines_from_file('verifiers.backend')
FILTER_NAME = utils.get_machines_from_file('filters.backend')

all_machines = utils.get_machines()
PROPERTY_FILE = sys.argv[1]

print 'Killing Java processes on needed machines...'

for m in all_machines:
    print 'Killing processes on: ' + m
    os.system('ssh %s \'killall java 2> /dev/null \' > /dev/null 2> /dev/null ' % m)

print 'Done machine cleaning.'

agent_path = '-agentlib:hprof=cpu=samples,interval=100,depth=10'

num_servers = int(commands.getstatusoutput('grep \"EXEC.* =\" %s | wc -l' % PROPERTY_FILE)[1])
num_verifiers = int(commands.getstatusoutput('grep \"VERIFIER.* =\" %s | wc -l' % PROPERTY_FILE)[1])
num_filters = int(commands.getstatusoutput('grep \"FILTER.* =\" %s | wc -l' % PROPERTY_FILE)[1])

print 'start exec nodes'
no_server_machines = len(SERVER_NAME)
for i in range (0, num_servers):
    current_machine = SERVER_NAME[i % no_server_machines]
    print 'start exec at ' + current_machine
    cmd_template = 'java -ea %s -Xms2G -Xmx4G -Djava.library.path=. -cp lib/zookeeper-3.2.2.jar:lib/log4j-1.2.15.jar:lib/bft.jar:lib/FlexiCoreProvider-1.6p3.signed.jar:lib/CoDec-build17-jdk13.jar:lib/netty-3.2.1.Final.jar:lib/h2.jar:lib/zookeeper-3.2.2.jar:lib/commons-javaflow-2.0-SNAPSHOT.jar:lib/commons-logging-1.1.3.jar Applications.tpcw_new.request_player.remote.RealtimeTPCWServer %s %s 2> jh_log/db_%s_err > jh_log/db_%s_out &' % (
        agent_path,  PROPERTY_FILE, str(i), str(i), str(i))
    cmd = 'ssh %s \'cd %s; %s \' ' % (current_machine, FILEPATH, cmd_template)
    print 'Executing command: ' + cmd
    os.system(cmd)
    time.sleep(5)

time.sleep(15)

print 'start verifier nodes'
no_verifier_machines = len(VERIFIER_NAME)
for i in range(0, num_verifiers):
    current_machine = VERIFIER_NAME[i % no_verifier_machines]
    print 'start verifier at ' + current_machine
    cmd_template = 'java %s -Xmx1024m -Djava.library.path=. -cp lib/log4j-1.2.15.jar:lib/bft.jar:lib/FlexiCoreProvider-1.6p3.signed.jar:lib/CoDec-build17-jdk13.jar:lib/netty-3.2.1.Final.jar BFT.verifier.VerifierBaseNode %s %s > jh_log/db_verifier_%s_out 2> jh_log/db_verifier_%s_err &' % (
        agent_path, str(i), PROPERTY_FILE, str(i), str(i))
    cmd = 'ssh %s \' cd %s; %s \' ' % (current_machine, FILEPATH, cmd_template)
    print 'Executing command: ' + cmd
    os.system(cmd)

time.sleep(5)

print 'start filter nodes'
no_filter_machines = len(FILTER_NAME)
for i in range(num_filters):
    current_machine = FILTER_NAME[i % no_filter_machines]
    print 'start filter at ' + current_machine
    cmd_template = 'java %s -Xmx1024m -Djava.library.path=. -cp conf:lib/log4j-1.2.15.jar:lib/bft.jar:lib/FlexiCoreProvider-1.6p3.signed.jar:lib/CoDec-build17-jdk13.jar:lib/netty-3.2.1.Final.jar BFT.filter.FilterBaseNode %s %s > jh_log/db_filter_%s_out 2> jh_log/db_filter_%s_err &' % (
        agent_path, str(i), PROPERTY_FILE, str(i), str(i))
    cmd = 'ssh %s \'cd %s; %s  \' ' % (current_machine, FILEPATH, cmd_template)
    print 'Executing command: ' + cmd
    os.system(cmd)
