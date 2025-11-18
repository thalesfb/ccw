## Remover arquivo grande do repositório

Este documento descreve opções seguras para remover `research/systematic_review.sqlite` do histórico Git (e evitar futuros commits).

Observações importantes:
- Faça um backup do repositório antes de reescrever o histórico.
- Reescrever o histórico exige `git push --force` e afetará colaboradores.

Opção A — Se o arquivo foi adicionado apenas no último commit local:
1. Remover do índice e fazer amend do commit:
```bash
git rm --cached research/systematic_review.sqlite
git commit --amend --no-edit
git push origin main
```

Opção B — Reescrever o histórico local (recomendado para commits múltiplos):
1. Instale `git-filter-repo` (recomendado):
```bash
# Linux / macOS
pip install git-filter-repo
```
2. Remover o arquivo do histórico:
```bash
git filter-repo --path research/systematic_review.sqlite --invert-paths
```
3. Limpar refs e empurrar força para o remoto:
```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force origin main
```

Opção C — Usando BFG (alternativa fácil):
1. Baixe o `bfg.jar` e rode:
```bash
java -jar bfg.jar --delete-files research/systematic_review.sqlite
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force origin main
```

Depois de reescrever o histórico, verifique `git log --all --stat` para confirmar que o arquivo foi removido.

Se você precisa manter esse arquivo no repositório (por motivos de histórico), considere usar Git LFS:
```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs install
git lfs track "*.sqlite"
git add .gitattributes
git add research/systematic_review.sqlite
git commit -m "Track sqlite in Git LFS"
git push origin main
```

Se precisar, posso aplicar estas mudanças e rodar o `git filter-repo`/BFG por você — confirme se quer que eu reescreva o histórico com força no remoto.

---
Arquivo alvo: `research/systematic_review.sqlite` ( ~104.6 MB )
*** End Patch