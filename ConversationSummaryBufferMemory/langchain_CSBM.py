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
from langchain.memory import ConversationSummaryBufferMemory

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

# https://zenn.dev/miketako3/articles/66ace6a67df338

#
# 要約するプロンプトを日本語にする。→ 要約も日本語になる。
#
summary_prompt = PromptTemplate(
    input_variables=["summary", "new_lines"],
    template='''
会話の行を徐々に要約し、前の要約に追加して新しい要約を返してください。

例：
現在の要約：
人間はAIに人工知能についてどう思うか尋ねます。AIは人工知能が善の力だと考えています。
新しい会話の行：
人間：なぜあなたは人工知能が善の力だと思いますか？
AI：人工知能は人間が最大限の潜在能力を発揮するのを助けるからです。
新しい要約：
人間はAIに人工知能についてどう思うか尋ねます。AIは人工知能が善の力だと考えており、それは人間が最大限の潜在能力を発揮するのを助けるからです。
例の終わり

現在の要約：
{summary}
新しい会話の行：
{new_lines}
新しい要約：
    ''',
)


# プロンプトテンプレート
prompt_template = PromptTemplate (
    input_variables   = ["history", "input"],  # 入力変数 
    template          = template,              # テンプレート
    validate_template = True,                  # 入力変数とテンプレートの検証有無
)

# 会話の記憶
memory = ConversationSummaryBufferMemory (
    llm = LLM,                  # 文章要約に用いるLLM (default: text-davinci-003)
    max_token_limit=500,        # これを超えたら要約する
    prompt=summary_prompt       # プロンプトを上書き
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
