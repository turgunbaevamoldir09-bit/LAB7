import os
import sys
import matplotlib.pyplot as plt
import pandas as pd


def load_transactions(path: str):
    return pd.read_csv(path)


def load_types(path: str):
    return pd.read_csv(path)


def main(trans_path: str, types_path: str):
    # Загружаем данные
    transactions = load_transactions(trans_path)
    tr_types = load_types(types_path)

    # Проверяем наличие нужных колонок
    required_cols = ['tr_type']
    for col in required_cols:
        if col not in transactions.columns:
            print(f'В файле транзакций нет колонки "{col}". Выход.')
            return

    if 'tr_type' not in tr_types.columns or 'tr_description' not in tr_types.columns:
        print('В файле типов нет нужных колонок. Выход.')
        return

    # ---- 1. Выбираем 1000 случайных tr_type ----
    sample_types = transactions['tr_type'].sample(1000, random_state=42)

    # ---- 2. Делаем словарь tr_type → tr_description (без merge) ----
    type_dict = dict(zip(tr_types['tr_type'], tr_types['tr_description']))

    # Сопоставляем описания
    sample_desc = sample_types.map(type_dict)

    # ---- 3. Ищем долю POS / ATM ----
    mask = sample_desc.str.contains("POS|ATM", case=False, na=False)
    share = mask.mean()

    print(f'Доля транзакций с POS или ATM: {share:.4f}')

    # ---- 4. Сохраняем данные ----
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)

    out_csv = os.path.join(out_dir, "sample_descriptions.csv")
    sample_desc.to_csv(out_csv, index=False)
    print(f'Описания сохранены: {out_csv}')

    # ---- 5. Рисуем график (ваш стиль) ----
    # seaborn → если нет, fallback
    try:
        import seaborn as sns
        sns.set_theme(style='darkgrid')
    except Exception:
        available = plt.style.available
        fallback = 'ggplot' if 'ggplot' in available else (available[0] if available else 'classic')
        plt.style.use(fallback)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['POS/ATM', 'Другие'], [mask.sum(), 1000 - mask.sum()])

    ax.set_title('POS/ATM vs другие транзакции')
    ax.set_ylabel('Количество')

    plt.tight_layout()

    out_png = os.path.join(out_dir, "pos_atm_share.png")
    fig.savefig(out_png)
    print(f'График сохранён: {out_png}')


if __name__ == "__main__":
    trans_path = sys.argv[1] if len(sys.argv) > 1 else "transactions.csv"
    types_path = sys.argv[2] if len(sys.argv) > 2 else "tr_types.csv"
    main(trans_path, types_path)
