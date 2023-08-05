#!/usr/bin/env bash
#Script to fix XLAL initial frequency error. Finds relevant error file, checks to see if the initial frequency is too high, and force passes and resubmits the job

ERROR_FILE=$(python -c'from runmonitor import heal; heal.check_error()')

if [[ $ERROR_FILE = ILE.sub ]]; then
	ITERATION=$(ls posterior_samples-*.dat | wc -l)
	JOB_ID=$(python -c'from runmonitor import heal; heal.get_ile_job()')
	if [$(python -c"from runmonitor import heal; heal.check_frequency_error($ITERATION, $JOB_ID)")]; then
        RMDIR=`pwd`
        python -c"from runmonitor import restore_tools; restore_tools.resumbit($RMDIR,None,True)"
    fi
fi