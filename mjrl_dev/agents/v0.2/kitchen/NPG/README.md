# Performance of NPG on Kitchen tasks for V0.2 release
In [V0.1](https://github.com/vikashplus/mjrl_dev/blob/redesign/mjrl_dev/agents/v0.1/kitchen/NPG/FinalPerf-NPG.pdf) we notice that `random_init` performs on par with `fixed_init`. Moving forward we are defaulting to `random_init`. Results for v0.2 are provided for [RANDOM_ENTRY_POINT](outputs_kitchenJ8a).
Note: Inference with respect to relay datasets will probably still need `fixed_init` to initialize in the demo distribution.

## Results
V0.2 (5M samples, 3 seeds)
- [Final performance](FinalPerf-NPG.pdf)
- [Training curves](TrainPerf-NPG.pdf)

Comparision: V0.2 vs V0.1 (5M samples, 3 seeds)
- [Final performance comparision](FinalPerf-NPG-version-comparisions.pdf)
- [Training curves comparision](TrainPerf-NPG-version-comparisions.pdf)


## Known Issues
- N/A

## Hashes
```
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