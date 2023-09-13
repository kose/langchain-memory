# LangChain の memory 機構

LangChainには Chat 履歴保存のための memory 機能があります。

- ConversationBufferMemory: チャット履歴を全て記録する。
- ConversationBufferWindowMemory: チャット履歴をいくつ保存するか指定する。
- ConversationSummaryMemory: チャット内容を要約して記録する。
- ConversationSummaryBufferMemory: チャット内容を要約して記録する。（max_token_limitを超えたら）

(使うならこれだろうと)ふたつ試した。


## Reference

- [LangchainのMemory機能の覚え書き](https://qiita.com/ayoyo/items/07da43bbab6652d37421)
- [【Python】LangChain Memoryとは｜ChatGPTが過去の会話履歴に基づき返答できる機能作成](https://di-acc2.com/programming/python/26917/)

