def get_symbol(date, month):
    if (month == 12 and date >= 22) or (month == 1 and date <= 19):
        return ["Capricorn", "Ground", "Secluded, Shy, Faithful, Conscientious, Ambitious, Loyal"]
    elif (month == 1 and date >= 20) or (month == 2 and date <= 18):
        return ["Aquarius", "Water", "Peace Lover, Clear-Sighted, Intuitive, Loyal, Inventive, Revolutionary"]
    elif (month == 2 and date >= 19) or (month == 3 and date <= 20):
        return ["The Pisces", "Water", "Empathy, Humane, Careless, Kind, Secretive, Easygoing, Inspiring"]
    elif (month == 3 and date >= 21) or (month == 4 and date <= 19):
        return ["Aries", "Fire", "Warm, Enthusiastic, Social, Emotional, Stressed, Impulse Driven, Aggressive"]
    elif(month == 4 and date >= 20) or (month == 5 and date <= 20):
        return ["Taurus", "Ground", "Stubborn, Protective, Loyal, Patient, Persistent, Stable, Practical, Realistic"]
    elif (month == 5 and date >= 21) or (month == 6 and date <= 21):
        return ["The Twins", "Air", "Quick, Communicative, Superficial, Curious, Independent, Brave, Impulsive, Stressed"]
    elif (month == 6 and date >= 22) or (month == 7 and date <= 22):
        return ["Crab", "Water", "The Parent, The Protector, The Custodian, The Faithful, The Loyal & Sympathetic"]
    elif (month == 7 and date >= 23) or (month == 8 and date <= 22):
        return ["Lion", "Sun", "Magnificent, Loving, Strong-Willed, Jealous, Leader, Faithful, Conscientious"]
    elif (month == 8 and date >= 23) or (month == 9 and date <= 22):
        return ["Virgo", "Ground", "Shy, Self-Aware, Analytical, Productive, Critical, Changeable"]
    elif (month == 9 and date >= 23) or (month == 10 and date <= 22):
        return ["Wave", "Air", "Love, Charm, Indecision, Seduction, Diplomacy, Social Skills"]
    elif (month == 10 and date >= 23) or (month == 11 and date <= 21):
        return ["Scorpio", "Water", "Intense, Jealous, Passionate, Quiet, Intense, Loyal, Brave, Strong"]
    else:
        return ["Error", "Details: Date and Month Must Be Numerical Values. Date and Month Must Be Real Dates and Months."]


def output_enter():
    print("Choose month. Must be a numerical value.")

    print("1. January")

    print("2. February")

    print("3. March")

    print("4. April")

    print("5. May")

    print("6. June")

    print("7. July")

    print("8. August")

    print("9. September")

    print("10. October")

    print("11. November")

    print("12. December")

    month = int(input('Month: '))

    print("Choose date. Must be a numerical value.")

    date = int(input('Date: '))

    symbol = get_symbol(date, month)

    if symbol[0] != "Error":
        print(f"Symbol: {symbol[0]}")
        print(f"Element: {symbol[1]}")
        print(f"Characteristics: {symbol[2]}")
    else:
        print(symbol)


def get_help():
    print("This package is a simple Star Symbol Finder.")
    print("To use it in your script just import it and then (if you imported it as starsymbolfinder), type starsymbolfinder.get_symbol(date, month)")
    print("Replace date and month with the date and month you want to find.")
    print("You can also use starsymbolfinder.output_enter() to make yourself able to type the date and month in the output.")
