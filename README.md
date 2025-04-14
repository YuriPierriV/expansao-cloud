# Estudo de Caso - Infraestrutura Cloud para Empresa X

## 📄 Sobre o Projeto
Este repositório documenta a solução proposta para o estudo de caso da migração parcial da infraestrutura de uma startup de e-commerce para a nuvem, aproveitando os recursos de escalabilidade, segurança e alta disponibilidade da AWS (Amazon Web Services).

---

## ⚙️ Infraestrutura Proposta

### VPC e Subredes
- **VPC:** CIDR Block 10.0.0.0/16
- **Subredes Públicas:**
  - 10.0.1.0/24 (Zona A)
  - 10.0.2.0/24 (Zona B)
- **Subredes Privadas:**
  - 10.0.3.0/24 (Zona A)
  - 10.0.4.0/24 (Zona B)

### Recursos de Rede
- **Internet Gateway** para acesso externo das subredes públicas
- **NAT Gateway** em subrede pública para acesso à internet pelas subredes privadas
- **Tabelas de Roteamento** separadas para subredes públicas e privadas

### Instâncias e Armazenamento
- **EC2:** Instâncias web em subredes públicas
- **EBS:** Armazenamento persistente acoplado às instâncias EC2
- **RDS:** Banco de dados relacional Multi-AZ em subredes privadas

### Grupos de Segurança
- Para EC2: HTTP, HTTPS e SSH (administradores)
- Para RDS: Acesso apenas das instâncias EC2

### AWS Lambda e S3
- Bucket S3: `pedido-novo`
- Função Lambda:
  - Disparada quando um novo arquivo JSON é carregado no bucket S3
  - Envia e-mail de confirmação de pedido usando Amazon SES

---

## 🔄 Integração da Solução

1. **Usuário realiza pedido via aplicação web** hospedada nas instâncias EC2.
2. **Detalhes do pedido são salvos no bucket S3** como um arquivo JSON.
3. **Trigger no S3 aciona uma função Lambda**, que processa o JSON e envia um e-mail de confirmação.
4. **Banco de dados RDS** armazena dados persistentes da aplicação.

---

## 📊 Arquitetura

O repositório também inclui:
- Diagrama completo da arquitetura AWS
- Capturas de tela do ambiente no console AWS
- Justificativas para cada decisão de projeto
- Código da função Lambda (Python 3.8)

---

## 📚 Como usar

Este repositório pode ser usado como modelo para:
- Projetos acadêmicos de computação em nuvem
- Implantação de arquiteturas cloud escaláveis
- Prova de conceito (PoC) com integração EC2 + S3 + Lambda + SES + RDS

