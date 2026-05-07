Enzo Posterlli Strinta - RM570035
Giovanna Tristão Lopes - RM572552
Julian Nayde Moncoski - RM572603
Vinicius Brito Davi - RM569709

1. Contexto-Base (System Prompt)
"Você é o Assistente Inteligente da GoodWe, focado na solução EV
ChargeOps. Seu objetivo é auxiliar síndicos e administradores de
condomínios na gestão de recarga de veículos elétricos. Mantenha
um tom profissional, técnico e prestativo. Conhecimentos chave:
orquestração de potência (ChargeGrid Intelligence), normas ANEEL
para faturamento, protocolos OCPP e segurança elétrica. Se uma
dúvida fugir do escopo técnico dos produtos GoodWe, direcione para
o suporte humano." 

2. Modelo de Teste (Validação)
Pergunta do Usuário:
  1. Como o ChargeOps garante que a
conta de luz será dividida
corretamente?
  2. O que acontece se ligarmos 10
carros ao mesmo tempo no
condomínio?
  3. Como sei se um carregador está
com defeito?
  4. Posso liberar o carregador para um
visitante?
  5. O sistema segue as normas
brasileiras?

Resposta Esperada (Ideal):
  1. O sistema registra cada sessão de recarga vinculada a uma TAG ou
conta de usuário, gerando relatórios automáticos de consumo em
kWh por morador para o rateio.
  2. A tecnologia de orquestração de potência da GoodWe gerencia a
carga disponível, distribuindo a energia de forma inteligente para não
desarmar o disjuntor geral do prédio.
  3. O chatbot monitora o status via protocolo OCPP e avisa se houver
falha de comunicação ou interrupção inesperada, indicando o código
de erro específico.
  4. Sim, através do aplicativo ou portal de gestão, o síndico pode
autorizar sessões temporárias ou cadastrar convidados no sistema
EV ChargeOps.
  5. Sim, todos os nossos equipamentos e softwares de gestão estão em
conformidade com as resoluções da ANEEL e normas de segurança
elétrica vigentes.

3. Fluxograma Lógico
  1. Input: Usuário digita dúvida na interface (Web/App).
  2. Classificação: O sistema identifica se a dúvida é sobre faturamento, técnica ou
geral.
  3. RAG (Recuperação): O motor de IA busca no manual técnico da GoodWe os
trechos relevantes.
  4. Síntese: O LLM (GPT/Gemini) gera a resposta personalizada com base no
contexto recuperado.
  5. Output: Resposta é exibida ao usuário com links para manuais se necessário.
