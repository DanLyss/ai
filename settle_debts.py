ExpenseItem = tuple[int, float, str, list[str]]

def encodeExpense(expense: ExpenseItem) -> str:
    return f"{expense[0]}:{expense[1]}:{expense[2]}:{','.join(expense[3])}"

def decodeExpense(data: str) -> ExpenseItem:
    object1, object2, object3, participants = data.split(":")
    return int(object1), float(object2), object3, list(participants.split(","))

DebtSummary = list[str, float, dict[str, float]]
def buildDebtSummaries(records: list[ExpenseItem]) -> list[DebtSummary]:
    summary: dict[str, list[float, dict[str, float]]] = {}

    for record in records:
        for person in record[3]:
            summary[person] = [0, {}]

    for record in records:
        payer = record[3][0]
        summ = record[1]
        shares_number = len(record[3])
        summary[payer][0] += (shares_number - 1) * summ / shares_number

        for lender in record[3]:
            if lender != payer:
                summary[lender][0] -= summ / shares_number
                if payer in summary[lender][1]:
                    summary[lender][1][payer] += summ / shares_number
                else:
                    summary[lender][1][payer] = summ / shares_number

    formatted_summary: list[DebtSummary] = []
    for person, person_summary in summary.items():
        person_summary = [person] + person_summary
        formatted_summary.append(DebtSummary(person_summary))
    return formatted_summary

def buildEdges(values: list[(float, int)]) -> dict[int, (int, float)]:
    n = len(values)
    values.sort(key=lambda x: x[0], reverse=True)
    edges = {}
    cumsum = 0

    for i in range(n - 1):
        cumsum += values[i][0]
        edges[values[i][1]] = (values[i+1][1], cumsum)
    cumsum += values[n - 1][0]

    if cumsum < 0:
        raise Exception("Incorrect list[DebtSummary]")
    return edges


def settleDebts(debts: list[DebtSummary]) -> list[DebtSummary]:
    mapping = {}
    values = []
    for i in range(len(debts)):
        mapping[i] = debts[i][0]
        if debts[i][1] != 0:
            values.append((-debts[i][1], i))

    edges = {}
    if len(values) != 0:
        edges = buildEdges(values)
    new_summary: list[DebtSummary] = []

    for i in range(len(debts)):
        if (i in edges) and (edges[i][1] != 0):
            new_summary.append(DebtSummary([mapping[i], debts[i][1], {mapping[edges[i][0]]: edges[i][1]}]))
        else:
            new_summary.append(DebtSummary([mapping[i], debts[i][1], {}]))
    return new_summary