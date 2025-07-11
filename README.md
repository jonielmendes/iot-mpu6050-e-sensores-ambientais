# 🌡️ IoT com Sensores de Luminosidade, Temperatura, Umidade e Acelerômetro 🚀

Este repositório contém exemplos de uso dos seguintes sensores em placas microcontroladoras compatíveis com MicroPython (como Raspberry Pi Pico, ESP32, BitDogLab e similares):

💡 **Luminosidade**: BH1750  
🌡️ **Temperatura e Umidade**: DHT11/DHT22 (ou similar)  
🌀 **Acelerômetro/Giroscópio**: MPU6050  

Os resultados das leituras dos sensores aparecem no display da BitDogLab.

## Funcionalidades

- Leitura do sensor de luminosidade BH1750 via I2C
- Leitura de temperatura e umidade com sensores DHT
- Leitura de aceleração e giroscópio com MPU6050
- Exibição dos dados em display OLED SSD1306
- Exemplos para integração de sensores ambientais

## Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/jonielmendes/iot-mpu6050-e-sensores-ambientais.git
   ```

2. Transfira os arquivos para sua placa microcontroladora usando Thonny, ampy, rshell, etc

3. Conecte os componentes conforme o esquema do seu projeto
   - Sensor BH1750 conectado ao barramento I2C
   - Display OLED SSD1306 conectado ao barramento I2C
   - Sensor DHT em pino digital compatível
   - Sensor MPU6050 via I2C

## Dependências

- MicroPython
- Biblioteca `ssd1306` para display OLED
- Placa microcontroladora compatível (Raspberry Pi Pico, ESP32, BitDogLab, etc)

## Contribuição

Sinta-se livre para abrir issues ou pull requests para novas funcionalidades ou correções 😃

## Licença

Este projeto está licenciado sob a licença MIT
