#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Azure ChatOpenAI
# https://python.langchain.com/docs/integrations/chat/azure_chat_openai

# Memory in LLMCHain
# https://python.langchain.com/docs/modules/memory/adding_memory

# langchain         0.2.6
# langchain-openai  0.1.14

import os
from langchain.chains import ConversationChain
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory

class AzureOpenAIChat:
    def __init__(self, verbose=False):

        self.verbose = verbose
        
        self.llm = AzureChatOpenAI (
            model_name="gpt-3.5-turbo-16k",
            azure_deployment="exam1",
            azure_endpoint="https://exam01.openai.azure.com/",
            api_version="2024-02-15-preview",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0,
            n=1,
        )

        self.prompt_template = PromptTemplate (
            input_variables=["history", "input"],
            template="""
                あなたは人間と会話するAIです。
                過去の会話履歴はこちらを参照: {history}
                Human: {input}
                AI:
                """,
            validate_template=True
        )

        self.summary_prompt = PromptTemplate (
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
            '''
        )

        self.memory = ConversationSummaryBufferMemory (
            llm=self.llm,
            max_token_limit=500,
            prompt=self.summary_prompt
        )

        # self.chain = LLMChain (
        self.chain = ConversationChain (
            llm=self.llm,
            prompt=self.prompt_template,
            verbose=self.verbose,
            memory=self.memory
        )

    def ask (self, question):
        return self.chain.predict(input=question)


def main():
    # インスタンスの作成
    azure_chat = AzureOpenAIChat(verbose=True)

    # メッセージに対して応答を生成
    messages = [
        "pythonとはなんですか？",
        "他のプログラムミング言語と比較してください。",
        "それらのプログラムミング言語の学びやすさの順位づけをしてください。",
        "あなたはどの言語が好みですか？"
    ]

    for question in messages:
        answer = azure_chat.ask(question)
        print(answer)

        import pdb; pdb.set_trace()

if __name__ == "__main__":
    main()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
    
