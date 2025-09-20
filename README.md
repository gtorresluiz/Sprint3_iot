# 📌 Projeto: Detector de Olhos Fechados com OpenCV + Node-RED

## 🎯 Objetivo

Este projeto tem como finalidade detectar automaticamente quando os olhos de uma pessoa permanecem fechados por mais de 2 segundos em um vídeo, utilizando apenas **Python + OpenCV**. Quando essa condição é atendida, o sistema envia uma **notificação por e-mail** via **Node-RED**.

---

## 🧰 Tecnologias Utilizadas

- Python 3.x
- OpenCV
- Haar Cascades
- Node-RED
- SMTP (Gmail)

---

## 📁 Estrutura do Projeto

  ###├── video.mp4 # Vídeo de entrada 
  ###├── detector.py # Script principal em Python 
  ###├── README.md


---

## 🚀 Como Executar

### 1. Instale as dependências:

  bash
  pip install opencv-python requests

### 2. Coloque o vídeo video.mp4 na raiz do projeto.

### 3. Execute o script:
  python detector.py

### 4. Inicie o Node-RED:
  node-red
  Acesse o editor em http://localhost:1880

---

## 🔗 Integração com Node-RED
O script Python envia uma requisição POST para o endpoint /both_eyes_closed quando os olhos permanecem fechados por mais de 2 segundos. O Node-RED recebe esse alerta e dispara um e-mail.

Fluxo básico no Node-RED:
  [HTTP IN] → [Function] → [Email] → [HTTP Response]

---

## 📦 Lógica de Detecção
  Utiliza haarcascade_frontalface_default.xml para detectar rostos.  
  
  Utiliza haarcascade_eye_tree_eyeglasses.xml para detectar olhos.
  
  Foca apenas na parte superior do rosto para evitar falsos positivos.
  
  Se nenhum olho for detectado por mais de 2 segundos, dispara o alerta.

---

## ⚖️ Considerações Éticas
Este projeto utiliza dados faciais para fins de detecção visual. É importante considerar:

Nenhum dado facial é armazenado ou compartilhado.

O vídeo utilizado deve ser de uso pessoal ou com consentimento explícito.

Este projeto não deve ser usado para vigilância sem consentimento.

Recomenda-se anonimizar ou desfocar rostos em vídeos públicos.

O uso responsável da tecnologia é essencial para preservar a privacidade e os direitos individuais.
