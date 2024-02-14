#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Azure ChatOpenAI
# https://python.langchain.com/docs/integrations/chat/azure_chat_openai

# Memory in LLMCHain
# https://python.langchain.com/docs/modules/memory/adding_memory

# openai: 1.8.0
# langchain: 0.0.351

from langchain.chains import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os

class AzureOpenAIChat:
    def __init__(self, verbose=False, buffer_k=2):

        self.verbose = verbose
        self.buffer_k = buffer_k
        
        self.llm = AzureChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            azure_deployment="exam1",
            azure_endpoint="https://exam01.openai.azure.com/",
            api_version="2023-07-01-preview",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0,
            n=1,
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""
            あなたは人間と会話するAIです。
            過去の会話履歴はこちらを参照: {history}
            Human: {input}
            AI:
            """,
            validate_template=True,
        )
        
        self.memory = ConversationBufferWindowMemory(k=self.buffer_k)
        
        self.chain = LLMChain (
            llm=self.llm,
            prompt=self.prompt_template,
            verbose=self.verbose,
            memory=self.memory,
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
