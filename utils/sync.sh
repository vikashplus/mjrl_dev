# Use "chmod +x sync.sh" once to use this script

# sync <source> <destination> <folder>
# EXAMPLE: sync local newton4 solveHMS
# EXAMPLE: sync newton1 local transferHMS

echo ==== Syncing $1:$3 to $2:$3 ====

if [ "$1" == "local" ] && ( [ "$2" == "bundle" ] || [ "$2" == "voltron" ] ) ; then
	rsync -av --progress --exclude='.git/' --exclude="__pycache__" ~/Libraries/$3/ vikash@$2.cs.washington.edu:~/Libraries/$3/
elif [ "$1" == "local" ] && [ "$2" == "instance1" ] ; then
	rsync -av -e "ssh -i /Users/vikashplus/.ssh/google_compute_engine" --progress --exclude='.git/' --exclude="__pycache__" ~/Libraries/$3/ vikashplus@35.203.146.127:~/Libraries/$3/
elif [ "$1" == "local" ] ; then
	rsync -av --progress --exclude='.git/' ~/Libraries/$3/ vikash@$2.banatao.berkeley.edu:~/Libraries/$3/


elif [ "$1" == "newton1" ] || [ "$1" == "newton2" ] || [ "$1" == "newton3" ] || [ "$1" == "newton4" ] || [ "$1" == "newton5" ] || [ "$1" == "newton6" ] || [ "$1" == "newton7" ] || [ "$1" == "allegrobase" ] ; then
	rsync -av --include='best_policy.pickle' --exclude='*.pickle' vikash@$1.banatao.berkeley.edu:~/Projects/$3 ~/Projects/
elif ( [ "$1" == "bundle" ]  || [ "$1" == "voltron" ] ) && [ "$2" == "local" ] ; then
	rsync -av --include='best_policy.pickle' --exclude='*.pickle' vikash@$1.cs.washington.edu:~/Projects/$3 ~/Projects/
elif [ "$1" == "instance1" ] && [ "$2" == "local" ] ; then
	rsync -av -e "ssh -i /Users/vikashplus/.ssh/google_compute_engine" --include='best_policy.pickle' --exclude='*.pickle' vikashplus@35.203.146.127:~/Projects/$3 ~/Projects/$3
else
	echo Unknown options "'$1'" "'$2'"
fi
