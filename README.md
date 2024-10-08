# Socrates News - Engine

> Automação do Jornal Sócrates

## Etapas da criação de uma matéria

1. Identificar matérias primárias
2. Clusterizar matérias
3. Extrair dados das matérias
4. Criar matéria para o Jornal Socrates, com título, preâmbulo, texto, imagem e fonte da imagem
5. Salvar matéria no banco de dados

## Estrutura de pastas

```
main.ipynb
|- src
  |- sections
  |- news_source
  |- jgc_news
  |- printer
  |- video
  |- utils
```

- `main.ipynb`: Código que precisa ser rodado diariamente para que todas as funcionalidades desenvolvidas no jornal sejam processadas corretamente
- `sections`: Responsável por identificar as matérias prmárias, que servirão como insumos para criar a matéria do Jornal Sócrates, clusterizá-las e rankear os clusters para priorizar quais matérias devem ser geradas primeiro
- `news_source`: Gerencia um conjunto de notícias primárias de um mesmo cluster, criando e salvando a notícia no Jornal Sócrates
- `jgc_news`: Com um arquivo para cada fonte de dados, é responsável por extrair os dados das notícias primárias do tipo escrita
- `printer`: Cria e disponibiliza a versão impressa do jornal
- `video`: Com um arquivo para cada fonte de dados, é responsável por extrair os dados das notícias primárias do tipo vídeo
- `utils`: Miscelânea de arquivos secundários

## Autores
