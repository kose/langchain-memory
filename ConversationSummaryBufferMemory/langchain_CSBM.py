#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenAI API と通信するライブラリです。

answer = Lang_Predictor.get_message(question)

question: 質問文 (文字列）
answer: 回答文 (文字列）

"""

import os

if 'OPENAI_API_KEY' not in os.environ:
    print("環境変数 OPENAI_API_KEY がセットされていません。")
    exit(-1)

#################################################################

import openai
from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
    
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = os.getenv("OPENAI_API_ENGINE")
model_name = os.getenv("OPENAI_API_MODEL")

class Lang_Predictor:

    def __init__(self, verbose=False):
        """
        verbose: デバッグ用のprompt表示
        """

        #
        # Prompt Template作成
        #
        template = \
            """
            あなたは人間と会話するAIです。
            過去の会話履歴はこちらを参照: {history}
            Human: {input}
            AI:
            """

        # プロンプトテンプレート
        prompt_template = PromptTemplate(
            input_variables   = ["history", "input"],  # 入力変数 
            template          = template,              # テンプレート
            validate_template = True,                  # 入力変数とテンプレートの検証有無
        )

        #
        # LLM作成
        #
        LLM = OpenAI(
            model_name        = model_name,
            engine            = engine,
            temperature       = 0,                  # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
            n                 = 1,                  # いくつの返答を生成するか           
            )

        #
        # memor
        #
        memory = ConversationSummaryBufferMemory (
            llm = OpenAI(),                          # 文章要約に用いるLLM (default: text-davinci-003)
            max_token_limit=500                      # これを超えたら要約する
        )
        
        #
        # LLM Chain
        #
        self.chain = LLMChain (
            llm     = LLM,             # LLMモデル 
            prompt  = prompt_template, # プロンプトテンプレート
            verbose = verbose,         # プロンプトを表示するか否か
            memory  = memory,          # メモリ
        )
        
        
    def get_message(self, question):

        answer = self.chain.predict(input=question)
            
        return answer



def main():

    predictor = Lang_Predictor(verbose=True)
    
    messages = ["pythonとはなんですか？",
                "他のプログラムミング言語と比較してください。",
                "それらのプログラムミング言語の学びやすさの順位づけをしてください。",
                "あなたはどの言語が好みですか？"]

    for question in messages:

        # ユーザ
        # LLM Chain実行
        answer = predictor.get_message(question)

        # 出力
        print(answer)

        # chain.memory.chat_memory.messages[n] ← Human, AI, Human, AI, ...
    
        import pdb; pdb.set_trace()


if __name__ == "__main__":
    main()
        
# import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
