
O objetivo desse projeto é construir uma rede neural convolucional que consiga classificar corretamente o tipo de lesão no pulmão, se é benígno, malígno ou normal.


Dataset: https://www.kaggle.com/datasets/adityamahimkar/iqothnccd-lung-cancer-dataset

 O conjunto de dados contém um total de 1190 imagens representando cortes de tomografia computadorizada de 110 casos

 Esses casos são agrupados em três classes: normal, benigno e maligno. Destes, 40 casos são diagnosticados como malignos; 15 casos diagnosticados como benignos e 55 casos classificados como casos normais.

 Dataset:
    120 benignos
    561 malignos
    416 normais

1. Baixe o conjunto de dados do site da kaggle: https://www.kaggle.com/datasets/adityamahimkar/iqothnccd-lung-cancer-dataset

2. Dentro do diretório do projeto, crie uma pasta chamada data, e coloque lá as pastas dos casos benígnos, malígnos e normais.

3. Criação do ambiente virtual:

    py -3.11 -m venv env_pulmao

4. Ativando o ambiente virtual:

    env_pulmao\Scripts\activate

5. Instale as dependências:

    pip install -r requirements.txt