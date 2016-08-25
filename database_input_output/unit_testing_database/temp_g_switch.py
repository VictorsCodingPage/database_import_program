def switch_gender(category_id, gender):
    # f_to_m = json.loads('{"3": 23, "4": 22, "5": 25, "6": 26, "8": 27, "15":31, "16": 32, "17": 33, "18": 34, "20": 37, "39": 35, "38": 36}')
    # m_to_f = json.loads('{"23": 3, "22": 4, "25": 5, "26": 6, "27": 8, "31":15, "32": 16, "33": 17, "34": 18, "37": 20, "35": 39, "36": 38}')

    f_to_m = {"3": 23, "4": 22, "5": 25, "6": 26, "8": 27, "15":31, "16": 32, "17": 33, "18": 34, "20": 37, "39": 35, "38": 36}
    m_to_f = {"23": 3, "22": 4, "25": 5, "26": 6, "27": 8, "31":15, "32": 16, "33": 17, "34": 18, "37": 20, "35": 39, "36": 38}

    category_id_2 = None
    gender_switched = False

    if category_id in range(22, 38, 1):
        if gender == "Women":
            category_id_2 = m_to_f.get(str(category_id))
            print "Man to Woman, {} to {}".format(category_id, category_id_2)
    elif gender == "Man":
            category_id_2 = f_to_m.get(str(category_id))
            print "Woman to Man, {} to {}".format(category_id, category_id_2)
    else:
        print "{} kept category_id {}".format(gender, category_id)

    if category_id_2 is not None:
        category_id = category_id_2
        gender_switched = True

    return (category_id, gender_switched)