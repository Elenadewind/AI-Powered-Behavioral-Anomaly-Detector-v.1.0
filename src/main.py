Главный модуль AIBAD.
Запускает сенсоры, анализатор и механизм реагирования.
"""
import yaml
import logging
from src.sensor import APISensor, ProcessSensor
from src.analyzer import BehavioralAnalyzer, PromptAnalyzer
from src.engine import ResponseEngine

def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_logging(config: dict):
    logging.basicConfig(
        level=config['logging']['level'],
        filename=config['logging']['file'],
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    # Загрузка конфигурации
    config = load_config('configs/default.yaml')
    setup_logging(config)

    # Инициализация компонентов
    api_sensor = APISensor(whitelist=config['api_whitelist'])
    process_sensor = ProcessSensor()
    behavioral_analyzer = BehavioralAnalyzer(model_path=config['models']['behavioral'])
    prompt_analyzer = PromptAnalyzer(model_path=config['models']['prompt_analyzer'])
    response_engine = ResponseEngine(action=config['response_action'])

    logging.info("AIBAD запущен. Ожидание событий...")

    while True:
        # Сбор данных
        api_calls = api_sensor.capture()
        process_events = process_sensor.monitor()

        # Анализ поведения
        behavioral_score = behavioral_analyzer.analyze(process_events)
        if behavioral_score > config['anomaly_threshold']:
            logging.warning(f!Аномальное поведение обнаружено: {behavioral_score}")
            response_engine.trigger(api_calls, process_events)

        # Анализ промтов
        for call in api_calls:
            if call['method'] == 'POST' and 'prompt' in call['body']:
                prompt_score = prompt_analyzer.evaluate(call['body']['prompt'])
                if prompt_score > config['anomaly_threshold']:
                    logging.warning(f!Подозрительный промт: {prompt_score}")
                    response_engine.trigger([call], [])

        time.sleep(config['check_interval'])

if __name__ == "__main__":
    main()
