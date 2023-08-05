#!/usr/bin/env python

 

import os
from runmonitor import environ_check
from runmonitor import check_tools as chu
from runmonitor import stat_tools as srd
from runmonitor import update_tools as upa
from runmonitor import restore_tools as resto
#import logging
import time
import daemon
import subprocess
from subprocess import PIPE
from daemon import pidfile


# see: http://www.gavinj.net/2012/06/building-python-daemon-process.html, 
# https://stackoverflow.com/questions/13106221/how-do-i-set-up-a-daemon-with-python-daemon
# https://www.python.org/dev/peps/pep-3143/
# note per https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/ the usage in the first link is deprecated --> trying DaemonContext instead
# https://linuxfollies.blogspot.com/2016/11/linux-daemon-using-python-daemon-with.html


class Main_Daemon():
    def __init__(self,rmdir,cluster="CIT",sender_email="runmonitor.rift.1@gmail.com",receiver=None,password=None,el=False,verbose=False,debug=False,attempt_healing=False,refresh_timer=1800):
        """
Inputs:
rmdir = the runmon directory

--------
Outputs:
sets up the daemon's attributes (currently not much to do)
        """  
        self.el = el
        self.rmdir = rmdir
        self.cluster = cluster
        self.receiver = receiver
        self.attempt_healing = attempt_healing 
        self.password = password
        self.sender_email = sender_email
        self.log = open(os.path.join(self.rmdir,"daemon/check_daemon.log"),'a')
        self.pidf=os.path.join(self.rmdir,"daemon/check_daemon.pid") 
        self.refresh_timer = refresh_timer
        """
        using logging package was running into weird OS errors when in DaemonContext, so for now we'll us the inelegant method of just printing to stdout
        self.logger = logging.getLogger('check_daemon')
        self.logger.setLevel(logging.INFO) 
        self.logf = os.path.join(rmdir,"daemon/daemon.log")       
        fh = logging.FileHandler(self.logf)
        fh.setLevel(logging.INFO)
        formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(formatstr)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        """
  
    def summon(self):
        """
inputs:
---------
self

outputs:
---------
Periodically uses check_up.py on all of the public directories, skipping if extrinsic_exists is present or job_status == 0

        """
        #creating the information associated with the daemon
        context = daemon.DaemonContext(stdout = self.log,stderr=self.log,working_directory=self.rmdir,pidfile=pidfile.TimeoutPIDLockFile(self.pidf),umask=0o002)  
        #entering the daemon
        #all prints write to stdout now, and all errors go to stderr
        with context:       
           while True:   
                print("starting update cycle")
                #assuming base/event/run hierarchy, and skipping over the files we know are not events
                #RUNMON should be kept clean, or we should actually keep track of the events (a dedicated textfile maybe?)
                if self.el:
                    with open(os.path.join(self.rmdir,"event_list.txt")) as f:
                        events = [ob.strip("\n") for ob in f.readlines()]
                else:
                    events = [os.path.join(self.rmdir,obj) for obj in os.listdir(self.rmdir) if obj != 'daemon' and obj != 'archived_runs_microstatus.txt' and obj != "event_list.txt"]
                runs = []
                #looping over runs
                for event in events:
                    runs = runs + [os.path.join(event,obj) for obj in os.listdir(event)]
                if self.receiver != None and self.password != None:
                    deltas = []
                    print(deltas)
                for run in runs:
                    #checking the time and the job status
                    now = time.asctime(time.gmtime(time.time()))
                    skip_run=False
                    if not os.path.exists(os.path.join(run,"job_status.txt")):
                      chu.update(run)
                    else:
                      lastline = subprocess.check_output(["tail","-n 1",os.path.join(run,"job_status.txt")],text=True).strip()
                      #if the exit was successful or extrinsic_exists exists, it moves on 
                      if lastline.split()[-1] == str(0) or 'extrinsic_exists.txt' in os.listdir(run):
                         print(now + "\t"+"found successful exit, will not update\t"+run)  
                         skip_run=True
                    #otherwise, it updates the logs with chu, and updates the archived_runs_microstatus with upa
                    if not skip_run:
                        print(now + "\t"+"updating logs\t"+run)
                        status = chu.update(run)
                        rundir = chu.read_wocc(run)
                        archive_orig = None
                        if self.receiver != None and self.password != None and os.path.exists(os.path.join(self.rmdir,"archived_runs_microstatus.txt")):
                            with open(os.path.join(self.rmdir,"archived_runs_microstatus.txt"),'r') as f:
                                archive_orig = f.readlines()
                        fullname = run.split("/")[-1]
                        lessername = fullname.split(":")[1]
                        cluster = fullname.split(":")[0]
                        eventname = run.split("/")[-2]
                        

                        resubmit = False # we want to catch various reasons we might want to resubmit
                        force_pass = False

                        with open(os.path.join(run,"job_status.txt"),'r') as f:
                            most_recent_status = f.readlines()[-1]
                        most_recent_status = int(most_recent_status.split()[-1])

                        if most_recent_status == 200000:
                            continue

                        if self.attempt_healing:
                            # Rail Correction
                            import runmonitor.rail_checker as rail                
                            itn = srd.scan_samples(rundir)[4]
                            posterior_review = os.path.join(rundir,f"posterior_{itn}_quality.txt") # a file tracking whether correction has happened
                            print("beginning rail check, for iteration "+str(itn))
                            if f"posterior_{itn}_quality.txt" in os.listdir(rundir) or int(itn) == 0:
                                pass
                            else:
                                with open(os.path.join(rundir,"CIP_0.sub"),'r') as f:
                                    original_args = f.readlines()
                                    original_args = [line for line in original_args if "arguments" in line]
                                with open(posterior_review,'w') as f:
                                    f.write("Original Args:\n")
                                    f.writelines(original_args)
                                mc_rail = rail.check_railing(rd=rundir,parameter="mc")
                                eta_rail = rail.check_railing(rd=rundir,parameter="eta")
                                if mc_rail == 0 and eta_rail == 0:
                                    with open(posterior_review,'w') as f:
                                        f.write("No railing found, CIP_arguments unmodified")
                                else:
                                    print("Found railing: MC railing code: "+str(mc_rail))
                                    print("Found railing: eta railing code: "+str(eta_rail))
                                    with open(os.path.join(rundir,"CIP_0.sub"),'r') as f:
                                        new_args = f.readlines()
                                        new_args = [line for line in new_args if "arguments" in line]
                                    with open(posterior_review,'a') as f:
                                        f.write("Modified Args:\n")
                                        f.writelines(new_args)
                                    dag_id = srd.query_dag_id(rundir)
                                    subprocess.Popen(["condor_rm",str(dag_id)],stdout=PIPE,stderr=PIPE)
                                    resubmit=True
                                    time.sleep(15) # a small of amount of time is needed for the rm to go through

                        if most_recent_status == 0 or most_recent_status == 2 or most_recent_status == 200000 or most_recent_status == 100000:
                            run_failed = False
                        else: 
                            run_failed = True
                        
                        if self.attempt_healing and run_failed:
                            from runmonitor import heal
                            error = heal.check_error(rd=rundir)
                            if error == "ILE.sub" or error == "ILE_puff.sub" or error == "ILE_extr.sub":
                                #iteration = srd.scan_samples(rundir)[4]
                                #job_id = heal.get_job_id(rd=rundir)
                                gpu_fail = heal.identify_gpu_config_fail(rd=rundir)
                                if gpu_fail != []:
                                    resubmit = True
                            encoding_error = heal.check_encodings_error(rd=rundir,check_node=True)
                            if encoding_error:
                                resubmit= True

                        #resubmit = True # for testing

                        if resubmit:
                            envinfo = resto.find_env(run)
                            cwd = os.getcwd()
                            if envinfo == None:
                                print("Cannot resubmit, no resubmission env available")
                            else:
                                os.chdir(rundir)
                                resubmit = subprocess.Popen(["python","-c",
                                    f"import runmonitor.restore_tools as resto; resto.resubmit(rundir='{rundir}',force_pass='{force_pass}')"],
                                    text=True,stdout=PIPE,stderr=PIPE,env=envinfo)
                                #resubmit = subprocess.Popen(["/bin/bash","-c","source "+env,"&&","python","-c",
                                #   "'import restore_tools as resto; resto.resubmit(rundir="+rundir+",fp="+str(force_pass)+")'"],
                                #   text=True,stdout=PIPE,stderr=PIPE)
                                print(resubmit.stderr.read())
                                print(resubmit.stdout.read())
                                os.chdir(cwd)
                            status = chu.update(run)

                        upa.update(lessername,eventname,self.rmdir,cluster)

                        if self.receiver != None and self.password != None and archive_orig != None: 
                            with open(os.path.join(self.rmdir,"archived_runs_microstatus.txt"),'r') as f:
                                archive_now= f.readlines()
                            for i,line in enumerate(archive_now):
                                if line != archive_orig[i]:
                                    deltas += [line]
                            print(deltas)

                if self.receiver != None and self.password != None and deltas != []:
                    #TODO emailing
                    import smtplib, ssl
                    smtp_server = "smtp.gmail.com"
                    port = 587
                    email_context = ssl.create_default_context()
                    try:
                        server = smtplib.SMTP(smtp_server,port)
                        server.ehlo()
                        server.starttls(context=email_context)
                        server.ehlo()
                        server.login(self.sender_email,self.password)
                        message = "Subject: runmonitor-rift updates \n\n\n \
                        You are receiving an automated email from runmonitor regarding your current runs on "+self.cluster+". If you do not wish to receive these emails please, dis-instantiate this daemon. If you did not instatiate this daemon, please contact rudall@caltech.edu. The following lines were found to have changed in your archived_run_microstatus.txt, indicating a state change for the run:\n"+" \n".join(deltas)
                        server.sendmail(self.sender_email,self.receiver,message)
                        print("sent email to "+self.receiver)
                    except Exception as fail:
                        print("failed to send email")
                        print(fail) 
                      
                #finally, it waits for the designated amount of time to rerun
                time.sleep(self.refresh_timer)
