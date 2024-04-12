def is_letter(character: str) -> bool:
    return character.isalpha()


def convert_to_lowercase(character: str) -> str:
    return character.lower()


def calculate_letter_frequency(text: str) -> dict:
    text = text.lower()
    letter_frequency = {}
    total_letters = 0
    for char in text:
        if char.isalpha():
            if char not in letter_frequency:
                letter_frequency[char] = 0
            letter_frequency[char] += 1
            total_letters += 1
    letter_frequency_percent = {letter: (count / total_letters) * 100 for letter, count in letter_frequency.items()}
    return letter_frequency_percent


def personal_info():
    print("Ad: Cennet")
    print("Soyad: Boylu")
    print("Öğrenci Numarası: 211213015")
    print("Not: Uyan ÇALIŞ")



   #Three men came to New York for a holiday. They came to a very large hotel and took a room there. Their room was on the forty-fifth floor. In the evening friends went to the theatre and came back to the hotel very late. “I’m very sorry,” said the clerk of the hotel, “but the lifts don’t work tonight. If you don’t want to walk up to your room, we shall make beds for you in the hall.” “No, no,” said one of the friends, “no, thank you. We don’t want to sleep in the hall. We shall walk up to our room.” Then he turned to his friends and said: “It’s not easy to walk up to the forty-fifth floor, but we shall make it easier. On the way to the room I shall tell you some jokes; then you, Andy, will sing us some songs; then you, Peter, will tell us some interesting stories.” So they began walking up to their room. Tom told them many jokes; Andy sang some songs. At last, they came to the thirty-sixth floor. They were tired and decided to have a rest. “Well,” said Tom, “now it’s your turn, Peter. After all the jokes, I would like to hear a sad story. Tell us a long and interesting story with a sad end.” “The story which I’m going to tell you,” said Peter, “is sad enough. We left the key to our room in the hall.”