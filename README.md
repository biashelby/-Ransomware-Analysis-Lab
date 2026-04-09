#### ☕ Ransomware Analysis Lab — Estudo de Mecanismo e Resposta a Incidente

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/cryptography_(Fernet)-2C2C2A?style=for-the-badge)
![Tipo](https://img.shields.io/badge/Tipo-Análise_Defensiva-7F77DD?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-3B6D11?style=for-the-badge)

Análise técnica do mecanismo de funcionamento de um ransomware didático, desenvolvida em ambiente de laboratório controlado. O estudo decompõe cada etapa do ciclo de ataque — da geração de chave à criptografia de arquivos — com foco em **entender para defender**: identificar indicadores de comprometimento (IoCs), compreender a criptografia envolvida e desenvolver a ferramenta de recuperação.

> ⚠️ **Aviso ético:** Este repositório contém **apenas análise técnica e a ferramenta de recuperação (defensiva)**. Nenhum vetor de ataque é disponibilizado. O estudo foi conduzido exclusivamente em ambiente isolado para fins acadêmicos.

---

#### ☕ Como um Ransomware Funciona — Análise do Mecanismo

O ciclo de ataque de um ransomware baseado em criptografia simétrica segue quatro etapas principais:

```
[1] GERAÇÃO DE CHAVE
    └── Fernet.generate_key() → chave simétrica única (256-bit AES)
    └── Chave salva localmente (vetor de controle do atacante)
           │
           ▼
[2] ENUMERAÇÃO DE ARQUIVOS
    └── os.walk() percorre o sistema de arquivos recursivamente
    └── Seleciona alvos por extensão ou diretório
           │
           ▼
[3] CRIPTOGRAFIA EM LUGAR (in-place)
    └── Arquivo lido em binário → f.encrypt() → sobrescrito
    └── Conteúdo original destruído sem backup
           │
           ▼
[4] NOTA DE RESGATE
    └── Arquivo .txt criado com instruções
    └── Usuário perde acesso até apresentar a chave
```

---

#### ☕ Análise Técnica: Criptografia Utilizada

| Componente | Detalhe |
|---|---|
| Algoritmo | **AES-128 em modo CBC** (via biblioteca Fernet) |
| Padding | PKCS7 |
| Autenticação | HMAC-SHA256 — impede adulteração dos dados cifrados |
| Formato da chave | Base64url — 32 bytes aleatórios gerados via `os.urandom()` |
| Operação nos arquivos | **Sobrescrita in-place** — sem extensão adicionada, sem cópia |

O uso de **Fernet** garante criptografia autenticada: sem a chave original, a descriptografia é computacionalmente inviável. Isso é exatamente o que torna o ransomware eficaz — e o que torna o backup offline a principal medida preventiva.

---

#### ☕ Indicadores de Comprometimento (IoCs)

Sinais que um sistema de monitoramento (SIEM/IDS) deveria detectar durante um ataque desse tipo:

| Indicador | Descrição |
|---|---|
| Acesso massivo a arquivos em sequência | `os.walk()` gera leitura/escrita em cascata em milissegundos |
| Criação de arquivo `.key` no diretório raiz | Armazenamento local da chave — comportamento atípico |
| Criação de `LEIA_ISSO.txt` / `README_DECRYPT.txt` | Padrão clássico de nota de resgate |
| Processos Python com alto I/O em disco | Indicativo de script de criptografia em execução |
| Arquivos com entropia elevada | Arquivos criptografados têm entropia próxima de 8.0 bits/byte |

---

#### ☕ Ferramenta de Recuperação (Defensiva)

O arquivo `descriptografar.py` implementa o processo inverso: dado o arquivo de chave (`chave.key`), restaura os arquivos ao estado original.

```python
from cryptography.fernet import Fernet
import os

def carregar_chave():
    return open("chave.key", "rb").read()

def descriptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados_encriptados = file.read()
    dados_restaurados = f.decrypt(dados_encriptados)
    with open(arquivo, "wb") as file:
        file.write(dados_restaurados)
```

**Limitação importante:** a recuperação só é possível se a `chave.key` estiver disponível. Em ataques reais, o atacante exfiltra a chave antes de executar a criptografia — o arquivo local é removido, tornando a recuperação impossível sem pagar o resgate ou restaurar de backup.

---

#### ☕ Medidas de Prevenção e Resposta

| Camada | Medida |
|---|---|
| **Prevenção** | Backups offline regulares (regra 3-2-1) |
| **Prevenção** | Princípio do menor privilégio — limitar acesso de escrita |
| **Detecção** | Monitoramento de entropia de arquivos (SIEM) |
| **Detecção** | Alertas para criação massiva de arquivos modificados |
| **Resposta** | Isolamento imediato do host da rede |
| **Resposta** | Preservação forense da imagem do disco antes de qualquer ação |
| **Recuperação** | Restauração a partir de backup — nunca pagar o resgate |

---

#### ☕ Estrutura do Repositório

```
ransomware-analysis-lab/
├── descriptografar.py    # Ferramenta de recuperação (defensiva)
├── analise_tecnica.md    # Relatório detalhado do mecanismo
└── README.md
```

> 🔒 O vetor de ataque (`ataque.py`) **não é publicado** neste repositório — apenas analisado nesta documentação.

---

> ⚠️ **Aviso ético:** Este estudo foi realizado em ambiente de laboratório isolado, exclusivamente para fins acadêmicos. A compreensão do mecanismo de ataque é fundamental para construir defesas eficazes.
