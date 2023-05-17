echo ==== Syncing $1:$3 to $2:$3 ====


# local => rpxx  ::  sync local remote <code_path>
if [ "$1" == "local" ] && ( [ "$2" == "rp00" ] || [ "$2" == "rp01" ] ) ; then
	rsync -av --progress --exclude='.git/' --exclude='*.pickle' --exclude='*.pkl' --exclude="__pycache__" ~/Libraries/$3/ $2:~/Libraries/$3/

# local => UW CSE  ::  sync local remote <code_path>
elif [ "$1" == "local" ] && ( [ "$2" == "bundle" ] || [ "$2" == "voltron" ] || [ "$2" == "kakade-gpu2" ] ) ; then
	sshpass -p handrobot1! rsync -av --progress --exclude='.git/' --exclude='*.pickle' --exclude='*.pkl' --exclude="__pycache__" ~/Libraries/$3/ vikash@$2.cs.washington.edu:~/Libraries/$3/

# local => GCP  ::  sync local gcp <code_path> <ec2_ip>
elif [ "$1" == "local" ] && [ "$2" == "gcp" ] ; then
	rsync -av --progress --exclude='.git/' --exclude="__pycache__" ~/Libraries/$3/ $4:~/Libraries/$3/

# local => EC2  ::  sync local ec2 <code_path> <ec2_ip>
elif [ "$1" == "local" ] && [ "$2" == "ec2" ] ; then
	rsync -av --progress -e "ssh -i ~/aws/Vik.pem" --exclude='.git/' --exclude='*.pdf' --exclude='*.pickle' --exclude='*.csv' --exclude="__pycache__" ~/Libraries/$3/ ubuntu@$4:~/Libraries/$3/

# local => devfair  ::  sync local devfair <code_path>
elif [ "$1" == "local" ] && [ "$2" == "devfair" ] ; then
	rsync -r -avz --partial --progress -e "ssh -p 1234" --exclude "datasets" --exclude "outputs" --exclude "agents" --exclude='.git/' --exclude="__pycache__" --exclude="*.DS_Store" ~/Libraries/$3/ localhost:~/Libraries/$3/

# Berkeley => local  :: sync remote local <log_path>
elif [ "$1" == "newton1" ] || [ "$1" == "newton2" ] || [ "$1" == "newton3" ] || [ "$1" == "newton4" ] || [ "$1" == "newton5" ] || [ "$1" == "newton6" ] || [ "$1" == "newton7" ] || [ "$1" == "allegrobase" ] ; then
	rsync -av --include='best_policy.pickle' --exclude='*.pickle' vikash@$1.banatao.berkeley.edu:~/Projects/$3 ~/Projects/

# UW => local
elif ( [ "$1" == "rp00" ]  || [ "$1" == "rp01" ] ) && [ "$2" == "local" ] ; then
	rsync -av --include='best_policy.pickle' --exclude='*.pickle' --exclude='*.out' $1:~/Projects/$3 ~/Projects/


# UW => local
elif ( [ "$1" == "bundle" ]  || [ "$1" == "voltron" ] ) && [ "$2" == "local" ] ; then
	rsync -av --include='best_policy.pickle' --exclude='*.pickle' --exclude='*.out' vikash@$1.cs.washington.edu:~/Projects/$3 ~/Projects/

# GCP => local
elif [ "$1" == "gcp" ] && [ "$2" == "local" ] ; then
	rsync -av --include='best_policy.pickle' --exclude='*.pickle' --exclude='*.out' $4:~/Projects/$3/ ~/Projects/$3/

# EC2 => local
elif [ "$1" == "ec2" ] && [ "$2" == "local" ] ; then
	rsync -av --progress -e "ssh -i ~/aws/Vik.pem" --include='best_policy.pickle' --exclude='*.pickle' --exclude='*.out' ubuntu@$4:~/Projects/$3/ ~/Projects/$3/

# devfair => local
elif [ "$1" == "devfair" ] && [ "$2" == "local" ] ; then
	rsync -r -avz --partial --progress -e "ssh -p 1234" --include='best_policy.pickle' --exclude='*.pickle' --exclude='*.hydra' --exclude='*.out' --exclude='ferm/*' --exclude='**/wandb/**' localhost:/checkpoint/vikashplus/$3/ ~/Projects/mj_envs/$3/
# elif [ "$1" == "devfair" ] && [ "$2" == "local" ] ; then
# 	rsync -r -avz --partial --progress -e "ssh -p 1234" --include='best_policy.pickle' --exclude='*.pickle' --exclude='*.out' --exclude='*.png' --include='*.log' --exclude='*/buffer/*.pt' --include='actor_2320000.pat' --include='critic_2320000.pat' --exclude='*.pt' --exclude='*/tb/*' --exclude='ferm/*' localhost:~/Projects/$3/ ~/Projects/$3/
# FERM
# elif [ "$1" == "devfair" ] && [ "$2" == "local" ] ; then
	# rsync -r -avz --partial --progress -e "ssh -p 1234" --include='best_policy.pickle' --exclude='*.pickle' --include='eval.log' --include='log.csv' --include='args.json' --exclude='*.*' localhost:~/Projects/$3/ ~/Projects/$3/

elif [ "$1" == "devfair-scp" ] && [ "$2" == "local" ] ; then
	scp -r -o ProxyJump=snc-fairjmp201 100.97.72.99:~/Projects/$3 ~/Projects/$3

# S3 => local
elif [ "$1" == "s3:sac" ] && [ "$2" == "local" ] ; then
	# aws s3 sync s3://$3/ ~/Projects/$3/ --exclude '*' --include '*/params.json' --include '*/progress.csv' #--include '*.txt' --include '*.csv' --include '*.json' --include '*.gz' --include '*.tar' --include '*.log' --include '*.pkl'
	aws s3 sync s3://$3/ ~/Projects/$3/ --exclude '*' --include '*/checkpoint_*000/policy.*' --include '*/params.json' --include '*/params.pkl' --include '*/progress.csv' #--include '*.txt' --include '*.csv' --include '*.json' --include '*.gz' --include '*.tar' --include '*.log' --include '*.pkl'

# S3:MJRL => local
elif [ "$1" == "s3:mjrl" ] && [ "$2" == "local" ] ; then
	aws s3 sync s3://$3/ ~/Projects/$3/ --exclude='*.pickle' --include "*/best_policy.pickle" --exclude='*.out'

# SAC:: remote => local
# Usage:: ./sync <src:sac> <dest> <checkpoint#>
elif ( [ "$1" == "bundle:sac" ]  || [ "$1" == "voltron:sac" ] ) && [ "$2" == "local" ] ; then
	sshpass -p handrobot1! rsync -av vikash@$1.cs.washington.edu:~/ray_results/ ~/ray_results/ --include '*/' --include '*params.json' --include '*params.pkl' --include '*progress.csv' --include "**/checkpoint_$3/policy*" --exclude '*' --prune-empty-dirs

else
	echo Unknown options "'$1'" "'$2'"
fi

