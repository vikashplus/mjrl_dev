# Performance of NPG on Kitchen tasks for V0.1 release

## Results
Results are provided for two variants
- [DEMO_ENTRY_POINT (Fixed init)](outputs_kitchenJ5c_3.8)
- [RANDOM_ENTRY_POINT (Random init)](outputs_kitchenJ5d_3.9)

We notice that `random_init` performs on par with `fixed_init`. Moving forwards it makes sense to defaul to `random_init`. Inference (especially with relay datasets) will probably still need `fixed_init` to initialize in the demo distribution.

## Known Issues
- envs are not serializable (fixed in v0.2dev)
- lots of redundent envs that needs clearning

## Hashes
```
 1a0ddda0040c332198375dcddaea4811f54736bb (mj_envs, tag: v0.1)
 0fe8a446c5b580ec49f2458d68747fcebb191fc0 sims/Adroit (v0.1)
 30e0d1f7f2c89f016c4962da8c5a6c173579170c sims/YCB_sim (30e0d1f)
 b8531308fa34d2bd637d9df468455ae36e2ebcd3 sims/dmanus_sim (heads/master)
 f821a0f6c6739999019221124e1abc46f681113d sims/fetch_sim (heads/master)
 51f0c9db8b723d96c902d2bf8748ffc1efaabfc8 sims/franka_sim (v0.1-1-g51f0c9d)
 079fbf4e38dffdba3157f3c264db633842e519b8 sims/furniture_sim (v0.1-9-g079fbf4)
 931272aca91c674a17e7450352686b4d4cd1d1d8 sims/neuromuscular_sim (v0.1-24-g931272a)
 78424cd0fea6ca4e155c9faab801267363cdd4ff sims/sawyer_sim (heads/master)
 0585477aca9bf34cbbd2d4ee721ec56875f31d92 sims/scene_sim (heads/master)
 ```