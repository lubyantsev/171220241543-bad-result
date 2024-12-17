import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Создает график, отображающий цены закрытия, скользящие средние, RSI, MACD и стандартное отклонение.

    :param data: DataFrame с историческими данными акций.
    :param ticker: Тикер акции.
    :param period: Период для графика.
    :param filename: Имя файла для сохранения графика.
    :param style: Стиль графика.
    """
    # Применяем выбранный стиль
    plt.style.use(style)

    # Создаем папку 'charts', если она не существует
    if not os.path.exists('charts'):
        os.makedirs('charts')

    plt.figure(figsize=(14, 10))

    # График цен закрытия и скользящих средних
    plt.subplot(4, 1, 1)
    if 'Date' in data.columns:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Цена закрытия', color='blue')
        if 'Moving_Average' in data.columns:
            plt.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее', color='orange')

        # Добавление стандартного отклонения
        std_dev = np.std(data['Close'])
        mean_price = np.mean(data['Close'])
        plt.fill_between(data['Date'],
                         mean_price - std_dev,
                         mean_price + std_dev,
                         color='gray', alpha=0.2, label='Стандартное отклонение')

        plt.title(f'{ticker} - Цена закрытия и скользящее среднее за {period}')
        plt.xlabel("Дата")
    else:
        plt.plot(data['Close'], label='Цена закрытия', color='blue')
        if 'Moving_Average' in data.columns:
            plt.plot(data['Moving_Average'], label='Скользящее среднее', color='orange')

        plt.title(f'{ticker} - Цена закрытия и скользящее среднее за {period}')

    plt.ylabel("Цена")
    plt.legend()
    plt.grid()

    # График RSI
    plt.subplot(4, 1, 2)
    plt.plot(data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red', label='Перепроданность')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green', label='Перепроданность')
    plt.title('Индекс относительной силы (RSI)')
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()
    plt.grid()

    # График MACD
    plt.subplot(4, 1, 3)
    plt.plot(data['MACD'], label='MACD', color='blue')
    plt.plot(data['Signal_Line'], label='Сигнальная линия', color='orange')
    plt.title('MACD')
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()
    plt.grid()

    # Сохранение графика
    filename = filename or f"{ticker}_{period}.png"
    filepath = os.path.join('charts', filename)
    plt.tight_layout()  # Улучшаем компоновку графиков
    plt.savefig(filepath)
    plt.close()  # Закрываем фигуру после сохранения
    print(f"График сохранен как {filepath}")