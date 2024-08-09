# NLP_VeriSeti
Bu repo İçerik Muhafızı takımımızın bert tabanlı model eğitiminde kullanılan veri setini ve eğitilen modelin nasıl kullanılacağını içerir.

# Model Kullanımı 
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "IcerikMuhafizi/bert-base-turkish-uncased-IM3"

model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
