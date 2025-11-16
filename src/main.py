#!/usr/bin/env python3
"""
AIBAD — AI‑Powered Behavioral Anomaly Detector
Main module with enhanced stability and error handling.
"""

import argparse
import logging
import sys
import time
import yaml
import os
from pathlib import Path
from signal import signal, SIGTERM, SIGINT

# Импорты компонентов (оставляем как в оригинале)
from src.sensor import APISensor, ProcessSensor
from src.analyzer import BehavioralAnalyzer, PromptAnalyzer
from src.engine import ResponseEngine



def load_config(config_path: str) -> dict:
    """Загружает и валидирует конфигурацию из YAML‑файла."""
    config_file = Path(config_path)
    if not config_file.exists():
        logging.error(f"Конфигурационный файл не найден: {config_path}")
        sys.exit(1)

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.error(f"Ошибка парсинга YAML: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Не удалось прочитать файл конфигурации: {e}")
        sys.exit(1)

    # Валидация обязательных полей
    required_keys = ['api_whitelist', 'models', 'anomaly_threshold', 'response_action', 'logging']
    for key in required_keys:
        if key not in config:
            logging.error(f"Отсутствует обязательный параметр в конфиге: {key}")
            sys.exit(1)

    return config



def setup_logging(config: dict, debug: bool = False):
    """Настраивает логирование с возможностью отладки."""
    log_level = config['logging']['level']
    if debug:
        log_level = 'DEBUG'

    logging.basicConfig(
        level=log_level,
        filename=config['logging']['file'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )



def check_model_paths(config: dict) -> bool:
    """Проверяет существование путей к ML‑моделям."""
    for model_name, model_path in config['models'].items():
        if not Path(model_path).exists():
            logging.error(f"Модель не найдена: {model_name} по пути {model_path}")
            return False
    return True



def signal_handler(signum, frame):
    """Обрабатывает сигналы завершения (SIGTERM, SIGINT)."""
    logging.info(f"Получен сигнал {signum}. Завершение работы...")
    sys.exit(0)



def main():
    # Обработка аргументов командной строки
    parser = argparse.ArgumentParser(description="AIBAD — AI‑Powered Behavioral Anomaly Detector")
    parser.add_argument("--config", type=str, default="configs/default.yaml", help="Путь к конфигурационному файлу")
    parser.add_argument("--debug", action="store_true", help="Включить режим отладки (DEBUG логгинг)")
    args = parser.parse_args()

    # Настройка обработки сигналов
    signal(SIGTERM, signal_handler)
    signal(SIGINT, signal_handler)

    try:
        # Загрузка и валидация конфигурации
        config = load_config(args.config)
        setup_logging(config, debug=args.debug)

        # Проверка путей к моделям
        if not check_model_paths(config):
            sys.exit(1)

        logging.info("AIBAD запущен. Ожидание событий...")

        # Инициализация компонентов
        api_sensor = APISensor(whitelist=config['api_whitelist'])
        process_sensor = ProcessSensor()
        behavioral_analyzer = BehavioralAnalyzer(model_path=config['models']['behavioral'])
        prompt_analyzer = PromptAnalyzer(model_path=config['models']['prompt_analyzer'])
        response_engine = ResponseEngine(action=config['response_action'])

        running = True
        while running:
            try:
                # Сбор данных с таймаутами (пример для API‑сенсора)
                api_calls = api_sensor.capture(timeout=5)  # Таймаут 5 сек
                process_events = process_sensor.monitor(timeout=5)

                # Анализ поведения
                behavioral_score = behavioral_analyzer.analyze(process_events, timeout=10)
                if behavioral_score > config['anomaly_threshold']:
                    logging.warning(f!Аномальное поведение обнаружено: {behavioral_score:.2f}")
                    response_engine.trigger(api_calls, process_events)

                # Анализ промтов
                for call in api_calls:
                    if call['method'] == 'POST' and 'prompt' in call['body']:
                        prompt_score = prompt_analyzer.evaluate(call['body']['prompt'], timeout=10)
                        if prompt_score > config['anomaly_threshold']:
                            logging.warning(f!Подозрительный промт: {prompt_score:.2f}")
                            response_engine.trigger([call], [])

            except TimeoutError as e:
                logging.warning(f"Таймаут операции: {e}")
            except Exception as e:
                logging.error(f"Неожиданная ошибка в основном цикле: {e}")

            time.sleep(config.get('check_interval', 1))  # Дефолтный интервал 1 сек

    except KeyboardInterrupt:
        logging.info("Завершение по запросу пользователя (Ctrl+C)")
    except SystemExit:
        pass
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)



if __name__ == "__main__":
    main()

