#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Azure ChatOpenAI
# https://python.langchain.com/docs/integrations/chat/azure_chat_openai

# Memory in LLMCHain
# https://python.langchain.com/docs/modules/memory/adding_memory

# openai: 1.6.0
# langchain: 0.0.351

from langchain.chains import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

import os

LLM = AzureChatOpenAI (
    model_name        = "gpt-3.5-turbo-16k",
    azure_deployment  = "exam1",
    azure_endpoint    = "https://exam01.openai.azure.com/",
    api_version       = "2023-07-01-preview",
    api_key           = os.getenv("AZURE_OPENAI_API_KEY"),
    #
    temperature       = 0, # 出力する単語のランダム性（0から1の範囲） 0であれば毎回返答内容固定
    n                 = 1, # いくつの返答を生成するか           
)

# Prompt Template作成
template = \
    """
    あなたは人間と会話するAIです。
    過去の会話履歴はこちらを参照: {history}
    Human: {input}
    AI:
    """

# プロンプトテンプレート
prompt_template = PromptTemplate (
    input_variables   = ["history", "input"],  # 入力変数 
    template          = template,              # テンプレート
    validate_template = True,                  # 入力変数とテンプレートの検証有無
)

# 会話の記憶
memory = ConversationBufferWindowMemory (
    k = 2,                      # いくつの対話を記録するか
)

# make chain
chain = LLMChain (
    llm = LLM,                  # LLMモデル 
    prompt  = prompt_template,  # プロンプトテンプレート
    verbose = True,             # プロンプトを表示するか否か
    memory  = memory,           # メモリ
)

messages = ["pythonとはなんですか？",
            "他のプログラムミング言語と比較してください。",
            "それらのプログラムミング言語の学びやすさの順位づけをしてください。",
            "あなたはどの言語が好みですか？"]

for question in messages:

    # LLM Chain実行
    answer = chain.predict(input=question)

    # 出力
    print(answer)

    # chain.memory.chat_memory.messages[n] ← Human, AI, Human, AI, ...

    import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
