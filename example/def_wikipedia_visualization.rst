
Topic visualizations of a Poisson-Gamma DEF (size 50-25-10) trained on 1,000 wikipedia articles
-----------------------------------------------------------------------------------------------

.. code:: 

    %pylab inline
    %load_ext autoreload
    %autoreload 2
    
    import pandas
    import sys


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib
    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload


.. parsed-literal::

    WARNING: pylab import has clobbered these variables: ['box', 'linalg', 'text', 'random', 'power', 'info', 'fft']
    `%matplotlib` prevents importing * from pylab and numpy


.. code:: 

    # specific imports
    sys.path += ['../scripts/']
    from utils import *
    from pyx import *
    from wand.image import Image as WImage
    from def_visualization import *

.. code:: 

    word_list = read_words('./vocab.dat')
    experiment_dir = '../experiments/def_wikipedia_1434725288667'

.. code:: 

    t = map(softrect, load_bin_model(experiment_dir + '/train_iter01000.model.bin'))

.. code:: 

    W0_shape, W0_scale, z0_shape, z0_scale = t[:4]    
    z1_shape, z1_scale, z2_shape, z2_scale = t[4:8]        
    W1_shape, W1_scale, W2_shape, W2_scale = t[8:]
    W0_mean = W0_shape * W0_scale
    W1_mean = W1_shape * W1_scale
    W2_mean = W2_shape * W2_scale

First layer topics
^^^^^^^^^^^^^^^^^^

.. code:: 

    g = top_words(W0_mean, word_list, k=10, W_shape=W0_shape, show_weight=True)


.. parsed-literal::

    Topic 0
    state 0.341688850243 17.8120743811
    party 0.266396299919 18.664387271
    national 0.125530215608 14.7028305909
    alabama 0.11259996231 18.566584038
    election 0.109002015749 18.6986190985
    governor 0.103520611551 19.1626345865
    arkansas 0.102276140417 17.2617603328
    vote 0.0972261548324 19.3580183463
    government 0.0851871717519 13.6195711971
    democratic 0.0843305840673 17.8221570027
    
    
    Topic 1
    novel 0.0874780204024 17.974768033
    play 0.0719818291177 17.2042960767
    stories 0.0567413823244 18.6402343842
    best 0.0504194294446 13.31251659
    murder 0.0501055232976 18.1011363256
    short 0.0496254920266 16.1028957148
    story 0.0493768255188 16.301524876
    book 0.0490051249294 11.4179205446
    character 0.043847161499 14.1439288862
    plays 0.0430505500842 17.9414175636
    
    
    Topic 2
    species 0.15095027799 19.3060348502
    family 0.116784969268 17.0666613815
    plants 0.076895045062 19.2684370357
    food 0.063013448874 16.8469749536
    animals 0.060496255285 17.2980767712
    genus 0.0544655345468 18.6177252814
    order 0.0489690231599 16.0086328966
    plant 0.0463831916658 17.4085005782
    agricultural 0.0399812151507 16.8478295401
    fish 0.0373797518917 15.8324416873
    
    
    Topic 3
    law 0.171070885209 17.2186974745
    property 0.0978889222137 17.5503117987
    state 0.0970791637472 14.0629411442
    act 0.0954956425588 14.9691121185
    free 0.0867581420438 15.7583295903
    society 0.0825887476592 15.3661049488
    austrian 0.0812394962357 16.6194508596
    rights 0.0798770794722 16.116761491
    private 0.0769261658317 17.4075753599
    market 0.073828080647 16.4319282312
    
    
    Topic 4
    apple 0.096268917424 21.4406549343
    system 0.0539576895435 18.9358058188
    software 0.0443668415609 21.3435837218
    computer 0.0437460107971 18.6823876947
    company 0.0264559503121 17.6486107991
    systems 0.0264456014955 16.8511851479
    new 0.0260737423571 13.6918737347
    released 0.0256231883601 19.8171289049
    based 0.0229260300411 15.9004979595
    memory 0.0205695643695 19.1369236001
    
    
    Topic 5
    chinese 2.28572962341 16.7068081329
    dishes 1.40568747796 17.4765079005
    popular 1.07993196725 13.261924076
    meat 1.04522945734 16.6940978868
    american 1.0191087221 0.711096701148
    called 1.01869937294 7.92132223452
    native 1.00442584534 13.4047564375
    made 0.941376863797 12.4831203534
    italian 0.90869609306 13.5612268907
    region 0.839748034905 11.4228004228
    
    
    Topic 6
    center 4.89074700042 18.081899016
    style 4.78943606662 17.7665207871
    background 3.2751123702 18.5698847037
    color 0.800568681039 16.8402558401
    text 0.680361580371 14.3542492806
    open 0.300284514558 16.6334682359
    hard 0.276584486409 17.0426369046
    year 0.144556078053 11.4404098586
    anna 0.129620736267 15.2657720938
    final 0.126181435731 13.5476914595
    
    
    Topic 7
    house 9.56848857185 10.285130994
    abbey 7.67401940855 13.8953137911
    monks 6.84056726282 13.3628780796
    side 5.54007994627 12.1932866584
    buildings 5.23463087207 10.9583074393
    superior 4.21698851135 11.9323853379
    church 4.03003449422 6.19925295354
    wall 3.95261049535 12.7084904901
    order 3.63334013408 7.53281407306
    rule 3.42773454182 10.3708694318
    
    
    Topic 8
    medicine 0.10461629492 18.9609286397
    treatment 0.0674128982554 20.4322557225
    medical 0.0634410254566 19.3880635873
    effects 0.0587334983134 19.446963451
    health 0.0564545599254 19.1908781292
    patients 0.0534872220053 20.2797777891
    alternative 0.0525662305252 17.4907750313
    pain 0.0427614050201 18.6135697133
    disease 0.0418795443011 20.0688088526
    evidence 0.0369882759094 17.4566770277
    
    
    Topic 9
    sea 0.0511888838158 19.8053886477
    south 0.0394126333324 16.965886564
    north 0.0372162120427 16.9874166924
    island 0.033497524383 18.4792174506
    east 0.02840929755 16.9578726509
    area 0.0280653717397 15.984714159
    river 0.0273337659915 17.7098019301
    islands 0.0272092796387 19.8389363107
    right 0.0265155605595 14.2117490501
    west 0.022486853032 15.8070987633
    
    
    Topic 10
    court 0.963023110649 16.2954840821
    car 0.691062653122 17.0344315083
    martin 0.593550319247 15.8937160862
    cars 0.580702651332 16.957520749
    age 0.389623619814 13.9831993752
    appeal 0.384827115083 16.1530862625
    engine 0.357712152625 14.1196017854
    assault 0.354880316129 15.830561311
    consent 0.292085801717 15.5747847808
    ford 0.280037685301 15.9573217147
    
    
    Topic 11
    bell 67.2249819335 19.7122349258
    att 27.5842215992 16.2649254748
    telephone 25.7783017078 17.5841179943
    sound 10.9405587401 13.4103126774
    deaf 9.78499640147 16.3894898948
    patent 8.69505534019 15.8362952125
    company 8.43536407139 10.319681472
    speech 7.68915017519 13.214257024
    graham 6.97884423909 14.7042350049
    alexander 5.42671091883 7.11303420372
    
    
    Topic 12
    art 1.95779707296 18.8280887107
    artist 0.320479822378 17.8155014918
    works 0.286406227871 15.6192527256
    andy 0.220495844489 17.2458515858
    arts 0.208083702799 16.1239890116
    artists 0.205436956558 17.2591797303
    work 0.175649933572 12.9761323147
    style 0.162774020606 7.69639290706
    artistic 0.161267757443 17.137899335
    new 0.155753663372 8.04085946539
    
    
    Topic 13
    city 0.144144515344 19.304849193
    university 0.0641667040477 17.3228845224
    built 0.035784503859 17.6104735359
    school 0.0331530324802 16.8699483108
    building 0.0297461440961 18.588368701
    college 0.0279653989094 17.1323214157
    area 0.0255879472083 15.0074680202
    park 0.0254137309206 18.9965515109
    house 0.022589672836 16.2924686729
    town 0.0205728039754 17.2511470313
    
    
    Topic 14
    apollo 0.553905643217 20.0911535157
    mission 0.368909508991 20.2556548265
    crew 0.32937903968 20.0780997831
    moon 0.275414892987 19.8117652688
    space 0.22663756336 18.6659476196
    earth 0.203303962422 18.1626753727
    first 0.191101079383 12.7649776789
    flight 0.165406761416 18.3970661225
    command 0.146940859324 19.3243997029
    landing 0.130577077039 18.4214463325
    
    
    Topic 15
    chain 80.0469519269 19.7247096298
    chains 38.7583338038 17.0614451365
    stock 24.654604166 15.8706686353
    game 18.6868495655 9.3780303507
    exchange 16.1857521344 10.8142287175
    shares 14.871109103 14.5301998113
    three 13.3816919543 6.97078718171
    board 10.7039148349 10.648490399
    acquired 10.4554895833 12.2231308629
    share 8.57640281327 11.246750981
    
    
    Topic 16
    language 0.0985669880624 19.1221728017
    arabic 0.0676594165731 20.8226760833
    languages 0.0512059415407 19.6573191004
    line 0.0377916095158 18.0626128631
    written 0.0303443578806 17.0129804529
    letters 0.0297546760325 18.903266464
    century 0.0282500096754 13.3801234447
    word 0.0279372514171 15.5021414248
    height 0.027340401861 17.995801398
    modern 0.0267237675307 15.3009484281
    
    
    Topic 17
    architecture 14.7584655888 15.1140072528
    social 11.5715325478 15.9842974614
    design 11.0518982154 13.631152098
    game 8.74101489115 14.7243246107
    base 7.77498631438 15.0792962684
    experience 6.83270411054 14.2047230367
    society 6.72911377555 11.2510244306
    requirements 5.62119747107 15.0277855193
    projects 4.39860444579 11.9167936809
    civilization 4.11042955869 13.2431967135
    
    
    Topic 18
    war 0.366636753142 13.4511219213
    air 0.257807875216 13.8546875614
    armour 0.247328141589 16.4528091975
    first 0.199427200368 7.0498551
    navy 0.172113903412 13.9443833331
    gun 0.154344302785 15.9295838725
    military 0.143964861247 13.6221699072
    flight 0.1414632128 9.73264468788
    world 0.136606940285 10.5126647941
    deck 0.110985815805 13.4369026211
    
    
    Topic 19
    african 30.7918911167 16.951177008
    americans 19.8098324199 16.6420315273
    american 16.8632911127 8.25570047146
    black 14.6287790373 15.0747227904
    day 9.52279511114 9.15004143247
    states 8.75055571676 8.04532498206
    tree 5.69955210284 13.4709155869
    trees 4.47181008592 13.0004534916
    native 3.99982056215 9.10649548528
    groups 3.99569617458 8.8733248122
    
    
    Topic 20
    empire 0.0191191638089 18.7594512713
    army 0.017535017032 18.7884392105
    roman 0.0155115170914 17.9714932066
    augustus 0.0128666162309 18.5791811493
    emperor 0.0111348218527 18.0194199484
    battle 0.0106147466746 18.2623251084
    rome 0.00961715107612 18.8251213556
    death 0.00948030023419 13.1677544926
    war 0.0085714085162 12.7165143612
    military 0.0085543337529 15.9501600782
    
    
    Topic 21
    ancient 0.0942549470866 18.0241689329
    greek 0.0779371001225 16.0785599947
    century 0.0629646126596 12.1568551499
    athens 0.0549776897891 14.8974609755
    period 0.0481868627021 15.5047475697
    known 0.0458343706066 9.53914049012
    egypt 0.0449946088346 17.2780135921
    temple 0.0387892587739 16.6752958805
    made 0.035772857763 9.99106734142
    stone 0.0347791626673 16.9030432292
    
    
    Topic 22
    title 60.3018572433 16.7566126515
    page 48.5331739981 16.729271373
    comment 39.6126931255 18.0061301284
    animals 26.9062085576 11.6192957456
    preserve 26.4730190096 15.4390849065
    animal 22.8141844215 12.2333475307
    farm 21.4926249487 13.9034036971
    book 19.8458888251 7.82061495477
    space 18.9529627135 11.2448011398
    napoleon 18.3287604385 13.6739327378
    
    
    Topic 23
    english 0.352921361714 17.3925807727
    american 0.186004499778 8.91551906388
    british 0.152514889194 15.8247183377
    word 0.148355517692 15.8880516679
    united 0.131854254036 11.3459728743
    words 0.111496852015 15.7834468518
    term 0.0872322438853 14.3140830299
    case 0.0846720569044 13.1642314485
    states 0.0839148280437 10.5229448002
    common 0.0815505919748 14.0988946982
    
    
    Topic 24
    computer 0.103151330019 16.2151434089
    time 0.0967879389877 14.5826065986
    ascii 0.0783216787987 18.4526213229
    code 0.0679424215628 17.8547020999
    standard 0.0661618948283 16.8236924034
    characters 0.0631680426962 17.1903835705
    language 0.0623123236943 13.8003098047
    data 0.0549262249758 17.0555616484
    program 0.0516359578167 16.4303673147
    character 0.0456923761187 15.9735493375
    
    
    Topic 25
    star 0.409317041294 16.7760624726
    angle 0.380780536417 15.1331340136
    stars 0.362429638917 17.7659766024
    earth 0.344122643185 14.7419895859
    sun 0.324056014183 16.5276860698
    angles 0.240742962285 14.2616154232
    system 0.230185624397 13.2142779772
    light 0.229713565894 14.2527948403
    objects 0.210094852684 15.9728530241
    moon 0.196964538909 14.6553371604
    
    
    Topic 26
    american 0.176619587151 22.5274110852
    actor 0.0354383553142 22.8294379272
    english 0.0311531756093 21.4713598991
    french 0.0307929554825 21.4143067511
    british 0.023944673033 20.4284299514
    canadian 0.0182633652119 23.057861751
    german 0.0164184728337 20.596811523
    first 0.0153804006432 17.3160659847
    john 0.0146162015882 20.8642546769
    writer 0.0143316819279 22.0777229493
    
    
    Topic 27
    series 1.2658579276 14.9871941536
    present 0.656620984896 15.8589672916
    characters 0.644922922094 13.4610739876
    character 0.571789866977 13.9334146341
    show 0.458730452062 14.148140221
    animated 0.453775793989 16.7971477637
    adventures 0.353784169476 17.2079775704
    children 0.287266467946 10.8407996078
    alien 0.276550968453 14.5241954566
    game 0.269674556165 11.8574704753
    
    
    Topic 28
    women 43.8255203957 17.1284385208
    hill 21.4630786556 9.4840992476
    sex 18.6032543966 14.4685718025
    woman 18.4697184626 14.2316162614
    thomas 15.2182308074 6.97418405575
    female 12.9991487246 12.1448211816
    sexual 12.1546643631 11.7682620325
    breast 11.2551533788 12.8439041745
    university 8.35750054531 2.06404900532
    life 8.32496477182 7.72438967437
    
    
    Topic 29
    jews 4.32531232017 18.9894360611
    jewish 2.74859763552 18.7899712674
    camp 1.00744795236 16.7677025324
    arab 0.991049112241 16.7453466883
    prisoners 0.545711522813 16.4275234484
    jesus 0.442340117047 13.2869465929
    christians 0.420565433314 14.3012782331
    lewis 0.40227720475 15.9692581852
    german 0.39200102675 10.6804391949
    israel 0.389619298715 14.2414601641
    
    
    Topic 30
    left 74.6406083355 18.983248148
    right 56.7124726017 17.7169093969
    partial 31.1695517029 19.2442232877
    time 10.155313071 6.49910360375
    sum 9.53443120998 14.9694417489
    tilde 9.22202908644 17.4796508498
    balance 8.42310800757 16.1698538715
    tree 5.68040030223 3.44349959451
    text 5.57478686536 7.40012573536
    factor 5.51849960988 7.69035388465
    
    
    Topic 31
    philosophy 0.0158643440518 21.2117845589
    book 0.0114641964102 16.202735982
    human 0.0111977413822 16.9639459788
    life 0.00995174929771 13.8608653004
    world 0.00953893660735 12.3184555056
    smith 0.0092771026091 17.96096267
    works 0.00849844937101 16.4942302781
    acts 0.0081756094542 17.2585490412
    nature 0.0078970343741 17.8217691524
    god 0.00779859640033 13.3256274153
    
    
    Topic 32
    team 0.0775154895153 21.5209363691
    first 0.0708712628727 16.3871648636
    league 0.0650324087714 21.563885793
    season 0.0543639171829 21.9282208898
    club 0.0464696440211 21.0589824667
    two 0.0380232377926 14.4442718589
    won 0.0350129523348 19.9664529543
    time 0.0348088432074 12.6432040817
    game 0.0344853408617 19.0403600588
    games 0.033911037349 20.351750164
    
    
    Topic 33
    section 24.5077708929 15.7650700899
    steel 20.0466239713 15.5058827221
    francisco 12.219222291 14.6507402209
    appears 10.2476938181 12.4191241533
    sections 7.83892645969 13.9558871419
    mentioned 7.68136226304 13.1924396433
    railroad 7.04735488924 12.6530815064
    james 6.57674763457 10.8921601481
    line 5.31201451445 4.36184630954
    john 5.06238646094 6.74978969636
    
    
    Topic 34
    god 0.0591746171486 16.9821495312
    name 0.0465587969857 14.9256558474
    son 0.0366289521902 15.7488008725
    king 0.0327199633067 12.3908843594
    abraham 0.0327072358572 17.6040799226
    greek 0.0269851282799 12.4140300384
    father 0.0241489910543 13.4846270521
    people 0.0231901522555 12.3988648977
    two 0.0206976159736 8.9580807908
    time 0.0183506796495 8.25993942315
    
    
    Topic 35
    german 8.43451012224 14.2695741177
    austria 7.21274601841 13.4695276119
    van 6.04762647303 16.4639287484
    dutch 5.10433832486 18.4016257609
    austrian 4.26134262589 12.3442520096
    germany 3.28539773859 14.0191288087
    der 2.47823833975 13.0482776572
    netherlands 2.06949812731 15.2370601171
    european 1.99575638233 11.1597099467
    vienna 1.52173432399 11.6352532829
    
    
    Topic 36
    number 0.0546221657408 15.0457494619
    numbers 0.0510620264647 18.0584401414
    theory 0.0507540298845 15.5505295174
    value 0.0451672165378 17.6531491807
    function 0.0406285856729 17.473932509
    choice 0.0377026511465 17.1047495891
    two 0.0328251888954 11.087050694
    real 0.0327650950389 17.3109564155
    argument 0.0324739451825 18.1356528746
    called 0.0305952102826 11.6873971094
    
    
    Topic 37
    first 0.0174563445405 11.4946712919
    years 0.0139636512965 14.4619447154
    two 0.0121624166391 13.1949320478
    life 0.0115214357371 15.1445206588
    time 0.0108724257154 12.4620270325
    new 0.00942431517629 10.7339289128
    year 0.00938387984911 13.274527602
    made 0.00757165311399 12.008319745
    death 0.00712545172439 13.9935728946
    early 0.00634405517136 12.3725231069
    
    
    Topic 38
    bones 12.4564539903 10.9223796094
    skull 11.4925210601 10.5718172004
    large 11.128403527 5.72804336819
    remains 10.0199979789 9.67898509478
    teeth 8.34404439705 6.86933282408
    formation 6.72887620545 5.94375360813
    prey 6.63073702395 5.74588926243
    specimen 6.59688354258 7.24031774647
    like 5.99789671802 3.76349717343
    genus 5.96688888018 3.31118158019
    
    
    Topic 39
    music 0.244972826584 17.8342655012
    song 0.190309371999 19.0118789653
    band 0.0944033119767 17.4848839644
    released 0.0845995696729 16.3712266614
    musical 0.0820588942433 17.9900230919
    group 0.0761197425987 14.4743393707
    single 0.0648762989933 14.7062683368
    opera 0.0595234626515 16.8929554716
    instruments 0.0557158792845 16.0886470388
    songs 0.055653065197 17.4987168846
    
    
    Topic 40
    work 0.0293017900623 15.6008489627
    university 0.0290519795207 16.3456440709
    theory 0.0200509888907 16.1529795799
    history 0.019062125521 14.4447236763
    analysis 0.0153338474385 18.0215874271
    science 0.0152223618461 17.9572037633
    research 0.0150101142178 17.4580956559
    study 0.0144442620431 17.2798292849
    century 0.0139684709618 11.2465966788
    modern 0.013704719145 12.7701234199
    
    
    Topic 41
    alexander 0.0891172615464 20.6880766512
    king 0.050938546488 18.2440157818
    iii 0.0269262334183 20.2059536881
    father 0.0220617372982 17.310019078
    albert 0.0211780891724 18.6096382093
    son 0.0189550070147 16.0749147113
    married 0.0179399093892 18.6900729414
    mother 0.0174602409039 17.8245379121
    pope 0.0170940077016 17.6526791033
    emperor 0.0158657764548 16.0223909121
    
    
    Topic 42
    lincoln 1.34329646738 19.6429201467
    war 0.970581891594 16.0646583506
    union 0.890187442627 18.7283198349
    states 0.870160074086 16.6179901548
    jackson 0.771964858748 18.221523822
    johnson 0.645375656891 17.2070004835
    president 0.489057365177 17.5835452908
    south 0.483327599115 14.7463713883
    confederate 0.446940925265 19.6415794098
    battle 0.431240314986 16.0787582294
    
    
    Topic 43
    japanese 4.03295370172 12.0436303784
    bow 3.12859375651 16.6983652287
    academy 3.03927816998 14.2943321325
    japan 2.83589522093 12.3102419673
    arrow 2.66658296934 16.8919110348
    arrows 2.60334983619 16.6170822966
    motion 2.28804982758 13.4093070332
    shooting 2.24050098067 15.4805244475
    picture 2.06731877132 15.0098915218
    shoot 1.99589094574 16.0449339455
    
    
    Topic 44
    british 1.35350309005 17.6798067962
    american 0.755891177695 10.1905496888
    new 0.717735123159 13.6793880354
    war 0.613531735752 14.1001481531
    congress 0.485162695929 16.5986862113
    states 0.443072970912 11.1869240374
    united 0.419213596292 9.53066193622
    colonies 0.404503184825 16.8722704904
    americans 0.398173971214 15.839108381
    washington 0.358830671017 15.7295751313
    
    
    Topic 45
    united 0.0309884068905 14.9163922905
    states 0.0243862033573 12.6939782214
    national 0.0190522966395 14.2428402357
    world 0.0181891829145 11.5932667532
    new 0.0178009724864 10.5687878887
    government 0.0177616412483 14.4764729212
    international 0.0173453478923 16.0116601792
    million 0.0144795400216 13.8790944906
    first 0.0140622426405 6.38302411075
    president 0.0124958481946 15.561041063
    
    
    Topic 46
    england 2.6975768559 17.0423911477
    alfred 1.92078374037 17.0395137256
    ashes 1.2636940781 13.6353682659
    english 1.20478510204 12.656038024
    saxon 1.11993914519 17.3754012034
    australia 1.11208906996 13.9044711631
    series 1.1038239231 10.1592295859
    made 0.874513292089 8.43425558681
    test 0.780996622269 13.7767475789
    history 0.383214486659 9.27136452185
    
    
    Topic 47
    population 0.0683053848068 19.3791388812
    state 0.0426021965616 10.1117065907
    country 0.0347772879553 16.6607371818
    government 0.0291466818687 15.0863457983
    oil 0.0289120230656 19.2602132577
    austin 0.0282136508976 17.1273919957
    people 0.0280655328187 12.2603344851
    area 0.0269760162347 14.2724050542
    largest 0.0258339969143 17.0792173207
    north 0.0251832471447 12.1863605135
    
    
    Topic 48
    church 0.236262214986 20.1054647124
    catholic 0.083546948926 20.1540154076
    churches 0.0692832120781 19.91681444
    roman 0.0553210784849 17.8036947583
    christian 0.0540839167125 18.4209030155
    god 0.0519898916139 15.6859775669
    christ 0.0502033508683 19.2768535134
    communion 0.0475419465384 19.4339406221
    jesus 0.0418865741648 17.8034227535
    succession 0.0406334056411 17.9630261897
    
    
    Topic 49
    two 0.00790115444999 15.9613621892
    form 0.00629226553919 18.8151466182
    called 0.00586023420865 16.883415402
    known 0.00522969723338 14.7108355963
    acid 0.00502750640659 22.3280698112
    different 0.00491934891282 18.5603299608
    number 0.00483822526832 16.2455163946
    water 0.00430048223097 20.3760500394
    first 0.00390821538419 11.1863832478
    found 0.00382394929034 15.3755557562
    
    


Second layer groups
^^^^^^^^^^^^^^^^^^^

.. code:: 

    #For each group we show: 
    # 1) Most probable words
    # 2) Top topics per group including their probability
    # 3) The top word per topic
    g = top_groups(W1_mean, W0_mean, word_list, k1=3, k=10, show_weight=True)


.. parsed-literal::

    group 0
    first work time new two american years university bell known
    37 40 49
    0.123751054626 0.0670412148524 0.0492089040261
    37  first years two life time new year made death early
    40  work university theory history analysis science research study century modern
    49  two form called known acid different number water first found
    group 1
    language arabic languages english line word century written form modern
    16 49 31
    0.292228244563 0.106261696067 0.0218289318463
    16  language arabic languages line written letters century word height modern
    49  two form called known acid different number water first found
    31  philosophy book human life world smith works acts nature god
    group 2
    city sea south north area east first island river world
    9 45 13
    0.310430258223 0.152166165333 0.111145216503
    09  sea south north island east area river islands right west
    45  united states national world new government international million first president
    13  city university built school building college area park house town
    group 3
    earth apollo first moon two star mission system angle stars
    49 37 9
    0.497952527712 0.0597400613132 0.0323294311621
    49  two form called known acid different number water first found
    37  first years two life time new year made death early
    09  sea south north island east area river islands right west
    group 4
    american english united first known new chinese called made states
    49 26 45
    0.071235625642 0.0283982709684 0.027125217071
    49  two form called known acid different number water first found
    26  american actor english french british canadian german first john writer
    45  united states national world new government international million first president
    group 5
    state states united national government american first party new war
    45 20 37
    0.230613331935 0.0763507056892 0.0717367931338
    45  united states national world new government international million first president
    20  empire army roman augustus emperor battle rome death war military
    37  first years two life time new year made death early
    group 6
    art first new life time two years series book made
    37 31 1
    0.459670164508 0.107075141686 0.0552817397358
    37  first years two life time new year made death early
    31  philosophy book human life world smith works acts nature god
    01  novel play stories best murder short story book character plays
    group 7
    number two called form numbers theory value different group function
    49 36 31
    1.12950134718 0.176591138862 0.0304059421632
    49  two form called known acid different number water first found
    36  number numbers theory value function choice two real argument called
    31  philosophy book human life world smith works acts nature god
    group 8
    title page comment animals preserve book animal first text farm
    40 41 31
    0.019120022751 0.01819631244 0.0155918749974
    40  work university theory history analysis science research study century modern
    41  alexander king iii father albert son married mother pope emperor
    31  philosophy book human life world smith works acts nature god
    group 9
    alexander king son father death time first name emperor iii
    20 41 37
    0.62544525721 0.514171626621 0.457520129121
    20  empire army roman augustus emperor battle rome death war military
    41  alexander king iii father albert son married mother pope emperor
    37  first years two life time new year made death early
    group 10
    title page first jews comment american art bell book animals
    40 49 20
    0.00725809447236 0.00651797387484 0.00533356093004
    40  work university theory history analysis science research study century modern
    49  two form called known acid different number water first found
    20  empire army roman augustus emperor battle rome death war military
    group 11
    right style center sea south first north left two background
    49 9 13
    0.0350008855936 0.0316154390833 0.0051195824249
    49  two form called known acid different number water first found
    09  sea south north island east area river islands right west
    13  city university built school building college area park house town
    group 12
    music song first new band american released group musical single
    37 39 49
    0.0626980805129 0.0312935523508 0.0204838021343
    37  first years two life time new year made death early
    39  music song band released musical group single opera instruments songs
    49  two form called known acid different number water first found
    group 13
    two known species form called found family different acid number
    49 2 8
    2.22501014371 0.10618909788 0.0803082897559
    49  two form called known acid different number water first found
    02  species family plants food animals genus order plant agricultural fish
    08  medicine treatment medical effects health patients alternative pain disease evidence
    group 14
    war first air armour navy world style gun flight center
    49 18 37
    0.216780631851 0.0170477108923 0.0160443884176
    49  two form called known acid different number water first found
    18  war air armour first navy gun military flight world deck
    37  first years two life time new year made death early
    group 15
    american title page first university english british comment war world
    40 31 9
    0.022935360636 0.0157983083931 0.0139405899314
    40  work university theory history analysis science research study century modern
    31  philosophy book human life world smith works acts nature god
    09  sea south north island east area river islands right west
    group 16
    apple computer system time first two called software systems based
    49 4 24
    0.897405858146 0.209953984253 0.0884871372906
    49  two form called known acid different number water first found
    04  apple system software computer company systems new released based memory
    24  computer time ascii code standard characters language data program character
    group 17
    american actor english french british first canadian german war john
    26 32 20
    1.14965776722 0.112563199814 0.0664066982786
    26  american actor english french british canadian german first john writer
    32  team first league season club two won time game games
    20  empire army roman augustus emperor battle rome death war military
    group 18
    center style art title american background page first comment work
    40 20 45
    0.0199687944108 0.0082935653619 0.00714065787009
    40  work university theory history analysis science research study century modern
    20  empire army roman augustus emperor battle rome death war military
    45  united states national world new government international million first president
    group 19
    american bell first title english left british time series right
    40 26 41
    0.00782300082724 0.00686779520655 0.00576757519762
    40  work university theory history analysis science research study century modern
    26  american actor english french british canadian german first john writer
    41  alexander king iii father albert son married mother pope emperor
    group 20
    american city first art new united world time university english
    45 13 26
    0.0101304475376 0.00818056384726 0.00679153636349
    45  united states national world new government international million first president
    13  city university built school building college area park house town
    26  american actor english french british canadian german first john writer
    group 21
    center style background color text open city hard first year
    37 41 13
    0.0508642793604 0.0136565638516 0.0136385090268
    37  first years two life time new year made death early
    41  alexander king iii father albert son married mother pope emperor
    13  city university built school building college area park house town
    group 22
    first work church university time century theory life world history
    37 31 40
    0.667715206946 0.640392266466 0.630158854901
    37  first years two life time new year made death early
    31  philosophy book human life world smith works acts nature god
    40  work university theory history analysis science research study century modern
    group 23
    american first city known series state university time new system
    49 40 37
    0.0167104439144 0.0103562024122 0.0101832173823
    49  two form called known acid different number water first found
    40  work university theory history analysis science research study century modern
    37  first years two life time new year made death early
    group 24
    title page first comment german art english american space states
    37 49 31
    0.0110106096513 0.0072003622595 0.00380316872361
    37  first years two life time new year made death early
    49  two form called known acid different number water first found
    31  philosophy book human life world smith works acts nature god


Third layer super groups
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: 

    g = top_supers(W2_mean, W1_mean, W0_mean, word_list, k2=5, k1=5, k=6, show_weight=True)


.. parsed-literal::

    SUPER 0
    american first english french actor two
    17 9 8 13 4
    4.75704920931 3.15565077209 2.1770083874 1.93258185117 1.88924506013
    group 0
    american actor english french british first
    26 32 20 45 13
    1.14965776722 0.112563199814 0.0664066982786 0.0284960443054 0.0251595129677
    26  american actor english french british canadian
    32  team first league season club two
    20  empire army roman augustus emperor battle
    45  united states national world new government
    13  city university built school building college
    group 1
    alexander king son father death time
    20 41 37 34 21
    0.62544525721 0.514171626621 0.457520129121 0.15864688743 0.0801005782384
    20  empire army roman augustus emperor battle
    41  alexander king iii father albert son
    37  first years two life time new
    34  god name son king abraham greek
    21  ancient greek century athens period known
    group 2
    title page comment animals preserve book
    40 41 31 9 37
    0.019120022751 0.01819631244 0.0155918749974 0.0150055669722 0.0117947661997
    40  work university theory history analysis science
    41  alexander king iii father albert son
    31  philosophy book human life world smith
    09  sea south north island east area
    37  first years two life time new
    group 3
    two known species form called found
    49 2 8 40 9
    2.22501014371 0.10618909788 0.0803082897559 0.0301053167546 0.0241809472234
    49  two form called known acid different
    02  species family plants food animals genus
    08  medicine treatment medical effects health patients
    40  work university theory history analysis science
    09  sea south north island east area
    group 4
    american english united first known new
    49 26 45 41 16
    0.071235625642 0.0283982709684 0.027125217071 0.0136646046541 0.0081071754926
    49  two form called known acid different
    26  american actor english french british canadian
    45  united states national world new government
    41  alexander king iii father albert son
    16  language arabic languages line written letters
    
    
    
    SUPER 1
    american first alexander king time two
    9 22 17 24 15
    6.49425227545 3.32671751736 2.73831780234 2.45471784812 2.39315655145
    group 0
    alexander king son father death time
    20 41 37 34 21
    0.62544525721 0.514171626621 0.457520129121 0.15864688743 0.0801005782384
    20  empire army roman augustus emperor battle
    41  alexander king iii father albert son
    37  first years two life time new
    34  god name son king abraham greek
    21  ancient greek century athens period known
    group 1
    first work church university time century
    37 31 40 48 49
    0.667715206946 0.640392266466 0.630158854901 0.102368555247 0.063817550481
    37  first years two life time new
    31  philosophy book human life world smith
    40  work university theory history analysis science
    48  church catholic churches roman christian god
    49  two form called known acid different
    group 2
    american actor english french british first
    26 32 20 45 13
    1.14965776722 0.112563199814 0.0664066982786 0.0284960443054 0.0251595129677
    26  american actor english french british canadian
    32  team first league season club two
    20  empire army roman augustus emperor battle
    45  united states national world new government
    13  city university built school building college
    group 3
    title page first comment german art
    37 49 31 45 48
    0.0110106096513 0.0072003622595 0.00380316872361 0.00376626028959 0.00315199944027
    37  first years two life time new
    49  two form called known acid different
    31  philosophy book human life world smith
    45  united states national world new government
    48  church catholic churches roman christian god
    group 4
    american title page first university english
    40 31 9 26 13
    0.022935360636 0.0157983083931 0.0139405899314 0.00748074473526 0.00383432643002
    40  work university theory history analysis science
    31  philosophy book human life world smith
    09  sea south north island east area
    26  american actor english french british canadian
    13  city university built school building college
    
    
    
    SUPER 2
    american first two time new known
    4 6 1 20 15
    2.8263173065 1.89090698541 1.79355751268 1.65932237772 1.45175531048
    group 0
    american english united first known new
    49 26 45 41 16
    0.071235625642 0.0283982709684 0.027125217071 0.0136646046541 0.0081071754926
    49  two form called known acid different
    26  american actor english french british canadian
    45  united states national world new government
    41  alexander king iii father albert son
    16  language arabic languages line written letters
    group 1
    art first new life time two
    37 31 1 26 39
    0.459670164508 0.107075141686 0.0552817397358 0.0205030646673 0.0151238162613
    37  first years two life time new
    31  philosophy book human life world smith
    01  novel play stories best murder short
    26  american actor english french british canadian
    39  music song band released musical group
    group 2
    language arabic languages english line word
    16 49 31 21 23
    0.292228244563 0.106261696067 0.0218289318463 0.0192625218568 0.0178765402334
    16  language arabic languages line written letters
    49  two form called known acid different
    31  philosophy book human life world smith
    21  ancient greek century athens period known
    23  english american british word united words
    group 3
    american city first art new united
    45 13 26 31 2
    0.0101304475376 0.00818056384726 0.00679153636349 0.00656465394158 0.00419999877609
    45  united states national world new government
    13  city university built school building college
    26  american actor english french british canadian
    31  philosophy book human life world smith
    02  species family plants food animals genus
    group 4
    american title page first university english
    40 31 9 26 13
    0.022935360636 0.0157983083931 0.0139405899314 0.00748074473526 0.00383432643002
    40  work university theory history analysis science
    31  philosophy book human life world smith
    09  sea south north island east area
    26  american actor english french british canadian
    13  city university built school building college
    
    
    
    SUPER 3
    american first two known time new
    13 0 2 9 3
    2.82243386268 2.21896672798 2.04509879731 1.95592322442 1.95016416095
    group 0
    two known species form called found
    49 2 8 40 9
    2.22501014371 0.10618909788 0.0803082897559 0.0301053167546 0.0241809472234
    49  two form called known acid different
    02  species family plants food animals genus
    08  medicine treatment medical effects health patients
    40  work university theory history analysis science
    09  sea south north island east area
    group 1
    first work time new two american
    37 40 49 41 26
    0.123751054626 0.0670412148524 0.0492089040261 0.00821391196035 0.00792996231651
    37  first years two life time new
    40  work university theory history analysis science
    49  two form called known acid different
    41  alexander king iii father albert son
    26  american actor english french british canadian
    group 2
    city sea south north area east
    9 45 13 49 37
    0.310430258223 0.152166165333 0.111145216503 0.104547062836 0.103731187619
    09  sea south north island east area
    45  united states national world new government
    13  city university built school building college
    49  two form called known acid different
    37  first years two life time new
    group 3
    alexander king son father death time
    20 41 37 34 21
    0.62544525721 0.514171626621 0.457520129121 0.15864688743 0.0801005782384
    20  empire army roman augustus emperor battle
    41  alexander king iii father albert son
    37  first years two life time new
    34  god name son king abraham greek
    21  ancient greek century athens period known
    group 4
    earth apollo first moon two star
    49 37 9 45 14
    0.497952527712 0.0597400613132 0.0323294311621 0.031345394341 0.0176203386152
    49  two form called known acid different
    37  first years two life time new
    09  sea south north island east area
    45  united states national world new government
    14  apollo mission crew moon space earth
    
    
    
    SUPER 4
    american first two known time new
    11 13 24 14 0
    2.98318536855 2.90556098163 2.86472288123 2.76474675494 2.29943545596
    group 0
    right style center sea south first
    49 9 13 16 8
    0.0350008855936 0.0316154390833 0.0051195824249 0.00460929709985 0.00413551495019
    49  two form called known acid different
    09  sea south north island east area
    13  city university built school building college
    16  language arabic languages line written letters
    08  medicine treatment medical effects health patients
    group 1
    two known species form called found
    49 2 8 40 9
    2.22501014371 0.10618909788 0.0803082897559 0.0301053167546 0.0241809472234
    49  two form called known acid different
    02  species family plants food animals genus
    08  medicine treatment medical effects health patients
    40  work university theory history analysis science
    09  sea south north island east area
    group 2
    title page first comment german art
    37 49 31 45 48
    0.0110106096513 0.0072003622595 0.00380316872361 0.00376626028959 0.00315199944027
    37  first years two life time new
    49  two form called known acid different
    31  philosophy book human life world smith
    45  united states national world new government
    48  church catholic churches roman christian god
    group 3
    war first air armour navy world
    49 18 37 4 24
    0.216780631851 0.0170477108923 0.0160443884176 0.0139357212822 0.00580174531109
    49  two form called known acid different
    18  war air armour first navy gun
    37  first years two life time new
    04  apple system software computer company systems
    24  computer time ascii code standard characters
    group 4
    first work time new two american
    37 40 49 41 26
    0.123751054626 0.0670412148524 0.0492089040261 0.00821391196035 0.00792996231651
    37  first years two life time new
    40  work university theory history analysis science
    49  two form called known acid different
    41  alexander king iii father albert son
    26  american actor english french british canadian
    
    
    
    SUPER 5
    american first two time alexander known
    9 13 22 2 7
    4.05535769811 3.00469723187 2.45702684166 2.00469571026 1.83722897902
    group 0
    alexander king son father death time
    20 41 37 34 21
    0.62544525721 0.514171626621 0.457520129121 0.15864688743 0.0801005782384
    20  empire army roman augustus emperor battle
    41  alexander king iii father albert son
    37  first years two life time new
    34  god name son king abraham greek
    21  ancient greek century athens period known
    group 1
    two known species form called found
    49 2 8 40 9
    2.22501014371 0.10618909788 0.0803082897559 0.0301053167546 0.0241809472234
    49  two form called known acid different
    02  species family plants food animals genus
    08  medicine treatment medical effects health patients
    40  work university theory history analysis science
    09  sea south north island east area
    group 2
    first work church university time century
    37 31 40 48 49
    0.667715206946 0.640392266466 0.630158854901 0.102368555247 0.063817550481
    37  first years two life time new
    31  philosophy book human life world smith
    40  work university theory history analysis science
    48  church catholic churches roman christian god
    49  two form called known acid different
    group 3
    city sea south north area east
    9 45 13 49 37
    0.310430258223 0.152166165333 0.111145216503 0.104547062836 0.103731187619
    09  sea south north island east area
    45  united states national world new government
    13  city university built school building college
    49  two form called known acid different
    37  first years two life time new
    group 4
    number two called form numbers theory
    49 36 31 40 41
    1.12950134718 0.176591138862 0.0304059421632 0.0284431497353 0.00634382429922
    49  two form called known acid different
    36  number numbers theory value function choice
    31  philosophy book human life world smith
    40  work university theory history analysis science
    41  alexander king iii father albert son
    
    
    
    SUPER 6
    first american two time known called
    13 9 7 22 3
    3.23476421683 3.19948173599 2.87804491507 2.71757206235 2.12204748022
    group 0
    two known species form called found
    49 2 8 40 9
    2.22501014371 0.10618909788 0.0803082897559 0.0301053167546 0.0241809472234
    49  two form called known acid different
    02  species family plants food animals genus
    08  medicine treatment medical effects health patients
    40  work university theory history analysis science
    09  sea south north island east area
    group 1
    alexander king son father death time
    20 41 37 34 21
    0.62544525721 0.514171626621 0.457520129121 0.15864688743 0.0801005782384
    20  empire army roman augustus emperor battle
    41  alexander king iii father albert son
    37  first years two life time new
    34  god name son king abraham greek
    21  ancient greek century athens period known
    group 2
    number two called form numbers theory
    49 36 31 40 41
    1.12950134718 0.176591138862 0.0304059421632 0.0284431497353 0.00634382429922
    49  two form called known acid different
    36  number numbers theory value function choice
    31  philosophy book human life world smith
    40  work university theory history analysis science
    41  alexander king iii father albert son
    group 3
    first work church university time century
    37 31 40 48 49
    0.667715206946 0.640392266466 0.630158854901 0.102368555247 0.063817550481
    37  first years two life time new
    31  philosophy book human life world smith
    40  work university theory history analysis science
    48  church catholic churches roman christian god
    49  two form called known acid different
    group 4
    earth apollo first moon two star
    49 37 9 45 14
    0.497952527712 0.0597400613132 0.0323294311621 0.031345394341 0.0176203386152
    49  two form called known acid different
    37  first years two life time new
    09  sea south north island east area
    45  united states national world new government
    14  apollo mission crew moon space earth
    
    
    
    SUPER 7
    american first new world city state
    5 2 22 17 21
    27.9054541582 27.7047876212 8.27769805108 5.23249340745 4.14337040695
    group 0
    state states united national government american
    45 20 37 49 47
    0.230613331935 0.0763507056892 0.0717367931338 0.060455248185 0.0317483782998
    45  united states national world new government
    20  empire army roman augustus emperor battle
    37  first years two life time new
    49  two form called known acid different
    47  population state country government oil austin
    group 1
    city sea south north area east
    9 45 13 49 37
    0.310430258223 0.152166165333 0.111145216503 0.104547062836 0.103731187619
    09  sea south north island east area
    45  united states national world new government
    13  city university built school building college
    49  two form called known acid different
    37  first years two life time new
    group 2
    first work church university time century
    37 31 40 48 49
    0.667715206946 0.640392266466 0.630158854901 0.102368555247 0.063817550481
    37  first years two life time new
    31  philosophy book human life world smith
    40  work university theory history analysis science
    48  church catholic churches roman christian god
    49  two form called known acid different
    group 3
    american actor english french british first
    26 32 20 45 13
    1.14965776722 0.112563199814 0.0664066982786 0.0284960443054 0.0251595129677
    26  american actor english french british canadian
    32  team first league season club two
    20  empire army roman augustus emperor battle
    45  united states national world new government
    13  city university built school building college
    group 4
    center style background color text open
    37 41 13 16 6
    0.0508642793604 0.0136565638516 0.0136385090268 0.00982958806594 0.00878233259808
    37  first years two life time new
    41  alexander king iii father albert son
    13  city university built school building college
    16  language arabic languages line written letters
    06  center style background color text open
    
    
    
    SUPER 8
    american first time two system apple
    16 1 13 24 20
    12.947402875 2.59675688685 2.56259511361 2.53526605861 2.23985033591
    group 0
    apple computer system time first two
    49 4 24 45 36
    0.897405858146 0.209953984253 0.0884871372906 0.0669129535887 0.0483910176081
    49  two form called known acid different
    04  apple system software computer company systems
    24  computer time ascii code standard characters
    45  united states national world new government
    36  number numbers theory value function choice
    group 1
    language arabic languages english line word
    16 49 31 21 23
    0.292228244563 0.106261696067 0.0218289318463 0.0192625218568 0.0178765402334
    16  language arabic languages line written letters
    49  two form called known acid different
    31  philosophy book human life world smith
    21  ancient greek century athens period known
    23  english american british word united words
    group 2
    two known species form called found
    49 2 8 40 9
    2.22501014371 0.10618909788 0.0803082897559 0.0301053167546 0.0241809472234
    49  two form called known acid different
    02  species family plants food animals genus
    08  medicine treatment medical effects health patients
    40  work university theory history analysis science
    09  sea south north island east area
    group 3
    title page first comment german art
    37 49 31 45 48
    0.0110106096513 0.0072003622595 0.00380316872361 0.00376626028959 0.00315199944027
    37  first years two life time new
    49  two form called known acid different
    31  philosophy book human life world smith
    45  united states national world new government
    48  church catholic churches roman christian god
    group 4
    american city first art new united
    45 13 26 31 2
    0.0101304475376 0.00818056384726 0.00679153636349 0.00656465394158 0.00419999877609
    45  united states national world new government
    13  city university built school building college
    26  american actor english french british canadian
    31  philosophy book human life world smith
    02  species family plants food animals genus
    
    
    
    SUPER 9
    first american time two new years
    6 9 3 22 8
    16.8411061162 6.00162928157 5.79468595137 4.98180637303 2.69681724246
    group 0
    art first new life time two
    37 31 1 26 39
    0.459670164508 0.107075141686 0.0552817397358 0.0205030646673 0.0151238162613
    37  first years two life time new
    31  philosophy book human life world smith
    01  novel play stories best murder short
    26  american actor english french british canadian
    39  music song band released musical group
    group 1
    alexander king son father death time
    20 41 37 34 21
    0.62544525721 0.514171626621 0.457520129121 0.15864688743 0.0801005782384
    20  empire army roman augustus emperor battle
    41  alexander king iii father albert son
    37  first years two life time new
    34  god name son king abraham greek
    21  ancient greek century athens period known
    group 2
    earth apollo first moon two star
    49 37 9 45 14
    0.497952527712 0.0597400613132 0.0323294311621 0.031345394341 0.0176203386152
    49  two form called known acid different
    37  first years two life time new
    09  sea south north island east area
    45  united states national world new government
    14  apollo mission crew moon space earth
    group 3
    first work church university time century
    37 31 40 48 49
    0.667715206946 0.640392266466 0.630158854901 0.102368555247 0.063817550481
    37  first years two life time new
    31  philosophy book human life world smith
    40  work university theory history analysis science
    48  church catholic churches roman christian god
    49  two form called known acid different
    group 4
    title page comment animals preserve book
    40 41 31 9 37
    0.019120022751 0.01819631244 0.0155918749974 0.0150055669722 0.0117947661997
    40  work university theory history analysis science
    41  alexander king iii father albert son
    31  philosophy book human life world smith
    09  sea south north island east area
    37  first years two life time new
    
    
    

