from scipy.optimize import linprog

def OptimizeMeal(main_calories, main_proteins, main_carbs, main_fats, 
                 side_calories, side_proteins, side_carbs, side_fats, 
                 max_meal_calories, proteins_limit, carbs_limit, fats_limit):
    
    Mm, Mp, Mc, Mf = main_calories, main_proteins, main_carbs, main_fats
    Ss, Sp, Sc, Sf = side_calories, side_proteins, side_carbs, side_fats
    MM = max_meal_calories
    PP = proteins_limit
    CC = carbs_limit
    FF = fats_limit

    #                            [MQ, SQ, Mp, Sp, Mc, Sc, Mf, Sf]
    coefficients_inequalities = [[Mm, Ss,  0,  0,  0,  0,  0,  0], # Main calories * Main quantity + Side calories * Side quantity < max_meal_calories
                                 [0,   0,  1,  1,  0,  0,  0,  0], # Main total proteins + Side total proteins < proteins_limit
                                 [0,   0,  0,  0,  1,  1,  0,  0], # Main carbs + Side carbs < carbs_limit
                                 [0,   0,  0,  0,  0,  0,  1,  1], # Main fats + Side fats < fats_limit
                                 [Mp, Sp,  0,  0,  0,  0,  0,  0], # Proteins per Main serving + Proteins per Side serving < proteins_limit
                                 [Mc, Sc,  0,  0,  0,  0,  0,  0], # Carbs per Main serving + Carbs per Side serving < carbs_limit
                                 [Mf, Sf,  0,  0,  0,  0,  0,  0]]

    constants_inequalities = [MM, PP, CC, FF, PP, CC, FF]

    coefficients_equalities   = [[-Mm,   0, 1, 0, 1, 0, 1, 0], 
                                 [  0, -Ss, 0, 1, 0, 1, 0, 1]]

    constants_equalities = [0, 0]

    coefficients_max = [-1, -1, 0, 0, 0, 0, 0, 0]  # maximize quantity of Main + Side
    res = linprog(coefficients_max,
                A_ub=coefficients_inequalities,
                b_ub=constants_inequalities,
                A_eq=coefficients_equalities,
                b_eq=constants_equalities)

    [main_q, side_q, main_p, side_p, main_c, side_c, main_f, side_f] = [round(val, 2) for val in res.x]
    return [main_q, side_q, main_p, side_p, main_c, side_c, main_f, side_f]
