import pandas as pd
from utils import extract_text, ats_scores

def rank_resumes(files, jd):
    data = []
    for f in files:
        text = extract_text(f)
        scores = ats_scores(text, jd)
        data.append({
            "Candidate": f.name,
            "ATS Match": scores["match"],
            "Job Fit": scores["fit"],
            "Quality": scores["quality"],
        })
    df = pd.DataFrame(data)
    return df.sort_values(by="ATS Match", ascending=False)
