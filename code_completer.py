from transformers import AutoModelForCausalLM, AutoTokenizer
from dataset_creation import data_gentle, data_nice
import csv

checkpoint = "bigcode/tiny_starcoder_py"
device = "cpu" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

def filewrite(filename, data):

    predictions = []
    references = []

    for data_sample in data:
            input_text = f"<fim_prefix>{data_sample[0]}<fim_suffix>{data_sample[2]}<fim_middle>"
            inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
            outputs = model.generate(inputs,
                                     max_length=(len(data_sample[0])+len(data_sample[1])+len(data_sample[2]))//2 + 30,
                                     num_return_sequences=1,
                                     temperature=0.7,
                                     top_k=50,
                                     top_p=0.9)
            result = tokenizer.decode(outputs[0])
            start = result.find("<fim_middle>") + len("<fim_middle>")
            end = result.find("<|endoftext|>")
            predictions.append(result[start:end])
            references.append(data_sample[1])

    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Reference", "Prediction"])
        for ref, pred in zip(references, predictions):
            writer.writerow([ref, pred])

filewrite("results.csv", data_gentle)
filewrite("results01.csv", data_nice)