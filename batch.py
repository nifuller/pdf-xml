# batch_size = 250
# pdf_tokens = pdf_text.split(" ")
# for i in range(0, len(pdf_tokens), batch_size):
#     if i < batch_size:
#         before_context = ""
#     else:
#         before_context = " ".join(pdf_tokens[i-batch_size:i])
#     pdf_to_convert = " ".join(pdf_tokens[i:i+batch_size])
#     if i+batch_size*2 >= len(pdf_tokens):
#         after_context = ""
#     else:
#         after_context = " ".join(pdf_tokens[i:i+batch_size:i+batch_size*2])