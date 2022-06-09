# Performance of NPG on HMS tasks for V0.2 release
- [V0](outputs_hands0.2a(v0)) envs are the original envs released with the [DAPG paper](https://sites.google.com/view/deeprl-dexterous-manipulation)
- [V1](outputs_hands0.2a(v1)) envs are new version of the same envs. Beyond unifying into a central codebase, main feature upgrade is that rewards calculated from obs_dict. This was needed especially for MBRL.

## Results
V0.2
- [Final performance](outputs_hands0.2a(v1)/FinalPerf-NPG.pdf)
- [Training curves](outputs_hands0.2a(v1)/TrainPerf-NPG.pdf)

Comparision: V0.2 vs V0.1 (5M samples, 3 seeds)
- [Final performance comparision](FinalPerf-NPG-version-comparisions.pdf)
- [Training curves comparision](TrainPerf-NPG-version-comparisions.pdf)

## Known Issues
- N/A

## Hashes
```
55726c3b135d908a871a8d30f3cf3a2cca16181b (mjrl)
5b29ccad3886156778cce23411a0b5ed01042b03 (mj_envs, tag: v0.2)
0fe8a446c5b580ec49f2458d68747fcebb191fc0 sims/Adroit (v0.1)
46edd9c361061c5d81a82f2511d4fbf76fead569 sims/YCB_sim (heads/main)
b8531308fa34d2bd637d9df468455ae36e2ebcd3 sims/dmanus_sim (heads/correct_bracket)
f821a0f6c6739999019221124e1abc46f681113d sims/fetch_sim (heads/master)
a261b9a42dd95fc9bb86e6902ec8e1d3665ea147 sims/franka_sim (v0.1-2-ga261b9a)
5b2317c6bb717deafe9dd321b5a49450e3bfef39 sims/furniture_sim (v0.1-14-g5b2317c)
31c11878e07b174cd02f4c5cd811a20b716ecf74 sims/neuromuscular_sim (v0.1-31-g31c1187)
87cd8dd5a11518b94fca16bc22bb04f6836c6aa7 sims/object_sim (heads/main)
68030f77f73e247518f9620ab0eed01286ace7b4 sims/robel_sim (heads/experimental-hand)
78424cd0fea6ca4e155c9faab801267363cdd4ff sims/sawyer_sim (heads/master)
8ca329fef00b7d6f985b3e6ef5460f48980c8f18 sims/scene_sim (heads/master)
49e689ee8d18f5e506ba995aac99822b66700b2b sims/trifinger_sim (heads/main)
 ```