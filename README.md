
# AutoStock - Gerenciamento de Peças e Modelos de Carros

## Como Rodar o Projeto

### Pré-requisitos

- **Docker** e **Docker Compose** instalados.
### Passos

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/autostock.git
   cd autostock

1. **Suba os contênieres:**
  Execute o seguinte comando para construir e iniciar os contêineres:
  
   ```bash
    docker-compose up --build

3. **Acesse a aplicação**:
	A aplicação estará disponível em:
	
    http://localhost:8000/swagger/

### Como Rodar os Testes
### Passos
1. **Execute os testes com Docker**:
	```bash
	 docker-compose exec app pytest
