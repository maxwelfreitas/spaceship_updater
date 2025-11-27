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

### Instalação a partir do GitHub

Você pode clonar e instalar este projeto diretamente do GitHub:

```bash
git clone https://github.com/maxwelfreitas/spaceship-dns-ipv6-updater.git
cd spaceship-dns-ipv6-updater
cp .env.example .env.spaceship
# Edite o arquivo .env.spaceship com suas credenciais da Spaceship
```

Depois, siga as instruções de configuração e uso abaixo.

### Configuração

Configure as seguintes variáveis de ambiente:

- `SPACESHIP_DOMAIN`: Seu domínio (ex: example.com)
- `SPACESHIP_API_KEY`: Sua chave de API da Spaceship
- `SPACESHIP_SECRET`: Seu secret da API da Spaceship

### Opções de configuração:

**Opção 1: Arquivo .env.spaceship** (recomendado)
```bash
export $(cat .env.spaceship | xargs)
```

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

- `obter_hostname()`: Obtém o hostname do servidor
- `obter_ipv6_publico()`: Obtém o IPv6 público do servidor
- `obter_variaveis_ambiente()`: Valida e retorna as variáveis de ambiente
- `obter_registros_dns()`: Consulta os registros DNS via API (GET)
- `encontrar_registro_aaaa()`: Localiza o registro IPv6 existente para o hostname
- `precisa_atualizar()`: Verifica se há necessidade de atualização
- `atualizar_registro_dns()`: Atualiza ou cria o registro DNS (PUT)
- `main()`: Orquestra todo o processo

## Agendamento (Opcional)

Para executar automaticamente, adicione ao crontab:

```bash
# Executar a cada hora
0 * * * * cd /caminho/para/spaceship_updater && /usr/bin/python3 updater.py >> /var/log/dns-updater.log 2>&1
```

## Exemplo de Saída

```
============================================================
Iniciando atualização de registro DNS IPv6
============================================================

Domínio: example.com

--- Obtendo hostname do servidor ---
Hostname do servidor: myserver

--- Obtendo IPv6 público ---
IPv6 público obtido: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

--- Consultando registros DNS ---
Registros DNS obtidos com sucesso

--- Verificando registro AAAA ---
Registro AAAA existente encontrado: 2001:0db8:85a3:0000:0000:8a2e:0370:1234

--- Verificando necessidade de atualização ---
IPv6 mudou de 2001:0db8:85a3:0000:0000:8a2e:0370:1234 para 2001:0db8:85a3:0000:0000:8a2e:0370:7334, será atualizado

--- Atualizando registro DNS ---
Registro DNS atualizado com sucesso!

============================================================
Processo concluído com sucesso!
============================================================
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
