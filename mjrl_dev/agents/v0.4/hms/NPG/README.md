# Performance of NPG on HMS tasks for V0.4 release
- V0 envs are the original envs released with the [DAPG paper](https://sites.google.com/view/deeprl-dexterous-manipulation)
- V1 envs are new version of the same envs. Beyond unifying into a central codebase, main feature upgrade is that rewards are calculated from obs_dict. This was needed especially for MBRL.

## Results
Comparision: V0.4 vs V0.3 (3 seeds)
- [Final performance comparision](FinalPerf-NPG.pdf)
- [Training curves comparision](TrainPerf-NPG.pdf)

## Known Issues
- N/A

## Hashes
```
83d35df95eb64274c5e93bb32a0a4e2f6576638a (mjrl)
65b63a375eab3deb835faf011cdf189aaa07e502 (robohive, tag: v04)
2ef4b752e85782f84fa666fce10de5231cc5c917 sims/Adroit (v0.1-2-g2ef4b75)
46edd9c361061c5d81a82f2511d4fbf76fead569 sims/YCB_sim (heads/main)
b8531308fa34d2bd637d9df468455ae36e2ebcd3 sims/dmanus_sim (heads/correct_bracket)
58d561fa416b6a151761ced18f2dc8f067188909 sims/fetch_sim (heads/master)
82aaf3bebfa29e00133a6eebc7684e793c668fc1 sims/franka_sim (v0.1-7-g82aaf3b)
eb6622db075d8d92436a5a41899070b8871d1f89 sims/furniture_sim (v0.1-19-geb6622d)
cee0634091e1c5bf8d0897c16f8297513366702b sims/myo_sim (v0.1-51-gcee0634)
87cd8dd5a11518b94fca16bc22bb04f6836c6aa7 sims/object_sim (87cd8dd)
68030f77f73e247518f9620ab0eed01286ace7b4 sims/robel_sim (heads/experimental-hand)
854d0bfb4e48b076e1d2aa4566c2e23bba17ebae sims/robotiq_sim (heads/main)
affaf56d56be307538e5eed34f647586281762b2 sims/sawyer_sim (heads/master)
145d4bbc3719f19a76e229ef640dff15263b50bc sims/scene_sim (145d4bb)
49e689ee8d18f5e506ba995aac99822b66700b2b sims/trifinger_sim (heads/main)
```