# AI-choose-your-own-adventure

Integrating the chatgtp api and a vector database to create a random and continuous game of choose your own adventure with memory.  
  
The chatgtp model itself has unreliable memory, so this program attempts to mitigate that by using retrieval augmented generation (RAG). Using a vector database, it stores previous data about the conversation and then injects it into the prompt.
