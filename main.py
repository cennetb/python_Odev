import module

if __name__ == "__main__":
    text = input("Lütfen bir metin girin: ")
    for length in [100, 1000, 10000]:
        letter_frequency = module.calculate_letter_frequency(text[:length])
        print(f"---Metin uzunluğu: {length}---")
        for letter, percent in letter_frequency.items():
            print(f"{letter}: %{percent:.2f}")
    module.personal_info()