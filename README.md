# Normalize Audio - Projeto

Descrição
--------
Este projeto fornece um utilitário simples para ajustar o volume de arquivos de áudio (MP3, WAV, etc.). Ele oferece:
- Normalização básica via `pydub` (maximiza o volume sem estourar picos quando possível).
- Aumento de ganho por decibéis (`--gain`) para forçar o áudio mais alto quando desejado.
- Normalização EBU R128 via `ffmpeg` `loudnorm` (`--loudness`) para resultados consistentes em LUFS.
- Processamento em lote de pastas inteiras com `--input-dir` e saída por arquivo com sufixo `_normalized.mp3`.

Use este repositório quando precisar preparar muitos arquivos de áudio para reprodução/streaming ou simplesmente aumentar o volume de faixas individuais.

Instruções rápidas para instalar dependências e executar o script `normalize.py` no Windows.

**Requisitos**
- Python 3.8+ (recomendo 3.11+)
- FFmpeg (binários no PATH)
- `pydub` (listado em `requirements.txt`)

**1) Instalar Python (Windows)**
- Baixe o instalador: https://www.python.org/downloads/windows/
- Execute o instalador e marque **Add Python to PATH**, clique em *Install Now*.

Verifique:
```powershell
python --version
pip --version
```

**2) Criar e ativar ambiente virtual (na pasta do projeto)**
```powershell
cd E:\projeto_som
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
# Se usar cmd.exe:
# .venv\Scripts\activate.bat
```

**3) Instalar dependências**
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` contém:

- `pydub`

**4) Instalar FFmpeg e adicionar ao PATH (Windows)**
- Baixe uma build estática (ex.: https://www.gyan.dev/ffmpeg/builds/).
- Extraia, por exemplo, em `C:\ffmpeg` de modo que exista `C:\ffmpeg\bin\ffmpeg.exe`.
- Adicione `C:\ffmpeg\bin` ao PATH do usuário (PowerShell):
```powershell
[Environment]::SetEnvironmentVariable('Path', $env:Path + ';C:\ffmpeg\bin', 'User')
# Depois feche e reabra o terminal
```

Verifique:
```powershell
ffmpeg -version
```

**5) Executar o script `normalize.py`**
Com o ambiente virtual ativado:
```powershell
python normalize.py -i "C:\Users\nando\OneDrive\Documents\sons-C3po\novo\[C-3PO]Camil......ando_.mp3" -o "E:\projeto_som\C3PO_Camil_ACDC_Melhorado.mp3"
```

Opções úteis:
- `--gain N` — aplicar ganho em dB em vez de normalizar.
- `--normalize` — forçar normalização (padrão se `--gain` não for usado).

Exemplo — converter todos os arquivos de uma pasta
-----------------------------------------------
Converter todos os MP3s de uma pasta e salvar em outra pasta, aplicando EBU R128 (-14 LUFS):
```powershell
python normalize.py --input-dir "C:\Users\nando\OneDrive\Documents\sons-C3po\novo" -o "D:\c3po\sons" --exts mp3 --loudness -14
```
Aplicar ganho fixo (+6 dB) em lote:
```powershell
python normalize.py --input-dir "C:\Users\nando\OneDrive\Documents\sons-C3po\novo" -o "D:\c3po\sons" --exts mp3 --gain 6
```


Se o `pydub` não localizar o `ffmpeg`, defina explicitamente no script (ex.: no topo de `normalize.py`):
```python
from pydub import AudioSegment
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
```

**Dúvidas / próximos passos**
- Posso rodar o script aqui se você confirmar que o Python/ffmpeg estão instalados no seu ambiente VS Code/terminal.
- Quer que eu adicione exemplos adicionais ou opções de processamento ao `normalize.py`?
