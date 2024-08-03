# -*- coding: utf-8 -*-p
"""
Created on Sat Aug  3 13:06:10 2024

@author: kalyan
"""

import os
import pandas as pd
import torch
import torch.nn as nn
import transformers
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
# Load the model name 7b parameter
tokenizer = transformers.AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")

# Create a text generation pipeline
generator = transformers.pipeline(
	"text-generation",
	model="tiiuae/falcon-7b-instruct",
	tokenizer=tokenizer,
	torch_dtype=torch.bfloat16,
	trust_remote_code=True,
	device_map="auto",
)

promt = ''
#ask question and press to exit
while promt != 'q':
 promt = input('Question: ')
 # Generate text sequences
 text_sequences = generator(
 	promt,
 	max_length=200,
 	do_sample=True,
 	top_k=10,
 	num_return_sequences=1,
 	eos_token_id=tokenizer.eos_token_id,
 )

 # Print the generated text sequences
for i in text_sequences:
 	print(f"Result: {i['generated_text']}")
