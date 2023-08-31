# import random
# import time

# def multiple_choice_test(dictionary):
#     score = 0
#     total_questions = len(dictionary)
#     used_questions = set()

#     while used_questions != set(dictionary.keys()):
#         # Chọn một câu hỏi ngẫu nhiên chưa được sử dụng
#         question_key = random.choice(list(dictionary.keys()))
#         while question_key in used_questions:
#             question_key = random.choice(list(dictionary.keys()))
        
#         used_questions.add(question_key)
#         question_data = dictionary[question_key]

#         is_english_to_vietnamese = random.choice([True, False])

#         if is_english_to_vietnamese:
#             question = f"\t{question_key} ?"
#             correct_answer = question_data
#             options = [correct_answer]
#             while len(options) < 4:
#                 random_option = random.choice(list(dictionary.values()))
#                 if random_option not in options:
#                     options.append(random_option)
#             random.shuffle(options)
#         else:
#             question = f"\t{question_data} ?"
#             correct_answer = question_key
#             options = [correct_answer]
#             while len(options) < 4:
#                 random_option = random.choice(list(dictionary.keys()))
#                 if random_option not in options:
#                     options.append(random_option)
#             random.shuffle(options)

#         print(question)
#         for i, option in enumerate(options):
#             print(f"{i + 1}. {option}")

#         user_answer = input("Chọn (1/2/3/4): ")
#         if options[int(user_answer) - 1] == correct_answer:
#             print("Đúng!")
#             score += 1
#         else:
#             print(f"Sai. Đáp án đúng là: {correct_answer}")

#         time.sleep(1)
#         print('-'*30)
#     print(f"Điểm: {score}/{total_questions}")

# def fill_in_the_blank_test(dictionary):
#     score = 0
#     total_questions = len(dictionary)

#     for vietnamese_phrase, english_translation in dictionary.items():
#         print(f"{english_translation}")
#         user_answer = input("Trả lời: ").lower()
        
#         if user_answer.strip() == english_translation:
#             print("Đúng!")
#             score += 1
#         else:
#             print(f"Sai. Đáp án đúng là: {english_translation}")
        
#         time.sleep(1)
#         print('-'*30)

#     print(f"Điểm: {score}/{total_questions}")

# if __name__ == "__main__":
    
#     dict_ = 'to work as a/an + N(job):làm nghề gì, shift:ca làm việc, night shift:ca đêm, biology:sinh học , biologist:nhà sinh học, biological:thuộc về sinh học, to join hands = to work together: chung tay, to be willing + V(bare):sẵn lòng làm gì, household chores:việc nhà, to run the hoursehold: điều hành gia đình, to make sure: đảm bảo, rush=hurry=go quickly : vội vã, responsibility: trách nhiệm, to be + responsible for V-ing/sth: chịu trách nhiệm về việc gì, to take the responsibility for + V-ing/sth: đảm nhận trách nhiệm về việc gì, pressure: áp lưc, to be + under pressure: bị áp lực, caring:quan tâm, to take out: xóa bỏ ,mischievous:tinh nghịch, mischief:sự tinh nghịch, give sb a hand = help sb:  giúp đỡ ai , obedient:ngoan ngoãn, disobedient: không ngoan, obeđience: sự ngoan ngoãn, obey:nghe theo, close-knit: gắn bó, be + supportive of sb: tương trợ ai, frankly: 1 cách thẳng thắn, frank: trung thực , to make a decision:đưa ra quyết định,  solve:giải quyết, solution: giải pháp, secure = safe:an toàn , security:bảo mật, to be + crowded with: đông đúc (ngươiè), wel_behaved: biết cư xử tốt, confidence: sự tự tin, to be + confidence : tin tưởng , to be + based on = to rely on: dự trên nền tẳng, come up = appear/happend : xảy ra, hard-working: chăm chỉ, to be + good at + V-ing: giỏi về cái gì  '



#     # Tách chuỗi thành danh sách các cặp key-value bằng dấu phẩy
#     pairs = dict_.split(', ')

#     # Khởi tạo một từ điển rỗng
#     dictionary = {}

#         # Duyệt qua từng cặp key-value và thêm vào từ điển
#     for pair in pairs:
#         # Split by the first colon only
#         parts = pair.split(':', 1)
        
#         # Check if there are exactly two parts
#         if len(parts) == 2:
#             key, value = parts
#             dictionary[key] = value


#     while True:
#         print("Chọn cách kiểm tra:")
#         print("1. Trắc nghiệm (English to Vietnamese / Vietnamese to English)")
#         print("2. Tự luận (Vietnamese to English)")
#         print("3. Exit")

#         choice = input("Nhập (1/2/3): ")

#         if choice == '1':
#             multiple_choice_test(dictionary)
#         elif choice == '2':
#             fill_in_the_blank_test(dictionary)
#         elif choice == '3':
#             break
#         else:
#             print("error, nhập 1 2 3 thôi.")



# Gán giá trị cho question_main trong dictionary
dict_ = {
    '1':('2', '3'),
    '2':('2', '3'),
    '3':('2', '3'),
    '4':('2', '3'),
    '5':('2', '3'),
    '6':('2', '3'),
}

vv = dict_.items()
# Trả về dictionary với question_main và giá trị của nó
for key, (c, d) in vv:
    print(key, c+ d)
