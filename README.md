# MWP_ExplanationGenerator
Math Word Problem - Explanation Generator
(https://www.youtube.com/watch?v=rHuOqZKNjP4 、 http://ct-joe-huang.weebly.com/research.html)

More than providing merely number as the answer to a Math Word Problem,
this application generates `Explanation Sentences` of a Math Word Problem according to 
the tagging information of Stanford CoreNLP Suit(https://www.youtube.com/watch?v=rHuOqZKNjP4 、http://stanfordnlp.github.io/CoreNLP/) as well as it's post-processing information.

In this archive, outputs of Stanford CoreNLP are arranged in files with ".scp" extension.
Besides,
".stc" files include OPERATOR information more than ".scp" files.
".lf" files and ".trace" as well as ".ie" files mean post-processing infos after 
Logic Form and Information Engine seperately. 
Explanation Generator takes them (mainly labels directly from Stanford CoreNLP)
to integrates explanation sentenses into a Math Word Problem.

Issues such as Voice, Active/Passive, Pronoun etc in explanation are all solved in this Algorithm.
For Tense, this project further adopts a standalone Context Free Grammar approach (in statemachine.py & statemachine_tv.py) 
to build automata state-machine, classifying answering sentences into 12 tenses in English.

Finally, plz kindly run `Regression Test` to get to know more!

```sh
    $ cd pkg
%%% UW dataset
    $ ./pkg/run_uwds_0.py
%%% UIUC dataset
    $ ./pkg/run_ilds_000.py
```
P.S. More detailed steps are written in ``` $ pkg/README.md```


#### EXPLANATION TEXTs OF UW-395 DATASET ARE in pkg_0/
- uwds1_golden_000.log
- uwds2_golden_000.log
- uwds3_golden_000.log

#### EXPLANATION TEXTs OF UIUC-562 DATASET ARE in pkg_0/
- ilds0_golden_000.log
- ilds1_golden_000.log
- ilds2_golden_000.log
- ilds3_golden_000.log
- ilds4_golden_000.log
- ilds5_golden_000.log

```sh
P.S.: PLEASE REFER TO pkg_0/README.txt FOR FURTHER INFORMATION
```

Acknowledgement:
Templates could be refactored with Strategy Pattern for modulization.
However, since there's only around more than 10 operators, I didn't refactor it at that time.
