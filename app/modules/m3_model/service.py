from .rules import deduplicate,totals

def execute(rows):
    good,bad=deduplicate(rows)
    return totals(good)|{'rows':good,'quarantine':bad,'accepted':len(good)}
