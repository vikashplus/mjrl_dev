# Performance of NPG on Kitchen tasks for V0.3 release
- In [V0.1](https://github.com/vikashplus/mjrl_dev/blob/redesign/mjrl_dev/agents/v0.1/kitchen/NPG/FinalPerf-NPG.pdf) we notice that `random_init` performs on par with `fixed_init`. Moving forward we are defaulting to `random_init`.
- Results for v0.2 are provided for `RANDOM_ENTRY_POINT`.
Note: Inference with respect to relay datasets will probably still need `fixed_init` to initialize in the demo distribution.

## Results
V0.3 (3 seeds + Comparision wrt V0.2 )
- [Final performance](FinalPerf-NPG.pdf)
- [Training curves](TrainPerf-NPG.pdf)

## Known Issues
- N/A

## Hashes
```
55726c3b135d908a871a8d30f3cf3a2cca16181b (mjrl)
508b6ce24857e9d78d91462ee8d4d430256ad19f (mj_envs, tag: v03)
0fe8a446c5b580ec49f2458d68747fcebb191fc0 sims/Adroit (v0.1)
46edd9c361061c5d81a82f2511d4fbf76fead569 sims/YCB_sim (heads/main)
b8531308fa34d2bd637d9df468455ae36e2ebcd3 sims/dmanus_sim (heads/correct_bracket)
f821a0f6c6739999019221124e1abc46f681113d sims/fetch_sim (heads/master)
1c7bc423e098abce0fb0699262fc8c0656fc7428 sims/franka_sim (v0.1-3-g1c7bc42)
100793bc69a9feeddce8343ecda1101518cf5b7c sims/furniture_sim (v0.1-16-g100793b)
ab2c83b071a31f877458593e627e7f40c174986f sims/neuromuscular_sim (v0.1-34-gab2c83b)
87cd8dd5a11518b94fca16bc22bb04f6836c6aa7 sims/object_sim (87cd8dd)
68030f77f73e247518f9620ab0eed01286ace7b4 sims/robel_sim (heads/experimental-hand)
891e813f1e03fc12b603137fbb39db5fb15ed663 sims/robotiq_sim (891e813)
78424cd0fea6ca4e155c9faab801267363cdd4ff sims/sawyer_sim (heads/master)
8ca329fef00b7d6f985b3e6ef5460f48980c8f18 sims/scene_sim (heads/master)
49e689ee8d18f5e506ba995aac99822b66700b2b sims/trifinger_sim (heads/main)
```