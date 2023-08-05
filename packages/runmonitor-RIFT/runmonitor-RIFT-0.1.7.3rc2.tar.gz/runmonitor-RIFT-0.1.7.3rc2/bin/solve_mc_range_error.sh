#!/usr/bin/env bash
#Script to fix error resulting from incorrect chirp mass range restrictions in CIP. Finds relevant error file, checks to see if the error is caused by the chirp mass range restrictions, finds the minimum and maximum chirp mass values as given in all.net, and sets that as the new range and resubmits the job.

ERROR_FILE=$(python -c'from runmonitor import heal; heal.check_error()')

if [[ $ERROR_FILE = CIP*.sub ]]; then
    ITERATION=$(ls posterior_samples-*.dat | wc -l)
    if [ $(python -c"from runmonitor import heal; heal.check_mc_range_error($ITERATION)") ]; then
        MINMC=$(sort -nk2 all.net | head -1 | awk '{print $2}')
        MAXMC=$(sort -nk2 all.net | tail -1 | awk '{print $2}')
        for FILE in CIP*.sub; 
            sed -i "s/--mc-range  '[*]'/--mc-range  '[$MINMC,$MAXMC]'" $FILE
        done
    fi
    RMDIR='pwd'
    python -c"from runmonitor import restore_tools; restore_tools.resubmit($RMDIR,None,False)"
fi