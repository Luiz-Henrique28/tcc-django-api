#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}   TCC: Script de Benchmark Automatizado      ${NC}"
echo -e "${BLUE}==============================================${NC}"

# Verifica se o ab está instalado
if ! command -v ab &> /dev/null; then
    echo -e "${RED}Erro: ApacheBench (ab) não está instalado.${NC}"
    echo "Instale usando: sudo apt install apache2-utils"
    exit 1
fi

URL_LARAVEL="http://127.0.0.1:8001/api/products"
URL_DJANGO="http://127.0.0.1:8002/api/products"
OUTPUT_DIR="benchmark_results"

mkdir -p $OUTPUT_DIR

# Pede ao usuário o nome do cenário atual
echo -e "Você está testando com ou sem PgBouncer?"
echo "1) Direto no Banco (Sem PgBouncer)"
echo "2) Com PgBouncer"
read -p "Escolha (1 ou 2): " MODE_CHOICE

if [ "$MODE_CHOICE" == "1" ]; then
    MODE_NAME="direto"
elif [ "$MODE_CHOICE" == "2" ]; then
    MODE_NAME="pgbouncer"
else
    echo -e "${RED}Escolha inválida.${NC}"
    exit 1
fi

# Função para extrair Requests per second
extract_rps() {
    grep "Requests per second:" $1 | awk '{print $4}'
}

# Função para extrair Time per request
extract_latency() {
    grep "Time per request:" $1 | grep "(mean)" | awk '{print $4}'
}

# Função para extrair Failed requests
extract_fails() {
    grep "Failed requests:" $1 | awk '{print $3}'
}

run_test() {
    local framework=$1
    local url=$2
    local scenario=$3
    local requests=$4
    local concurrency=$5
    local output_file="${OUTPUT_DIR}/${framework}_${scenario}_${MODE_NAME}.txt"
    
    echo -e "${YELLOW}>> Iniciando teste: ${framework} | Cenário: ${scenario} | Modo: ${MODE_NAME}${NC}"
    echo "   Requests: $requests | Concorrência: $concurrency"
    
    # Executa o ApacheBench
    ab -n $requests -c $concurrency -s 120 $url > $output_file 2>&1
    
    # Extrai resultados
    if grep -q "Complete requests:" "$output_file"; then
        RPS=$(extract_rps $output_file)
        LATENCY=$(extract_latency $output_file)
        FAILS=$(extract_fails $output_file)
        
        echo -e "${GREEN}   Sucesso! RPS: ${RPS} req/s | Latência Média: ${LATENCY} ms | Falhas: ${FAILS}${NC}"
        
        # Salva no CSV consolidado
        echo "${framework},${MODE_NAME},${scenario},${requests},${concurrency},${RPS},${LATENCY},${FAILS}" >> $CSV_FILE
    else
        echo -e "${RED}   Falha ao executar o teste. Verifique o arquivo $output_file${NC}"
    fi
    
    echo "   Aguardando 5 segundos para resfriamento do servidor..."
    sleep 5
}

CSV_FILE="${OUTPUT_DIR}/resultados_consolidados.csv"

# Se o CSV não existe, cria com cabeçalho
if [ ! -f $CSV_FILE ]; then
    echo "Framework,Modo,Cenario,Total_Requests,Concurrency,RPS,Latency_ms,Failed_Requests" > $CSV_FILE
fi

echo -e "\n${BLUE}--- Iniciando Cenário 1: Ocioso (100 reqs, 10 simultâneas) ---${NC}"
run_test "Laravel" $URL_LARAVEL "Ocioso" 100 10
run_test "Django" $URL_DJANGO "Ocioso" 100 10

echo -e "\n${BLUE}--- Iniciando Cenário 2: Moderado (1000 reqs, 100 simultâneas) ---${NC}"
run_test "Laravel" $URL_LARAVEL "Moderado" 1000 100
run_test "Django" $URL_DJANGO "Moderado" 1000 100

echo -e "\n${BLUE}--- Iniciando Cenário 3: Estresse (5000 reqs, 300 simultâneas) ---${NC}"
run_test "Laravel" $URL_LARAVEL "Estresse" 5000 300
run_test "Django" $URL_DJANGO "Estresse" 5000 300

echo -e "\n${GREEN}==============================================${NC}"
echo -e "${GREEN}Testes concluídos!${NC}"
echo -e "Os logs detalhados estão na pasta: ${OUTPUT_DIR}/"
echo -e "O consolidado em CSV está em: ${CSV_FILE}"
echo -e "==============================================\n"
