import torch
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

quantized_model_dir = "webbigdata/ALMA-7B-Ja-GPTQ-Ja-En"
model_basename = "gptq_model-4bit-128g"

tokenizer = AutoTokenizer.from_pretrained(quantized_model_dir)

model = AutoGPTQForCausalLM.from_quantized(
        quantized_model_dir,
        model_basename=model_basename,
        use_safetensors=True,
        device="cuda:0")


def translate(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt", padding=True, max_length=200, truncation=True).input_ids.cuda()
    with torch.no_grad():
        generated_ids = model.generate(input_ids=input_ids, num_beams=5, max_new_tokens=250, do_sample=True, temperature=0.6, top_p=0.9)
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return outputs[0]


def translate_ja2en(v):
    prompt = "Translate this from Japanese to English:\nJapanese: " + v + "\nEnglish:"
    out = translate(prompt)
    res = out.split("English:")[-1]
    return res


def translate_en2ja(v):
    prompt = "Translate this from English to Japanese:\nEnglish: " + v + "\nJapanese:"
    out = translate(prompt)
    res = out.split("Japanese:")[-1]
    return res
