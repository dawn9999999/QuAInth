
rouge_l = 0.28
keyword_coverage = 0.625
cosine_similarity = 0.19


weight_rouge_l = 0.2
weight_cosine = 0.2
weight_keyword_coverage = 0.6


total_score = (weight_rouge_l * rouge_l) + (weight_cosine * cosine_similarity) + (weight_keyword_coverage * keyword_coverage)
print("Total Score:", total_score)
