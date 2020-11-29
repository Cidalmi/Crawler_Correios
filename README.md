# Crawler Correios

Este repositório contém a solução desenvolvida para coletar todas as faixas de CEP dos [Correios](http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm), retirando as duplicatas e gerando um id único. Ao obter esses dados será gerado um arquivo jsonl com a localidade, faixa de cep e id gerado.

# Inciando
Essa são instruções de como você pode configurar seu projeto localmente. Para obter uma cópia local instalada e funcionando, siga estas etapas a seguir.

## Requisitos

* Python 3.7
* Pip (ou outro instalador de pacotes)


O arquivo requirements.txt tem todas as bibliotecas em Python das quais são necessárias para executar o projeto e serão instaladas usando:

```
pip install -r requirements.txt
```
### Bibliotecas usadas
* Scrapy 2.4
* Bson 0.5.10

## Uso

Baixar o projeto na sua máquina:
* Branch main
  
    ```
    git clone https://github.com/Cidalmi/Crawler_Correios.git
    ```
* Branch dev
    
    ```
    git clone --branch dev https://github.com/Cidalmi/Crawler_Correios.git
    ```

### Executando o scrapy:
    cd Crawler_Correios
    scrapy crawl correios


# Descrição

A solução foi desenvolvida em Python 3.7 usando o framework Scrapy. Scrapy é uma estrutura de aplicativo para escrever web spiders que rastreiam sites e extraem dados deles [[Scrapy FAQ](https://docs.scrapy.org/en/latest/faq.html)].

O spider ``CorreiosSpider`` é responsável por percorrer todos os estados e seus municípios, rastreando todas as páginas geradas por estado, deste modo obteremos os dados necessários (localidade e faixa de cep). Este spider possuir as constantes UFS, URL e PAGE_LIMIT: ``UFS`` (todas as UFS a ser buscado), ``URL`` (a url única a ser verificada)  e ``PAGE_LIMIT`` (número máximo de itens que devem ser buscados por cada post).

Em uma próxima etapa, no pipeline no item denominado ``DuplicatesPipeline`` vamos receber os itens gerados e verificar se existe registros duplicados e caso exista, removê-los.

Seguindo no pipeline, temos o segunda class denominado `` JsonWriter`` recebe os objetos tratados pelo ``DuplicatesPipeline`` e os salva em arquivo jsonl na pasta output.
