def file_open(filename):
    data = []
    with open(filename, "r") as f:
        data_sample = ""
        is_in_empty = False

        line = f.readline()
        while (line):
            if line == "\n":
                if not is_in_empty:
                    data.append(data_sample)
                    data_sample = ""
                    is_in_empty = True
            else:
                is_in_empty = False
                data_sample += line
            line = f.readline()

    data_gentle = []
    for sample in data:
        words = sample.split(" ")
        len_words = len(words)
        start = " ".join(words[:len_words// 3])
        mid = " ".join(words[len_words// 3:len_words // 3 * 2])
        end = " ".join(words[len_words // 3 * 2:])
        data_gentle.append([start, mid, end])
    return data_gentle

data_gentle = file_open("rotating.py")
data_nice = file_open("settle_debts.py")