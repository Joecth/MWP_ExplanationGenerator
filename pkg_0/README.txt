0. cd pkg_0

### Execute:
1. python3 __init__.py -i [input.trace.xml] -o [out.xml] 
    // default output: output.xml,
    // log files: raw_tree.xml, build_tree.log.xml
 
### Regression:
1. ./runreg.py     
    // script, run under Unix environment since popen2 cannot be found in PyCharm
2. vi ./reg_output_new/report.xml
    // to see the diff of all cases in regression this run
