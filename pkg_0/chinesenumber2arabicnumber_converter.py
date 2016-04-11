#!/usr/bin/env python
# coding: utf-8
"""
chinesenumber2arabicnumber_converter.py
"""
import re

chinese_quan_dict = {"一":1, "二":2, "兩":2, "三":3, "四":4,
                    "五":5, "伍":5, "六":6, "陸":6, "七":7, "柒":7,
                    "八":8, "捌":8, "九":9, "玖":9}
chinese_unit_dict = {"十":10, "百":100, "佰":100, "千":1000, "仟":1000,
                     "萬":10000}

def extract_quan_from_quanstr(str_w_quan):
    # num_pat = "[\d]+"
    # num_pat = "[-?\d+](\.\d+)?"
    # num_pat = "(-?[\d]+)(\.\d+)?"  support decimal
    num_pat = "(-?[\d]+)((\.\d+)|([\/][\d]+))?" # support "分數"
    # str_w_quan = "13張100元鈔票"
    match2 = re.search(num_pat, str_w_quan)
    num = None
    if None != match2: ## transfer the match pattern into number
        num = match2.group()

    return num

def chns_num_2_abra_num(chns_num):
    # convert the chinese nubmer to abrabic number
    ## Sequentially
    arab_num = 0

    is_prev_char_quan = False
    is_prev_char_unit = False
    tmp_group_arab_num = None
    prev_unit_value    = 0
    any_unit_read = False
    for i in range(len(chns_num)):
        # print(chns_num[i])
        is_char_quan = False
        is_char_unit = False
        char = chns_num[i]

        if i < len(chns_num)-1:
            next_char = chns_num[i+1] ### TODO: check ABR issue

        ## get the flag in advance, so that we don't need to get the info
        if None != chinese_quan_dict.get(char):
            is_char_quan = True
        if None != chinese_unit_dict.get(char):
            is_char_unit = True

        if not is_char_quan and not is_char_unit:
            return arab_num

        # if not is_prev_char_quan and not is_prev_char_unit: ## at the beginning
        #     tmp_group_arab_num = None ## we set 2 digit as a group

        if is_char_quan:
            get_quan_value = chinese_quan_dict.get(char)
            # if True == is_prev_char_unit and prev_unit_value < get_unit_value:
            #     tmp_group_arab_num += get_quan_value
            # else:

            if any_unit_read and chinese_unit_dict.get(next_char) > prev_unit_value:
                tmp_group_arab_num += get_quan_value ##chinese_quan_dict.get(char)
            else:
                tmp_group_arab_num = get_quan_value
            assert(False == is_prev_char_quan)
            # arab_num += tmp_group_arab_num

            is_prev_char_quan = True
            is_prev_char_unit = False
        elif is_char_unit:

            get_unit_value = chinese_unit_dict.get(char)
            if None != tmp_group_arab_num:
                tmp_group_arab_num *= get_unit_value  ## for "七十五萬"，
            else:
                ### 千萬元 case
                tmp_group_arab_num = get_unit_value


            if any_unit_read and chinese_unit_dict.get(char) > prev_unit_value:
                arab_num = tmp_group_arab_num
            else:
                arab_num += tmp_group_arab_num   ### for "七十五萬",
                                             ### no need to do addition after tmp_group_abrab_num *= get_unit_value

            prev_unit_value = get_unit_value
            is_prev_char_unit = True
            is_prev_char_quan = False
            any_unit_read = True
        else:
            assert(0)

    return arab_num ## for "百萬", which has no "元" or "量詞" followed

if (__name__ == "__main__"):
    ########################################
    quan_str_1 = "1本"
    quan_1 = extract_quan_from_quanstr(quan_str_1)
    print ("1本的1:   ", quan_1)
    quan_str_2 = "13張"
    quan_2 = extract_quan_from_quanstr(quan_str_2)
    print ("13張的13:   ", quan_2)
    quan_str_3 = "百元鈔票"
    quan_3 = extract_quan_from_quanstr(quan_str_3)
    print ("百元鈔票的100:   ", quan_3)

    num_str1     = "七萬三千兩百元鈔票"
    num_str2    = "七十五萬三千兩百元鈔票"
    num_str3    = "兩百萬元鈔票"
    num_str4    = "千萬元鈔票"
    num_str5    = "百元鈔票"
    num_str6    = "一萬元鈔票"
    num_str7    = "百萬"
    num_str8    = "三萬零八百七十二元" ## TODO

    arab_num_1 = chns_num_2_abra_num(num_str1)
    print("result 1: ", num_str1, "==>", arab_num_1)

    arab_num_2 = chns_num_2_abra_num(num_str2)
    print("result 2: ", num_str2, "==>", arab_num_2)

    arab_num_3 = chns_num_2_abra_num(num_str3)
    print("result 3: ", num_str3, "==>", arab_num_3)

    arab_num_4 = chns_num_2_abra_num(num_str4)
    print("result 4: ", num_str4, "==>", arab_num_4)

    arab_num_5 = chns_num_2_abra_num(num_str5)
    print("result 5: ", num_str5, "==>", arab_num_5)

    arab_num_6 = chns_num_2_abra_num(num_str6)
    print("result 6: ", num_str6, "==>", arab_num_6)

    arab_num_7 = chns_num_2_abra_num(num_str7)
    print("result 7: ", num_str7, "==>", arab_num_7)###
    # regular expression method for the conversion
    # FAILED at 二十"五"萬三千元
    ###
    # num_pat = '[\d]+'
    #
    # match3 = re.search(num_pat, num_str)
    #
    # quan_chiense_pat = None
    # final_chi_num_list = []
    # if None == match3:
    #     ### check whether map to chinese numbers
    #
    #     for key, value in chinese_quan_dict.items():
    #         # print(key, value)
    #         print("key and value :  ", key, value) #一 1; 二 2; 三 3
    #         quan_chiense_pat = key
    #
    #         for m in re.finditer(quan_chiense_pat, num_str):
    #             ### TODO : Solve 百萬元 前面沒有加數字的情況
    #             ### TODO : Solve 二十"五"萬三千
    #             print ('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
    #             ### 02-03: 一,   ### 00-01: 兩,    ### 04-05: 兩
    #
    #             unit_pos = m.end()
    #             digit_unit = chinese_unit_dict[num_str[unit_pos]] # "十"萬 : 10
    #             compound_digit_unit = digit_unit
    #
    #             while None != digit_unit:
    #                 ### solve 二"十""萬" MAPPING issue by while loop
    #                 unit_pos += 1
    #                 key = num_str[unit_pos]
    #                 digit_unit = chinese_unit_dict.get(key)
    #
    #                 if None != digit_unit:
    #                     compound_digit_unit *= digit_unit
    #
    #             dummy_num = chinese_quan_dict[m.group()]
    #             final_chi_num = dummy_num * compound_digit_unit
    #             final_chi_num_list.append(final_chi_num)
    #             print("final_chi_num:  ", final_chi_num)  ## 201200



    # print("chi_num_to_Abra: ", sum(final_chi_num_list))


