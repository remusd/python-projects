import json
import random
from MealOptimizer import OptimizeMeal

PROTEIN_CAL = 4
CARBS_CAL = 4
FATS_CAL = 9


class DailyIntake():

    indices = {
        "male"   : [864, 9.72, 14.2, 503, [1.0, 1.12, 1.27, 1.54]],
        "female" : [387, 7.31, 10.9, 660.7, [1.0, 1.14, 1.27, 1.45]]
    }

    def __get__(self, instance, owner=None):
        [x, y, z, t, PA] = self.indices[instance.gender]
        return x - y * instance.age + PA[instance.activity_level-1] * (z * instance.weight + t * instance.height / 100)


class DietaryRestrictions():
    
    def __get__(self, instance, owner=None):
        file = open('foods.json')
        all_foods = json.load(file)
        allowed = [food for food in all_foods if not list(set(instance.restrictions) & set(food['tags'])) ]
        return allowed


class DietaryPlan():

    # [carbs, proteins, fats]
    # All percentages
    diet_plans = {
        'Default'      : [50, 30, 20],
        'Vegetarian'   : [53, 15, 32],
        'Mediteranean' : [51, 18, 31],
        'HighProtein'  : [40, 30, 30]
    }

    def __get__(self, instance, owner=None):
        return self.diet_plans[instance.diet_type]


class MealPlan():

    # Percentages
    meal_plans = {
        3 : {
            'Breakfast' : 35,
            'Lunch'     : 40, 
            'Dinner'    : 25
            },

        4 : {
            'Breakfast'     : 30,
            'Morning snack' : 5,
            'Lunch'         : 40, 
            'Dinner'        : 25
            },

        5 : {
            'Breakfast'       : 30,
            'Morning snack'   : 5,
            'Lunch'           : 40,
            'Afternoon snack' : 5, 
            'Dinner'          : 20
            }
    }

    def __get__(self, instance, owner=None):
        return self.meal_plans[instance.meals_number]


class Person():

    calories = DailyIntake()
    allowed_foods = DietaryRestrictions()
    diet_plan = DietaryPlan()
    meal_plan = MealPlan()

    def __init__(self, age, gender, weight, height, activity_level, meals_number=3, diet_type="Default", restrictions=[]):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.height = height
        self.activity_level = activity_level
        self.restrictions = restrictions
        self.diet_type = diet_type
        self.meals_number = meals_number


class Meal():

    def __init__(self, name, calories_total, carbs_w, protein_w, fats_w, allowed_foods):
        self.name = name
        self.calories_total = calories_total
        self.carbs_w = carbs_w
        self.protein_w = protein_w
        self.fats_w = fats_w
        self.allowed_foods = allowed_foods

    def prepare(self):

        main = random.choice([food for food in self.allowed_foods if 'protein' in food['tags']])
        side = random.choice([food for food in self.allowed_foods if 'vegetable' in food['tags']])

        # Following are multipled to convert from grams of nutrient to nutrient calories
        main_p = PROTEIN_CAL * main['protein']
        side_p = PROTEIN_CAL * side['protein']
        main_c = CARBS_CAL * main['carbohydrate']
        side_c = CARBS_CAL * side['carbohydrate']
        main_f = FATS_CAL * main['fat']
        side_f = FATS_CAL * side['fat']

        max_calories = self.calories_total
        max_p = self.protein_w * max_calories / 100
        max_c = self.carbs_w * max_calories / 100
        max_f = self.fats_w * max_calories / 100

        [main_q, side_q, main_p, side_p, main_c, side_c, main_f, side_f] = OptimizeMeal(main['calories'], main_p, main_c, main_f,
                                                                                        side['calories'], side_p, side_c, side_f,
                                                                                        max_calories, max_p, max_c, max_f)
        main_weight = round(main_q * main['grams'])
        side_weight = round(side_q * side['grams'])
        main_calories = round(main_p + main_c + main_f)
        side_calories = round(side_p + side_c + side_f)
        total_protein_calories = round(main_p + side_p)
        total_carbs_calories = round(main_c + side_c)
        total_fats_calories = round(main_f + side_f)
        total_calories = total_protein_calories + total_carbs_calories + total_fats_calories

        print("Recommendation:")
        print(f"{main_weight}gr {main['name']} ({main_calories} kcal)")
        print(f"{side_weight}gr {side['name']} ({side_calories} kcal)")
        print(f"Proteins: {total_protein_calories} kcal")
        print(f"Carbs   : {total_carbs_calories} kcal")
        print(f"Fats    : {total_fats_calories} kcal")
        print(f"Total   : {total_calories} kcal")



if __name__ == "__main__":

    # while True:

    #     print()
    #     age = input("Age (15-100): ")
    #     if int(age) not in range(15, 100):
    #         print("Age must be between 15-100")
    #         continue
        
    #     gender = input("Gender (male/female): ")
    #     if gender not in ["male", "female"]:
    #         print("Gender must be male or female")
    #         continue

    #     weight = input("Weight in Kg (40-150): ")
    #     if int(weight) not in range(40, 150):
    #         print("Weight must be between 40-150")
    #         continue

    #     height = input("Height in cm (140-240): ")
    #     if int(height) not in range(140, 240):
    #         print("Weight must be between 140-240 cm")
    #         continue

    #     print("Activity Level")
    #     print("1 - Sedentary. Little or no exercise")
    #     print("2 - Light. Exercise 1-3 times a week")
    #     print("3 - Moderate. Exercise 4-5 times a week")
    #     print("4 - Active. Daily exercise")
    #     activity = input("Enter value (1-4): ")
    #     if int(activity) not in range(1, 5):
    #         print("Activity must be between 1-4")
    #         continue

    #     break

    age = 34
    gender = "male"
    weight = 71
    height = 174
    activity = 1

    person = Person(int(age), gender, int(weight), int(height), int(activity))

    daily_intake = person.calories
    print(f"\nRecommended daily intake: {daily_intake}kcal\n")

    [carbs_w, protein_w, fats_w] = person.diet_plan
    print(f"Chosen diet plan [{person.diet_type}] - {carbs_w}% Carbs, {protein_w}% Protein, {fats_w}% Fats\n")

    meal_plan = person.meal_plan
    print(f"Recommended daily plan for {len(meal_plan)} meals:\n")


    for meal in meal_plan:

        meal_intake = int(daily_intake * meal_plan[meal] / 100)
        print(f"{meal}: {meal_intake} kcal")

        dish = Meal(meal, meal_intake, carbs_w, protein_w, fats_w, person.allowed_foods)

        if meal in ['Breakfast', 'Lunch', 'Dinner']:
            cal_proteins = round(protein_w / 100 * meal_intake)
            cal_carbs = round(carbs_w / 100 * meal_intake)
            cal_fats = round(fats_w / 100 * meal_intake)
            print(f"\t- proteins {cal_proteins} kcal / ~{round(cal_proteins/PROTEIN_CAL)}g")
            print(f"\t- carbs {cal_carbs} kcal / ~{round(cal_carbs/CARBS_CAL)}g")
            print(f"\t- fats {cal_fats} kcal / ~{round(cal_fats/FATS_CAL)}g")
            dish.prepare()
            print()
        else:
            print("\t\t- snacks\n")