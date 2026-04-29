def extract_important_info(text):
    text = text.lower()
    data = []

    if "my name is" in text:
        data.append(("name", text.split("is")[-1].strip()))

    if "nickname" in text:
        data.append(("nickname", text.split("is")[-1].strip()))

    if "i like" in text:
        data.append(("preference", text))

    return data
