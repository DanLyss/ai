from sacrebleu.metrics import CHRF
from sacrebleu import corpus_bleu
from rouge_score import rouge_scorer
import csv

def exact_match(predictions, references):
    cleaned_predictions = [''.join(pred.split()) for pred in predictions]
    cleaned_references = [''.join(ref.split()) for ref in references]

    matches = sum(1 for pred, ref in zip(cleaned_predictions, cleaned_references) if pred == ref)

    if len(predictions) == 0:
        return 0.0

    return (matches / len(predictions)) * 100


def chrf_score(predictions, references):
    chrf = CHRF()
    return chrf.corpus_score(predictions, [references]).score


def bleu_score(predictions, references):
    return corpus_bleu(predictions, [references]).score


def rouge_l_score(predictions, references):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = [scorer.score(pred, ref) for pred, ref in zip(predictions, references)]
    avg_rougeL = sum(score['rougeL'].fmeasure for score in scores) / len(scores)
    return avg_rougeL


def metrics(filename):
    references = []
    predictions = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            references.append(row["Reference"])
            predictions.append(row["Prediction"])

    em = exact_match(predictions, references)
    chrf = chrf_score(predictions, references)
    bleu = bleu_score(predictions, references)
    rougel = rouge_l_score(predictions, references)

    metric_scores = [em, chrf, bleu, rougel]
    return {"exact match" : em, "chrf": chrf, "bleu": bleu, "rouge_L" : rougel}


metrics_geometry = metrics("results.csv")
metrics_debts = metrics("results01.csv")

with open("results.csv", mode="a", encoding="utf-8", newline="") as file:
    fieldnames = metrics_geometry.keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerow(metrics_geometry)

with open("results01.csv", mode="a", encoding="utf-8", newline="") as file:
    fieldnames = metrics_debts.keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerow(metrics_debts)
