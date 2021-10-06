help="
USAGE:
./hydra/train_rs_tasks.sh <task> <target>
    <task> choices:     kitchen, biomechanics
    <target> choices:   '', local, slurm

Example:
./hydra/train_rs_tasks.sh kitchen       # runs natively
./hydra/train_rs_tasks.sh kitchen local # use local launcher
./hydra/train_rs_tasks.sh kitchen slurm # use slurm launcher
"

# Configure launch
if [ "$#" -ne 2 ] ; then
    config=""
else
    config="--multirun hydra/output=$2 hydra/launcher=$2"
fi

# Configure envs
if [ "$1" == "kitchen" ] ; then
    envs="kitchen_micro_open-v3,kitchen_rdoor_open-v3,kitchen_ldoor_open-v3,kitchen_sdoor_open-v3,kitchen_light_on-v3,kitchen_knob4_on-v3,kitchen_knob3_on-v3,kitchen_knob2_on-v3,kitchen_knob1_on-v3"

    config="--config-name hydra_kitchen_config.yaml $config"

elif [ "$1" == "biomechanics" ] ; then
    envs="FingerReachMotorFixed-v0,FingerReachMotorRandom-v0,FingerReachMuscleFixed-v0,FingerReachMuscleRandom-v0,FingerPoseMotorFixed-v0,FingerPoseMotorRandom-v0,FingerPoseMuscleFixed-v0,FingerPoseMuscleRandom-v0,ElbowPose1D1MRandom-v0,ElbowPose1D6MRandom-v0,ElbowPose1D6MExoRandom-v0,HandKeyTurnFixed-v0,HandKeyTurnRandom-v0,HandPenTwirlFixed-v0,HandPenTwirlRandom-v0,BaodingFixed-v1,BaodingFixed4th-v1,BaodingFixed8th-v1"

    config="--config-name hydra_biomechanics_config.yaml $config"

else
    # echo $help
    printf "$help"
    exit 0
fi

# Disp NPG commands
echo "NPG: ======="
echo "python hydra_mjrl_launcher.py --config-path config $config env=$envs"

# Disp SAC commands
echo "SAC: ======="
echo "python launcher_vrl.py --config-path config $config env=$envs env_args.from_pixels=False algos=sac"