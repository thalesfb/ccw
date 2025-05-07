## Detalhamento das APIs Utilizadas na Revisão Sistemática

Este documento serve como um guia rápido para as APIs usadas na coleta de dados para a revisão sistemática, detalhando endpoints, parâmetros, autenticação, campos relevantes e estratégias de uso.

### 1. Semantic Scholar API

- **Descrição**: API que fornece acesso a um vasto corpus de artigos científicos com foco em ciência da computação e áreas relacionadas. Ideal para encontrar artigos relevantes e suas conexões.
- **Vantagens**: Oferece pontuações de influência (não usadas neste projeto), referências estruturadas e acesso a textos completos quando disponíveis (`isOpenAccess`, `url`). **Nota:** Geralmente fornece *links* (`url`) para a página do artigo, onde o texto completo pode ser encontrado (especialmente se `isOpenAccess` for true), não o texto diretamente na resposta.
- **Autenticação**: Opcional via API Key (`x-api-key` no header). Sem chave, o limite de taxa é mais restrito (100 requisições por 5 minutos).
- **Endpoint principal**: `https://api.semanticscholar.org/graph/v1/paper/search` (Método GET)

- **Parâmetros essenciais**:
  - `query`: Termos de busca (ex: `"mathematics education" AND "machine learning"`). Suporta operadores booleanos.
  - `limit`: Número máximo de resultados por chamada (máx. 100).
  - `offset`: Posição inicial para paginação (usado com `limit`).
  - `fields`: Campos a serem retornados. Essenciais para o projeto: `paperId`, `title`, `authors.name`, `year`, `venue` (publicação), `url` (link), `abstract`, `isOpenAccess`.

- **Exemplo de chamada (Python `requests`)**:

```python
headers = {"User-Agent": "YourApp/1.0"} # Obrigatório
# if api_key: headers["x-api-key"] = api_key
params = {
    "query": '"mathematics education" AND "machine learning"',
    "limit": 50,
    "offset": 0, # Para a primeira página
    "fields": "paperId,title,authors.name,year,venue,url,abstract,isOpenAccess"
}
response = session.get("https://api.semanticscholar.org/graph/v1/paper/search", headers=headers, params=params)
```

- **Mapeamento para `Paper` (`_item_to_paper`)**:
  - `paperId` -> `paper_id` (prefixado com `s2:`)
  - `title` -> `title`
  - `authors` (lista de dicts) -> `authors` (string concatenada)
  - `year` -> `year`
  - `venue` -> `source_publication`
  - `abstract` -> `abstract`
  - `url` -> `doi_url` (usado como URL principal)
  - `isOpenAccess` -> `is_open_access`
  - `tldr`: (Se disponível) Resumo curto gerado pela API, pode indicar técnicas/tópicos chave. Útil para `comp_techniques`, `math_topic`, `main_results`.
  - `fieldsOfStudy`: Lista de campos detectados, pode ajudar a confirmar relevância ou `math_topic`.
  - `country`: Código do país da publicação, se disponível.
  - `study_type`: Tipo de estudo, conforme a estrutura de dados do Semantic Scholar.

- **Filtros Aplicados**:
  - **API**: Apenas `query`. Filtros de ano/idioma não são diretamente suportados na busca.
  - **Pós-processamento (`is_relevant_paper`)**: Ano (`>= year_min`), idioma (heurística no texto), palavras-chave no título/resumo.
  - **Enriquecimento (`enrich_paper_data`)**: Inferência de `comp_techniques`, `math_topic` a partir de `title`, `abstract`, `tldr`, `fieldsOfStudy`.

- **Paginação**: Via `limit` e `offset`. O código atual busca um lote maior (`limit * 2`) e filtra depois, sem paginação explícita.

- **Rate Limiting e Erros**:
  - Limite: ~100 requisições / 5 minutos (sem chave).
  - Erros comuns: `429 Too Many Requests`.
  - Estratégia: Delay fixo (`rate_delay`) e retry com backoff exponencial via `requests.Session`.

- **Documentação**: [Semantic Scholar API Docs](https://api.semanticscholar.org/corpus/) para detalhes adicionais sobre filtros e parâmetros.

### 2. OpenAlex API

- **Descrição**: Base de dados aberta que sucede o Microsoft Academic Graph, oferecendo metadados abrangentes de publicações científicas, autores, instituições, etc.
- **Vantagens**: Dados abertos (CC0), boa cobertura de citações, informações sobre instituições e conceitos. Usa um índice invertido para resumos (`abstract_inverted_index`). **Nota:** Fornece `doi` e status `open_access` para ajudar a localizar o texto completo externamente, mas não o retorna diretamente.
- **Autenticação**: Nenhuma chave necessária, mas recomenda-se fornecer um email no `User-Agent` (formato `mailto:your.email@example.com`) para usar o "polite pool" com limites de taxa mais altos.
- **Endpoint principal**: `https://api.openalex.org/works` (Método GET)

- **Parâmetros essenciais**:
  - `search`: Termos de busca (palavras-chave no título, resumo, etc.). Não suporta operadores booleanos complexos diretamente como Semantic Scholar.
  - `filter`: Filtros poderosos por campos (ex: `publication_year:>2014`, `language:en`, `has_abstract:true`, `concepts.id:C12345`). Múltiplos filtros separados por vírgula.
  - `per-page`: Resultados por página (máx. 200).
  - `page`: Número da página para paginação.
  - `select`: Para especificar quais campos retornar (otimiza a resposta).

- **Exemplo de chamada (Python `requests`)**:

```python
headers = {"User-Agent": "YourApp/1.0 (mailto:your.email@example.com)"}
params = {
    "search": "mathematics education machine learning", # Termos simples
    "filter": f"publication_year:>{year_min-1},language:en|pt", # Filtro de ano e idioma (OR)
    "per-page": 50,
    "page": 1,
    "select": "id,doi,title,publication_year,authorships,host_venue,abstract_inverted_index,open_access" # Campos selecionados
}
response = session.get("https://api.openalex.org/works", headers=headers, params=params)
```

- **Mapeamento para `Paper` (`_item_to_paper`)**:
  - `title` -> `title`
  - `authorships` (lista de dicts) -> `authors` (extrai `author.display_name`)
  - `publication_year` -> `year`
  - `host_venue.display_name` -> `source_publication`
  - `abstract_inverted_index` -> `abstract` (requer reconstrução)
  - `doi` (URL completo) -> `doi_url`
  - `open_access.is_oa` -> `is_open_access`

- **Campos Relevantes Adicionais**:
  - `concepts`: Lista de conceitos associados (ex: { "id": "C123", "wikidata": "Q...", "display_name": "Machine learning", "level": 1, "score": 0.8 }). **Muito útil** para `comp_techniques`, `math_topic`. Filtrar por `level` e `score` pode ser necessário.
  - `topics`: Tópicos associados, similar a `concepts`. **Útil** para `comp_techniques`, `math_topic`.
  - `keywords`: Palavras-chave fornecidas pelo autor. **Útil** para `comp_techniques`, `math_topic`.
  - `grants`: Informações de financiamento (menos direto).
  - `referenced_works`, `related_works`: Para exploração adicional (snowballing).

- **Filtros Aplicados**:
  - **API**: Ano (`publication_year`), Idioma (`language`), `search` para termos. Pode-se filtrar por `concepts.id` também.
  - **Pós-processamento (`is_relevant_paper`)**: Palavras-chave específicas no título/resumo reconstruído.
  - **Enriquecimento (`enrich_paper_data`)**: Inferência de `comp_techniques`, `math_topic` a partir de `title`, `abstract`, `concepts`, `topics`, `keywords`.

- **Paginação**: Via `page` e `per-page`. O código implementa a busca página por página até `max_results`.

- **Rate Limiting e Erros**:
  - Limite: ~10 requisições/segundo (polite pool).
  - Erros comuns: `429 Too Many Requests`.
  - Estratégia: Delay (`rate_delay`) e retry com backoff exponencial via `requests.Session`.

- **Documentação**: [OpenAlex API Docs](https://docs.openalex.org) para detalhes adicionais sobre filtros e parâmetros.

### 3. Crossref API (via `crossref.restful`)

- **Descrição**: Foco em metadados de publicações e DOIs, especialmente forte para artigos de periódicos. Usado via biblioteca `crossref.restful`.
- **Vantagens**: Padrão para DOIs, metadados geralmente precisos para publicações formais. A biblioteca simplifica as chamadas.
- **Autenticação**: Nenhuma chave necessária com `crossref.restful`, mas pode ser configurado com `mailto` para o pool educado (feito implicitamente pela biblioteca ou configurável).
- **Endpoint principal**: Abstraído pela biblioteca. Chamadas como `Works().query(...)`.

- **Parâmetros essenciais (via métodos da biblioteca)**:
  - `query(bibliographic=...)`: Busca por termos no título, autor, etc. (geralmente preferível a `query=`).
  - `filter(...)`: Filtros por campos (ex: `from_pub_date='YYYY-MM-DD'`, `type='journal-article'`).
  - `sort(...)`: Ordenação (ex: `'relevance'`, `'published'`).
  - `order(...)`: Direção da ordenação (`'asc'`, `'desc'`).
  - `sample(...)`: Retorna um gerador com um número amostrado de resultados (útil para limitar).

- **Exemplo de chamada (Python `crossref.restful`)**:

```python
from crossref.restful import Works

works = Works() # Instância global ou local

# Exemplo de busca
results_generator = works.query(bibliographic='mathematics education machine learning')\
                       .filter(from_pub_date='2015-01-01')\
                       .sort('relevance').order('desc')\
                       .sample(100) # Pega até 100 resultados

for item in results_generator:
    # Processar item (dicionário)
    print(item.get('title'))
```

- **Mapeamento para `Paper` (`_item_to_paper`)**:
  - `title` (lista) -> `title` (primeiro elemento)
  - `author` (lista de dicts) -> `authors` (string concatenada com nomes)
  - `published-print` ou `published-online` (dict com `date-parts`) -> `year`
  - `container-title` (lista) -> `source_publication` (primeiro elemento)
  - `abstract` -> `abstract` (pode conter XML, requer limpeza)
  - `DOI` -> `doi_url` (prefixado com `https://doi.org/`)
  - `URL` -> `doi_url` (se DOI não estiver presente)
  - `is_oa` (booleano) ou `license` (lista) -> `is_open_access`

- **Filtros Aplicados**:
  - **API (via `filter`)**: `from_pub_date`.
  - **Pós-processamento (`is_relevant_paper`)**: Ano (`>= year_min`), idioma (heurística), palavras-chave.

- **Paginação**: A biblioteca `crossref.restful` lida com a paginação ao iterar sobre o gerador retornado por `query()` ou `sample()`.

- **Rate Limiting e Erros**:
  - A biblioteca respeita os limites do Crossref (pool educado se `mailto` configurado).
  - Erros (`requests.exceptions.RequestException`) são capturados no wrapper `BaseSearcher`.
  - Estratégia: Delay (`rate_delay`) e retry com backoff no `BaseSearcher`.

- **Documentação**: [crossref.restful Docs](https://github.com/fabiobatalha/crossrefapi) (GitHub) e [Crossref REST API Docs](https://api.crossref.org/swagger-ui/index.html).

### 4. CORE API

- **Descrição**: Agregador de artigos de pesquisa de acesso aberto de repositórios institucionais e periódicos.
- **Vantagens**: Foco em acesso aberto, frequentemente fornece links diretos para PDFs (`downloadUrl`) e texto completo extraído (`fullText`) diretamente na resposta da API.
- **Autenticação**: Requer API Key (`apiKey` como parâmetro na URL ou no header `Authorization: Bearer YOUR_KEY`).
- **Endpoint principal**: `https://api.core.ac.uk/v3/search/works` (Método POST com corpo JSON)

- **Corpo da Requisição (JSON)**:
  - `q`: Query string (suporta sintaxe Lucene, ex: `title:("machine learning") AND yearPublished:>2015 AND language.code:en`).
  - `page` / `pageSize`: Para paginação (alternativa: `scrollId` para buscas profundas).
  - `limit` / `offset`: Alternativa para paginação simples.
  - `fields`: Especificar campos a retornar (ex: `id`, `title`, `authors`, `yearPublished`, `abstract`, `doi`, `downloadUrl`, `language`, `documentType`).
  - `scroll`: `true` para usar `scrollId` para paginação eficiente.

- **Exemplo de chamada (Python `requests`)**:

```python
# POST request
api_key = "YOUR_CORE_API_KEY"
url = f"https://api.core.ac.uk/v3/search/works?apiKey={api_key}"
# Ou usar header: headers = {"Authorization": f"Bearer {api_key}"}
payload = {
    "q": f'("mathematics education" OR "math learning") AND ("machine learning" OR "adaptive learning") AND yearPublished:>={year_min} AND language.code:(en OR pt)',
    "page": 1,
    "pageSize": 50,
    "fields": ["id", "title", "authors", "yearPublished", "publisher", "abstract", "fullText", "doi", "downloadUrl", "documentType", "language"]
}
response = session.post(url, json=payload) # Note: POST
```

- **Mapeamento para `Paper` (`_item_to_paper`)**:
  - `title` -> `title`
  - `authors` (lista de dicts) -> `authors` (extrai `name`)
  - `yearPublished` -> `year`
  - `publisher` -> `source_publication`
  - `abstract` -> `abstract`
  - `fullText` -> `full_text` (texto completo extraído pela CORE, se disponível)
  - `doi` ou `downloadUrl` -> `doi_url` (prioriza DOI, usa downloadUrl como fallback)
  - `documentType` -> `study_type`
  - `language.name` -> Verificado no filtro, não armazenado diretamente.
  - `is_open_access` -> Definido como `True` (CORE foca em OA).

- **Campos Relevantes Adicionais**:
  - `topics`: Tópicos associados pela CORE. **Útil** para `comp_techniques`, `math_topic`.
  - `subjects`: Assuntos associados. **Útil** para `math_topic`.
  - `relations`: Links para outras versões ou recursos.

- **Filtros Aplicados**:
  - **API**: Query (`q` ou `query` na v3) com ano, idioma e termos. A v3 permite filtros mais estruturados (`filter`).
  - **Pós-processamento (`is_relevant_paper`)**: Verificação adicional de palavras-chave.
  - **Enriquecimento (`enrich_paper_data`)**: Inferência de `comp_techniques`, `math_topic` a partir de `title`, `abstract`, `fullText` (se disponível), `topics`, `subjects`.

- **Paginação**: Via `page` e `pageSize` (usado no código com `pageToken` na v3). A API v3 usa `pageToken` retornado na resposta para buscar a próxima página.

- **Rate Limiting e Erros**:
  - Limite: Varia, mas geralmente mais restrito. A chave API é essencial.
  - Erros comuns: `429 Too Many Requests`, `5xx Server Error` (como visto nos logs).
  - Estratégia: Delay maior (`rate_delay`), retry robusto com backoff via `requests.Session` (aumentado para 5 tentativas no código).

---

**Observação Geral**: A função `is_relevant_paper` aplica filtros adicionais (ano, idioma, palavras-chave) após a coleta dos dados da API, garantindo que apenas os artigos mais relevantes sejam incluídos, mesmo que os filtros da API não sejam perfeitos ou totalmente abrangentes. A estratégia de cache (`load_from_cache`, `save_to_cache`) evita requisições repetidas para a mesma query.