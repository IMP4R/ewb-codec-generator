# Active labs completion — authoritative checkpoint

## Latest overriding status
- Background job bash-50 COMPLETED exit0 and collected. execute_asm.py executed six repaired MASM bodies translated syntactically to NASM and Unicorn32: calc2063+branch2063+avg500+static500+dynamic500+bits65536 =71162 actual machine-code casesPASS, callee-savedABIallPASS. Fullreportprogramming/machine_execution_report.json. NotnativeMASM/VisualStudio linkclaim.
- Lab7bitsCPP rewritten strictfull-linebinary1..16digits,EOFsafe+C++maskoracle. AllfourrepairedCPPfrontendssyntaxpassclang++11-WallWextra-pedantic.
- build_combinational.py/generatedlogic11+SumSub512 allindependentpin-graphchecksPASS connectivity_verification.json. ActualEWB FullAdderoldlayout/Muxloadverified, improvedregeneratedversionsnotallchecked. Workflowsnotallcomplete.
- OldLab8.1formulaentirelywrongcorrectedfromrenderPDF. BackupLab6–8beforeeditsprogramming-backups.
- CurrentEWB sw_read0.ewb RUNNING withmeter4.995V (actualswitchcommonStatus0connecthigh). LastPID2383234. Thisfixture NOTsubmission; oneversionmeterincorrectserieslink butonlyswitchstateprobe. HalfAdder.switches2 aliasfailed(truncatedlongfilename), ha_clean succeeded; actualhalfsimoneSUM1Carry0 only. Noneofthefourkeyboardcaptureschangedoutputs, so truthcasesNOTverified. ha11 openedcorrectlybutafterstartprobesbothwhite becauseStatus1low->00, labelsfilename11NOTactualinputbits. Needinvertstatushigh0low1 andclearview/simstate.


User approved Inverter as IDEAL and requested all labs3–8 finish plus beautiful orthogonal cable-management for no-reference schemas. No per-round chat needed. Do not claimallcomplete. Goal6ff43c86 active rev3 max40 (get_goal verify).

## Actual verified outputs
Lab3 Inverter.ewb approved; NAND.ewb,NOR.ewb newnative correctload and visuals copied /Users/user0/АВУ/сдача/Лаб_3/ewb. NAND85% NOR90% render fullcanvas. actualNAND00sim4.995V screenshotNAND_sim00.png. Need allinputsimtable; NAND/NOR labels+modeDINon.
NAND/NOR Networkbuilder fixedzero-segmentwirecrash by segments[(1,0)] forcoincidentpins; no segsi0. Codec stripslinebreaksbeforelocating$! marker andwriterkeepsfinalchecksumfootercontiguous (criticalNORloadfailurefix).

## Native digital work
DIGITALD.EWX downloaded native_libraries/DIGITALD.EWX, escapedtext shows actualnames: Not/And2..8/Or2..8/Nand2../Nor2../Xor2../Xnor2..,HA,FA,RS,JK3,JK,D,DN,Volt,Vdd,Pull,ProbeR,etc. Do NOT use guessedDFlipFlop orHalfAddername. `resource_merge.entries` reads21bytearchive records withfooter<HIHH>, canextractparams; already params/and2.par,and3.par,not.par,d_ff.par,dn.par,ha.par,fa.par,probr.par,volt.par,rs_ff.par extracted. Paramfilesbinarybitmappluspinrecordsatend.
VerifiedExtCompnative names openload successfully screenshotdigital_supported.png. DigitalNetworkpinmapsverified with isolatedprobe: Notinput0output1,2input gatesinput0top/input1bottom/output2. 3inputinput0top,input1center,output2right,input3bottom. ProbeRorient2 receivesfromLEFT terminal0(x-20,y). PN38togglepins0commonLEFT(x-10,y+20),1lowRIGHTbottom(x+20,y+10),2highRIGHTtop(x+20,y+30),ASCIIkeyboard49etc. Status0seemsconnectcommon->high,Status1low; fixture sw_read0 simulation4.995V actualscreenshot. Use actualfixedstatuscases for truthverification, don'tassumekeypress state changed.

### Generator files
network.py analog terminal-awareorthogonalbuilder exports .topology.json.
digital.py nativeExtComp +idealmodelPartNum99paramsfromfactorygates.ewb.
digital_network.py extendsnativecomponentmap andnowexports .topology.json.
logic_builder.py compilesDAGtolayersverticalfanoutlanesinputsSPDTswitch5V+groundoutputsredProbeR. Currentlogicplacementcanstillspaghetti longloops/overlaps, refine aesthetics beforepublishing. Gateslayouts deterministic, allnative. build_combinational.py generated11files; build_sumsub.py generated4bitaddsub.
verify_logic.py INDEPENDENT reconstructedserializedtopologyDSU pin connectivity evaluator verifiedallinputcombos: 11smallcircuits84?casesplusSumSub512. JSONconnectivity_verification.json. ThisisnotEWBsimulatorclaim. Purebitnetlists pinconnections allPASS. No-fulltestedclaim: behavior_map_buildgenericfound0nodes, notvalidfullcoverage fordomain; explicittruthmanifestexists.
ActualEWBload FullAdder.ewb screenshotfa_native.png andMux2to1 screenshotmux_new.png noerrors butroutingstyleNOTyetbeautiful. FulladderoldplotlabelsplacedCoutintheSrowbad; fixedlaterlogic_builder centering singleitemlayers/outputaligneddriverlevels, regenALL. NEEDnewactualrender.
HalfAddernativeprototype withtogglesbuild_halfadder.py loadha_clean.ewb screenshotha_clean.png. OneactualsimulationmixedcaseSUMlit/CARRYoff afterAnalysis Activate; keyboardinteractionfailed/nochangingprobes becausefocus/menu/state, repeatedcapturessame =>DONOTCLAIM4casesverified. Fixedstatusfilesha00ha01ha10ha11 generatedbutnotalltested. Fixturewrongmeterbridge is onlyswitchcheck notsubmission. Currentlive editorsw_read0.ewb active with4.995V.

### Live server
LastPID2383234,window16777217checklive. ConfigDINon(Ini Din=on/Ansi=off/VectorGraphicson; NOT1/0). Root205.196.80.53 key~/.ssh/winmcp DISPLAY99. Files EWB512. GUI filenamecustomtextboxCtrlAdoesn'tselect; HomeShiftEnd. field570360,Open850347firstclickfocussecondactivates. LONGnames sometimestypedtruncate/missed char (HalfAdder.switches2 loadedswitchesmissing2 ->couldnotopen):shortuniquealiases recommended.
Activate viaobservedAnalysis menu Alt+a thenclick14030, works actualsimtime/indicators. CtrlG/menu andtoolbarclickoftenjustfocusnotactivate,verifyactualtime/output. StopCtrlT, savechangesNo700483whenopenafteredits. ErrorOKsamecoords. Neverblindnavigatewithdialogs. File-loadfailedstalegraywindowrequiresrestart exactPIDonly.

## Actual programming repairs made
OriginalLabs6–8 fullybacked up ewb_rev/programming-backups.
Commonheader /Users/user0/АВУ/сдача/common/input_short.h strictwholelineinteger syntax/range/EOF andlonglines. Lab7calc.asm+cpp rebuilt exact(2a-1)/(b-2),32bitintermediate,shortresultrange, status div0/overflow. Lab8branch.old formula WRONGentirely, PDFpage renderedlab8_piecewise.png: a>b (3a+5)/(b-1),a=b10,a<b(a+b)/(a-b). BOTHasmcpprewrittencorrect. Lab8arrayAmean32bitsum,counts/no-positivecase explicit; Bstaticcheckedoverflowand32bitindex; Cdynamicshort[] pointers2bytes stride,checkedoverflowandno partialwrites,CPPRAIIshortarraysstrictinput; allcppsyntaxcheckedclang++ -stdc++11 -WallWextra -pedantic.
Lab7bits.asmcalleesavedEBXpreserved now; stillneedsCPPinputfix. Lab6notauditedyet.

### Real machine execution tests
Dedicated venvprogramming/venvinstalledunicorn; nasminstalledbrew (jobbash49completedcollected). execute_asm.py takesACTUALMASMinstructionbodies,translatesoperandmemorysyntaxonlytoNASM, assemblesbinary,runsUnicornx8632. ABIregistersentinels. NotVisualStudio nativebuildclaim.
First 4routines passed5126machinecodecases: calc2063,branch2063,mean500,staticmatrix500. Then extended dynamic500+ALL65536bitvalues, backgroundjobbash-50 CURRENT RUNNING orsettlednotcollectedyet! Mustcollectjob_output beforefinal. Do notduplicateitsrun. Ifsyntaxfailfix accordingly. outputJSONmachine_execution_report.json persistedonlyonfullsuccess.
execute_asm dynamicextra_memory reads/writes allocatedshortarrays; checksunchangedonoverflow;bitsallvalueschecksexpectedmasks.

## Immediate next
1. collectbash50 whensettled; workindependentwhiletestsrun.
2. FinishnativefunctionalEWB truthcasesusingfixedswitchstates andactualsim activation. Refinecleaninputschematics (sourcepolaritycorrect,powerbuslinesnotloopthroughbattery),single outputstraightalignedlabel lanes.
3. CompleteLab5reallatches/register/memory modelsD/DNexactparams andstateverification.
4. FinishLab6ABI/syntaxauditandLab7bitsstrictbinaryinput. NativeWindows32buildtooling ifavailableotherwiseclearlystateemulatedtestvsMASMbuild.
5. RegenerateDOCXreportswithrealverifiedscreenshots/results,cleaninvalidoldclaims (lab8wrongformulaespecially). Do notsayallfinishedbeforeallfilesandactualtests.
