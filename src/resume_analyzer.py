import re

def analyze_resume(resume_content, job_description):
    keywords = extract_keywords(job_description)
    analysis_results = {
        'matched_keywords': [],
        'missing_keywords': [],
        'score': 0
    }

    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', resume_content, re.IGNORECASE):
            analysis_results['matched_keywords'].append(keyword)
        else:
            analysis_results['missing_keywords'].append(keyword)

    analysis_results['score'] = len(analysis_results['matched_keywords']) / len(keywords) * 100 if keywords else 0
    return analysis_results

def extract_keywords(job_description):
    # Simple keyword extraction logic (can be improved)
    return re.findall(r'\b\w+\b', job_description) 