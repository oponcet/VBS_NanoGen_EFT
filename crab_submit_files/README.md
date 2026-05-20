# Crab submission

Two config files are available for crab submission: 2017 and 2018. To launch crab generation simply run 

```
cmssw-cc7
cmsrel CMSSW_10_6_19_patch3
cd CMSSW_10_6_19_patch3/src; cmsenv; cd -
crab submit crab_sub_2018.py
```

Or equivalently ```crab submit crab_sub_2017.py``` or 2016.


With the current setup, I am writing to Bari T2:
`gfal-ls davs://webdav.recas.ba.infn.it:8443/cms/store/user/mpresill/osWW_EFT/OSWWemu_EWK_dim6_topU3l/OSWWemu_EWK_dim6_topU3l/250715_154441/0000`
