import random

def generate_answer(message):
    answers = [
        "This is 1",
        "This is 2",
        "This is 3",
        "This is 4",
        "This is 5",
        "This is 6",
        "This is 7",
        "This is 8",
        "This is 9",
        "This is 10"
    ]
    
    # 리스트에서 랜덤하게 하나의 문장을 선택해서 반환
    return random.choice(answers)
