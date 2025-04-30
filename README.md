# 📚 University Assignments — Blockchain Technologies

Этот репозиторий содержит задания, выполненные в рамках университетского курса **Blockchain Technologies**. В нём представлены проекты, связанные с разработкой блокчейна, смарт-контрактами, валидацией блоков, деревьями Меркла и другими ключевыми темами технологии распределённых реестров.

## 🗂️ Содержание

- `bl3.1/` — Создание *ERC20Token*, перевод с функциями allowance и проверка транзакций с условиями проверки.
- `bl3.2/` — Реализация блокчейн-системы с использованием структуры *Merkle Tree*.

## 🚀 Быстрый старт

```bash
git clone https://github.com/your-username/blockchain-technologies-assignments.git
cd blockchain-technologies-assignments
```

## 📥 Как скачать только одну директорию из репозитория

Если тебе нужно скачать только одну директорию (например, `assignment3`), выполни следующие шаги:

1. Установи [`git sparse-checkout`](https://git-scm.com/docs/git-sparse-checkout), если ещё не установлен.
2. Запусти следующие команды:

```bash
git clone --filter=blob:none --no-checkout hthttps://github.com/ValliKaz/Blockchain/tree/main
cd blockchain_3
git sparse-checkout init --cone
git sparse-checkout set bl3.1
git checkout main
```

Теперь у тебя будет только директория `bl3.1` локально.

## 📌 Требования

- Git
- Java / Python / Solidity (в зависимости от задания)
- Node.js (если есть фронтенд к смарт-контрактам)

## 🧑‍🎓 Автор

Alinur — студент курса **Blockchain Technologies**  
Факультет: Software Engineering  
Университет: **A**stana **IT** **U**niversity **AITU**

## 📄 Лицензия

Этот проект предназначен только для учебных целей. Не использовать для коммерческих целей без разрешения.
