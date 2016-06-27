0. cd pkg_0

### Execute:
1. python3 __init__.py -i [input.trace.xml] -l [input.lft.xml] -s [input.stc.xml] -o [out.xml] 
    // default output: output.xml,
    // log files: raw_tree.xml, build_tree.log.xml
    Example:
        python3 __init__.py -i demo_cases/task.UWDS.20160407/data.ENG.UW.DS3.new/uwds-0275.trace.xml -l demo_cases/task.UWDS.20160407/data.ENG.UW.DS3.new/uwds-0275.lft.xml -s demo_cases/task.UWDS.20160407/data.ENG.UW.DS3.new/uwds-0275.stc.xml
    
    P.S. currently only demo_cases/ directory collects *lft.xml and *stc.xml 

### Regression:
Reg 1)
    1. ./runreg.py     
    // script, run under shell; popen2 package cannot be found in PyCharm
    2. vi ./reg_output_new/report.xml
    // to see the diff of all cases in regression this run
Reg 2) UW's dataset
    ./run_uwds_0.py
Reg 3) UIUC's dataset
    ./run_ilds_000.py

#### Input Files location:
under demo_cases/
