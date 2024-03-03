from Ai_brain import Openai, geminai

flag = 0


def reply_chat(query, chat_log=None):
    global flag
    with open("chat_log.txt", "r") as file_log:
        chat_log_template = file_log.read()
    if "use open ai model" in query.lower():
        flag = 1
        return "using open AI"
    elif "use gemini ai model" in query.lower():
        flag = 0
        return "using gemini AI"
    if chat_log is None:
        chat_log = chat_log_template
    prompt = f'{chat_log} You: {query}\n Park: '
    if flag == 1:
        answer = Openai.generate_response(prompt)
        chat_log_template_update = chat_log_template + f"\n You: {query}. \n Park: {answer} "
        with open("chat_log.txt", "w") as file_log:
            file_log.write(chat_log_template_update)
    else:
        answer = geminai.generate_response(f"'this information only for you don't repeat this in answer - i use this "
                                           f"model chatbot,your name is Park,so answer to the point,and don't return '*' in answer'\n{query}.")

    return answer

