# Spaceship DNS IPv6 Updater

Script Python para atualizar automaticamente registros DNS IPv6 (AAAA) na plataforma Spaceship.

## Funcionalidades

- Obtém o hostname do servidor local
- Obtém o IPv6 público do servidor via https://api6.ipify.org
- Consulta os registros DNS atuais via API da Spaceship (GET)
- Compara o IPv6 atual com o IPv6 do registro DNS
- Atualiza ou cria o registro AAAA (hostname@domain) se necessário via API (PUT)
- Código modular dividido em funções específicas

## Pré-requisitos

- Python 3.6 ou superior (somente bibliotecas padrão)
- Acesso à internet (IPv6)
- Credenciais da API Spaceship

## Instalação

Clone o repositório do GitHub:

```bash
git clone https://github.com/maxwelfreitas/spaceship_updater.git
cd spaceship_updater
```

## Configuração

Configure as seguintes variáveis de ambiente:

- `SPACESHIP_DOMAIN`: Seu domínio (ex: example.com)
- `SPACESHIP_API_KEY`: Sua chave de API da Spaceship
- `SPACESHIP_SECRET`: Seu secret da API da Spaceship

### Opções de configuração:

**Opção 1: Arquivo .env.spaceship** (recomendado)

Crie um arquivo `.env.spaceship` no diretório do projeto:

```bash
SPACESHIP_DOMAIN=seudominio.com
SPACESHIP_API_KEY=sua_api_key
SPACESHIP_SECRET=seu_secret
```

O script carregará automaticamente essas variáveis ao ser executado.

**Opção 2: Variáveis de ambiente diretas**
```bash
export SPACESHIP_DOMAIN="seudominio.com"
export SPACESHIP_API_KEY="sua_api_key"
export SPACESHIP_SECRET="seu_secret"
```

## Uso

Execute o script:
```bash
python updater.py
```

Ou torne-o executável:
```bash
chmod +x updater.py
./updater.py
```

## Estrutura do Código

O programa está dividido nas seguintes funções:

- `load_dotenv()`: Carrega variáveis de ambiente do arquivo .env.spaceship
- `get_hostname()`: Obtém o hostname do servidor
- `get_public_ipv6()`: Obtém o IPv6 público do servidor
- `get_env_variables()`: Valida e retorna as variáveis de ambiente
- `get_dns_records()`: Consulta os registros DNS via API (GET)
- `find_aaaa_record()`: Localiza o registro IPv6 existente para o hostname
- `needs_update()`: Verifica se há necessidade de atualização
- `update_dns_record()`: Atualiza ou cria o registro DNS (PUT)
- `main()`: Orquestra todo o processo

## Agendamento (Opcional)

Para executar automaticamente, adicione ao crontab:

```bash
# Executar a cada hora
0 * * * * cd /caminho/para/spaceship_updater && /usr/bin/python3 updater.py >> /var/log/dns-updater.log 2>&1
```

## Exemplo de Saída

```
2025-12-04 10:00:00 Starting IPv6 DNS record update
2025-12-04 10:00:00 Domain: example.com
2025-12-04 10:00:00 Getting server hostname
2025-12-04 10:00:00 Server hostname: myserver
2025-12-04 10:00:00 Getting public IPv6 address
2025-12-04 10:00:00 Public IPv6 obtained: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
2025-12-04 10:00:00 Querying DNS records
2025-12-04 10:00:00 DNS records successfully obtained
2025-12-04 10:00:00 Checking AAAA record
2025-12-04 10:00:00 Existing AAAA record found: {'id': '123', 'type': 'AAAA', 'name': 'myserver', 'address': '2001:0db8:85a3:0000:0000:8a2e:0370:1234'}
2025-12-04 10:00:00 Checking if update is needed
2025-12-04 10:00:00 IPv6 changed from 2001:0db8:85a3:0000:0000:8a2e:0370:1234 to 2001:0db8:85a3:0000:0000:8a2e:0370:7334, will update
2025-12-04 10:00:00 Updating DNS record
2025-12-04 10:00:00 DNS record updated successfully!
2025-12-04 10:00:00 Process finished successfully!
```

## Tratamento de Erros

O script inclui tratamento de erros para:
- Falha na conexão com a API do IPv6
- Variáveis de ambiente faltando
- Erros na API da Spaceship
- Registros DNS inválidos

## Documentação da API

- [Spaceship DNS Records API](https://docs.spaceship.dev/#tag/DNS-records/operation/saveRecords)
- [IPv6 Detection Service](https://www.ipify.org/)

## Licença

Este é um script de uso livre.
