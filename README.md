# ⏳ KronoSort

**KronoSort** é uma poderosa ferramenta de automação multiplataforma desenvolvida em Python para organizar exportações de mídia bagunçadas (como o Google Takeout) em uma estrutura de pastas limpa e cronológica.

## 🚀 Funcionalidades

- **Multiplataforma**: Funciona perfeitamente em Windows e Linux usando `pathlib`.
- **Detecção Inteligente de Data**:
  - **1ª Prioridade**: Metadados EXIF (`DateTimeOriginal`).
  - **2ª Prioridade**: Regex no nome do arquivo (Detecta `YYYYMMDD` ou `YYYY-MM-DD`).
  - **Fallback**: Move arquivos não identificados para uma pasta chamada `Outros`.
- **Gerenciamento Robusto de Arquivos**:
  - **Prevenção de Colisão**: Renomeia arquivos automaticamente com sufixos numéricos se já existir um arquivo com o mesmo nome no destino.
  - **Suporte a Formatos**: Processa `.jpg`, `.jpeg`, `.png`, `.heic`, `.mp4`, `.mov`.
  - **Suporte HEIC**: Integrado com `pi-heif` para formatos de foto modernos de iPhone.
- **Leitura Direta de ZIP**: Processa arquivos sem necessidade de extração manual prévia.
- **Fácil de Usar**: Acompanhamento de progresso em tempo real com `tqdm`.

## 🛠️ Instalação

Como as versões modernas do Linux (Debian/Ubuntu) protegem o ambiente do sistema, recomendamos o uso de um ambiente virtual (**venv**):

1. **Clone ou baixe** os arquivos para sua máquina.
2. **Crie o ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```
3. **Ative o ambiente**:
   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Uso

Execute o script e siga as instruções:

```bash
python kronosort.py
```

- **Caminho de Origem**: Pode ser um único arquivo `.zip` ou uma pasta contendo vários arquivos `.zip` do Google Takeout.
- **Caminho de Destino**: Onde você deseja que as pastas `Ano/Mês/` sejam criadas.

O script lerá os arquivos diretamente dos ZIPs sem precisar de extração manual prévia!

## 📂 Exemplo de Saída

```text
Destino/
├── 2023/
│   ├── 01/
│   │   └── photo_01.jpg
│   └── 12/
│       └── video_holiday.mp4
├── 2024/
│   └── 05/
│       └── image_1.png
└── Outros/
    └── unknown_file.heic
```

## ⚖️ Licença
MIT License - Sinta-se à vontade para usar e modificar!

---
Desenvolvido com ❤️ para facilitar a organização de memórias digitais.
