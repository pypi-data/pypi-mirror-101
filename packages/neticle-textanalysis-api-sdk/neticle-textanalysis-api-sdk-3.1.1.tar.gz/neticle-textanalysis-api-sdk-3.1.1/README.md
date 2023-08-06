# Who we are
[Neticle](https://neticle.com/company/en/)'s proprietary sentiment and semantic analysis technology works with outstanding human-level precision. We know how to get insights automatically from texts and we build products and services applying this technology.

# About this package 
[Neticle Text Analysis](https://neticle.com/textanalysisapi/en/) provides market leading, humanly accurate sentiment and semantic analysis toolkits for in-house corporate use. Or are you looking for NLP (natural language processing)? Yes, that's what we do.

# Getting Started
This package was meant to use with Neticle's Text Analysis API. For further information please visit the project's [home page](https://neticle.com/textanalysisapi/en/).

Start with importing the package into your project:
```python
from textanalysis_python_sdk import NeticleException, TextAnalysis
```
 
After this you can easily use the API with the following code snippet:

```python
textAnalysisApi = TextAnalysis(token='REPLACE-WITH-YOUR-TOKEN')
neticleTextAnalysisAnswer = None
try:
    neticleTextAnalysisAnswer = textAnalysisApi.getTextAnalyzed(language='en',
        input='This is a very good example text.')
except NeticleException as e:
    print('Something went wrong while getting the answer from Neticle Text Analysis API! The error message is: ' + str(e))

# Few example methods:
print('The provided text decorated with HTML spans around recognized entities, synonyms and phrases: ' + neticleTextAnalysisAnswer.getFullHTMLText())
print('The overall sentiment score (opinion index) calculated from the provided text: ' + str(neticleTextAnalysisAnswer.getOpinionIndex()))
# For a detailed description of provided methods please refer to the TextAnalysisAnswer class's documentation.
```