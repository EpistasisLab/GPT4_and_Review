This repository has been established to house the supplementary materials associated with the study titled **Using GPT-4 to Write a Scientific Review Article: A Pilot Evaluation Study**. The contents include:

* **Prompts and content evaluations**: detailed analysis of the prompts used and the subsequent evaluations of the content generated by GPT-4.
   - BRP-1 - Contains the detailed prompts and responses for each section and sub-section of BRP-1. For each section and sub-section, there are two documents - one contains the prompts and responses from the API CHATGPT-4, and the other contains prompts and responses from the baseline model. There are prompts and responses for the projections section and the reproducibility tests.
   - BRP-2 - Contains the detailed prompts and responses that was used to recreate the images and tables that are present in BRP-2.
   - list_of_points.xlsx - This excel sheet contains the final prompts used for evaluation between the original and the GPT-4 responses. It has separate spreadsheets for each section and sub-section of BRP-1. It also contains sheets for the projections and reproducibility tests. The final sheet contains the evaluation between the table in BRP-2 and the table created by API CHATGPT-4
* **Plagiarism check results**: outcomes of plagiarism assessments conducted on the GPT-4 generated content.
   - sex_differences_in_cancer.pdf : reference-based content generation
   - sex_differences_in_cancer_baseline.pdf : baseline content generation
* **ChatGPT API code**: the source code utilized for interfacing with the ChatGPT API during the study.
   - code script (remove API key)
* **Similarity comparison code**: algorithms developed to compare and contrast the similarity between the generated content and existing literature.
   - compare.py - This Python script was used for comparing the semantic similarity between two sets of sentences. It requires a CSV file where the first column is named Original and the second is named GPT. Under Original, the text from the target section was provided, and the response from GPT was provided under GPT.
