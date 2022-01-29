def get_decl(number: int, titles: list) -> str:
    number = number % 100
    if 11 <= number <= 19:
        answer = titles[2]
    else:
        item = number % 10
        if item == 1:
            answer = titles[0]
        elif item in (2, 3, 4):
            answer = titles[1]
        else:
            answer = titles[2]
    return answer
