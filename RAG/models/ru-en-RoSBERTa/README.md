---
model-index:
- name: ru-en-RoSBERTa
  results:
  - dataset:
      config: default
      name: MTEB CEDRClassification (default)
      revision: c0ba03d058e3e1b2f3fd20518875a4563dd12db4
      split: test
      type: ai-forever/cedr-classification
    metrics:
    - type: accuracy
      value: 44.68650371944739
    - type: f1
      value: 40.7601061886426
    - type: lrap
      value: 70.69633368756747
    - type: main_score
      value: 44.68650371944739
    task:
      type: MultilabelClassification
  - dataset:
      config: default
      name: MTEB GeoreviewClassification (default)
      revision: 3765c0d1de6b7d264bc459433c45e5a75513839c
      split: test
      type: ai-forever/georeview-classification
    metrics:
    - type: accuracy
      value: 49.697265625
    - type: f1
      value: 47.793186725286866
    - type: f1_weighted
      value: 47.79131720298068
    - type: main_score
      value: 49.697265625
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB GeoreviewClusteringP2P (default)
      revision: 97a313c8fc85b47f13f33e7e9a95c1ad888c7fec
      split: test
      type: ai-forever/georeview-clustering-p2p
    metrics:
    - type: main_score
      value: 65.42249614873316
    - type: v_measure
      value: 65.42249614873316
    - type: v_measure_std
      value: 0.8524815312312278
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB HeadlineClassification (default)
      revision: 2fe05ee6b5832cda29f2ef7aaad7b7fe6a3609eb
      split: test
      type: ai-forever/headline-classification
    metrics:
    - type: accuracy
      value: 78.0029296875
    - type: f1
      value: 77.95151940601424
    - type: f1_weighted
      value: 77.95054643947716
    - type: main_score
      value: 78.0029296875
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB InappropriatenessClassification (default)
      revision: 601651fdc45ef243751676e62dd7a19f491c0285
      split: test
      type: ai-forever/inappropriateness-classification
    metrics:
    - type: accuracy
      value: 61.32324218750001
    - type: ap
      value: 57.11029460364367
    - type: ap_weighted
      value: 57.11029460364367
    - type: f1
      value: 60.971337406307214
    - type: f1_weighted
      value: 60.971337406307214
    - type: main_score
      value: 61.32324218750001
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB KinopoiskClassification (default)
      revision: 5911f26666ac11af46cb9c6849d0dc80a378af24
      split: test
      type: ai-forever/kinopoisk-sentiment-classification
    metrics:
    - type: accuracy
      value: 63.27333333333334
    - type: f1
      value: 61.007042785228116
    - type: f1_weighted
      value: 61.007042785228116
    - type: main_score
      value: 63.27333333333334
    task:
      type: Classification
  - dataset:
      config: ru
      name: MTEB MIRACLReranking (ru)
      revision: 6d1962c527217f8927fca80f890f14f36b2802af
      split: dev
      type: miracl/mmteb-miracl-reranking
    metrics:
    - type: MAP@1(MIRACL)
      value: 30.691000000000003
    - type: MAP@10(MIRACL)
      value: 49.178
    - type: MAP@100(MIRACL)
      value: 51.225
    - type: MAP@1000(MIRACL)
      value: 51.225
    - type: MAP@20(MIRACL)
      value: 50.613
    - type: MAP@3(MIRACL)
      value: 42.457
    - type: MAP@5(MIRACL)
      value: 46.172000000000004
    - type: NDCG@1(MIRACL)
      value: 51.002
    - type: NDCG@10(MIRACL)
      value: 56.912
    - type: NDCG@100(MIRACL)
      value: 61.197
    - type: NDCG@1000(MIRACL)
      value: 61.197
    - type: NDCG@20(MIRACL)
      value: 59.453
    - type: NDCG@3(MIRACL)
      value: 51.083
    - type: NDCG@5(MIRACL)
      value: 53.358000000000004
    - type: P@1(MIRACL)
      value: 51.002
    - type: P@10(MIRACL)
      value: 14.852000000000002
    - type: P@100(MIRACL)
      value: 1.9529999999999998
    - type: P@1000(MIRACL)
      value: 0.19499999999999998
    - type: P@20(MIRACL)
      value: 8.657
    - type: P@3(MIRACL)
      value: 31.435000000000002
    - type: P@5(MIRACL)
      value: 23.608999999999998
    - type: Recall@1(MIRACL)
      value: 30.691000000000003
    - type: Recall@10(MIRACL)
      value: 67.006
    - type: Recall@100(MIRACL)
      value: 79.952
    - type: Recall@1000(MIRACL)
      value: 79.952
    - type: Recall@20(MIRACL)
      value: 73.811
    - type: Recall@3(MIRACL)
      value: 49.142
    - type: Recall@5(MIRACL)
      value: 57.553
    - type: main_score
      value: 56.912
    - type: nAUC_MAP@1000_diff1(MIRACL)
      value: 10.786403475779332
    - type: nAUC_MAP@1000_max(MIRACL)
      value: 29.477246196287275
    - type: nAUC_MAP@1000_std(MIRACL)
      value: 15.938834129839046
    - type: nAUC_MAP@100_diff1(MIRACL)
      value: 10.786403475779332
    - type: nAUC_MAP@100_max(MIRACL)
      value: 29.477246196287275
    - type: nAUC_MAP@100_std(MIRACL)
      value: 15.938834129839046
    - type: nAUC_MAP@10_diff1(MIRACL)
      value: 12.255091348037595
    - type: nAUC_MAP@10_max(MIRACL)
      value: 26.72625370045134
    - type: nAUC_MAP@10_std(MIRACL)
      value: 14.180071586837812
    - type: nAUC_MAP@1_diff1(MIRACL)
      value: 28.616487922173768
    - type: nAUC_MAP@1_max(MIRACL)
      value: 12.986192530664518
    - type: nAUC_MAP@1_std(MIRACL)
      value: 4.086145762604503
    - type: nAUC_MAP@20_diff1(MIRACL)
      value: 11.360341572700476
    - type: nAUC_MAP@20_max(MIRACL)
      value: 28.612330384153832
    - type: nAUC_MAP@20_std(MIRACL)
      value: 15.787480742877937
    - type: nAUC_MAP@3_diff1(MIRACL)
      value: 18.033783954867623
    - type: nAUC_MAP@3_max(MIRACL)
      value: 20.97092332905034
    - type: nAUC_MAP@3_std(MIRACL)
      value: 9.106058710108279
    - type: nAUC_MAP@5_diff1(MIRACL)
      value: 14.784231238848433
    - type: nAUC_MAP@5_max(MIRACL)
      value: 23.841145797143
    - type: nAUC_MAP@5_std(MIRACL)
      value: 11.25686258970321
    - type: nAUC_NDCG@1000_diff1(MIRACL)
      value: 1.4728095471561125
    - type: nAUC_NDCG@1000_max(MIRACL)
      value: 39.84262968697792
    - type: nAUC_NDCG@1000_std(MIRACL)
      value: 22.4186410243652
    - type: nAUC_NDCG@100_diff1(MIRACL)
      value: 1.4728095471561125
    - type: nAUC_NDCG@100_max(MIRACL)
      value: 39.84262968697792
    - type: nAUC_NDCG@100_std(MIRACL)
      value: 22.4186410243652
    - type: nAUC_NDCG@10_diff1(MIRACL)
      value: 5.242996478950954
    - type: nAUC_NDCG@10_max(MIRACL)
      value: 33.86925934510759
    - type: nAUC_NDCG@10_std(MIRACL)
      value: 19.457386638149625
    - type: nAUC_NDCG@1_diff1(MIRACL)
      value: 16.925455715967676
    - type: nAUC_NDCG@1_max(MIRACL)
      value: 36.72266755084653
    - type: nAUC_NDCG@1_std(MIRACL)
      value: 18.357456476212622
    - type: nAUC_NDCG@20_diff1(MIRACL)
      value: 3.361697278095995
    - type: nAUC_NDCG@20_max(MIRACL)
      value: 37.38923489423496
    - type: nAUC_NDCG@20_std(MIRACL)
      value: 22.29168372402657
    - type: nAUC_NDCG@3_diff1(MIRACL)
      value: 10.936904314592084
    - type: nAUC_NDCG@3_max(MIRACL)
      value: 30.547718047674284
    - type: nAUC_NDCG@3_std(MIRACL)
      value: 15.142352896765665
    - type: nAUC_NDCG@5_diff1(MIRACL)
      value: 8.618074920961075
    - type: nAUC_NDCG@5_max(MIRACL)
      value: 30.808600807482367
    - type: nAUC_NDCG@5_std(MIRACL)
      value: 15.793512242130051
    - type: nAUC_P@1000_diff1(MIRACL)
      value: -24.81839490148569
    - type: nAUC_P@1000_max(MIRACL)
      value: 34.16200383739091
    - type: nAUC_P@1000_std(MIRACL)
      value: 20.95890369662007
    - type: nAUC_P@100_diff1(MIRACL)
      value: -24.818394901485657
    - type: nAUC_P@100_max(MIRACL)
      value: 34.16200383739092
    - type: nAUC_P@100_std(MIRACL)
      value: 20.958903696620112
    - type: nAUC_P@10_diff1(MIRACL)
      value: -22.646461560750986
    - type: nAUC_P@10_max(MIRACL)
      value: 34.57373514819872
    - type: nAUC_P@10_std(MIRACL)
      value: 24.27599718176041
    - type: nAUC_P@1_diff1(MIRACL)
      value: 16.925455715967676
    - type: nAUC_P@1_max(MIRACL)
      value: 36.72266755084653
    - type: nAUC_P@1_std(MIRACL)
      value: 18.357456476212622
    - type: nAUC_P@20_diff1(MIRACL)
      value: -23.33449798384014
    - type: nAUC_P@20_max(MIRACL)
      value: 34.92822081787735
    - type: nAUC_P@20_std(MIRACL)
      value: 25.048280657629267
    - type: nAUC_P@3_diff1(MIRACL)
      value: -11.60659490286
    - type: nAUC_P@3_max(MIRACL)
      value: 38.187883056013035
    - type: nAUC_P@3_std(MIRACL)
      value: 21.234776997940628
    - type: nAUC_P@5_diff1(MIRACL)
      value: -18.86697977242918
    - type: nAUC_P@5_max(MIRACL)
      value: 35.6110661197626
    - type: nAUC_P@5_std(MIRACL)
      value: 22.11165620702996
    - type: nAUC_Recall@1000_diff1(MIRACL)
      value: -31.456413113303867
    - type: nAUC_Recall@1000_max(MIRACL)
      value: 63.785265733309636
    - type: nAUC_Recall@1000_std(MIRACL)
      value: 36.587933217871914
    - type: nAUC_Recall@100_diff1(MIRACL)
      value: -31.456413113303867
    - type: nAUC_Recall@100_max(MIRACL)
      value: 63.785265733309636
    - type: nAUC_Recall@100_std(MIRACL)
      value: 36.587933217871914
    - type: nAUC_Recall@10_diff1(MIRACL)
      value: -9.518740341549913
    - type: nAUC_Recall@10_max(MIRACL)
      value: 35.00853357699468
    - type: nAUC_Recall@10_std(MIRACL)
      value: 22.79313936486099
    - type: nAUC_Recall@1_diff1(MIRACL)
      value: 28.616487922173768
    - type: nAUC_Recall@1_max(MIRACL)
      value: 12.986192530664518
    - type: nAUC_Recall@1_std(MIRACL)
      value: 4.086145762604503
    - type: nAUC_Recall@20_diff1(MIRACL)
      value: -17.771143411342166
    - type: nAUC_Recall@20_max(MIRACL)
      value: 47.59780316487735
    - type: nAUC_Recall@20_std(MIRACL)
      value: 33.25494707686132
    - type: nAUC_Recall@3_diff1(MIRACL)
      value: 10.171226133119783
    - type: nAUC_Recall@3_max(MIRACL)
      value: 21.097634288680847
    - type: nAUC_Recall@3_std(MIRACL)
      value: 10.087211861733298
    - type: nAUC_Recall@5_diff1(MIRACL)
      value: 1.6868374913242932
    - type: nAUC_Recall@5_max(MIRACL)
      value: 25.874440474993165
    - type: nAUC_Recall@5_std(MIRACL)
      value: 13.46380924822079
    task:
      type: Reranking
  - dataset:
      config: ru
      name: MTEB MIRACLRetrieval (ru)
      revision: main
      split: dev
      type: miracl/mmteb-miracl
    metrics:
    - type: main_score
      value: 53.909
    - type: map_at_1
      value: 24.308
    - type: map_at_10
      value: 43.258
    - type: map_at_100
      value: 46.053
    - type: map_at_1000
      value: 46.176
    - type: map_at_20
      value: 44.962
    - type: map_at_3
      value: 36.129
    - type: map_at_5
      value: 40.077
    - type: mrr_at_1
      value: 49.92012779552716
    - type: mrr_at_10
      value: 62.639554490592865
    - type: mrr_at_100
      value: 63.09260401526302
    - type: mrr_at_1000
      value: 63.10428906436666
    - type: mrr_at_20
      value: 62.94919151853632
    - type: mrr_at_3
      value: 60.15708200212997
    - type: mrr_at_5
      value: 61.83439829605969
    - type: nauc_map_at_1000_diff1
      value: 24.249990208199268
    - type: nauc_map_at_1000_max
      value: 25.29688440384686
    - type: nauc_map_at_1000_std
      value: 2.4312163206740536
    - type: nauc_map_at_100_diff1
      value: 24.2554939267347
    - type: nauc_map_at_100_max
      value: 25.25054164924535
    - type: nauc_map_at_100_std
      value: 2.4121726280069757
    - type: nauc_map_at_10_diff1
      value: 24.411765629418987
    - type: nauc_map_at_10_max
      value: 23.13035697774593
    - type: nauc_map_at_10_std
      value: -0.1673711528601927
    - type: nauc_map_at_1_diff1
      value: 30.55123128484441
    - type: nauc_map_at_1_max
      value: 13.83849108263988
    - type: nauc_map_at_1_std
      value: -7.087181528435525
    - type: nauc_map_at_20_diff1
      value: 24.125033292556417
    - type: nauc_map_at_20_max
      value: 24.563171125814296
    - type: nauc_map_at_20_std
      value: 1.266006461448722
    - type: nauc_map_at_3_diff1
      value: 25.71581305774253
    - type: nauc_map_at_3_max
      value: 18.708623514300097
    - type: nauc_map_at_3_std
      value: -4.772722288463871
    - type: nauc_map_at_5_diff1
      value: 25.352787694389097
    - type: nauc_map_at_5_max
      value: 20.974296353287084
    - type: nauc_map_at_5_std
      value: -3.4007260047029835
    - type: nauc_mrr_at_1000_diff1
      value: 29.492072727604622
    - type: nauc_mrr_at_1000_max
      value: 34.60333674990558
    - type: nauc_mrr_at_1000_std
      value: 11.223537361751173
    - type: nauc_mrr_at_100_diff1
      value: 29.47919553914885
    - type: nauc_mrr_at_100_max
      value: 34.618795300361995
    - type: nauc_mrr_at_100_std
      value: 11.243824787491663
    - type: nauc_mrr_at_10_diff1
      value: 29.481060608078298
    - type: nauc_mrr_at_10_max
      value: 34.752363175415745
    - type: nauc_mrr_at_10_std
      value: 10.98618160728943
    - type: nauc_mrr_at_1_diff1
      value: 31.81056902767142
    - type: nauc_mrr_at_1_max
      value: 30.351978574096773
    - type: nauc_mrr_at_1_std
      value: 9.735911194663025
    - type: nauc_mrr_at_20_diff1
      value: 29.390754002995035
    - type: nauc_mrr_at_20_max
      value: 34.75816984434079
    - type: nauc_mrr_at_20_std
      value: 11.325226515477347
    - type: nauc_mrr_at_3_diff1
      value: 29.948364490803186
    - type: nauc_mrr_at_3_max
      value: 33.973850208221556
    - type: nauc_mrr_at_3_std
      value: 9.988883050022485
    - type: nauc_mrr_at_5_diff1
      value: 29.477773016468696
    - type: nauc_mrr_at_5_max
      value: 34.38532892473932
    - type: nauc_mrr_at_5_std
      value: 10.206783034393654
    - type: nauc_ndcg_at_1000_diff1
      value: 24.15494700259076
    - type: nauc_ndcg_at_1000_max
      value: 32.367504385127035
    - type: nauc_ndcg_at_1000_std
      value: 10.372857487814498
    - type: nauc_ndcg_at_100_diff1
      value: 23.97247958991815
    - type: nauc_ndcg_at_100_max
      value: 32.21110774026889
    - type: nauc_ndcg_at_100_std
      value: 11.065328347817761
    - type: nauc_ndcg_at_10_diff1
      value: 24.038789867355796
    - type: nauc_ndcg_at_10_max
      value: 28.14682223937745
    - type: nauc_ndcg_at_10_std
      value: 4.518525314723316
    - type: nauc_ndcg_at_1_diff1
      value: 31.81056902767142
    - type: nauc_ndcg_at_1_max
      value: 30.351978574096773
    - type: nauc_ndcg_at_1_std
      value: 9.735911194663025
    - type: nauc_ndcg_at_20_diff1
      value: 23.157990079778138
    - type: nauc_ndcg_at_20_max
      value: 30.521172934621703
    - type: nauc_ndcg_at_20_std
      value: 7.660125728373433
    - type: nauc_ndcg_at_3_diff1
      value: 24.44153871615053
    - type: nauc_ndcg_at_3_max
      value: 27.08209732696818
    - type: nauc_ndcg_at_3_std
      value: 3.8766269917792537
    - type: nauc_ndcg_at_5_diff1
      value: 24.952468410841863
    - type: nauc_ndcg_at_5_max
      value: 26.29873769608537
    - type: nauc_ndcg_at_5_std
      value: 1.3359423751654511
    - type: nauc_precision_at_1000_diff1
      value: -9.104010991734798
    - type: nauc_precision_at_1000_max
      value: 20.36838078039637
    - type: nauc_precision_at_1000_std
      value: 26.889986331386297
    - type: nauc_precision_at_100_diff1
      value: -7.181546793298205
    - type: nauc_precision_at_100_max
      value: 24.32969645433586
    - type: nauc_precision_at_100_std
      value: 31.546209514202232
    - type: nauc_precision_at_10_diff1
      value: -1.0044021788494442
    - type: nauc_precision_at_10_max
      value: 29.37074096666726
    - type: nauc_precision_at_10_std
      value: 25.000959926288214
    - type: nauc_precision_at_1_diff1
      value: 31.81056902767142
    - type: nauc_precision_at_1_max
      value: 30.351978574096773
    - type: nauc_precision_at_1_std
      value: 9.735911194663025
    - type: nauc_precision_at_20_diff1
      value: -5.242529022989003
    - type: nauc_precision_at_20_max
      value: 28.199268120740822
    - type: nauc_precision_at_20_std
      value: 28.460986811065037
    - type: nauc_precision_at_3_diff1
      value: 9.46419634664173
    - type: nauc_precision_at_3_max
      value: 32.203956451949914
    - type: nauc_precision_at_3_std
      value: 16.4095713138301
    - type: nauc_precision_at_5_diff1
      value: 3.719098257572974
    - type: nauc_precision_at_5_max
      value: 30.53411024247047
    - type: nauc_precision_at_5_std
      value: 17.926227114457067
    - type: nauc_recall_at_1000_diff1
      value: 12.347919922311121
    - type: nauc_recall_at_1000_max
      value: 62.10824756167678
    - type: nauc_recall_at_1000_std
      value: 65.9625810682273
    - type: nauc_recall_at_100_diff1
      value: 11.945066948287723
    - type: nauc_recall_at_100_max
      value: 37.07070306829974
    - type: nauc_recall_at_100_std
      value: 38.76495395051901
    - type: nauc_recall_at_10_diff1
      value: 14.793964290237943
    - type: nauc_recall_at_10_max
      value: 23.170920682517334
    - type: nauc_recall_at_10_std
      value: 5.07461971737137
    - type: nauc_recall_at_1_diff1
      value: 30.55123128484441
    - type: nauc_recall_at_1_max
      value: 13.83849108263988
    - type: nauc_recall_at_1_std
      value: -7.087181528435525
    - type: nauc_recall_at_20_diff1
      value: 10.349310874535616
    - type: nauc_recall_at_20_max
      value: 27.72667852012557
    - type: nauc_recall_at_20_std
      value: 13.37946493360006
    - type: nauc_recall_at_3_diff1
      value: 20.660181561801195
    - type: nauc_recall_at_3_max
      value: 16.734608747226137
    - type: nauc_recall_at_3_std
      value: -5.887299100086449
    - type: nauc_recall_at_5_diff1
      value: 19.292387971699007
    - type: nauc_recall_at_5_max
      value: 18.151647291256193
    - type: nauc_recall_at_5_std
      value: -5.3874570564310895
    - type: ndcg_at_1
      value: 49.919999999999995
    - type: ndcg_at_10
      value: 53.909
    - type: ndcg_at_100
      value: 61.346999999999994
    - type: ndcg_at_1000
      value: 62.831
    - type: ndcg_at_20
      value: 57.44200000000001
    - type: ndcg_at_3
      value: 48.034
    - type: ndcg_at_5
      value: 50.151
    - type: precision_at_1
      value: 49.919999999999995
    - type: precision_at_10
      value: 16.206
    - type: precision_at_100
      value: 2.467
    - type: precision_at_1000
      value: 0.27499999999999997
    - type: precision_at_20
      value: 9.847999999999999
    - type: precision_at_3
      value: 33.013999999999996
    - type: precision_at_5
      value: 25.495
    - type: recall_at_1
      value: 24.308
    - type: recall_at_10
      value: 64.226
    - type: recall_at_100
      value: 88.532
    - type: recall_at_1000
      value: 96.702
    - type: recall_at_20
      value: 73.855
    - type: recall_at_3
      value: 43.75
    - type: recall_at_5
      value: 53.293
    task:
      type: Retrieval
  - dataset:
      config: ru
      name: MTEB MassiveIntentClassification (ru)
      revision: 4672e20407010da34463acc759c162ca9734bca6
      split: test
      type: mteb/amazon_massive_intent
    metrics:
    - type: accuracy
      value: 66.96704774714189
    - type: f1
      value: 63.75700201120695
    - type: f1_weighted
      value: 65.79948352494334
    - type: main_score
      value: 66.96704774714189
    task:
      type: Classification
  - dataset:
      config: ru
      name: MTEB MassiveScenarioClassification (ru)
      revision: fad2c6e8459f9e1c45d9315f4953d921437d70f8
      split: test
      type: mteb/amazon_massive_scenario
    metrics:
    - type: accuracy
      value: 71.79556153328849
    - type: f1
      value: 71.04798190430378
    - type: f1_weighted
      value: 71.11136110921589
    - type: main_score
      value: 71.79556153328849
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB RUParaPhraserSTS (default)
      revision: 43265056790b8f7c59e0139acb4be0a8dad2c8f4
      split: test
      type: merionum/ru_paraphraser
    metrics:
    - type: cosine_pearson
      value: 69.4312341087414
    - type: cosine_spearman
      value: 76.16273410937974
    - type: euclidean_pearson
      value: 73.59970264325928
    - type: euclidean_spearman
      value: 76.16273410937974
    - type: main_score
      value: 76.16273410937974
    - type: manhattan_pearson
      value: 73.63850191752708
    - type: manhattan_spearman
      value: 76.22156395676978
    - type: pearson
      value: 69.4312341087414
    - type: spearman
      value: 76.16273410937974
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB RiaNewsRetrieval (default)
      revision: 82374b0bbacda6114f39ff9c5b925fa1512ca5d7
      split: test
      type: ai-forever/ria-news-retrieval
    metrics:
    - type: main_score
      value: 78.864
    - type: map_at_1
      value: 67.61
    - type: map_at_10
      value: 75.44800000000001
    - type: map_at_100
      value: 75.73
    - type: map_at_1000
      value: 75.74
    - type: map_at_20
      value: 75.63
    - type: map_at_3
      value: 74.058
    - type: map_at_5
      value: 74.935
    - type: mrr_at_1
      value: 67.61
    - type: mrr_at_10
      value: 75.44837698412663
    - type: mrr_at_100
      value: 75.7296913526584
    - type: mrr_at_1000
      value: 75.7404584781072
    - type: mrr_at_20
      value: 75.62998240983255
    - type: mrr_at_3
      value: 74.05833333333295
    - type: mrr_at_5
      value: 74.93533333333274
    - type: nauc_map_at_1000_diff1
      value: 76.73003886073126
    - type: nauc_map_at_1000_max
      value: 23.880592237559313
    - type: nauc_map_at_1000_std
      value: -16.639489061431295
    - type: nauc_map_at_100_diff1
      value: 76.72565072181389
    - type: nauc_map_at_100_max
      value: 23.881455390102456
    - type: nauc_map_at_100_std
      value: -16.63176355032267
    - type: nauc_map_at_10_diff1
      value: 76.64273887966773
    - type: nauc_map_at_10_max
      value: 23.81082154251487
    - type: nauc_map_at_10_std
      value: -16.77740307482434
    - type: nauc_map_at_1_diff1
      value: 79.73607180360645
    - type: nauc_map_at_1_max
      value: 21.20262368559921
    - type: nauc_map_at_1_std
      value: -19.089796155513238
    - type: nauc_map_at_20_diff1
      value: 76.7030611694817
    - type: nauc_map_at_20_max
      value: 23.838907707504127
    - type: nauc_map_at_20_std
      value: -16.672743811541736
    - type: nauc_map_at_3_diff1
      value: 76.50523775835022
    - type: nauc_map_at_3_max
      value: 23.60179905501101
    - type: nauc_map_at_3_std
      value: -17.693757802981956
    - type: nauc_map_at_5_diff1
      value: 76.61576372823448
    - type: nauc_map_at_5_max
      value: 23.862587318336775
    - type: nauc_map_at_5_std
      value: -17.0437966767025
    - type: nauc_mrr_at_1000_diff1
      value: 76.73003886073126
    - type: nauc_mrr_at_1000_max
      value: 23.880592237559313
    - type: nauc_mrr_at_1000_std
      value: -16.639489061431295
    - type: nauc_mrr_at_100_diff1
      value: 76.72565072181389
    - type: nauc_mrr_at_100_max
      value: 23.881455390102456
    - type: nauc_mrr_at_100_std
      value: -16.63176355032267
    - type: nauc_mrr_at_10_diff1
      value: 76.64273887966773
    - type: nauc_mrr_at_10_max
      value: 23.81082154251487
    - type: nauc_mrr_at_10_std
      value: -16.77740307482434
    - type: nauc_mrr_at_1_diff1
      value: 79.73607180360645
    - type: nauc_mrr_at_1_max
      value: 21.20262368559921
    - type: nauc_mrr_at_1_std
      value: -19.089796155513238
    - type: nauc_mrr_at_20_diff1
      value: 76.7030611694817
    - type: nauc_mrr_at_20_max
      value: 23.838907707504127
    - type: nauc_mrr_at_20_std
      value: -16.672743811541736
    - type: nauc_mrr_at_3_diff1
      value: 76.50523775835022
    - type: nauc_mrr_at_3_max
      value: 23.60179905501101
    - type: nauc_mrr_at_3_std
      value: -17.693757802981956
    - type: nauc_mrr_at_5_diff1
      value: 76.61576372823448
    - type: nauc_mrr_at_5_max
      value: 23.862587318336775
    - type: nauc_mrr_at_5_std
      value: -17.0437966767025
    - type: nauc_ndcg_at_1000_diff1
      value: 76.016960312922
    - type: nauc_ndcg_at_1000_max
      value: 25.434179222015285
    - type: nauc_ndcg_at_1000_std
      value: -14.489226598374966
    - type: nauc_ndcg_at_100_diff1
      value: 75.87402195675239
    - type: nauc_ndcg_at_100_max
      value: 25.562687163467295
    - type: nauc_ndcg_at_100_std
      value: -14.165819919505346
    - type: nauc_ndcg_at_10_diff1
      value: 75.47305900096035
    - type: nauc_ndcg_at_10_max
      value: 24.9111489869184
    - type: nauc_ndcg_at_10_std
      value: -15.106328069022739
    - type: nauc_ndcg_at_1_diff1
      value: 79.73607180360645
    - type: nauc_ndcg_at_1_max
      value: 21.20262368559921
    - type: nauc_ndcg_at_1_std
      value: -19.089796155513238
    - type: nauc_ndcg_at_20_diff1
      value: 75.71180859144839
    - type: nauc_ndcg_at_20_max
      value: 25.12671193294504
    - type: nauc_ndcg_at_20_std
      value: -14.582900241958443
    - type: nauc_ndcg_at_3_diff1
      value: 75.32126900936046
    - type: nauc_ndcg_at_3_max
      value: 24.39543091769943
    - type: nauc_ndcg_at_3_std
      value: -17.183511551234538
    - type: nauc_ndcg_at_5_diff1
      value: 75.46170695160178
    - type: nauc_ndcg_at_5_max
      value: 25.001670951020937
    - type: nauc_ndcg_at_5_std
      value: -15.861405796419376
    - type: nauc_precision_at_1000_diff1
      value: 65.48397136632431
    - type: nauc_precision_at_1000_max
      value: 77.05533391807842
    - type: nauc_precision_at_1000_std
      value: 54.14509238038628
    - type: nauc_precision_at_100_diff1
      value: 66.6077978535527
    - type: nauc_precision_at_100_max
      value: 54.07639576230772
    - type: nauc_precision_at_100_std
      value: 28.071043659958185
    - type: nauc_precision_at_10_diff1
      value: 68.71592258481675
    - type: nauc_precision_at_10_max
      value: 31.40944055975099
    - type: nauc_precision_at_10_std
      value: -4.421548783271478
    - type: nauc_precision_at_1_diff1
      value: 79.73607180360645
    - type: nauc_precision_at_1_max
      value: 21.20262368559921
    - type: nauc_precision_at_1_std
      value: -19.089796155513238
    - type: nauc_precision_at_20_diff1
      value: 68.87539427047768
    - type: nauc_precision_at_20_max
      value: 35.602508001542176
    - type: nauc_precision_at_20_std
      value: 3.6366951424017184
    - type: nauc_precision_at_3_diff1
      value: 70.84549884977267
    - type: nauc_precision_at_3_max
      value: 27.35862016332144
    - type: nauc_precision_at_3_std
      value: -15.255203279510601
    - type: nauc_precision_at_5_diff1
      value: 70.27864341297163
    - type: nauc_precision_at_5_max
      value: 30.29162962827962
    - type: nauc_precision_at_5_std
      value: -10.193470309556703
    - type: nauc_recall_at_1000_diff1
      value: 65.48397136632475
    - type: nauc_recall_at_1000_max
      value: 77.05533391807865
    - type: nauc_recall_at_1000_std
      value: 54.14509238038722
    - type: nauc_recall_at_100_diff1
      value: 66.60779785355253
    - type: nauc_recall_at_100_max
      value: 54.07639576230805
    - type: nauc_recall_at_100_std
      value: 28.071043659958207
    - type: nauc_recall_at_10_diff1
      value: 68.71592258481655
    - type: nauc_recall_at_10_max
      value: 31.409440559751168
    - type: nauc_recall_at_10_std
      value: -4.421548783271414
    - type: nauc_recall_at_1_diff1
      value: 79.73607180360645
    - type: nauc_recall_at_1_max
      value: 21.20262368559921
    - type: nauc_recall_at_1_std
      value: -19.089796155513238
    - type: nauc_recall_at_20_diff1
      value: 68.87539427047763
    - type: nauc_recall_at_20_max
      value: 35.60250800154217
    - type: nauc_recall_at_20_std
      value: 3.6366951424018716
    - type: nauc_recall_at_3_diff1
      value: 70.84549884977265
    - type: nauc_recall_at_3_max
      value: 27.358620163321408
    - type: nauc_recall_at_3_std
      value: -15.255203279510626
    - type: nauc_recall_at_5_diff1
      value: 70.2786434129717
    - type: nauc_recall_at_5_max
      value: 30.291629628279733
    - type: nauc_recall_at_5_std
      value: -10.193470309556629
    - type: ndcg_at_1
      value: 67.61
    - type: ndcg_at_10
      value: 78.864
    - type: ndcg_at_100
      value: 80.211
    - type: ndcg_at_1000
      value: 80.50699999999999
    - type: ndcg_at_20
      value: 79.514
    - type: ndcg_at_3
      value: 76.05499999999999
    - type: ndcg_at_5
      value: 77.625
    - type: precision_at_1
      value: 67.61
    - type: precision_at_10
      value: 8.941
    - type: precision_at_100
      value: 0.9570000000000001
    - type: precision_at_1000
      value: 0.098
    - type: precision_at_20
      value: 4.598
    - type: precision_at_3
      value: 27.267000000000003
    - type: precision_at_5
      value: 17.118
    - type: recall_at_1
      value: 67.61
    - type: recall_at_10
      value: 89.41
    - type: recall_at_100
      value: 95.67
    - type: recall_at_1000
      value: 98.02
    - type: recall_at_20
      value: 91.96
    - type: recall_at_3
      value: 81.8
    - type: recall_at_5
      value: 85.59
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB RuBQReranking (default)
      revision: 2e96b8f098fa4b0950fc58eacadeb31c0d0c7fa2
      split: test
      type: ai-forever/rubq-reranking
    metrics:
    - type: main_score
      value: 70.8676293869892
    - type: map
      value: 70.8676293869892
    - type: mrr
      value: 76.21519142795738
    - type: nAUC_map_diff1
      value: 37.107477549298316
    - type: nAUC_map_max
      value: 24.03175751284917
    - type: nAUC_map_std
      value: 10.543266622518289
    - type: nAUC_mrr_diff1
      value: 41.59000224211641
    - type: nAUC_mrr_max
      value: 31.06363682531277
    - type: nAUC_mrr_std
      value: 14.95221681925582
    task:
      type: Reranking
  - dataset:
      config: default
      name: MTEB RuBQRetrieval (default)
      revision: e19b6ffa60b3bc248e0b41f4cc37c26a55c2a67b
      split: test
      type: ai-forever/rubq-retrieval
    metrics:
    - type: main_score
      value: 66.77499999999999
    - type: map_at_1
      value: 38.964
    - type: map_at_10
      value: 58.679
    - type: map_at_100
      value: 59.74699999999999
    - type: map_at_1000
      value: 59.784000000000006
    - type: map_at_20
      value: 59.386
    - type: map_at_3
      value: 53.183
    - type: map_at_5
      value: 56.619
    - type: mrr_at_1
      value: 56.08747044917257
    - type: mrr_at_10
      value: 67.69477747757892
    - type: mrr_at_100
      value: 68.11028091076142
    - type: mrr_at_1000
      value: 68.12016895906572
    - type: mrr_at_20
      value: 67.99200829920431
    - type: mrr_at_3
      value: 65.40583136327825
    - type: mrr_at_5
      value: 66.86564223798278
    - type: nauc_map_at_1000_diff1
      value: 35.13932221843019
    - type: nauc_map_at_1000_max
      value: 31.603311334444573
    - type: nauc_map_at_1000_std
      value: -8.046320861408992
    - type: nauc_map_at_100_diff1
      value: 35.10777181986462
    - type: nauc_map_at_100_max
      value: 31.603059769116086
    - type: nauc_map_at_100_std
      value: -8.027533855390534
    - type: nauc_map_at_10_diff1
      value: 34.864122757362644
    - type: nauc_map_at_10_max
      value: 31.625252670171776
    - type: nauc_map_at_10_std
      value: -8.334256854154406
    - type: nauc_map_at_1_diff1
      value: 40.90418146524424
    - type: nauc_map_at_1_max
      value: 22.269308553048656
    - type: nauc_map_at_1_std
      value: -9.89932822257807
    - type: nauc_map_at_20_diff1
      value: 34.88664926631265
    - type: nauc_map_at_20_max
      value: 31.60883821879978
    - type: nauc_map_at_20_std
      value: -8.095294415067395
    - type: nauc_map_at_3_diff1
      value: 35.13227486507324
    - type: nauc_map_at_3_max
      value: 28.53848590790504
    - type: nauc_map_at_3_std
      value: -9.223288317647375
    - type: nauc_map_at_5_diff1
      value: 35.0811457266201
    - type: nauc_map_at_5_max
      value: 30.904120563551984
    - type: nauc_map_at_5_std
      value: -9.190854442617361
    - type: nauc_mrr_at_1000_diff1
      value: 43.43247399448727
    - type: nauc_mrr_at_1000_max
      value: 37.599979998251435
    - type: nauc_mrr_at_1000_std
      value: -8.461570912726742
    - type: nauc_mrr_at_100_diff1
      value: 43.42803056119293
    - type: nauc_mrr_at_100_max
      value: 37.60590141137654
    - type: nauc_mrr_at_100_std
      value: -8.456064029069271
    - type: nauc_mrr_at_10_diff1
      value: 43.34260974243939
    - type: nauc_mrr_at_10_max
      value: 37.7505248362988
    - type: nauc_mrr_at_10_std
      value: -8.4789005424329
    - type: nauc_mrr_at_1_diff1
      value: 46.8647472051038
    - type: nauc_mrr_at_1_max
      value: 34.40507832070825
    - type: nauc_mrr_at_1_std
      value: -9.148947481764475
    - type: nauc_mrr_at_20_diff1
      value: 43.37024314535158
    - type: nauc_mrr_at_20_max
      value: 37.62040185137823
    - type: nauc_mrr_at_20_std
      value: -8.497477607790167
    - type: nauc_mrr_at_3_diff1
      value: 42.980588675445404
    - type: nauc_mrr_at_3_max
      value: 37.43524263010435
    - type: nauc_mrr_at_3_std
      value: -8.698337782804687
    - type: nauc_mrr_at_5_diff1
      value: 43.224910985482765
    - type: nauc_mrr_at_5_max
      value: 38.00633132611649
    - type: nauc_mrr_at_5_std
      value: -8.554751807691591
    - type: nauc_ndcg_at_1000_diff1
      value: 36.58393000267959
    - type: nauc_ndcg_at_1000_max
      value: 34.491617466873194
    - type: nauc_ndcg_at_1000_std
      value: -6.968933918560401
    - type: nauc_ndcg_at_100_diff1
      value: 35.909285337288004
    - type: nauc_ndcg_at_100_max
      value: 34.60361766529284
    - type: nauc_ndcg_at_100_std
      value: -6.3241815724593256
    - type: nauc_ndcg_at_10_diff1
      value: 34.86940448346685
    - type: nauc_ndcg_at_10_max
      value: 34.89327996781203
    - type: nauc_ndcg_at_10_std
      value: -7.377912505502211
    - type: nauc_ndcg_at_1_diff1
      value: 47.16372543032823
    - type: nauc_ndcg_at_1_max
      value: 34.48620759685232
    - type: nauc_ndcg_at_1_std
      value: -8.881483248224074
    - type: nauc_ndcg_at_20_diff1
      value: 34.901006085701795
    - type: nauc_ndcg_at_20_max
      value: 34.766948088105174
    - type: nauc_ndcg_at_20_std
      value: -6.680375186500669
    - type: nauc_ndcg_at_3_diff1
      value: 35.16537335241684
    - type: nauc_ndcg_at_3_max
      value: 31.385279916552566
    - type: nauc_ndcg_at_3_std
      value: -8.871530629591442
    - type: nauc_ndcg_at_5_diff1
      value: 35.152664105492605
    - type: nauc_ndcg_at_5_max
      value: 33.89982336069226
    - type: nauc_ndcg_at_5_std
      value: -8.92795810387048
    - type: nauc_precision_at_1000_diff1
      value: -6.773234121047722
    - type: nauc_precision_at_1000_max
      value: 7.0059404092503925
    - type: nauc_precision_at_1000_std
      value: 4.757430160226248
    - type: nauc_precision_at_100_diff1
      value: -6.88009476644726
    - type: nauc_precision_at_100_max
      value: 10.391099419327492
    - type: nauc_precision_at_100_std
      value: 7.203837158689326
    - type: nauc_precision_at_10_diff1
      value: -0.7155570800016817
    - type: nauc_precision_at_10_max
      value: 21.06902041338105
    - type: nauc_precision_at_10_std
      value: 3.7465404459270815
    - type: nauc_precision_at_1_diff1
      value: 47.16372543032823
    - type: nauc_precision_at_1_max
      value: 34.48620759685232
    - type: nauc_precision_at_1_std
      value: -8.881483248224074
    - type: nauc_precision_at_20_diff1
      value: -4.695792117927824
    - type: nauc_precision_at_20_max
      value: 16.53698826752203
    - type: nauc_precision_at_20_std
      value: 6.681726081495262
    - type: nauc_precision_at_3_diff1
      value: 12.446292477522807
    - type: nauc_precision_at_3_max
      value: 27.622770072159884
    - type: nauc_precision_at_3_std
      value: -2.243774812074271
    - type: nauc_precision_at_5_diff1
      value: 5.851972491534291
    - type: nauc_precision_at_5_max
      value: 25.400246002612235
    - type: nauc_precision_at_5_std
      value: -0.8059534151280825
    - type: nauc_recall_at_1000_diff1
      value: 17.33619903703495
    - type: nauc_recall_at_1000_max
      value: 46.39520954734979
    - type: nauc_recall_at_1000_std
      value: 59.70020859630654
    - type: nauc_recall_at_100_diff1
      value: 9.309667388080348
    - type: nauc_recall_at_100_max
      value: 35.92482580062717
    - type: nauc_recall_at_100_std
      value: 24.021627313676188
    - type: nauc_recall_at_10_diff1
      value: 19.87959406394684
    - type: nauc_recall_at_10_max
      value: 35.00740821313158
    - type: nauc_recall_at_10_std
      value: -2.6455284599102784
    - type: nauc_recall_at_1_diff1
      value: 40.90418146524424
    - type: nauc_recall_at_1_max
      value: 22.269308553048656
    - type: nauc_recall_at_1_std
      value: -9.89932822257807
    - type: nauc_recall_at_20_diff1
      value: 15.028975252982061
    - type: nauc_recall_at_20_max
      value: 34.901307836728016
    - type: nauc_recall_at_20_std
      value: 2.9027647776175494
    - type: nauc_recall_at_3_diff1
      value: 26.13225834790859
    - type: nauc_recall_at_3_max
      value: 27.915627935543725
    - type: nauc_recall_at_3_std
      value: -8.069525359773976
    - type: nauc_recall_at_5_diff1
      value: 24.184086614024686
    - type: nauc_recall_at_5_max
      value: 32.607378848166675
    - type: nauc_recall_at_5_std
      value: -7.730984752196379
    - type: ndcg_at_1
      value: 55.969
    - type: ndcg_at_10
      value: 66.77499999999999
    - type: ndcg_at_100
      value: 70.324
    - type: ndcg_at_1000
      value: 70.95700000000001
    - type: ndcg_at_20
      value: 68.613
    - type: ndcg_at_3
      value: 59.256
    - type: ndcg_at_5
      value: 63.223
    - type: precision_at_1
      value: 55.969
    - type: precision_at_10
      value: 13.297999999999998
    - type: precision_at_100
      value: 1.585
    - type: precision_at_1000
      value: 0.167
    - type: precision_at_20
      value: 7.222
    - type: precision_at_3
      value: 32.467
    - type: precision_at_5
      value: 23.073
    - type: recall_at_1
      value: 38.964
    - type: recall_at_10
      value: 81.248
    - type: recall_at_100
      value: 95.124
    - type: recall_at_1000
      value: 99.30600000000001
    - type: recall_at_20
      value: 87.35199999999999
    - type: recall_at_3
      value: 62.785000000000004
    - type: recall_at_5
      value: 71.986
    task:
      type: Retrieval
  - dataset:
      config: default
      name: MTEB RuReviewsClassification (default)
      revision: f6d2c31f4dc6b88f468552750bfec05b4b41b05a
      split: test
      type: ai-forever/ru-reviews-classification
    metrics:
    - type: accuracy
      value: 67.958984375
    - type: f1
      value: 67.250877785427
    - type: f1_weighted
      value: 67.25215701797296
    - type: main_score
      value: 67.958984375
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB RuSTSBenchmarkSTS (default)
      revision: 7cf24f325c6da6195df55bef3d86b5e0616f3018
      split: test
      type: ai-forever/ru-stsbenchmark-sts
    metrics:
    - type: cosine_pearson
      value: 79.11336124619963
    - type: cosine_spearman
      value: 78.69157477180703
    - type: euclidean_pearson
      value: 77.84066073571212
    - type: euclidean_spearman
      value: 78.69157477180703
    - type: main_score
      value: 78.69157477180703
    - type: manhattan_pearson
      value: 77.79213012957939
    - type: manhattan_spearman
      value: 78.61384378877501
    - type: pearson
      value: 79.11336124619963
    - type: spearman
      value: 78.69157477180703
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB RuSciBenchGRNTIClassification (default)
      revision: 673a610d6d3dd91a547a0d57ae1b56f37ebbf6a1
      split: test
      type: ai-forever/ru-scibench-grnti-classification
    metrics:
    - type: accuracy
      value: 59.326171875
    - type: f1
      value: 58.01171745357119
    - type: f1_weighted
      value: 58.02106511480968
    - type: main_score
      value: 59.326171875
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB RuSciBenchGRNTIClusteringP2P (default)
      revision: 673a610d6d3dd91a547a0d57ae1b56f37ebbf6a1
      split: test
      type: ai-forever/ru-scibench-grnti-classification
    metrics:
    - type: main_score
      value: 55.46570753380975
    - type: v_measure
      value: 55.46570753380975
    - type: v_measure_std
      value: 0.9813885872798612
    task:
      type: Clustering
  - dataset:
      config: default
      name: MTEB RuSciBenchOECDClassification (default)
      revision: 26c88e99dcaba32bb45d0e1bfc21902337f6d471
      split: test
      type: ai-forever/ru-scibench-oecd-classification
    metrics:
    - type: accuracy
      value: 46.328125
    - type: f1
      value: 44.19158709013339
    - type: f1_weighted
      value: 44.190957945676026
    - type: main_score
      value: 46.328125
    task:
      type: Classification
  - dataset:
      config: default
      name: MTEB RuSciBenchOECDClusteringP2P (default)
      revision: 26c88e99dcaba32bb45d0e1bfc21902337f6d471
      split: test
      type: ai-forever/ru-scibench-oecd-classification
    metrics:
    - type: main_score
      value: 47.28635342613908
    - type: v_measure
      value: 47.28635342613908
    - type: v_measure_std
      value: 0.7431017612993989
    task:
      type: Clustering
  - dataset:
      config: ru
      name: MTEB STS22 (ru)
      revision: de9d86b3b84231dc21f76c7b7af1f28e2f57f6e3
      split: test
      type: mteb/sts22-crosslingual-sts
    metrics:
    - type: cosine_pearson
      value: 63.10139371129796
    - type: cosine_spearman
      value: 67.06445400504978
    - type: euclidean_pearson
      value: 62.74563386470613
    - type: euclidean_spearman
      value: 67.06445400504978
    - type: main_score
      value: 67.06445400504978
    - type: manhattan_pearson
      value: 62.540465664732395
    - type: manhattan_spearman
      value: 66.65899492022648
    - type: pearson
      value: 63.10139371129796
    - type: spearman
      value: 67.06445400504978
    task:
      type: STS
  - dataset:
      config: default
      name: MTEB SensitiveTopicsClassification (default)
      revision: 416b34a802308eac30e4192afc0ff99bb8dcc7f2
      split: test
      type: ai-forever/sensitive-topics-classification
    metrics:
    - type: accuracy
      value: 33.0712890625
    - type: f1
      value: 38.063573562290024
    - type: lrap
      value: 49.586995442707696
    - type: main_score
      value: 33.0712890625
    task:
      type: MultilabelClassification
  - dataset:
      config: default
      name: MTEB TERRa (default)
      revision: 7b58f24536063837d644aab9a023c62199b2a612
      split: dev
      type: ai-forever/terra-pairclassification
    metrics:
    - type: cosine_accuracy
      value: 61.563517915309454
    - type: cosine_accuracy_threshold
      value: 75.3734290599823
    - type: cosine_ap
      value: 60.78861909325018
    - type: cosine_f1
      value: 67.25663716814158
    - type: cosine_f1_threshold
      value: 54.05237674713135
    - type: cosine_precision
      value: 50.836120401337794
    - type: cosine_recall
      value: 99.34640522875817
    - type: dot_accuracy
      value: 61.563517915309454
    - type: dot_accuracy_threshold
      value: 75.37343502044678
    - type: dot_ap
      value: 60.78861909325018
    - type: dot_f1
      value: 67.25663716814158
    - type: dot_f1_threshold
      value: 54.05237674713135
    - type: dot_precision
      value: 50.836120401337794
    - type: dot_recall
      value: 99.34640522875817
    - type: euclidean_accuracy
      value: 61.563517915309454
    - type: euclidean_accuracy_threshold
      value: 70.18057107925415
    - type: euclidean_ap
      value: 60.78861909325018
    - type: euclidean_f1
      value: 67.25663716814158
    - type: euclidean_f1_threshold
      value: 95.86195945739746
    - type: euclidean_precision
      value: 50.836120401337794
    - type: euclidean_recall
      value: 99.34640522875817
    - type: main_score
      value: 60.78861909325018
    - type: manhattan_accuracy
      value: 60.91205211726385
    - type: manhattan_accuracy_threshold
      value: 1813.1645202636719
    - type: manhattan_ap
      value: 60.478709337038936
    - type: manhattan_f1
      value: 67.10816777041943
    - type: manhattan_f1_threshold
      value: 2475.027275085449
    - type: manhattan_precision
      value: 50.66666666666667
    - type: manhattan_recall
      value: 99.34640522875817
    - type: max_ap
      value: 60.78861909325018
    - type: max_f1
      value: 67.25663716814158
    - type: max_precision
      value: 50.836120401337794
    - type: max_recall
      value: 99.34640522875817
    - type: similarity_accuracy
      value: 61.563517915309454
    - type: similarity_accuracy_threshold
      value: 75.3734290599823
    - type: similarity_ap
      value: 60.78861909325018
    - type: similarity_f1
      value: 67.25663716814158
    - type: similarity_f1_threshold
      value: 54.05237674713135
    - type: similarity_precision
      value: 50.836120401337794
    - type: similarity_recall
      value: 99.34640522875817
    task:
      type: PairClassification
license: mit
language:
- ru
- en
tags:
- mteb
- transformers
- sentence-transformers
base_model: ai-forever/ruRoberta-large
---

# Model Card for ru-en-RoSBERTa

The ru-en-RoSBERTa is a general text embedding model for Russian. The model is based on [ruRoBERTa](https://huggingface.co/ai-forever/ruRoberta-large) and fine-tuned with ~4M pairs of supervised, synthetic and unsupervised data in Russian and English. Tokenizer supports some English tokens from [RoBERTa](https://huggingface.co/FacebookAI/roberta-large) tokenizer.

For more model details please refer to our [article](https://arxiv.org/abs/2408.12503).

## Usage

The model can be used as is with prefixes. It is recommended to use CLS pooling. The choice of prefix and pooling depends on the task. 

We use the following basic rules to choose a prefix:
- `"search_query: "` and `"search_document: "` prefixes are for answer or relevant paragraph retrieval
- `"classification: "` prefix is for symmetric paraphrasing related tasks (STS, NLI, Bitext Mining)
- `"clustering: "` prefix is for any tasks that rely on thematic features (topic classification, title-body retrieval)

To better tailor the model to your needs, you can fine-tune it with relevant high-quality Russian and English datasets.

Below are examples of texts encoding using the Transformers and SentenceTransformers libraries.

### Transformers

```python
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


def pool(hidden_state, mask, pooling_method="cls"):
    if pooling_method == "mean":
        s = torch.sum(hidden_state * mask.unsqueeze(-1).float(), dim=1)
        d = mask.sum(axis=1, keepdim=True).float()
        return s / d
    elif pooling_method == "cls":
        return hidden_state[:, 0]

inputs = [
    # 
    "classification: Он нам и <unk> не нужон ваш Интернет!",
    "clustering: В Ярославской области разрешили работу бань, но без посетителей",
    "search_query: Сколько программистов нужно, чтобы вкрутить лампочку?",

    # 
    "classification: What a time to be alive!",
    "clustering: Ярославским баням разрешили работать без посетителей",
    "search_document: Чтобы вкрутить лампочку, требуется три программиста: один напишет программу извлечения лампочки, другой — вкручивания лампочки, а третий проведет тестирование.",
]

tokenizer = AutoTokenizer.from_pretrained("ai-forever/ru-en-RoSBERTa")
model = AutoModel.from_pretrained("ai-forever/ru-en-RoSBERTa")

tokenized_inputs = tokenizer(inputs, max_length=512, padding=True, truncation=True, return_tensors="pt")

with torch.no_grad():
    outputs = model(**tokenized_inputs)
    
embeddings = pool(
    outputs.last_hidden_state, 
    tokenized_inputs["attention_mask"],
    pooling_method="cls" # or try "mean"
)

embeddings = F.normalize(embeddings, p=2, dim=1)

sim_scores = embeddings[:3] @ embeddings[3:].T
print(sim_scores.diag().tolist())
# [0.4796873927116394, 0.9409002065658569, 0.7761015892028809]
```

### SentenceTransformers

```python
from sentence_transformers import SentenceTransformer


inputs = [
    # 
    "classification: Он нам и <unk> не нужон ваш Интернет!",
    "clustering: В Ярославской области разрешили работу бань, но без посетителей",
    "search_query: Сколько программистов нужно, чтобы вкрутить лампочку?",

    # 
    "classification: What a time to be alive!",
    "clustering: Ярославским баням разрешили работать без посетителей",
    "search_document: Чтобы вкрутить лампочку, требуется три программиста: один напишет программу извлечения лампочки, другой — вкручивания лампочки, а третий проведет тестирование.",
]

# loads model with CLS pooling
model = SentenceTransformer("ai-forever/ru-en-RoSBERTa")

# embeddings are normalized by default
embeddings = model.encode(inputs, convert_to_tensor=True)

sim_scores = embeddings[:3] @ embeddings[3:].T
print(sim_scores.diag().tolist())
# [0.47968706488609314, 0.940900444984436, 0.7761018872261047]
```

or using prompts (sentence-transformers>=2.4.0):

```python
from sentence_transformers import SentenceTransformer


# loads model with CLS pooling
model = SentenceTransformer("ai-forever/ru-en-RoSBERTa")

classification = model.encode(["Он нам и <unk> не нужон ваш Интернет!", "What a time to be alive!"], prompt_name="classification")
print(classification[0] @ classification[1].T) # 0.47968706488609314

clustering = model.encode(["В Ярославской области разрешили работу бань, но без посетителей", "Ярославским баням разрешили работать без посетителей"], prompt_name="clustering")
print(clustering[0] @ clustering[1].T) # 0.940900444984436

query_embedding = model.encode("Сколько программистов нужно, чтобы вкрутить лампочку?", prompt_name="search_query")
document_embedding = model.encode("Чтобы вкрутить лампочку, требуется три программиста: один напишет программу извлечения лампочки, другой — вкручивания лампочки, а третий проведет тестирование.", prompt_name="search_document")
print(query_embedding @ document_embedding.T) # 0.7761018872261047
```

## Citation

```
@misc{snegirev2024russianfocusedembeddersexplorationrumteb,
      title={The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design}, 
      author={Artem Snegirev and Maria Tikhonova and Anna Maksimova and Alena Fenogenova and Alexander Abramov},
      year={2024},
      eprint={2408.12503},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2408.12503}, 
}
```

## Limitations

The model is designed to process texts in Russian, the quality in English is unknown. Maximum input text length is limited to 512 tokens.
