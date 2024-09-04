# Você precisa ter o Langchain instalado
# O requests
# O black para fazer formatação no código
# Para fazer o scrapping vamos usar o beautifulsoup4

#Criar ferramenta para pesquisar documentações
#Criar ferramenta para formatar o código
#Criar o agente que vai usar essas ferramentas

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool


load_dotenv()

# Pegando a API Key de dentro do .env
openai_api_key = os.getenv("OPENAI_API_KEY")


# Utilizando o decorator do langchain para definir uma ferramenta para agentes
@tool
def black_formatter_tool(path: str) -> str:
    """ Essa ferramenta recebe um input de caminho onde se encontra um
     script em python e roda um black formater para formatar o código python
     desse arquivo."""
    
    try:
        os.system(f"conda run black {path}")
        return "Feito com Sucesso!"
    except:
        return "Falha!"
    

# Lista de ferramentas que o meu agente terá
toolkit = [black_formatter_tool]

llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
            Você é um assistente de programação. Use suas ferramentas para melhor responder 
         as questões do usuário. Se você não tem a ferramenta necessária para responder,
         diga que não tem.

         Retorne apenas as respostas.
         """),
         MessagesPlaceholder("chat_history", optional=True),
         ("human", "{input}"),
         MessagesPlaceholder("agent_scratchpad")
    ]
)

agent = create_openai_tools_agent(llm, toolkit, prompt)

agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)

response = agent_executor.invoke({"input":"""Tenho esse código aqui:
                                  {'codigoParaFormatar.py'}, poderia formatar pra mim?"""})

print(response)

# de fato, o código que estava no meu ambiente e antes era mal formatado, foi formatado!








    




