import discord
from discord.ext import commands
import random

#antes de rodar o codigo, considere permitir as intents lá na config do bot no portal do desenvolvedor do discord no seu bot e conceder pemissão de gerenciar mensagens.

#lembre-se tamém de colocar o token do seu bot no comando run no final do código.

# O jogo é baseado em tentar acertar as palavras e tem dois modos de jogo, solo e duo.

# dê !comandos para poder visualizar os comandos do bot.


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)


palavras = [
  {
    "palavra":
    "cadeira",
    "dicas": [
      "Usada para sentar", "Tem quatro pernas",
      "Muito comum em salas de estar", "É feita de madeira ou metal",
      "Pode ter almofada"
    ]
  },
  {
    "palavra":
    "telefone",
    "dicas": [
      "Usado para fazer chamadas", "Geralmente colocado no bolso",
      "Tem uma tela sensível ao toque", "Usado para enviar mensagens",
      "Pode ser um celular ou fixo"
    ]
  },
  {
    "palavra":
    "caneta",
    "dicas": [
      "Usada para escrever", "Tem tinta dentro",
      "Comum em escritórios e escolas", "Geralmente tem uma tampa",
      "Faz parte do material escolar"
    ]
  },
  {
    "palavra":
    "livro",
    "dicas": [
      "Contém páginas", "Usado para ler", "Pode ser de ficção ou não ficção",
      "Tem capa", "Geralmente é composto por vários capítulos"
    ]
  },
  {
    "palavra":
    "mesa",
    "dicas": [
      "Usada para apoiar objetos", "Geralmente feita de madeira",
      "Pode ser encontrada em salas de jantar", "Tem uma superfície plana",
      "Usada para refeições ou trabalho"
    ]
  },
  {
    "palavra":
    "computador",
    "dicas": [
      "Usado para navegar na internet", "Tem um monitor",
      "Usado para digitar e jogar", "Composto por teclado e mouse",
      "Tem um processador e memória"
    ]
  },
  {
    "palavra":
    "garrafa",
    "dicas": [
      "Usada para armazenar líquidos", "Pode ser de vidro ou plástico",
      "Comum em mesas de refeição", "Tem uma tampa",
      "Pode ser reutilizável ou descartável"
    ]
  },
  {
    "palavra":
    "janela",
    "dicas": [
      "Pode ser aberta para ventilação", "Fica em uma parede", "Tem vidro",
      "Comum em quartos e salas", "Permite a entrada de luz e ar"
    ]
  },
  {
    "palavra":
    "refrigerante",
    "dicas": [
      "Bebida gasosa", "Comumente tem sabores como cola e laranja",
      "Vendida em latas ou garrafas", "Tem um sabor doce",
      "É uma bebida popular em festas"
    ]
  },
]


jogos_ativos = {}



@bot.command()
async def jogar(ctx):
  await ctx.send(
    "Você quer jogar sozinho ou com outra pessoa? (Responda com 'sozinho' ou '2')"
  )

  def check(message):
    return message.author == ctx.author and message.content.lower() in [
      'sozinho', '2'
    ]

  resposta = await bot.wait_for("message", check=check, timeout=30)

  if resposta.content.lower() == 'sozinho':
    await ctx.send(f"Você escolheu jogar sozinho, {ctx.author.mention}!")
    await jogar_sozinho(ctx)
  else:
    await ctx.send(
      f"Você escolheu jogar com outra pessoa, {ctx.author.mention}! Digite `!jogar2 @player2` para convidar alguém."
    )



async def jogar_sozinho(ctx):
  jogador_da_vez = ctx.author 

  
  if jogador_da_vez.id not in jogos_ativos:
    jogo = random.choice(palavras)
    palavra_secreta = jogo["palavra"]
    dicas = jogo["dicas"]

    
    jogos_ativos[jogador_da_vez.id] = {
      'palavra': palavra_secreta,
      'dicas': dicas,
      'dica_atual': 0,
      'tentativas': 0,
      'modo': 'sozinho',
      'iniciado': False
    }

  
  jogo = jogos_ativos[jogador_da_vez.id]
  palavra_secreta = jogo["palavra"]
  dicas = jogo["dicas"]
  dica_atual = jogo["dica_atual"]

  
  if not jogo['iniciado']:
    await ctx.send(
      f"O jogo começou, {jogador_da_vez.mention}! O bot escolheu uma palavra e dará a primeira dica."
    )
    jogo['iniciado'] = True  

 
  if dica_atual < len(dicas):
    await ctx.send(f"Dica {dica_atual + 1}: {dicas[dica_atual]}")
    await ctx.send(
      f"Tente adivinhar a palavra! Dicas restantes: {5 - dica_atual}")

    def check_resposta(message):
      return message.author == ctx.author  

    resposta = await bot.wait_for("message", check=check_resposta, timeout=30)

   
    if resposta.content.lower() == palavra_secreta:
      await ctx.send(
        f"Parabéns {ctx.author.mention}! Você acertou a palavra: {palavra_secreta}. Você venceu a rodada!"
      )
      del jogos_ativos[jogador_da_vez.id]
      await ctx.send(f"Digite `!jogar` para jogar novamente!")
    else:
      
      jogos_ativos[jogador_da_vez.id]['dica_atual'] += 1
      jogos_ativos[jogador_da_vez.id]['tentativas'] += 1
      await jogar_sozinho(ctx)  
  else:
    
    await ctx.send(
      f"Você esgotou todas as dicas! A palavra era {palavra_secreta}. Você perdeu a rodada!"
    )
    await cumprir_aprenda(ctx)



async def cumprir_aprenda(ctx):
  aprendas = [
    "Envia uma foto engraçada ou algo engraçado em imagem!",
    "Escreva uma mensagem divertida no chat, algo como 'Desafio aceito!'",
    "Envie um emoji muito engraçado!",
    "Compartilhe uma piada divertida com todos!",
    "Mande um áudio engraçado ou meme (se o Discord permitir)!",
  ]

  aprenda = random.choice(aprendas)
  await ctx.send(
    f"Você perdeu, {ctx.author.mention}! Agora, é hora de cumprir sua aprenda! {aprenda}"
  )

  
  del jogos_ativos[ctx.author.id]
  await ctx.send(f"Digite `!jogar` para jogar novamente!")



@bot.command()
async def cansar(ctx):
  if ctx.author.id not in jogos_ativos:
    await ctx.send(
      "Você não está em uma partida. Digite !jogar para começar uma.")
    return

  jogo = jogos_ativos[ctx.author.id]
  palavra_secreta = jogo['palavra']

  
  await ctx.send(f"Você desistiu! A palavra era: {palavra_secreta}")
  await cumprir_aprenda(ctx)

  
  del jogos_ativos[ctx.author.id]
  await ctx.send(f"Digite `!jogar` para jogar novamente!")



@bot.command()
@commands.has_permissions(manage_messages=True)
async def limparchat(ctx, quantidade: int):
  """Limpa uma quantidade específica de mensagens no canal."""
  if quantidade <= 0:
    await ctx.send(
      "Por favor, insira um número válido de mensagens a serem apagadas.")
    return


  deleted = await ctx.channel.purge(limit=quantidade)

  
  await ctx.send(f"{len(deleted)} mensagens foram apagadas!", delete_after=5)



bot.run(
  'TOKEN DO SEU BOT')
