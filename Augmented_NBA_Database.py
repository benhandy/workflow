{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/twoandhalfben/workflow/blob/main/Augmented_NBA_Database.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "1jLhUNBJrmyz"
      },
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "8NkUafOlzanM"
      },
      "outputs": [],
      "source": [
        "\n",
        "import sqlite3\n",
        "import pandas as pd\n",
        "import numpy as np"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "budIJEJJzjgp"
      },
      "outputs": [],
      "source": [
        "# creating in-memory database for prototyping\n",
        "conn = sqlite3.connect(':memory:')\n",
        "cursor = conn.cursor()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "jEu3CEXyzjsC"
      },
      "outputs": [],
      "source": [
        "# tabulating\n",
        "cursor.execute('''\n",
        "    CREATE TABLE IF NOT EXISTS nba_stats (\n",
        "        id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "        player_name TEXT NOT NULL,\n",
        "        team_name TEXT NOT NULL,\n",
        "        points INTEGER DEFAULT 0,\n",
        "        assists INTEGER DEFAULT 0,\n",
        "        rebounds INTEGER DEFAULT 0\n",
        "    )\n",
        "''')\n",
        "conn.commit()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "UIlfJNeBzjzB"
      },
      "outputs": [],
      "source": [
        "# adding some player data to my database\n",
        "sample_data_1 = [\n",
        "    (\"LeBron James\", \"Lakers\", 35, 8, 7),\n",
        "    (\"Stephen Curry\", \"Warriors\", 40, 10, 5),\n",
        "    (\"Kevin Durant\", \"Suns\", 25, 6, 9),\n",
        "    (\"Giannis Antetokounmpo\", \"Bucks\", 30, 5, 11),\n",
        "    (\"Jayson Tatum\", \"Celtics\", 34, 4, 8),\n",
        "    (\"Luka Doncic\", \"Mavericks\", 36, 9, 7),\n",
        "    (\"Nikola Jokic\", \"Nuggets\", 28, 8, 14),\n",
        "    (\"Ja Morant\", \"Grizzlies\", 32, 10, 6),\n",
        "    (\"Jimmy Butler\", \"Heat\", 27, 5, 7),\n",
        "    (\"Kawhi Leonard\", \"Clippers\", 26, 6, 5),\n",
        "    (\"Pat Connaughton\", \"Bucks\", 17, 5, 3)\n",
        "]\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "S_3uSm2Y3kMl"
      },
      "outputs": [],
      "source": [
        "sample_data_2 = [\n",
        "    (\"Anthony Davis\", \"Lakers\", 31, 3, 12),\n",
        "    (\"Damian Lillard\", \"Bucks\", 29, 8, 4),\n",
        "    (\"Devin Booker\", \"Suns\", 26, 5, 5),\n",
        "    (\"James Harden\", \"Clippers\", 20, 11, 4),\n",
        "    (\"Chris Paul\", \"Warriors\", 18, 12, 3),\n",
        "    (\"Kyrie Irving\", \"Mavericks\", 25, 7, 4),\n",
        "    (\"Joel Embiid\", \"76ers\", 33, 4, 10),\n",
        "    (\"Zion Williamson\", \"Pelicans\", 27, 3, 8),\n",
        "    (\"Trae Young\", \"Hawks\", 28, 10, 4),\n",
        "    (\"Paul George\", \"Clippers\", 24, 6, 6)\n",
        "]\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "X9XaWkH23kU_"
      },
      "outputs": [],
      "source": [
        "sample_data_3 = [\n",
        "    (\"Bradley Beal\", \"Suns\", 23, 5, 4),\n",
        "    (\"Jaylen Brown\", \"Celtics\", 26, 3, 6),\n",
        "    (\"DeMar DeRozan\", \"Bulls\", 24, 4, 5),\n",
        "    (\"Rudy Gobert\", \"Timberwolves\", 12, 2, 15),\n",
        "    (\"Karl-Anthony Towns\", \"Timberwolves\", 23, 3, 9),\n",
        "    (\"Shai Gilgeous-Alexander\", \"Thunder\", 31, 6, 4),\n",
        "    (\"Donovan Mitchell\", \"Cavaliers\", 28, 5, 4),\n",
        "    (\"Jamal Murray\", \"Nuggets\", 23, 6, 4),\n",
        "    (\"Draymond Green\", \"Warriors\", 8, 8, 8),\n",
        "    (\"Andrew Wiggins\", \"Warriors\", 17, 2, 5)\n",
        "]\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "KW93FSBV3kcZ"
      },
      "outputs": [],
      "source": [
        "# aggregating data batches\n",
        "all_data = sample_data_1 + sample_data_2 + sample_data_3\n",
        "\n",
        "cursor.executemany('''\n",
        "  INSERT INTO nba_stats (player_name, team_name, points, assists, rebounds)\n",
        "    VALUES (?, ?, ?, ?, ?)\n",
        "''', all_data)\n",
        "conn.commit()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "juRBwC1ozj5B",
        "outputId": "48167f52-abb9-4bce-f38a-1535dca26658"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "(1, 'LeBron James', 'Lakers', 35, 8, 7)\n",
            "(2, 'Stephen Curry', 'Warriors', 40, 10, 5)\n",
            "(3, 'Kevin Durant', 'Suns', 25, 6, 9)\n",
            "(4, 'Giannis Antetokounmpo', 'Bucks', 30, 5, 11)\n",
            "(5, 'Jayson Tatum', 'Celtics', 34, 4, 8)\n",
            "(6, 'Luka Doncic', 'Mavericks', 36, 9, 7)\n",
            "(7, 'Nikola Jokic', 'Nuggets', 28, 8, 14)\n",
            "(8, 'Ja Morant', 'Grizzlies', 32, 10, 6)\n",
            "(9, 'Jimmy Butler', 'Heat', 27, 5, 7)\n",
            "(10, 'Kawhi Leonard', 'Clippers', 26, 6, 5)\n",
            "(11, 'Pat Connaughton', 'Bucks', 17, 5, 3)\n",
            "(12, 'Anthony Davis', 'Lakers', 31, 3, 12)\n",
            "(13, 'Damian Lillard', 'Bucks', 29, 8, 4)\n",
            "(14, 'Devin Booker', 'Suns', 26, 5, 5)\n",
            "(15, 'James Harden', 'Clippers', 20, 11, 4)\n",
            "(16, 'Chris Paul', 'Warriors', 18, 12, 3)\n",
            "(17, 'Kyrie Irving', 'Mavericks', 25, 7, 4)\n",
            "(18, 'Joel Embiid', '76ers', 33, 4, 10)\n",
            "(19, 'Zion Williamson', 'Pelicans', 27, 3, 8)\n",
            "(20, 'Trae Young', 'Hawks', 28, 10, 4)\n",
            "(21, 'Paul George', 'Clippers', 24, 6, 6)\n",
            "(22, 'Bradley Beal', 'Suns', 23, 5, 4)\n",
            "(23, 'Jaylen Brown', 'Celtics', 26, 3, 6)\n",
            "(24, 'DeMar DeRozan', 'Bulls', 24, 4, 5)\n",
            "(25, 'Rudy Gobert', 'Timberwolves', 12, 2, 15)\n",
            "(26, 'Karl-Anthony Towns', 'Timberwolves', 23, 3, 9)\n",
            "(27, 'Shai Gilgeous-Alexander', 'Thunder', 31, 6, 4)\n",
            "(28, 'Donovan Mitchell', 'Cavaliers', 28, 5, 4)\n",
            "(29, 'Jamal Murray', 'Nuggets', 23, 6, 4)\n",
            "(30, 'Draymond Green', 'Warriors', 8, 8, 8)\n",
            "(31, 'Andrew Wiggins', 'Warriors', 17, 2, 5)\n"
          ]
        }
      ],
      "source": [
        "# using SQL to fetch all data\n",
        "cursor.execute(\"SELECT * FROM nba_stats\")\n",
        "rows = cursor.fetchall()\n",
        "\n",
        "# print\n",
        "for row in rows:\n",
        "    print(row)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "YfNP3vOTzj-j"
      },
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BWHJXXYc5CGg",
        "outputId": "9e60b731-d2c2-4370-c2ff-6ed23a12e16a"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "    id              player_name     team_name  points  assists  rebounds\n",
            "0    1             LeBron James        Lakers      35        8         7\n",
            "1    2            Stephen Curry      Warriors      40       10         5\n",
            "2    3             Kevin Durant          Suns      25        6         9\n",
            "3    4    Giannis Antetokounmpo         Bucks      30        5        11\n",
            "4    5             Jayson Tatum       Celtics      34        4         8\n",
            "5    6              Luka Doncic     Mavericks      36        9         7\n",
            "6    7             Nikola Jokic       Nuggets      28        8        14\n",
            "7    8                Ja Morant     Grizzlies      32       10         6\n",
            "8    9             Jimmy Butler          Heat      27        5         7\n",
            "9   10            Kawhi Leonard      Clippers      26        6         5\n",
            "10  11          Pat Connaughton         Bucks      17        5         3\n",
            "11  12            Anthony Davis        Lakers      31        3        12\n",
            "12  13           Damian Lillard         Bucks      29        8         4\n",
            "13  14             Devin Booker          Suns      26        5         5\n",
            "14  15             James Harden      Clippers      20       11         4\n",
            "15  16               Chris Paul      Warriors      18       12         3\n",
            "16  17             Kyrie Irving     Mavericks      25        7         4\n",
            "17  18              Joel Embiid         76ers      33        4        10\n",
            "18  19          Zion Williamson      Pelicans      27        3         8\n",
            "19  20               Trae Young         Hawks      28       10         4\n",
            "20  21              Paul George      Clippers      24        6         6\n",
            "21  22             Bradley Beal          Suns      23        5         4\n",
            "22  23             Jaylen Brown       Celtics      26        3         6\n",
            "23  24            DeMar DeRozan         Bulls      24        4         5\n",
            "24  25              Rudy Gobert  Timberwolves      12        2        15\n",
            "25  26       Karl-Anthony Towns  Timberwolves      23        3         9\n",
            "26  27  Shai Gilgeous-Alexander       Thunder      31        6         4\n",
            "27  28         Donovan Mitchell     Cavaliers      28        5         4\n",
            "28  29             Jamal Murray       Nuggets      23        6         4\n",
            "29  30           Draymond Green      Warriors       8        8         8\n",
            "30  31           Andrew Wiggins      Warriors      17        2         5\n"
          ]
        }
      ],
      "source": [
        "# using pandas to read the data\n",
        "df = pd.read_sql_query(\"SELECT * FROM nba_stats\", conn)\n",
        "print(df)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 607
        },
        "id": "7a94Fqul5CST",
        "outputId": "4a0e7f72-b58d-4f1a-91f6-dd582e09f7b3"
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1000x600 with 1 Axes>"
            ],
            "image/png": "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BwCAK90AgDjjm2++sfjx41vv3r3dlvfv398khRuVu2LFim4Dk2XPnt2aNWtma9assXv37kVJTTdv3jQfH59wyxMnTuysf1ChV7sfZHCyN954w9auXWtr1661hQsXWtu2be21116ziRMnum138eJFW7NmjbVt29ZZ1qpVK3O5XPbFF1/85+8pUqSI7d6929q3b29//vmnTZw40Zo3b24ZM2a0jz/+2Nlu7dq1dvXqVXvllVecf3uo0G7627dvt3PnztmLL77otk3jxo2tYMGC9vXXX4f7/S+88ILb40WLFlnKlCmtbt26zpX+CxcuWOnSpS158uS2fv16t+1z5cpl9evXd1uWKlUqMzNbvny5BQcH/2cbAADiNkI3ACDO+OuvvyxLlizm6+vrtjx0NPO//vrLbXlEI4fnz5/fbty4YefPn4+SmpIkSRLhfdu3bt1y1j+olClTWp8+fWzFihW2a9euf922WLFiVqdOHatTp461bt3aPv/8c2vSpIm98sorbv+2hQsX2p07d6xkyZJ25MgRO3LkiF26dMnKly//wF3M8+fPb5999plduHDB9u7da++++64lSJDAevToYd99952Zhdz7bWZWtGjRSF8n9O9ToECBcOsKFiwY7u+XIEECy5Ytm9uyw4cPW0BAgGXIkMHSp0/v9nPt2rVwg7vlypUr3O96+umnrXLlytatWzfLmDGjtWnTxr744gsCOAAgQoxeDgCAF2XOnDnCKcVCl2XJkuWhXu/ll1+28ePH2/Dhw23ChAkP9dzatWvbypUrbevWrda4cWMzMydYV65cOcLn/PHHH5Y7d+4Hev348eNbsWLFrFixYlaxYkWrWbOmzZ071+rUqfNQdT4oHx+fcPfKBwcHW4YMGSI9YZA+fXq3xxGd9EiSJIn98MMPtn79evv6669t9erVtnDhQqtVq5Z9++23Fj9+/Kj7RwAAYjxCNwAgzsiRI4d99913dvXqVber3b///ruzPqzDhw+He41Dhw5Z0qRJw4WzR1WiRAn78ccfLTg42C0gbtmyxZImTWr58+d/qNcLvdr95ptvRjgo2r+5e/eumZldu3bNzMyOHTtmv/zyi/Xq1cuqV6/utm1wcLA9++yzNm/ePBs6dOhD/R4zszJlypjZPycX8uTJY2Zm+/fvt7x580b4nNC/z8GDB61WrVpu6w4ePBjhCOn3y5Mn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mjVrZjly5LC0adPa559/bpkzZ7Z3333XZsyYYUFBQV6qNgoJeEyCg4Od/x86dKjKlSunX3/9VYcOHVLHjh1Vrlw55c6dW5988okKFSqkZs2aea/YaObevXtuj3/88Udt27ZNd+/elSQ99dRTqlixorZv3+623Ysvvqhnn31WN2/efGy1xmRh23nt2rX67LPPtGzZMt24cUMBAQH66quvtHHjRrf3crly5TRt2jRvlBvjDB48WIkSJZK/v79cLpdGjBjhvIclKTAwUK+88opcLpfWrVvnxUqjh507d2rgwIG6ffu22/JvvvlG+fPndz7voe/bkydPKnPmzPLz89Po0aMfe70xwaBBg5QiRQrlz59fSZIk0auvvqpDhw5Jko4eParcuXPLz89PJUqUUIECBcK1PR7d/d9jH3/8sV599VUFBAToxo0bGjlypMqXL6/Jkyc7f5Nff/1VlSpV0l9//eWNkhGBAQMGKFeuXKpbt66aNGkil8ulVatWSZK2bt2qfPnyqXXr1vrxxx+9XGn0df9nIdTPP/+sYsWK6Z133tGZM2ec5bt371bhwoW1d+/ex1WiR4UeQ23YsEEHDhzQokWLlDt3bh0/flySFBQUJEn6+++/lSpVKhUoUECTJ0/2Wr1RhdCNx27r1q1q2rSpfv75Z2dZUFCQAgMD1b9/f7Vp00Zp06aVy+XSwoULvVhp9HP37l0FBwcrX758yp07t3bs2CFJWrVqlerVq6fSpUtr8eLFWrZsmfr27atUqVLFmp304zRo0CBly5ZN1atXV8GCBVWlShXnoEKSrl+/rr///lsNGjRQyZIl3YIjIrZjxw5VrFhRmzdv1q+//qq33npL8eLF0/Tp0922u3LliqZMmaI7d+54qdLoJfTgZNq0afr2228lSVevXlW+fPlUv359nT592tl2//79atGihaZNmxbpQV1cE/YE2ebNm1WzZk398ssvCg4O1qRJk5Q/f369/PLLOnjwoCTpxo0bevPNNzVu3DjnPch7MWrc/57s3r27/P39NWrUKF29elVSyL5VCvm7BQUFqWHDhqpXr57b3xHeM2/ePGXKlMk54bds2bJwx2qbN2+Wr6+vXnvtNW+VGa2F/RzMnz9fkyZN0ocffqgLFy5Ikt5++20VKlRI/fv3188//6wDBw6ofv36qlq1aqzar3///fdyuVz69ttvdfLk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M88848XqPC8gIEDVqlVT7ty5nQFAb9++rV69eil58uQRHnPBHaEbbgYMGKD06dMrderUypUrl6ZOnarLly9LImQ/iK+++kp16tRR1apVne7i938hVq1aVV26dPFGeTHWg7z37g/eLVu21Pbt2z1dWqwW9r07depUZcuWTWPHjvViRdHLzZs3tXjxYhUoUEBPPPGEJKlt27YqWrSoc+X2/vfuL7/8wsmf/3f79m29/PLL8vPzU/78+VW1alU1bdpUTz31lI4ePaqRI0e6jUo+ZswY5c6d27knFZ7z4YcfKmnSpP85yF/orBwSgdvbvvjiCy1dulR///23ZsyYoapVq+rq1avhtvvpp5/0448/huuNB3cTJkxweguECr3inSZNGjVv3txZfuDAgThxAjo0eOfJk0e7du3Syy+/rCRJkjAe0QMidMdxYQ8Iv//+e5UtW1YbN27UmTNn1L17dxUtWlRjx47VpUuXwm2Pf4Rtl9ABpqpWrRruivexY8dUs2ZNZ0oV2vO/hf0iu3fvXrjeAxFtu337duXKlUsdOnR4PEXGYmHbf+nSpQTG+wQFBWnZsmXKkyePUqRIoWLFijlzx4d9j/bu3Vtnz551HtOOIc6fP6/+/furefPmeu6557Rz507Vq1dPzZs3V8mSJeVyudy6bX7++ee0XRSLqCfb6dOnVbt2bb333nuS4naPlpjg8OHDypo1qwoUKKAsWbIof/78crlcatOmjSZOnKj169drz549zrFcKD5LEbt9+7amTp2qtGnT6rnnnnNbd+/ePfXv318ul0uVK1cOty62CwgIUK1ateRyuZQsWTIC90NwSZIhzps7d65t377dEiZMaGPGjHGW9+7d29avX2+dOnWyLl26WOrUqb1YZfQmyVwul5mZrVixwj788EMLCgqy2bNnW+7cuc3M7JVXXrG1a9faihUrLGvWrN4sN0YI26Zjx461Xbt2WUBAgL399ttWsmTJCJ8THBxs8eLFs02bNlnlypXt22+/tTp16jzOsqO10Pa537179yx+/PgP9Jx/2za2C/ueDHX79m375ptvbPjw4ZYqVSpbv3692/qmTZvazz//bOfOnbMECRI8znKjtdD31fnz5+3dd9+1TZs22TPPPGO9e/e2bdu22TfffGNz5syxr776yooUKeL23Lj8HvSUW7duWeLEiZ3HPXv2tA0bNtiv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AC8vL8yePRudOnXC119/jaioKJw9exZOTk5Qq9XQ09Nj0du/aOXKlQgPD4eZmRmcnJywfv165XnuyjgjCtU1DN1EREREVO+Fh4cjMTERoaGhuHv3LhISEtCmTRtER0ejY8eOyMnJwbZt21BQUAAbGxv4+flBrVaz6O1f1K9fP/z888/45ptvYGdnp+vmED0RDN1EREREVK88ePAAJiYmSg2dc+fOwcfHB4mJiXjppZcAAD/++CNeffVV2NnZYd68eejatWuV92EP9x8erkf0qNcAsGjRInz55ZfYvXs3mjZtyl5tqhf4DSciIiKiemPKlCmIiIhATk6OEgoNDAygVqthYmICACgpKUGrVq2we/dunDx5EvPnz8cPP/xQ5b0YuMtpNBrlWN68eRNA1fpEKpUKKpUKo0ePxs2bNxEREQEADNxUL/BbTkRERET1RlZWFr777jssXboUOTk5AAATExMUFBTgxIkTAKAUtHN2doaLiwuOHz+OmJgYZGRk6LLpNVLlnuqoqChMmzYNR44ceeS2ZWVlMDMzw/Dhw3H79u0qU60R1VUM3URERERU5x0/fhwAkJCQgO7du2P79u1YsmQJ7t69i2eeeQYzZszAlClTsHnzZqjVaqjVamg0Gnh4eGDVqlVISkrCunXrdPwpahYRUQL31KlTERMTg0GDBsHBwUFru4rq8BUjA0aNGoXNmzdDpVIxeFO9wKoPRERERFSnTZkyBffv34e7uzsMDAzwySefYPz48dixYwdEBOPHj8fYsWORnp6OoUOH4ocffoC1tTV++OEHZGdnY8WKFfDy8sKZM2d0/VFqhMzMTFhbWytDyPfu3YstW7YgKSkJbm5u0Gg0uHfvHi5cuIBu3bopIwcqQrejoyMAVimn+oPfciIiIiKq0/z9/bFs2TIYGBjgp59+AgAsXrwY3bp1w44dO7BkyRKUlJRg4cKFSExMxNmzZ/H999/DysoKqampAID8/Hw888wzOvwUNUPv3r2xaNEirWX379+Hqakp3NzccPnyZURGRqJ9+/bw8/NDnz59ADz6+XcGbqovWL2ciIiIiOqkhytob968GQsXLsScOXOUMDhhwgQcOnQIr7/+Ot577z00atQI+fn5MDU1BQCUlpbigw8+wNq1a/H999/jueee08lnqSkuXLgAZ2dnGBoaIicnBxYWFkhOTsbEiRNhbm6O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\n"
          },
          "metadata": {}
        }
      ],
      "source": [
        "# running a data viz\n",
        "top_scorers = df.sort_values(by='points', ascending=False).head(10)\n",
        "\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "plt.figure(figsize=(10, 6))\n",
        "plt.bar(top_scorers['player_name'], top_scorers['points'], color='orange')\n",
        "plt.xlabel('Player Name')\n",
        "plt.ylabel('Points')\n",
        "plt.title('Top 10 NBA Scorers')\n",
        "plt.xticks(rotation=45)\n",
        "plt.tight_layout()\n",
        "plt.show()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "hzDLbnEv5CZb"
      },
      "outputs": [],
      "source": [
        "# now i am going to automate the generation of player data to generate 1000 players\n",
        "import random\n",
        "\n",
        "# base players to derive new data\n",
        "base_players = [\n",
        "    (\"LeBron James\", \"Lakers\", 35, 8, 7),\n",
        "    (\"Stephen Curry\", \"Warriors\", 40, 10, 5),\n",
        "    (\"Kevin Durant\", \"Suns\", 25, 6, 9),\n",
        "    (\"Giannis Antetokounmpo\", \"Bucks\", 30, 5, 11),\n",
        "    (\"Jayson Tatum\", \"Celtics\", 34, 4, 8),\n",
        "    (\"Luka Dončić\", \"Mavericks\", 36, 9, 7),\n",
        "    (\"Nikola Jokić\", \"Nuggets\", 28, 8, 14),\n",
        "    (\"Ja Morant\", \"Grizzlies\", 32, 10, 6),\n",
        "    (\"Jimmy Butler\", \"Heat\", 27, 5, 7),\n",
        "    (\"Kawhi Leonard\", \"Clippers\", 26, 6, 5),\n",
        "      (\"Pat Connaughton\", \"Bucks\", 17, 5, 3),\n",
        "]\n",
        "\n",
        "\n",
        "# team pool to randomize assignments\n",
        "teams = [\n",
        "    \"Lakers\", \"Warriors\", \"Suns\", \"Bucks\", \"Celtics\", \"Mavericks\", \"Nuggets\",\n",
        "    \"Grizzlies\", \"Heat\", \"Clippers\", \"76ers\", \"Hawks\", \"Pelicans\", \"Thunder\",\n",
        "    \"Bulls\", \"Knicks\", \"Raptors\", \"Spurs\", \"Cavaliers\", \"Jazz\"\n",
        "]\n",
        "\n",
        "# generate 1000 players\n",
        "player_data = []\n",
        "for i in range(1000):\n",
        "    base_player = random.choice(base_players)\n",
        "    player_name = f\"{base_player[0]}_{i}\"  # add a unique suffix to each name\n",
        "    team_name = random.choice(teams)\n",
        "    points = base_player[2] + random.randint(-5, 5)  # add variability\n",
        "    assists = base_player[3] + random.randint(-2, 2)\n",
        "    rebounds = base_player[4] + random.randint(-3, 3)\n",
        "    player_data.append((player_name, team_name, points, assists, rebounds))\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "l6kHMOD96ieQ"
      },
      "outputs": [],
      "source": [
        "# insert augmented player data into database\n",
        "cursor.executemany('''\n",
        "    INSERT INTO nba_stats (player_name, team_name, points, assists, rebounds)\n",
        "    VALUES (?, ?, ?, ?, ?)\n",
        "''', player_data)\n",
        "conn.commit()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "QxFbpkyi6imH",
        "outputId": "3d0b8f92-f49b-4e36-8bf8-2b125df773e0"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Total Players: 1031\n",
            "(1, 'LeBron James', 'Lakers', 35, 8, 7)\n",
            "(2, 'Stephen Curry', 'Warriors', 40, 10, 5)\n",
            "(3, 'Kevin Durant', 'Suns', 25, 6, 9)\n",
            "(4, 'Giannis Antetokounmpo', 'Bucks', 30, 5, 11)\n",
            "(5, 'Jayson Tatum', 'Celtics', 34, 4, 8)\n",
            "(6, 'Luka Doncic', 'Mavericks', 36, 9, 7)\n",
            "(7, 'Nikola Jokic', 'Nuggets', 28, 8, 14)\n",
            "(8, 'Ja Morant', 'Grizzlies', 32, 10, 6)\n",
            "(9, 'Jimmy Butler', 'Heat', 27, 5, 7)\n",
            "(10, 'Kawhi Leonard', 'Clippers', 26, 6, 5)\n"
          ]
        }
      ],
      "source": [
        "# fetching amount of players to verify correct... should be 1031 players total\n",
        "    cursor.execute(\"SELECT COUNT(*) FROM nba_stats\")\n",
        "      total_players = cursor.fetchone()[0]\n",
        "          print(f\"Total Players: {total_players}\")  # should print 1000\n",
        "\n",
        "# fetch and display the first 10 rows\n",
        "    cursor.execute(\"SELECT * FROM nba_stats LIMIT 10\")\n",
        "      rows = cursor.fetchall()\n",
        "        for row in rows:\n",
        "           print(row)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "tKbSb6I-6itR",
        "outputId": "7b8f137e-6301-4d27-a661-e406156328ea"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "            points      assists     rebounds\n",
            "count  1031.000000  1031.000000  1031.000000\n",
            "mean     30.084384     6.847721     7.467507\n",
            "std       6.814865     2.485900     3.415650\n",
            "min       8.000000     2.000000     0.000000\n",
            "25%      25.000000     5.000000     5.000000\n",
            "50%      30.000000     7.000000     7.000000\n",
            "75%      35.000000     9.000000     9.000000\n",
            "max      45.000000    12.000000    17.000000\n"
          ]
        }
      ],
      "source": [
        "# analysis\n",
        "  df = pd.read_sql_query(\"SELECT * FROM nba_stats\", conn)\n",
        "\n",
        "\n",
        "    print(df[['points', 'assists', 'rebounds']].describe())\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_UU7gLGI66-t",
        "outputId": "9ba592cf-641b-4617-95b4-1b93d05f1468"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "            points      assists\n",
            "count  1031.000000  1031.000000\n",
            "mean     30.084384     6.847721\n",
            "std       6.814865     2.485900\n",
            "min       8.000000     2.000000\n",
            "25%      25.000000     5.000000\n",
            "50%      30.000000     7.000000\n",
            "75%      35.000000     9.000000\n",
            "max      45.000000    12.000000\n"
          ]
        }
      ],
      "source": [
        "# messing around\n",
        "df = pd.read_sql_query(\"SELECT * FROM nba_stats \", conn)\n",
        "\n",
        "\n",
        "    print(df[['points', 'assists']].describe())\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "54GwY62-8gnL"
      },
      "outputs": [],
      "source": [
        "import random\n",
        "\n",
        "# base players to expand data\n",
        "base_players = [\n",
        "    (\"LeBron James\", \"Lakers\", 35, 8, 7),\n",
        "    (\"Stephen Curry\", \"Warriors\", 40, 10, 5),\n",
        "    (\"Kevin Durant\", \"Suns\", 25, 6, 9),\n",
        "    (\"Giannis Antetokounmpo\", \"Bucks\", 30, 5, 11),\n",
        "    (\"Jayson Tatum\", \"Celtics\", 34, 4, 8),\n",
        "    (\"Luka Dončić\", \"Mavericks\", 36, 9, 7),\n",
        "    (\"Nikola Jokić\", \"Nuggets\", 28, 8, 14),\n",
        "    (\"Ja Morant\", \"Grizzlies\", 32, 10, 6),\n",
        "    (\"Jimmy Butler\", \"Heat\", 27, 5, 7),\n",
        "    (\"Kawhi Leonard\", \"Clippers\", 26, 6, 5)\n",
        "]\n",
        "\n",
        "teams = [\n",
        "    \"Lakers\", \"Warriors\", \"Suns\", \"Bucks\", \"Celtics\", \"Mavericks\", \"Nuggets\",\n",
        "      \"Grizzlies\", \"Heat\", \"Clippers\", \"76ers\", \"Hawks\", \"Pelicans\", \"Thunder\",\n",
        "         \"Bulls\", \"Knicks\", \"Raptors\", \"Spurs\", \"Cavaliers\", \"Jazz\"\n",
        "]\n",
        "\n",
        "# create data function\n",
        "def generate_large_dataset(base_players, num_rows=1000000):\n",
        "    large_dataset = []\n",
        "    for i in range(num_rows):\n",
        "        base_player = random.choice(base_players)\n",
        "        player_name = f\"{base_player[0]}_{i}\"\n",
        "        team_name = random.choice(teams)\n",
        "        points = max(0, base_player[2] + random.randint(-10, 10))\n",
        "        assists = max(0, base_player[3] + random.randint(-3, 3))\n",
        "        rebounds = max(0, base_player[4] + random.randint(-5, 5))\n",
        "        large_dataset.append((player_name, team_name, points, assists, rebounds))\n",
        "    return large_dataset\n",
        "\n",
        "# generate 1 million rows\n",
        "     large_dataset = generate_large_dataset(base_players, num_rows=1000000)\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "eoTqQrxD9YCa",
        "outputId": "94a2e5a4-384b-49ef-df00-251b62d3b456"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "('Stephen Curry_59', '76ers', 45)\n",
            "('Stephen Curry_94', 'Lakers', 45)\n",
            "('Stephen Curry_114', 'Grizzlies', 45)\n",
            "('Stephen Curry_217', 'Warriors', 45)\n",
            "('Stephen Curry_303', 'Knicks', 45)\n",
            "('Stephen Curry_405', 'Mavericks', 45)\n",
            "('Stephen Curry_451', 'Cavaliers', 45)\n",
            "('Stephen Curry_472', 'Warriors', 45)\n",
            "('Stephen Curry_510', 'Knicks', 45)\n",
            "('Stephen Curry_37', 'Knicks', 44)\n",
            "('Stephen Curry_92', 'Warriors', 44)\n",
            "('Stephen Curry_120', 'Spurs', 44)\n",
            "('Stephen Curry_165', 'Mavericks', 44)\n",
            "('Stephen Curry_312', 'Grizzlies', 44)\n",
            "('Stephen Curry_385', 'Bulls', 44)\n"
          ]
        }
      ],
      "source": [
        "# retrieve top 15 players with the highest points scored\n",
        "query = '''\n",
        "SELECT player_name, team_name, points\n",
        "  FROM nba_stats\n",
        "  ORDER BY points DESC\n",
        "LIMIT 15\n",
        "'''\n",
        "cursor.execute(query)\n",
        "result = cursor.fetchall()\n",
        "\n",
        "\n",
        "for row in result:\n",
        "    print(row)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PlKmQiYCY1P6",
        "outputId": "30f2d72b-7dbf-4452-9c08-01e1053dae65"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Player Efficiency Rankings:\n",
            "('Draymond Green', 'Warriors', 8, 8, 8, 1.5)\n",
            "('Chris Paul', 'Warriors', 18, 12, 3, 1.41)\n",
            "('Pat Connaughton_61', 'Clippers', 12, 7, 2, 1.38)\n",
            "('Pat Connaughton_263', 'Hawks', 12, 6, 6, 1.38)\n",
            "('Pat Connaughton_649', 'Clippers', 13, 7, 5, 1.38)\n",
            "('James Harden', 'Clippers', 20, 11, 4, 1.37)\n",
            "('Pat Connaughton_663', 'Pelicans', 14, 7, 5, 1.37)\n",
            "('Pat Connaughton_115', 'Jazz', 15, 7, 6, 1.36)\n",
            "('Nikola Jokić_453', 'Cavaliers', 23, 10, 13, 1.36)\n",
            "('Nikola Jokić_659', 'Spurs', 23, 10, 12, 1.36)\n"
          ]
        }
      ],
      "source": [
        "# this algorithm to determine efficiency assumes points are proportional to shot attempts, and calculates \"efficiency\" based on points per stat action\n",
        "query = '''\n",
        "  SELECT player_name, team_name,\n",
        "           points, assists, rebounds,\n",
        "           ROUND((points + assists * 2 + rebounds * 1.5) / (points + assists + rebounds), 2) AS efficiency\n",
        "  FROM nba_stats\n",
        "  ORDER BY efficiency DESC\n",
        "  LIMIT 10;\n",
        "'''\n",
        "\n",
        "\n",
        "cursor.execute(query)\n",
        "results = cursor.fetchall()\n",
        "\n",
        "\n",
        "print(\"Player Efficiency Rankings:\")\n",
        "for row in results:\n",
        "    print(row)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DunB6PDmY1Yf",
        "outputId": "ebdb6f41-9480-4f85-c97e-21994fa336a0"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Average Performance Metrics Per Team:\n",
            "('Celtics', 31.84, 6.95, 7.42)\n",
            "('Warriors', 30.93, 7.24, 7.69)\n",
            "('Knicks', 30.9, 6.67, 7.77)\n",
            "('76ers', 30.57, 6.83, 7.87)\n",
            "('Spurs', 30.51, 7.0, 6.91)\n",
            "('Clippers', 30.44, 6.69, 6.92)\n",
            "('Mavericks', 30.39, 7.17, 7.06)\n",
            "('Heat', 30.29, 6.79, 7.88)\n",
            "('Cavaliers', 30.29, 7.07, 6.89)\n",
            "('Grizzlies', 29.97, 7.12, 7.86)\n",
            "('Bucks', 29.89, 6.77, 7.67)\n",
            "('Jazz', 29.88, 7.29, 7.55)\n",
            "('Hawks', 29.88, 7.45, 7.55)\n",
            "('Nuggets', 29.83, 6.9, 7.28)\n",
            "('Suns', 29.69, 6.57, 7.14)\n",
            "('Thunder', 29.47, 6.24, 7.61)\n",
            "('Lakers', 29.45, 6.93, 6.7)\n",
            "('Raptors', 29.43, 6.57, 7.91)\n",
            "('Pelicans', 29.14, 6.14, 7.95)\n",
            "('Bulls', 28.79, 6.48, 7.83)\n",
            "('Timberwolves', 17.5, 2.5, 12.0)\n"
          ]
        }
      ],
      "source": [
        "# average performance metrics per team\n",
        "query = '''\n",
        "  SELECT team_name,\n",
        "           ROUND(AVG(points), 2) AS avg_points,\n",
        "           ROUND(AVG(assists), 2) AS avg_assists,\n",
        "           ROUND(AVG(rebounds), 2) AS avg_rebounds\n",
        "  FROM nba_stats\n",
        "  GROUP BY team_name\n",
        "  ORDER BY avg_points DESC;\n",
        "'''\n",
        "cursor.execute(query)\n",
        "results = cursor.fetchall()\n",
        "\n",
        "print(\"Average Performance Metrics Per Team:\")\n",
        "for row in results:\n",
        "    print(row)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "MIwadKAxY1fw",
        "outputId": "61249875-fb2a-4e01-a1ac-338bbf6c03ef"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Players with Triple-Doubles:\n",
            "('Luka Dončić_18', 'Nuggets', 41, 11, 10)\n",
            "('Nikola Jokić_189', 'Raptors', 27, 10, 15)\n",
            "('LeBron James_205', 'Cavaliers', 32, 10, 10)\n",
            "('Nikola Jokić_288', 'Grizzlies', 31, 10, 13)\n",
            "('Nikola Jokić_358', 'Heat', 27, 10, 13)\n",
            "('Nikola Jokić_384', 'Warriors', 32, 10, 14)\n",
            "('LeBron James_390', 'Cavaliers', 31, 10, 10)\n",
            "('Nikola Jokić_437', 'Lakers', 33, 10, 13)\n",
            "('Nikola Jokić_453', 'Cavaliers', 23, 10, 13)\n",
            "('Nikola Jokić_530', 'Grizzlies', 25, 10, 15)\n",
            "('Luka Dončić_572', 'Cavaliers', 32, 11, 10)\n",
            "('Nikola Jokić_659', 'Spurs', 23, 10, 12)\n",
            "('Nikola Jokić_766', '76ers', 30, 10, 13)\n",
            "('Nikola Jokić_891', 'Mavericks', 26, 10, 17)\n",
            "('Nikola Jokić_909', '76ers', 28, 10, 15)\n",
            "('Nikola Jokić_917', 'Pelicans', 31, 10, 11)\n",
            "('LeBron James_939', 'Bucks', 40, 10, 10)\n",
            "('Nikola Jokić_966', 'Hawks', 31, 10, 16)\n",
            "('Nikola Jokić_972', '76ers', 25, 10, 11)\n",
            "('Nikola Jokić_977', 'Hawks', 27, 10, 15)\n",
            "('Nikola Jokić_987', 'Grizzlies', 24, 10, 13)\n"
          ]
        }
      ],
      "source": [
        "# players with triple-doubles\n",
        "query = '''\n",
        "SELECT player_name, team_name, points, assists, rebounds\n",
        "  FROM nba_stats\n",
        "  WHERE points >= 10 AND assists >= 10 AND rebounds >= 10;\n",
        "'''\n",
        "cursor.execute(query)\n",
        "results = cursor.fetchall()\n",
        "\n",
        "print(\"Players with Triple-Doubles:\")\n",
        "for row in results:\n",
        "    print(row)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 965
        },
        "id": "OYQDI-JaZ49f",
        "outputId": "25f5020b-bb4e-4fbe-db48-38392fa732db"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "       Team Name  Total Points\n",
            "0       Clippers          1857\n",
            "1       Warriors          1794\n",
            "2        Nuggets          1790\n",
            "3        Celtics          1751\n",
            "4      Grizzlies          1738\n",
            "5          Bucks          1704\n",
            "6          Spurs          1678\n",
            "7      Cavaliers          1666\n",
            "8      Mavericks          1641\n",
            "9        Thunder          1503\n",
            "10        Knicks          1483\n",
            "11          Jazz          1464\n",
            "12         Hawks          1464\n",
            "13          Suns          1455\n",
            "14         76ers          1437\n",
            "15       Raptors          1383\n",
            "16         Bulls          1382\n",
            "17        Lakers          1296\n",
            "18          Heat          1272\n",
            "19      Pelicans          1224\n",
            "20  Timberwolves            35\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<Axes: title={'center': 'Total Points by Team'}, xlabel='Team Name'>"
            ]
          },
          "metadata": {},
          "execution_count": 225
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 640x480 with 1 Axes>"
            ],
            "image/png": "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RKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqY/AA4+7uDo1Gk2kJCgoCAPj5+WXa9vnnn2vVuH79Olq2bAlra2sUKVIEw4YNQ0pKiqGbSkRERCplZuiCR44cQWpqqvL69OnTaNKkCT7++GNlXa9evTB27FjltbW1tfJxamoqWrZsCWdnZ4SHh+PWrVvo2rUr8uXLh/Hjxxu6uURERKRCBg8whQsX1no9ceJEeHp6on79+so6a2trODs7Z/n527dvx9mzZ7Fjxw44OTnBx8cH3333HYYPH47g4GCYm5sbuslERESkMkbtA5OcnIw///wTn332GTQajbJ+yZIlcHR0RMWKFTFy5Eg8fvxY2RYREQFvb284OTkp6/z9/REfH48zZ85ke6ykpCTEx8drLURERPRuMvgVmIzWrVuHBw8eoHv37sq6Tp06wc3NDS4uLoiKisLw4cNx4cIFrFmzBgAQGxurFV4AKK9jY2OzPdaECRMQEhJi+C+CiIiIch2jBpi5c+eiefPmcHFxUdb17t1b+djb2xtFixZFo0aNEB0dDU9PT52PNXLkSAwePFh5HR8fD1dXV53rERERUe5ltAATExODHTt2KFdWslOzZk0AwOXLl+Hp6QlnZ2ccPnxYa5+4uDgAyLbfDABYWFjAwsJCz1YTERGRGhitD8z8+fNRpEgRtGzZ8qX7RUZGAgCKFi0KAPD19cWpU6dw+/ZtZZ/Q0FDY2tqifPnyxmouERERqYhRrsCkpaVh/vz56NatG8zM/neI6OhoLF26FC1atICDgwOioqIwaNAg1KtXD5UqVQIANG3aFOXLl0eXLl0wadIkxMbGYtSoUQgKCuIVFiIiIgJgpACzY8cOXL9+HZ999pnWenNzc+zYsQPTpk1DYmIiXF1d0a5dO4waNUrZx9TUFBs3bsQXX3wBX19f5M+fH926ddMaN4aIiIjyNqMEmKZNm0JEMq13dXXFnj17Xvn5bm5u2Lx5szGaRkRERO8AzoVEREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqmPwABMcHAyNRqO1lC1bVtn+9OlTBAUFwcHBAQUKFEC7du0QFxenVeP69eto2bIlrK2tUaRIEQwbNgwpKSmGbioRERGplJkxilaoUAE7duz430HM/neYQYMGYdOmTVi1ahXs7OzQt29ftG3bFgcOHAAApKamomXLlnB2dkZ4eDhu3bqFrl27Il++fBg/frwxmktEREQqY5QAY2ZmBmdn50zrHz58iLlz52Lp0qVo2LAhAGD+/PkoV64cDh48iFq1amH79u04e/YsduzYAScnJ/j4+OC7777D8OHDERwcDHNzc2M0mYiIiFTEKH1gLl26BBcXF5QsWRIBAQG4fv06AODYsWN49uwZGjdurOxbtmxZlChRAhEREQCAiIgIeHt7w8nJSdnH398f8fHxOHPmTLbHTEpKQnx8vNZCRERE7yaDB5iaNWtiwYIF2Lp1K2bPno2rV6+ibt26ePToEWJjY2Fubg57e3utz3FyckJsbCwAIDY2Viu8pG9P35adCRMmwM7OTllcXV0N+4URERFRrmHwW0jNmzdXPq5UqRJq1qwJNzc3rFy5ElZWVoY+nGLkyJEYPHiw8jo+Pp4hhoiI6B1l9Meo7e3tUaZMGVy+fBnOzs5ITk7GgwcPtPaJi4tT+sw4Oztneiop/XVW/WrSWVhYwNbWVmshIiKid5PRA0xCQgKio6NRtGhRVKtWDfny5cPOnTuV7RcuXMD169fh6+sLAPD19cWpU6dw+/ZtZZ/Q0FDY2tqifPnyxm4uERERqYDBbyENHToUrVq1gpubG/7991+MGTMGpqam6NixI+zs7BAYGIjBgwejUKFCsLW1Rb9+/eDr64tatWoBAJo2bYry5cujS5cumDRpEmJjYzFq1CgEBQXBwsLC0M0lIiIiFTJ4gLl58yY6duyIu3fvonDhwqhTpw4OHjyIwoULAwCmTp0KExMTtGvXDklJSfD398cvv/yifL6pqSk2btyIL774Ar6+vsifPz+6deuGsWPHGrqpREREpFIGDzDLly9/6XZLS0vMmjULs2bNynYfNzc3bN682dBNIyIioncE50IiIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVYYAhIiIi1WGAISIiItVhgCEiIiLVMXiAmTBhAt577z3Y2NigSJEi+PDDD3HhwgWtffz8/KDRaLSWzz//XGuf69evo2XLlrC2tkaRIkUwbNgwpKSkGLq5REREpEJmhi64Z88eBAUF4b333kNKSgq+/vprNG3aFGfPnkX+/PmV/Xr16oWxY8cqr62trZWPU1NT0bJlSzg7OyM8PBy3bt1C165dkS9fPowfP97QTSYiIiKVMXiA2bp1q9brBQsWoEiRIjh27Bjq1aunrLe2toazs3OWNbZv346zZ89ix44dcHJygo+PD7777jsMHz4cwcHBMDc3N3SziYiISEWM3gfm4cOHAIBChQpprV+yZAkcHR1RsWJFjBw5Eo8fP1a2RUREwNvbG05OTso6f39/xMfH48yZM1keJykpCfHx8VoLERERvZsMfgUmo7S0NAwcOBC1a9dGxYoVlfWdOnWCm5sbXFxcEBUVheHDh+PChQtYs2YNACA2NlYrvABQXsfGxmZ5rAkTJiAkJMRIXwkRERHlJkYNMEFBQTh9+jT279+vtb53797Kx97e3ihatCgaNWqE6OhoeHp66nSskSNHYvDgwcrr+Ph4uLq66tZwIiIiytWMdgupb9++2LhxI3bv3o3ixYu/dN+aNWsCAC5fvgwAcHZ2RlxcnNY+6a+z6zdjYWEBW1tbrYWIiIjeTQYPMCKCvn37Yu3atdi1axc8PDxe+TmRkZEAgKJFiwIAfH19cerUKdy+fVvZJzQ0FLa2tihfvryhm0xEREQqY/BbSEFBQVi6dCnWr18PGxsbpc+KnZ0drKysEB0djaVLl6JFixZwcHBAVFQUBg0ahHr16qFSpUoAgKZNm6J8+fLo0qULJk2ahNjYWIwaNQpBQUGwsLAwdJOJiIhIZQx+BWb27Nl4+PAh/Pz8ULRoUWVZsWIFAMDc3Bw7duxA06ZNUbZsWQwZMgTt2rXDhg0blBqmpqbYuHEjTE1N4evri86dO6Nr165a48YQERFR3mXwKzAi8tLtrq6u2LNnzyvruLm5YfPmzYZqFhEREb1DOBcSERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqQ4DDBEREakOAwwRERGpDgMMERERqY7Z224AERERvRvcR2zK0f7XJrbU+Vi8AkNERESqk6sDzKxZs+Du7g5LS0vUrFkThw8ffttNIiIiolwg1waYFStWYPDgwRgzZgyOHz+OypUrw9/fH7dv337bTSMiIqK3LNcGmClTpqBXr17o0aMHypcvj19//RXW1taYN2/e224aERERvWW5shNvcnIyjh07hpEjRyrrTExM0LhxY0RERGT5OUlJSUhKSlJeP3z4EAAQHx+fad+0pMc5ak9WNbJjzNq5rb6a257T+mpuu7Hrq7ntOa2v5rbntL6a257T+mpuu7Hrv422p68TkZd/suRC//zzjwCQ8PBwrfXDhg2TGjVqZPk5Y8aMEQBcuHDhwoULl3dguXHjxkuzQq68AqOLkSNHYvDgwcrrtLQ03Lt3Dw4ODtBoNK/8/Pj4eLi6uuLGjRuwtbU1aNuMWVvt9dn2d7M+2/5u1ldz241dn203XH0RwaNHj+Di4vLS/XJlgHF0dISpqSni4uK01sfFxcHZ2TnLz7GwsICFhYXWOnt7+xwf29bW1ijfQGPXVnt9tv3drM+2v5v11dx2Y9dn2w1T387O7pX75MpOvObm5qhWrRp27typrEtLS8POnTvh6+v7FltGREREuUGuvAIDAIMHD0a3bt1QvXp11KhRA9OmTUNiYiJ69OjxtptGREREb1muDTCffvop7ty5g9GjRyM2NhY+Pj7YunUrnJycjHI8CwsLjBkzJtNtqNxeW+312fZ3sz7b/m7WV3PbjV2fbX/z9TUir3pOiYiIiCh3yZV9YIiIiIhehgGGiIiIVIcBhoiIiFSHAYaIiIhUhwGGiIiIVIcBhoj08uzZM3h6euLcuXNvuyk6adiwIUJCQjKtv3//Pho2bPgWWkSkbjdu3MDNmzeV14cPH8bAgQMxZ84cgx4nzwaYhQsXYtOmTcrrr776Cvb29nj//fcRExNj8OPFx8dj3bp1qvgjb+wfvq1bt2L//v3K61mzZsHHxwedOnXC/fv3DXIMYzH2e3P8+HGcOnVKeb1+/Xp8+OGH+Prrr5GcnGyQYxhavnz58PTp07fdDJ2FhYVh5syZ+PDDD5GYmKisT05Oxp49e95iy16fGn9uXubBgwdvuwmkh06dOmH37t0AgNjYWDRp0gSHDx/GN998g7FjxxruQIaZP1p9ypQpIzt37hQRkfDwcLG2tpbffvtNWrVqJR999JHe9T/++GP5+eefRUTk8ePHUrp0acmXL5+YmZnJ6tWr9a7/oocPH8ratWvl7NmzeteqU6eOLFq0SEREbt26Jba2tuLr6yuOjo4SEhKid/2KFSvKpk2bREQkKipKLCwsZOTIkVKrVi3p3r273vWvX7+uNYvpoUOHZMCAAfLbb7/pXdvY70316tWVn4/o6GixtLSUjh07SqlSpWTAgAF6139RSkqKnDhxQu7du6dXne+//166desmz549M1DLMtuyZYvs27dPeT1z5kypXLmydOzYUa/2azQaiYyMlJo1a0rFihXl6tWrIiISGxsrJiYm+jZbREQWLFggGzduVF4PGzZM7OzsxNfXV65du6Z3/Tf5c2PIvzUiIhMnTpTly5crrz/++GMxMTERFxcXiYyM1Lu+Mf8eiIgcO3ZMoqKilNfr1q2TNm3ayMiRIyUpKUmv2j169JD4+PhM6xMSEqRHjx561RYx3ntjb28v58+fFxGR6dOny/vvvy8iItu2bRMPDw+9ameUZwOMlZWVxMTEiIjIV199JV26dBERkdOnT4ujo6Pe9Z2cnJRfviVLlkipUqUkMTFRfvnlF/Hx8dG7vjEDkrF/+PLnz6/8kxgzZoy0a9dORJ7/IXByctK7vjFDhrHfG1tbW7l8+bKIPP/D3rRpUxER2b9/vxQvXlzv+gMGDJA//vhDRJ6Hl9q1a4tGo5H8+fPL7t27da774Ycfio2NjRQtWlSaNm0qH330kdZiCMYKvhqNRuLi4uTp06fSsWNHcXR0lN27dxs0wBj7hMmYPzfGPhlzd3eXAwcOiIjI9u3bxd7eXrZt2yaBgYHSpEkTveur+aTDxMRE4uLiMq2/c+eOmJqa6lVbxHjvTca/8a1atZKJEyeKiEhMTIxYWlrq3e50eTbAFC5cWI4fPy4iIj4+Pso38fLly5I/f36961taWsr169dFRKRLly4yfPhwEXn+DTREfWMGJGP/8BUsWFDOnDkjIiK1a9dW0v7Vq1fFyspK7/rGDBnGfm9sbGzk4sWLIiLSuHFjmTZtmkHrFytWTI4cOSIiImvXrhUXFxe5cOGCjBo1SnmfdNG9e/eXLoZgrOD74j+J7777TiwsLGT06NEGCzDGPmEy5s+NsU/GMv6t7N+/v/Tu3VtERC5cuCD29vZ611fjScfDhw/lwYMHotFo5PLly/Lw4UNluXfvnixcuFCKFi2qd9uN9d7UqFFDhg8fLnv37hVLS0vl5yciIkKKFSumd7vT5dkA06lTJ6lataoEBgaKtbW1/PfffyIisn79eqlQoYLe9UuXLi0rVqyQhIQEKVy4sHL2FRkZKQ4ODnrXN2ZAMvYPX6tWrcTf31/Gjh0r+fLlk5s3b4rI81+a0qVL613fmCHD2O9NgwYNpGvXrrJo0SLJly+fXLp0SUREwsLCxM3NTe/6FhYWyiXjXr16KWeIV65cERsbG73rG5Oxgm/6FZiMVq9eLfnz5zdYgDH2CZMxf26MfTJWtGhR5QpMmTJlZOXKlSIicv78eYP8TKrxpEOj0YiJiUm2i6mpqYwbN07vthvrvdm9e7fY29uLiYmJ1q2ukSNHGuyKrEgeDjD379+Xvn37SuvWrWXLli3K+tGjRxvkB2PWrFliZmYm9vb2UrlyZUlNTRURkRkzZoifn5/e9Y0ZkIz9wxcTEyMtW7aUSpUqKbczREQGDhwo/fr107u+MUOGsd+bkydPSsWKFcXW1laCg4OV9X379pWOHTvqXb9EiRKybds2SUlJEVdXV6VfxunTp/U+23327JmEhobKr7/+qty3/+eff+TRo0d6t1vEeMH32rVrkpaWlmn96dOnZcGCBTrXzcjYJ0zG/Lkx9slYUFCQuLm5SePGjcXBwUH5eVm2bJlUqVJF7/pqPOkICwuT3bt3i0ajkTVr1khYWJiyhIeHyz///KN3u0WM+96kpKRk6pt29erVLG+J6SpPBphnz55JSEiIVuclYzh69KisWbNG6w/4xo0bZf/+/XrXNnZAehM/fMZirJCRlpYmMTExEh8fb5T3JiUlRfbs2ZNlh9QnT55IcnKyXvVFnt96sbOzk7Jly0qJEiXk6dOnIiIyd+5cqVWrls51r127JmXLlhVra2sxNTWV6OhoEXl+S6BPnz56t1vEeMF34cKFypWdjJ48eSILFy7UuW5G9+/fl6CgIKOdMGXHED83xv5bk5ycLD/++KP0799fuUolIjJlyhT5/fff9a6v5pOOa9euKe+3MRjzvTH2CY1IHg0wItqXzgwtOTlZSpYsabBe+tnJLiClX47V1ZUrV5RLohldvHjRYO/Z5cuX5ZtvvpEOHToo//g3b94sp0+fNkh9YwSw1NRUyZcvX5bvjaFYWFjIlStXjFZfRGTVqlUyZcoUrQC/YMECWbdunc4127RpI507d5akpCQpUKCAEmB2794tpUqV0rvNr/L48WOdP1ej0UiBAgUydUg1ZCfel4WIO3fuGOQYIiJJSUly48YNiYmJ0Vr0ZayTseTkZOnRo4fRf+aNdUL2Jk46REQSExPl3LlzcvLkSa3FEIzx3ryJExqRPBxgWrdubbDLw1lxcXExaoAJCQmRxMTETOsfP36sd8/6evXqZfneLF68WOrXr69XbZHnl0etrKykcePGYm5urvxwT5gwQemYqY+lS5dmu23o0KF61S5fvrxEREToVeNlqlWrJjt27DBa/ZddddTn6ypUqJDSGTBjgDFUx2wRyfYqS0JCgl5XAjQajfz0009iZWUlY8aMUdbHxsaKRqPRuW5Gbdu2zfI2VWxsrEFuIV24cEHq1KmTqa9Eel8KXb2JkzFbW1ujBxhjMuZJx+3bt6Vly5bZ9oXJrd7UCU2eDTCzZ88WZ2dnGTJkiCxdulTWr1+vtejL2ONiZPd43X///af3D7aNjY1yHzejS5cuiZ2dnV61RURq1aolP/30k4ho/7M7dOiQQe5J29nZyebNmzOtHzhwoDg7O+tV+++//5Y6derIqVOn9KqTnS1btoiPj49s2LBB/v33X62nDx4+fKh3/XLlysndu3czrd+/f79e31t7e3vlNkzG7+m+ffukSJEiOtfNqGTJkjJ69GitdQkJCVKnTh2pU6eOznXTO/FGRESIs7OztGvXTh4/fmzQKzDVq1eXzz77TGvdrVu3pGzZsgYJ7e+//77Uq1dPNm/eLCdOnJDIyEitRR/GPhnr2rWrTJkyxaA1fXx8pEqVKq+16MuYJx2dOnWS2rVry5EjRyR//vyyfft2Wbx4sXh5eWmNK6Sr2NhY6dy5sxQtWlRMTU0NFpDexAmNiIiZ4YbEU5cvv/wSADBlypRM2zQaDVJTU/Wqf+TIEezcuRPbt2+Ht7c38ufPr7V9zZo1etUXEWg0mkzrT548iUKFCulVW6PR4NGjR5nWP3z4UO/3BQBOnTqFpUuXZlpfpEgR/Pfff3rXX7JkCTp27IiNGzeiTp06AIB+/fphzZo1yuiQuuratSseP36MypUrw9zcHFZWVlrb7927p1f9Fi1aAABat26t9f1N/37r+/7XqlULTZs2xe7du2FjYwMA2Lt3Lz744IMsh9N/XU2bNsW0adOUEYk1Gg0SEhIwZswY5WvS1/bt21G3bl0ULFgQAwcOxKNHj+Dv7w8zMzNs2bJF57rp73OtWrVw6NAhtG7dGu+//z5+/fVXg7QbADZv3ox69eph8ODBmDJlCv799180aNAAlStXxvLly/WuHxkZiWPHjqFs2bIGaK22oKAg/PDDD/jjjz9gZmb4fxmlS5fG2LFjceDAAVSrVi3T38r+/fvnuOaHH35ooNa92rhx4zB06FB89913Wbbf1tZW59q7du3C+vXrUb16dZiYmMDNzQ1NmjSBra0tJkyYgJYtW+rV9u7du+P69ev49ttvUbRo0Sz/p+giLS0ty79VN2/eVP7uGIJGRMRg1UjRo0ePl26fP3++TnULFiwIjUaDhw8fwtbWVusHLjU1FQkJCfj8888xa9YsneoDQKtWrWBlZYVly5bB1NRUqf3pp58iMTFRr38WAFC8eHGsXLkS77//PmxsbHDy5EmULFkSa9euxdChQxEdHa1XfQBYunQp+vbti9DQUMydOxfr16/H7t27UaZMGb3qLly48KXbu3Xrplf9Vw1dX79+fb3qp6WloX379rh37x62bduG8PBwtG7dGuPGjcOAAQN0rnvz5k34+/tDRHDp0iVUr14dly5dgqOjI/bu3YsiRYro1e50UVFRaNCgAcaMGYNly5bBwsICmzZtyvRPIydMTEwQGxurtPHx48cICAjAzp07kZiYaJDQDjyfhqJOnTpo164dNm7ciKpVq2LJkiXK75g+3nvvPUydOlUJ7Ib00UcfYefOnShQoIBRTsY8PDyy3abRaHDlyhW96hubicn/ZuQx9EmHra0toqKi4O7uDjc3NyxduhS1a9fG1atXUaFCBTx+/FivttvY2GDfvn3w8fHRq86LPv30U9jZ2WHOnDmwsbFBVFQUChcujDZt2qBEiRI6//97EQMMgKdPn8LS0vJtN+O1LFy4ECKCzz77DNOmTYOdnZ2yzdzcHO7u7vD19dXrGGfPnkW9evVgb2+PunXrAgD27duH+Ph47Nq1CxUrVtSr/tChQ3Ho0CGsWrUKZcqUwfHjxxEXF4euXbuia9euGDNmjF710/3yyy8YPHgwChcujN27d6NUqVIGqat2ycnJaNmyJR4/foyoqChMmDABffv21btuSkoKli9fjqioKCQkJKBq1aoICAjIdJVKXxEREWjSpAlq1qyJjRs36l0/JCQEw4YNg7W1tdb6MWPGYO/evXpftcvo4sWLqFu3Lpo0aYLFixcb7Ix3165dGDVqFMaPHw9vb2/ky5dPa7s+VwGMdTL2rjDmScd7772HcePGwd/fH61bt4a9vT0mTJiAGTNmYPXq1Xqf7JUvXx5LlixBlSpV9Krzojd1QpNnA0xqairGjx+PX3/9FXFxcbh48SJKliyJb7/9Fu7u7ggMDDTIce7cuYMLFy4AALy8vFC4cGGD1N2zZw9q165tlEu6APDvv/9i5syZOHnyJKysrFCpUiX07dtX79tTwPN/oEFBQViwYAFSU1NhZmaG1NRUdOrUCQsWLNDpjHTw4MFZrl+1ahWqVq0KT09PZV1Wtw1f1/Xr11+6vUSJEjrXTrdv3z789ttvuHLlClatWoVixYph8eLF8PDw0OkMOyoqKtO6R48eoWPHjmjZsiW++OILZX2lSpX0aruhValSJct/8jExMShSpIhWeDl+/PibbNorpV8tfdHjx49hYWGh9XOu763H9KsALx7PULce35T0f0f6Brvs3vus6PveG9Off/6JlJQUdO/eHceOHUOzZs1w7949mJubY8GCBfj000/1qr99+3b89NNP+O233+Du7m6YRv+/N3FCk2cDzNixY7Fw4UKMHTsWvXr1wunTp1GyZEmsWLEC06ZNQ0REhF71ExMT0a9fPyxatAhpaWkAAFNTU3Tt2hU///xzprM9XURHR2P+/PmIjo7G9OnTUaRIEWzZsgUlSpRAhQoV9K5vbNevX8fp06eRkJCAKlWqoHTp0jrXatCgwWvtp9FosGvXLp2PY2Ji8tI/jPr+o/jrr7/QpUsXBAQEYPHixTh79ixKliyJmTNnYvPmzdi8eXOOa6a3OeOvesbX6R/n9B/d33///dr7tm7d+vUbnEFO+uXoe+Xu7NmzuH79utbszRqNBq1atdKp3qtuN2aU2289pqSkICwsDNHR0ejUqRNsbGzw77//wtbWFgUKFNCrNgAsWrQIkydPxqVLlwAAZcqUwbBhw9ClSxed6r3J9x4w/ElHdh4/fozz58+jRIkScHR01LtewYIF8fjxY6SkpMDa2jrTlTtdw92buquRZwNMqVKl8Ntvv6FRo0Za/TDOnz8PX19f3L9/X6/6ffr0wY4dOzBz5kzUrl0bALB//370798fTZo0wezZs/Wqv2fPHjRv3hy1a9fG3r17ce7cOZQsWRITJ07E0aNHsXr16hzVi4qKQsWKFWFiYpLlGXtGue0s/U06efKk1utnz57hxIkTmDJlCr7//nu0bdtWr/pVqlTBoEGD0LVrV62fyxMnTqB58+aIjY3Ncc2YmJjX3tfNze2198147x9AppCUvg7QP9gZ05UrV/DRRx/h1KlTmYIdkLvb/ibExMSgWbNmuH79OpKSkpSr1QMGDEBSUpLenZ2nTJmCb7/9Fn379tX6Wzlr1iyMGzcOgwYNMsSXYTTGOOl4UXJyMq5evQpPT0+DXnU3Vp8+W1tbfPTRR+jcuTMaNWqU6W+FwRjseSaVsbS0VKaxz/iY15kzZwwyv4eDg0OWs/vu2rXLIJO3GfpR5IzzwaSPHaHRaDItuj5aN2jQIElISFA+ftmirwcPHmT5qPDdu3cN8ihyVjZu3GiQMXKsrKyUwQIzfl+jo6PFwsJC7/rGEhoaKlWrVpWtW7cqj3xv3bpVqlevLtu3bzfIMQ4fPiwHDx7MtP7gwYPKBJW6+OCDD6RNmzZy584dKVCggJw9e1b27dsnNWrUkL179+rTZEWXLl1k3rx5yqR/hrZnz56XLvow9pge7u7uWY54vGDBAnF3d9e7/ouD+hl6kD8fHx+l/Rnfn+PHj+s1yajI8wHsPvvsMzE1NdUaEK5v374yYcIE/RpuRGvWrJH27duLlZWVODs7y4ABA/T6Hc1Ong0wVatWlcWLF4uI9g9dSEiIXmNKpLOysspy7ITTp0+LtbW13vXz58+vDJ704nP2uvyjyzgfzLVr11666MLPz0/u37+vfJzd0qBBA53qZ9SsWTOZNWtWpvWzZ8+W5s2b610/K5cuXTLI99XDw0NCQ0NFRPv7unDhQilXrpze9cePHy9z587NtH7u3LnKRG66qFChguzbty/T+r1790rZsmV1rpvRe++9J6tWrcq0/q+//pIaNWroXNfBwUEZ1dTW1lYZv2Lnzp0GmW1ZRCQwMFBKly4tGo1GihcvLgEBAfL7778bbFTn7E42DDHgmbHH9LCwsMhy3KmLFy8aJLS/amJEfRnzpKN///5SrVo12bdvn+TPn1+pvW7dOoP9bKZ78uSJwcedio+Pl3nz5kmTJk3E1NRUSpcurfdAqxnl2QCzbt06sbOzk4kTJ4q1tbVMnjxZevbsKebm5gY5Y2zYsKF8/PHH8uTJE2Xd48eP5eOPP5ZGjRrpXb9YsWLKlAEZf2nWrFkjJUuW1Kv2nj17shyA79mzZ3qfzb0JBQsWzDI8njt3TgoVKqRX7Rd/wR88eCDnzp2TTz/9VCpXrqxXbZHnAaN8+fJy8OBBsbGxkX379smff/4phQsXlhkzZuhd383NLcupJg4ePKjX2a6lpWWWg/udPHnSIDP+iojWH/CMrly5IgUKFNC5rr29vXIyULJkSdm1a5eIPJ/uwpCDbomI3Lx5U5YuXSp9+vSRsmXLiomJiUEGb3zw4IHWcufOHdm+fbvUrFlT70HWjD1IYYUKFeT777/PtP67776TihUr6l3/xUH9jhw5InPmzJGyZcvKX3/9pXd9Y550lChRQhkhO2PtS5cuGWSm7oSEBAkKCpLChQsbfaTfM2fOiI+Pj0Hr5tkAI/L87LBx48ZSuHBhsbKyktq1a8u2bdsMUvvUqVPi4uIiDg4O0rBhQ2nYsKE4ODhIsWLFDDLfz5AhQ6ROnTpy69YtZeTc/fv3S8mSJbUmFNOFMUf5fROsra0lKioq0/qoqCi9/yFldTan0WikRIkSEh4erldtkecTRo4bN07y58+vnElbWlrKqFGj9K4tkv2w5/qeLdatW1eaNGkisbGxyrrY2Fhp2rSp1KtXT+e6GRUqVCjL9/jAgQN6zaRdp04dWbt2rYiIdOzYUZo1ayb79++Xrl27GmSY/4wSExNl27ZtMmLECKlVq5aYm5sb/Ew6o7CwMKlatapeNT755BPp1auXiDz/J3rlyhV59OiRNGzYULp37653G1evXi2mpqbKTONjx44Vf39/MTMzkzVr1uhdPzuGuu1rzJMOKysrJbRkDDCRkZFia2urd9u//PJLKVeunKxevVqsrKxk3rx58t1330nx4sXlzz//1Lv+kydPZMWKFdKmTRuxsLCQEiVKyPDhw/Wumy5PBxhjS0xMlDlz5sjgwYNl8ODB8vvvv+s16VxGSUlJ0rNnTzEzMxONRiP58uUTExMT6dy5s6SkpOhVW6PRyO3btzOtv3Dhgs6p/6OPPnrtRV9+fn7St2/fTOu//PJLvW8PZpzWPiwsTPbu3Svnzp0z+JQRSUlJcubMGTl06JBBZ28tVaqUcus0o0WLFomHh4fOdS9duiQVK1YUc3Nz8fT0FE9PTzE3N5cKFSpkeXtAFx06dJD69evLgwcPlHX379+X+vXry8cff6xz3a1btypn4hcvXhQvLy/RaDTi6OhosCHiR44cKb6+vmJpaSlVqlSRgQMHyrp167KcBNCQzp07p3efvhs3bkj58uWlXLlyYmZmJrVq1RIHBwfx8vIy2Oz0R48elYCAAKlatapUrVpVAgICtGamNgZD3fY15klH3bp1lRCUHh5FnveB8ff317u+q6ur0lcz4xQyixYt0ut2+9atW6Vr165ia2srhQoVkt69exvl6n2efQop3dGjR3Hu3DkAzwf1qVat2ltuUc4Y8lHk9Cdo1q9fj2bNmsHCwkLZlpqaiqioKHh5eWHr1q05rv2qwbAy0ndgrAMHDqBx48Z477330KhRIwDAzp07ceTIEWU4+rxq0qRJmDRpEiZPnoyGDRsCeP7efPXVVxgyZAhGjhypc20RQWhoKM6fPw8AKFeuHBo3bmywwdr++ecf1KtXD3fv3lUG3oqMjISTkxNCQ0Ph6upqkOMAzx8fzclYIq9iYmKCwoULY9CgQWjbtq3eI0K/6MUnB0UEt27dwsSJE5GSkoL9+/frVT8lJQUrVqzAyZMnjTpIoTHEx8drvU5/b4KDg3H+/HlERkbqVf/Zs2fIly8fkpOTcfnyZSQkJKB8+fIoUKAA/vvvP70ed96/fz+aN2+Ozp07Y8GCBejTpw/Onj2L8PBw7NmzR+//VwUKFMDZs2dRokQJFC9eHGvWrEGNGjVw9epVeHt7IyEhQae61tbW+OCDDxAQEIAWLVpkejzbUPJsgLl58yY6duyIAwcOwN7eHgDw4MEDvP/++1i+fDmKFy+e45p///03mjdvjnz58r1yjAxdx8UwpvSQsXDhQnzyySdaf5zSR/nt1auXQcYfMLbIyEhMnjwZkZGRykB8I0eO1Cvgpbtw4QJ+/vlnJfiWK1cOffv21XkemrZt22LBggWwtbV95WPYhphDa8SIEZgxY4Yy3omlpSWGDx+O0aNH61X7TUhMTMSSJUu0Bljs2LGjTn8gX+eRdzMzMzg7O6NJkyY6jwcDPH/8fs+ePQgLC8O+fftgbm6O+vXrw8/PD35+fnoHmqzG+gGez+80b948o8yRZCimpqa4detWptFZ7969iyJFiuj9GHtWYzeJCFxdXbF8+XK9Ry5v164dVq9enekYcXFxaNSoEU6fPq1X/ejoaEycOFErPA4fPhze3t561QWeD4nx888/o379+mjcuDF8fHzw448/YsaMGZg0aRJu3rypU91Hjx4ZdM6j7OTZANOsWTM8ePAACxcuhJeXF4Dn/5h69OgBW1tbna4yZJxT5WXPvRtiZMzsRp7VaDSwtLREqVKl0KZNG51Gzg0JCcHQoUP1ml/mZcaOHYs6deooVwDSJSYm4qeffsrV/0j/+usvdOjQAdWrV1f+8B08eBBHjhzB8uXL0a5duxzX7NGjB2bMmAEbG5s3Nmx7QkICzp07BysrK5QuXVrrapuudu7ciZ07d+L27dvK4I3p5s2bp3d9Q3udq4JpaWm4ffs29uzZg6FDh2Ls2LEGOfbJkycxdepULFmyJNuJ73LixbF+0q/46DOYWFJSEkxMTJRwGB0djXnz5uH69etwc3NDYGDgS+cxel0vzkWV7t9//4WnpyeePHmiV/2wsDCtcJH+3pQqVcogY6q89957qFSpEubOnausu3XrFho2bIgKFSrkeEwuIPNVo+zoM0UEAEydOhWmpqbo378/duzYgVatWkFE8OzZM0yZMiVH86O9bpsB/dudLs8GGCsrK4SHh2eaA+LYsWOoW7eu3pNkGVuDBg1w/PhxpKamKgHs4sWLMDU1RdmyZXHhwgVoNBrs378f5cuXf8ut1Zb+R3HChAlaQSwuLg4uLi56/zE35nD/np6eCAgIyPSPbMyYMfjzzz8NMhGlGoWEhGDs2LGoXr16lrParl27Vqe6ueWq5saNG/Hll1++8mcrOyKCEydOICwsDGFhYdi/fz/i4+NRqVIl1K9fH1OnTtWpbkREBO7evYsPPvhAWbdo0SKMGTMGiYmJ+PDDD/Hzzz/rFFD9/PzQt29ftG/fHgcOHECjRo3g5eWFcuXK4eLFi7hw4QJ27Nih8xWMGTNmAAAGDRqE7777TmtE39TUVOzduxfXrl3DiRMndKqf7u7du3BwcADwfELN33//HU+ePEHr1q0Ncjv5zp07qFevHpo3b57lTOO6DOL2qhG/xUhTRMTExODYsWMoVapUjgcsfVWbAcO3O88GmDJlyuDPP/9EjRo1tNYfPnwYnTp1wuXLl3Wu/ezZMzRr1gy//vqrQW5ZZGXatGnYt28f5s+fr6TZhw8fomfPnqhTpw569eqFTp064cmTJ9i2bdsr62U350xW9J1zxsTEBMuWLUNQUBBatWqF3377Debm5gYLMMYc7t/a2hpRUVGZJoa8dOkSKleunCuD75u4RVW0aFFMmjRJ56Hfs/Mmr2q+zIMHD/DZZ5/p/P4ULFgQCQkJqFy5snLrqG7dusrta101b94cfn5+GD58OADg1KlTqFq1Krp3745y5cph8uTJ6NOnD4KDg3Nc287ODkePHkXp0qXh5+eHqlWras0j9u2332L37t06969Jv3oTExOD4sWLa80NlX7LeuzYsahZs6ZO9U+dOoVWrVrhxo0bKF26NJYvX45mzZohMTERJiYmSExMxOrVq/Hhhx/qVD8jQ880nnFqCBFBixYt8Mcff6BYsWJa++k7RYQhvWo6i4wM1W7jzASoApMnT0a/fv0wa9YsVK9eHcDzDr0DBgzAjz/+qFftfPnyvXI4fn1NnjwZoaGhWpfi7OzsEBwcjKZNm2LAgAEYPXo0mjZt+lr1DPFLnBMNGjTAoUOH0KpVK/j5+WHdunUGq/3iGduLw/3rw8/PD/v27csUYPbv36/z2Zyxw6OdnZ1SP+Ps5YaUnJyM999/3+B1M96KevG21Jtkb2+vV/+jP//8E3Xr1jXYpfN0kZGR+O6775TXy5cvR82aNfH7778DAFxdXTFmzBidAkxqaqoSCs+fP4/p06drbe/evTumTZumc9uvXr0K4PnfgjVr1qBgwYI618rKV199BW9vbyxZsgSLFy/GBx98gJYtWyrvTb9+/TBx4kSD/O1zdXVFaGiowWYaf/EfvKmpKWrVqoWSJUvq21Qt/fv3R6lSpdC/f3+t9TNnzsTly5dz9P19G2Eqz16ByTiJVfp90PSPX+z7ocuEVoMGDYKFhQUmTpxokPa+qECBAti4cSP8/Py01oeFhaFVq1Z49OgRrly5Ah8fnxzdm3wTMnbai4+PxyeffIIzZ87g119/RevWrY12Jr1p0yZMnjwZYWFhOtf49ddfMXr0aHzyySeoVasWgOd9YFatWoWQkBC4uLgo+77uLY03NWGhiODGjRsoXLiwwZ8eGT58OAoUKIBvv/3WoHXp5SwtLXHp0iXlCaw6deqgefPm+OabbwAA165dg7e3Nx49epTj2o0aNUKzZs0wbNgw1K5dG3369EHXrl2V7X/99RcGDx6co7m2XkUMNBs1ADg6OmLXrl2oVKkSEhISYGtriyNHjihP7pw/fx61atXCgwcPclz7Tc40DkBrXjRDKlasGP7+++9MTzMdP34crVu31rkTL/D8quXcuXOVhx0qVKiAzz77zKAnUXn2Cow+Zw6vIyUlBfPmzcOOHTtQrVq1TKEo46VYXbRp0wafffYZfvrpJ7z33nsAgCNHjmDo0KHKGcXhw4d1frrhwYMHWL16NaKjozFs2DAUKlQIx48fh5OTU6bLmDmVMTPb2tpi8+bNGDhwoNGvAnl5eeHIkSN61fjyyy8BAL/88gt++eWXLLcBObuloe8syq9LRFCqVCmcOXPG4Lc2nz59ijlz5mDHjh2oVKlSpqeC9P15T6e2jsIZHT16FCtXrsw04zWg+607JycnXL16Fa6urkhOTsbx48e1AvGjR490foR13LhxaN68ORITE9GxY0cMGTIEly5dQrly5XDhwgXMmDFDr8fuM5o7dy6mTp2qzEZdunRpDBw4ED179tS55r179+Ds7Azg+Qlf/vz5ta7yFCxYUKdgBxj//8ebcvfu3SwDha2tLf777z+d6x49ehT+/v6wsrJSummkXwHfvn07qlatqnPtjPJsgDHEFOovc/r0aeWbdPHiRa1thji7+O233zBo0CB06NABKSkpAJ4/8tmtWzelQ2DZsmXxxx9/5Lh2VFQUGjduDDs7O1y7dg29evVCoUKFsGbNGly/fh2LFi3Sq+3z58/X+qUxMTHBjBkzUKVKFezdu1ev2sDLx33Q9x/327yNoS8TExOULl0ad+/eNXiAiYqKgo+PDwBkemzUUGOpvKqjcG62fPlydO3aFf7+/ti+fTuaNm2KixcvIi4uDh999JHOdVu0aIERI0bghx9+wLp162Btba11KzMqKgqenp461fb19cWWLVswePBgHDp0CACUW7AuLi4IDg7O0VMq2Rk9ejSmTJmCfv36KR2CIyIiMGjQIFy/fl2vJ79e/Bkx1M+Msf9/ZMUYP++lSpXC1q1b0bdvX631W7Zs0etqz6BBg9C6dWv8/vvvWnc4evbsiYEDBxrk7zyAvDsbtYhISkqKrFq1Shm+evXq1QYZUTUlJUX27Nlj9FE2RUQePXokJ0+elJMnTxpsxNZGjRrJsGHDRER7+OoDBw6Im5ub3vVjYmLk6dOnmdanpqYaZHZYYwz3Hx4eLhs2bNBat3DhQnF3d5fChQtLr169svyaciolJUUmT54s7733njg5OUnBggW1Fn39/fffUqdOnSznLcrtnJ2dZdGiRW+7GTrx9vaWmTNnisj/fqfS0tKkV69eMnr0aJ3r3rlzR+rWrSsajUZsbGwyDb3fsGFD+frrr/Vqu4jI7du35eDBgxIeHq5MXGgojo6OsnTp0kzrly5dKg4ODjrX1Wg00qJFC2WEbzMzM2natKnyukWLFgafGsVQEyK+ODr5i2031Kjlc+fOFSsrKxk9erQyuvi3334r1tbWMmfOHJ3rWlpayrlz5zKtP3PmjEHnF8uzfWDOnDmD1q1bIzY2Vusx5MKFC2PDhg2oWLGiXvUtLS1x7tw5g4yT8KbZ2dnh+PHj8PT01Lr3GhMTAy8vLzx9+lSv+iYmJihXrhz+/vtvrbNDQz2FZIxxH4z5tEdGo0ePxh9//IEhQ4Zg1KhR+Oabb3Dt2jWsW7cOo0ePztTZLqcy9v0yNzfP1BfGEPfrjcXBwQGHDx/W+YrC25Q/f36cOXMG7u7ucHBwQFhYGLy9vXHu3Dk0bNgQt27d0qv+w4cPUaBAgUxPvdy7dw8FChSAubl5jmv269cPn3zyidFHrra3t8eRI0cyXRW8ePEiatSooVMfFeD1R//Wd2ylxMREDB8+HCtXrsTdu3czbdfl79mbajsAzJ49G99//z3+/fdfAIC7uzuCg4O1+jvllJOTExYvXpzpIZJt27aha9euiIuL06vN6fLsLaSePXuiQoUKOHr0qHJf9P79++jevTt69+6N8PBwvepXrFgRV65cMVqA+eijj7K8pJhxILtOnTop4SwnLCwssuz4mx7wDKFcuXKoUaMGVq5cqQz3DyDTSKK68Pb2Nvi4D8Z82iOjJUuW4Pfff0fLli0RHByMjh07wtPTE5UqVcLBgwf1DjDGunffoEGDl17i3rVrl97H6NmzJ5YuXarKjsIZ+1sUK1YMp0+fhre3Nx48eGCQR++z6xipy0CW6WbNmoVffvkFnp6eCAwMRLdu3ZQ+JYbUpUsXzJ49O1M/qTlz5iAgIEDnuoYa9PFVvvrqK+zevRuzZ89Gly5dMGvWLPzzzz/47bffdH6I4021HQC++OILfPHFF7hz5w6srKy0xuPR1aefforAwED8+OOPytOJBw4cwLBhw9CxY0e96ysMdi1HZSwtLbOcFfrUqVNiaWmpd/0tW7aIj4+PbNiwQf7991+DXFbMqFu3bmJnZydubm7Stm1badu2rbi7u4u9vb188skn4uXlJRYWFrJ///4c1w4MDJQPP/xQkpOTlQnEYmJipEqVKjJgwAC9254+2/WUKVPEwsJCpk+fLiLPZy/W55JuVFSUuLm5iYmJiXh5ecmJEyfEyclJChQoILa2tmJqaqrMOpxTFhYWcv36deV17dq1Zdy4ccrrq1evSoECBXRuezpra2vlNpqzs7McO3ZMRJ7PFm2I2WeNZeDAgVpLUFCQ1K5dW+zs7KR///4GOUb//v3F3t5e6tWrJ3379pVBgwZpLblZx44d5aeffhIRkbFjx0rhwoWlZ8+e4ubmZpBbAcag0Whkx44dMmDAAHF0dJR8+fJJ69atZcOGDZKammqw4/Tt21dsbW2lQoUKEhgYKIGBgVKxYkWxtbXN9H3OjYw1IaKaJSUlSf/+/cXc3Fy5jW9hYSEDBw40yK32dHn2FlLlypUxderUTMPZ79q1CwMGDMCpU6f0qp9x0K2MZ6ZioJEIR4wYgfj4eMycOVM5VlpaGgYMGAAbGxt8//33+Pzzz3HmzJkcDzT18OFDtG/fHkePHsWjR4/g4uKC2NhY1KpVC1u2bNF7ioGMg5Nt2bIFHTt2xMcff4zRo0fD3d1d5/emefPmMDMzw4gRI7B48WJs3LgR/v7+WuM+HDt2DAcPHsxxbTc3NyxevBj16tVDcnIy7O3tsWHDBuXq0alTp1C/fn29b8F4eXlh0aJFqFmzJurUqYMPPvgAI0aMwIoVK9CvXz/cvn1br/rA8yHh58+fj+joaEyfPl35PpQoUQIVKlTQu35GwcHBSEhI0HtsJeD5VZ7sPHr0CEePHtX7GMZy7949PH36FC4uLkhLS8OkSZMQHh6O0qVLY9SoUQYfA8UQMv6ePnv2DGvXrlWerHRyckL37t3Ro0ePTGMi5dTLvq8ZaTQag1zJMzRjTYhoLFWrVsXOnTtRsGDBV45Bpe+gpY8fP1ZGJ/f09IS1tbVe9TIxWBRSmU2bNkmFChVk1apVcuPGDblx44asWrVKvL29ZdOmTXpfLUnvEJXdoi9HR0e5cOFCpvUXLlxQOr5FRUWJnZ2dzsfYv3+/zJo1S3744QcJDQ3Vuc6LNBqNxMXFKa/PnDkjnp6eUqlSJb2uwDg4OMjJkydF5HnnZo1GI0ePHlW2nzt3Tuf34/PPPxdfX1/Zu3evDB48WBwcHCQpKUnZ/ueff0r16tV1bnu64cOHy/fffy8iIsuXLxczMzMpVaqUmJuby/Dhw/WuHxYWJlZWVtK4cWMxNzdXOmhPmDBB2rVrp3f9F126dEnvzsdTpkx56fb4+Hh5//339TqGsbx45TW7JTd68fc0XUxMjIwZM0a52pnXeXt7K3/TGzVqJEOGDBERkenTp4uLi8vbbFqWgoODJTExUfn4ZYuudu7cKU+ePDFUk7OVZwOMRqNRloxPqrz4Orf+gtrb28v69eszrV+/fr3Y29uLiMjFixeVj1/Hzp07pVy5cln+QX3w4IGUL19e9u7dq3uj/5+fn5/cv39fa91///0n9erVE41Go3PdF//gZnyCSkS/W1Rv6mmPF0VERMhPP/0kf//9t0Hq1apVS7mVkfH9OXTokBQrVswgx8ho0aJFUrRoUb1qWFpaysKFC7PclpCQILVr1xYvLy+9jmEsWT0Rl9WSG2UXYNKlpaXJ9u3b32CLcqcpU6Yot8FDQ0PF0tJSLCwsxMTERKZNm/aWW/d25M+fXywsLKROnToyatQoCQ0NlcePHxv8OHm2E+/u3bvfyHEeP36c5cBVOZ0o60VdunRBYGAgvv76a62B7MaPH6/0Ht+zZ0+ObglMmzYNvXr1ynK4czs7O/Tp0wdTpkzR+6mErN57BweHHM2lkR1jjfvg6OiIvXv3Zvu0x6pVqwzS+e3p06daMwjXqlVLGfHXEE6dOoWlS5dmWl+kSBG9Bq56cY4l+f+xd44ePap3p9vFixejS5cusLe31xrdOCEhAc2aNcPt27f1Gl3ZmDL+rMtL5rTJjdzc3F46l49Go0GTJk0McixjDPL3pgwaNEj5uHHjxjh//jyOHTsGR0dH/Pnnn2+xZW/P/fv3cfjwYezZswd79uzBtGnTkJycjOrVq6NBgwYYN26cQY6TZ/vAGNudO3fQo0cPbNmyJcvt+vaBSU1NxcSJEzFz5kzlkTQnJyf069cPw4cPh6mpKa5fvw4TExMUL178tWq6ublh69atKFeuXJbbz58/j6ZNm+o0I298fLwSjF41tYGu88WYmJigefPmysy7GzZsQMOGDZU+O0lJSdi6datRJ/3Tl62tLT766CN07twZjRo10mkm25cpXrw4Vq5ciffff1/rEfm1a9di6NChOs+m/eJjn+mPrjds2PC15+N6mT/++AMDBgzApk2b4Ofnh8TERDRr1gyxsbHYs2eP1hQOuZmxhoRXs1cN8vcmn8gxpJMnT6Jq1aq57u9NdtMgZMVQwyqcOXMGkydPxpIlS5CWlmaw9yRPXYGJiopCxYoVYWJi8srJFvW9QjJw4EA8ePAAhw4dgp+fH9auXYu4uDiMGzcOP/30k161gefzCX3zzTf45ptvlEDw4j/+EiVK5KhmXFzcS4cdNzMzw507d3LeWDz/pUmf/8je3j7LXyDRs4Pzi6Njdu7cOdM++oxt8CYsXLgQS5cuRZs2bWBnZ4dPP/0UnTt3ViYc1VeHDh0wfPhwrFq1ChqNBmlpaThw4ACGDh2q13tj7H8yPXv2xL1799CmTRusX78eo0ePxr///quq8EJZGz9+PKZOnYqgoCDY2Nhg+vTp8PDwQJ8+fVC0aNG33bx3zpuYBuHixYsICwtDWFgY9uzZg6SkJNStWxc//vhjpvn79GLwm1K5WMZ7uun3pjP2hcnYB0Zfzs7OcujQIRF5/mhdeofb9evXS+3atfWubwwlS5Z86WPGf/31l3h4eOhUOywsTBnl2NgdnN8F8fHxMm/ePGnSpImYmppK6dKlJSQkRO+6SUlJ0rNnTzEzMxONRiP58uUTExMT6dy5s6SkpBik/o0bNyQmJkZrMZThw4eLiYmJlCxZUuuxdrV4sV8WPR86IH1030KFCklUVJSIiJw9e1acnZ3fYsv0ExkZmWv7NxmbRqORIkWKyPfffy8nT56UtLQ0oxwnT12BuXr1qjIQW/pU7saSmJiIIkWKAHh+9eHOnTsoU6YMvL299X40DQA8PDxeehnwypUrOa7ZokULfPvtt2jWrJlWPwwAePLkCcaMGYMPPvggx3WB/021npKSgj179uCzzz577VtbeZGNjQ169OiBHj164OzZswgICEBISAhGjx6tV11zc3P8/vvv+Pbbb3H69GkkJCSgSpUqes+NdPHiRQQGBmYaAFIMMGzAi/1r8uXLB0dHx0zz8OT2vhLp1DSH05tg7EH+6OWMMaxC//79sXfvXowdOxYbN26En58f/Pz8UKdOHYM+Sp2nAoybm1uWHxuDl5cXLly4AHd3d1SuXBm//fYb3N3d8euvvxrksujAgQO1Xj979gwnTpzA1q1bMWzYMJ1qjho1CmvWrEGZMmXQt29fZRTf8+fPY9asWUhNTcU333yjV7vNzMwwefLkXH8r5217+vQp/v77byxduhRbt26Fk5OTzt/XjPbv3486deqgRIkSOb7F+DI9evSAmZkZNm7caPCJFl8cZdagI3ka2Yvh6+nTp/j8888zjaWklvBlDPXq1UNoaCi8vb3x8ccfY8CAAdi1axdCQ0MzjdOVm7z4vX2RrlMgvEl79uxB8+bNUbt2bezduxfff/89ihQpgpMnT2Lu3LlYvXq1TnXTb1M9ePAA+/btw549e/DNN9/gzJkzqFKlCg4cOGCQ9uepAPP333+/9r4Zn3bIiatXr8LDwwMDBgxQ5jcZM2YMmjVrhiVLlsDc3BwLFizQqXZG2c0CO2vWLJ0H9HJyckJ4eDi++OILjBw5UhnWX6PRwN/fH7NmzYKTk5PObU7XsGFD7NmzB+7u7nrXetds27YNS5cuxbp162BmZob27dtj+/btqFevnkHqN2zYEMWKFUPHjh3RuXNnlC9f3iB1IyMjcezYMZQtW9Yg9TJSaydOIHP4yqpfVl43c+ZMZX61b775Bvny5UN4eDjatWuHoUOHvuXWZS+76Rsybs/tJ2ojRozAuHHjMHjwYNjY2CjrGzZsiJkzZ+pdPzU1Fc+ePUNSUhKePn2KpKQkXLhwQe+66fLUU0iv+0SHPpe8TUxM4ObmhgYNGihL8eLF8fjxY5w/fx4lSpSAo6OjTrVfx5UrV+Dj4/PKJ31e5f79+7h8+TJEBKVLlzboSKG//vorQkJCEBAQgGrVqmU6G9U1PL4LrK2t8cEHHyAgIAAtWrR4aadqXfz3339Yvnw5li1bhoiICFSqVAkBAQHo2LGjXrf03nvvPUydOhV16tQxYGspr3r69ClmzZqFyZMnIzY29m03551VoEABnDp1Ch4eHlpPyF27dg1ly5bVeeLefv36Yc+ePTh79iwKFiyIevXqoX79+vDz84O3t7fhrtAapWdNHrZ7924ZM2aM1K9fXywtLcXExERKlSolvXv3lmXLlklsbKxRj//DDz+Im5ubUY+hr6w6ThuyA7WaxcfHv7FjXblyRcaNGycVKlQQU1NTadCgQY4+P+NIsjt37hRfX1/ZvXu3/Pfff6oYaZberqdPn8qIESOkWrVq4uvrqzxAMG/ePHFxcRFXV1eZOHHi223kO65YsWJy4MABEdHuYL5mzRopWbKkznXbt28vP//8s5w6dcog7cxOngswb2q0WRGRJ0+eyM6dO+Xbb7+VunXrKqMzli9fXu/aPj4+UqVKFWXx8fERZ2dnMTU1ld9++80Arae37cmTJ0YPAikpKbJhwwbx8fHJcXh8cZTZrEadZSil7Hz11VdiZ2cn7dq1k6JFi4qZmZn06tVLvL29ZdmyZQZ5Ko5ebsiQIVKnTh25deuWMhHl/v37pWTJkjpPJZCcnCw9evSQK1euGLi1meWpW0jA89sTDRo00Bo9MaMZM2Zg9+7dWLt2rcGOmZycjAMHDmDLli347bffkJCQoPdAPsHBwVqX4dIHDvPz8zNKPwRDePLkCXbu3Kk8yTRy5EgkJSUp283MzDB27NhMT0DlJYmJiRg+fDhWrlyJu3fvZtpuqAGgDhw4gCVLlmD16tV4+vQp2rRpg4CAADRr1uy1a+Rk5OT0p9CI0pUsWRLTpk1D69atcfr0aVSqVAndu3fH3Llz+aTWG5KcnIy+fftiwYIFSElJgZmZGVJTU9GpUycsWLDgpSMxv4ydnR0iIyPh4eFh4Ba/wOgRKZcpUaKEnD17Ntvt586dE1dXV72OkZSUJHv27JHg4GDx8/MTKysrKVOmjPTs2VMWLVpk0HEx1GT27NnywQcfKK8LFCggNWvWFD8/P/Hz8xNnZ2dlnp686ssvv5Ry5crJ6tWrxcrKSubNmyffffedFC9eXP7880+9648YMULc3d3F3NxcWrZsKUuXLlUmdtNFSEiIXp9PeVe+fPnk5s2bymtLS0tlDBgyrtTUVJk4caK8//77Ur16dfnss89k06ZNsmLFCrl48aLe9bt27frKSVgNIc9dgbG0tMTp06eznQL+8uXL8Pb2xpMnT3Sq37BhQxw6dAgeHh6oX78+6tati/r16xtsREkTE5NXnp1oNBqkpKQY5HiGVLduXXz11Vdo1aoVgMzDqv/555+YNWsWIiIi3mYz36oSJUpg0aJF8PPzg62tLY4fP45SpUph8eLFWLZsGTZv3qxX/dq1ayMgIACffPKJQTqTm5qaKiMsE+WEqakpYmNjlbG5bGxsEBUVZfyzdsJ3332H4OBgNG7cGFZWVti2bRs6duyIefPmGaR++ojzjRo1yvJBjf79+xvkOHnqMWrgfwMlZRdgoqKi9Aob+/btQ9GiRdGwYUP4+fmhfv36cHBw0Lnei152aysiIgIzZsxAWlqawY5nSOnhMJ2lpaXWk2E1atRAUFDQ22harnHv3j0l0Nna2ipzkdSpUwdffPGF3vUNNf5Cujx2/kMGJCLo3r27MncZx8h5cxYtWoRffvkFffr0AQDs2LEDLVu2xB9//GGQ+dfmzp0Le3t7HDt2DMeOHdPaptFoGGB0ZczRZoH/DdwTFhaGH374AR07dkSZMmWUR8jq16+vnHHook2bNpnWXbhwASNGjMCGDRsQEBCAsWPH6lzfmB48eKDV5+XFeZXS0tK0tudFJUuWxNWrV1GiRAmULVsWK1euRI0aNbBhwwbY29sb7Dhnz57NcuZfXR5hZ38F0sXrzF1GxnH9+nW0aNFCed24cWNoNBr8+++/Bhkh3dgj3afLc7eQ4uLiULVqVZiammY72uzx48cNMmAbADx69Aj79+/H7t27ERYWhpMnT6J06dI4ffq03rX//fdfjBkzBgsXLoS/vz8mTJiAihUrGqDVxlG6dGlMnDgR7dq1y3L7ypUr8fXXX+Py5ctvuGW5x9SpU2Fqaor+/ftjx44daNWqFUQEycnJmDp1arYDGL6uK1eu4KOPPsKpU6eg0Wi0BisEct5J2MTEBHZ2dq8MMYaa1ZaI9Pfi7TvAOLfwkpOTcfXqVXh6esLMzPDXS/LcFZg3Ndpsuvz586NQoUIoVKgQChYsCDMzM5w7d06vmg8fPsT48ePx888/w8fHBzt37kTdunUN1GLjadGiBUaPHo2WLVtmefUrJCQELVu2fEutyx0yPh3XuHFjnD9/HseOHUPp0qW1br/pasCAAfDw8MDOnTvh4eGBw4cP4+7duxgyZAh+/PFHnWqGhIS8clRSIso9Xrx9B2R9C0/X23ePHz9Gv379sHDhQgDP50orWbIk+vXrh2LFimHEiBH6fQH/L89dgcnIGKPNpqWl4ejRowgLC8Pu3btx4MABJCYmolixYlqj8+o6F9OkSZPwww8/wNnZGePHj8/yllJuFRcXBx8fH5ibm6Nv374oU6YMgOe3wGbOnImUlBScOHHCoAFSLXbt2oW+ffvi4MGDsLW11dr28OFDvP/++/j111/1DqqOjo7YtWsXKlWqBDs7Oxw+fBheXl7YtWsXhgwZghMnTuSonomJCWJjY9mJl0hFevTo8Vr76TqNx4ABA3DgwAFMmzYNzZo1Q1RUFEqWLIn169cjODg4x39nspOnA4wx2NraIjExEc7OzkpY8fPzg6enp0Hqm5iYwMrKCo0bN37pM/q5tePb1atX8cUXXyA0NFTr6leTJk3wyy+/KB1Y85o3NT5RwYIFcfz4cXh4eMDT0xN//PEHGjRogOjoaHh7e+d49l8+hUREL3Jzc8OKFStQq1YtradNL1++jKpVq+o91U26PHcLydgmT56MBg0aKFcXDK1r166q7jTp4eGBrVu34t69e0pfl1KlSqFQoUJvuWVv18mTJ/HDDz9ku71p06Y63+LJqGLFijh58iQ8PDxQs2ZNTJo0Cebm5pgzZ45O4ZHnP0T0ojt37mR5UpOYmGjQ/18MMAaW/liasRhiJuvcoFChQqhRo8bbbkauERcX99KJG83MzDI9taWLUaNGITExEcDzviutWrVC3bp14eDggOXLl+e4Xm59ZJ+I3p7q1atj06ZN6NevH4D/PSTwxx9/wNfX12DHYYAhygWMPT5ROn9/f+Xj0qVL4/z587h37x4KFiyo6it7RJR7jB8/Hs2bN8fZs2eRkpKC6dOn4+zZswgPD8/RFCSvwj4wRLlAv379EBYWhiNHjmT5hFaNGjXQoEEDzJgxQ6f6n3322WvtZ6iROIkob4uOjsbEiRNx8uRJJCQkoGrVqhg+fLhBnqZMxwBDlAsYe3wiExMTuLm5oUqVKi/tt2LISUyJiIyJAYYol4iJicEXX3yBbdu2ZTk+kT4DTAUFBWHZsmVwc3NDjx490Llz5zzfcZqIjCc1NRVr165Vxj0rX7482rRpY9AB7RhgiHIZY4xPBABJSUlYs2YN5s2bh/DwcLRs2RKBgYFo2rQp+78QkcGcOXMGrVu3RmxsrHI1+eLFiyhcuDA2bNhgsBHjGWCI8qCYmBgsWLAAixYtQkpKCs6cOYMCBQq87WYR0TvA19cXhQsXxsKFC5UTsPv376N79+64c+cOwsPDDXIcPoVElAeZmJgocyHldP4jIqKXiYyMxNGjR7WuHhcsWBDff/893nvvPYMdR/95s4lIFZKSkrBs2TI0adIEZcqUwalTpzBz5kxcv36dV1+IyGDKlCmDuLi4TOtv376d7VARuuAVGKI84Msvv8Ty5cvh6uqKzz77DMuWLYOjo+PbbhYRvSMyTg8wYcIE9O/fH8HBwahVqxYA4ODBgxg7duxLRxzPKfaBIcoDTExMUKJECVSpUuWlHXZz6xxaRJS7pd+WTpfxScoXXxvqtjWvwBDlAWqfQ4uIcrfdu3e/8WPyCgwRERGpDq/AEBERkUE9ffoUUVFRuH37dqZJX1u3bm2QYzDAEBERkcFs3boVXbt2xX///ZdpmyH7wPAxaiIiIjKYfv364eOPP8atW7eQlpamtRhy3Cn2gSEiIiKDsbW1xYkTJ+Dp6WnU4/AKDBERERlM+/btERYWZvTj8AoMERERGczjx4/x8ccfo3DhwvD29ka+fPm0tvfv398gx2GAISIiIoOZO3cuPv/8c1haWsLBwUFrDCqNRoMrV64Y5DgMMERERGQwzs7O6N+/P0aMGAETE+P1VGEfGCIiIjKY5ORkfPrpp0YNLwADDBERERlQt27dsGLFCqMfhwPZERERkcGkpqZi0qRJ2LZtGypVqpSpE++UKVMMchz2gSEiIiKDadCgQbbbNBoNdu3aZZDjMMAQERGR6rAPDBEREakO+8AQERGRXtq2bYsFCxbA1tYWbdu2fem+a9asMcgxGWCIiIhIL3Z2dsqAdXZ2dm/kmOwDQ0RERHobO3Yshg4dCmtr6zdyPAYYIiIi0pupqSlu3bqFIkWKvJHjsRMvERER6e1NXw9hgCEiIiKDyDhxo9GPxVtIREREpC8TExOtzrzZuXfvnkGOx6eQiIiIyCBCQkL4FBIRERGph4mJCWJjY9mJl4iIiNTjTfZ/ARhgiIiIyADe9A0d3kIiIiIi1eEVGCIiIlIdBhgiIiJSHQYYIiIiUh0GGCIiIlIdBhgiykSj0bx0CQ4OfttNBAAEBwdDo9Hg888/11ofGRkJjUaDa9euvZ2GEZHRMcAQUSa3bt1SlmnTpsHW1lZr3dChQ992ExWWlpaYO3cuLl269LabQkRvEAMMEWXi7OysLOlzm2Rct3z5cpQrVw6WlpYoW7YsfvnlF63PHz58OMqUKQNra2uULFkS3377LZ49e6ZsDw4Oho+PD+bNm4cSJUqgQIEC+PLLL5GamopJkybB2dkZRYoUwffff//Ktnp5eaFBgwb45ptvst0nNTUVgYGB8PDwgJWVFby8vDB9+nStfbp3744PP/wQ48ePh5OTE+zt7TF27FikpKRg2LBhKFSoEIoXL4758+drfd6NGzfwySefwN7eHoUKFUKbNm145YfoDeBcSESUI0uWLMHo0aMxc+ZMVKlSBSdOnECvXr2QP39+dOvWDQBgY2ODBQsWwMXFBadOnUKvXr1gY2ODr776SqkTHR2NLVu2YOvWrYiOjkb79u1x5coVlClTBnv27EF4eDg+++wzNG7cGDVr1nxpmyZOnIj33nsPR48eRfXq1TNtT0tLQ/HixbFq1So4ODggPDwcvXv3RtGiRfHJJ58o++3atQvFixfH3r17ceDAAQQGBiI8PBz16tXDoUOHsGLFCvTp0wdNmjRB8eLF8ezZM/j7+8PX1xf79u2DmZkZxo0bh2bNmiEqKgrm5uYGeteJKBMhInqJ+fPni52dnfLa09NTli5dqrXPd999J76+vtnWmDx5slSrVk15PWbMGLG2tpb4+Hhlnb+/v7i7u0tqaqqyzsvLSyZMmJBt3TFjxkjlypVFRKRDhw7SsGFDERE5ceKEAJCrV69m+7lBQUHSrl075XW3bt3Ezc0t0/Hr1q2rvE5JSZH8+fPLsmXLRERk8eLF4uXlJWlpaco+SUlJYmVlJdu2bcv22ESkP16BIaLXlpiYiOjoaAQGBqJXr17K+pSUFK0ZaFesWIEZM2YgOjoaCQkJSElJga2trVYtd3d32NjYKK+dnJxgamoKExMTrXW3b99+rbaNGzcO5cqVw/bt27OcTG7WrFmYN28erl+/jidPniA5ORk+Pj5a+1SoUCHT8StWrKi8NjU1hYODg9KmkydP4vLly1pfBwA8ffoU0dHRr9VuItINAwwRvbaEhAQAwO+//57pto6pqSkAICIiAgEBAQgJCYG/vz/s7OywfPly/PTTT1r758uXT+u1RqPJcl1aWtprtc3T0xO9evXCiBEjMHfuXK1ty5cvx9ChQ/HTTz/B19cXNjY2mDx5Mg4dOqRXmxISElCtWjUsWbIkU3sKFy78Wu0mIt0wwBDRa3NycoKLiwuuXLmCgICALPcJDw+Hm5ubVqfamJiYN9K+0aNHw9PTE8uXL9daf+DAAbz//vv48ssvlXWGuEJStWpVrFixAkWKFMl0hYmIjItPIRFRjoSEhGDChAmYMWMGLl68iFOnTmH+/PmYMmUKAKB06dK4fv06li9fjujoaMyYMQNr1659I21zcnLC4MGDMWPGDK31pUuXxtGjR7Ft2zZcvHgR3377LY4cOaL38QICAuDo6Ig2bdpg3759uHr1KsLCwtC/f3/cvHlT7/pElD0GGCLKkZ49e+KPP/7A/Pnz4e3tjfr162PBggXw8PAAALRu3RqDBg1C37594ePjg/DwcHz77bdvrH1Dhw5FgQIFtNb16dMHbdu2xaeffoqaNWvi7t27WldjdGVtbY29e/eiRIkSaNu2LcqVK4fAwEA8ffqUV2SIjEwjIvK2G0FERESUE7wCQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqsMAQ0RERKrDAENERESqwwBDREREqvN/3di6w7mMsUoAAAAASUVORK5CYII=\n"
          },
          "metadata": {}
        }
      ],
      "source": [
        "# visualization for total points per team\n",
        "import pandas as pd\n",
        "\n",
        "query = '''\n",
        "  SELECT team_name, SUM(points) AS total_points\n",
        "    FROM nba_stats\n",
        "    GROUP BY team_name\n",
        "    ORDER BY total_points DESC;\n",
        "'''\n",
        "cursor.execute(query)\n",
        "results = cursor.fetchall()\n",
        "\n",
        "# convert\n",
        "df = pd.DataFrame(results, columns=['Team Name', 'Total Points'])\n",
        "\n",
        "\n",
        "    print(df)\n",
        "\n",
        "        df.plot(x='Team Name', y='Total Points', kind='bar', legend=False, title='Total Points by Team')\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "L1MmX8ftZ5Nk"
      },
      "outputs": [],
      "source": [
        "# going to try and augment another 10 million random player records\n",
        "# i need to update/modify the table schema first to add a 'year' column\n",
        "\n",
        "cursor.execute('''\n",
        "    CREATE TABLE IF NOT EXISTS nba_stats (\n",
        "        id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "        player_name TEXT NOT NULL,\n",
        "        team_name TEXT NOT NULL,\n",
        "        points INTEGER DEFAULT 0,\n",
        "        assists INTEGER DEFAULT 0,\n",
        "        rebounds INTEGER DEFAULT 0,\n",
        "        year INTEGER NOT NULL\n",
        "    )\n",
        "''')\n",
        "conn.commit()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "ZiwhqJlhZ5VB"
      },
      "outputs": [],
      "source": [
        "# updated function to include 'year' column\n",
        "# went back and changed rows from 1 mil to 100,000\n",
        "\n",
        "import random\n",
        "\n",
        "def generate_historical_data(num_records=100000):\n",
        "\n",
        "    teams = [\"Lakers\", \"Warriors\", \"Suns\", \"Bucks\", \"Celtics\", \"Mavericks\", \"Nuggets\", \"Grizzlies\", \"Heat\", \"Clippers\"]\n",
        "\n",
        "    # new synthetic data\n",
        "    data = []\n",
        "    for _ in range(num_records):\n",
        "        player_name = f\"Player_{random.randint(1, num_records)}\"  # random names\n",
        "        team_name = random.choice(teams)\n",
        "        points = random.randint(0, 50)   # points\n",
        "        assists = random.randint(0, 15)  # assists\n",
        "        rebounds = random.randint(0, 20)  # rebounds\n",
        "        year = random.randint(1980, 2024)  # years between 1980 2024\n",
        "        data.append((player_name, team_name, points, assists, rebounds, year))\n",
        "    return data\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "F7kvCAKDogUM",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "e0ea05af-6e34-4999-f4d2-1af75971a470"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Total rows in the database: 1031\n",
            "(1, 'LeBron James', 'Lakers', 35, 8, 7)\n",
            "(2, 'Stephen Curry', 'Warriors', 40, 10, 5)\n",
            "(3, 'Kevin Durant', 'Suns', 25, 6, 9)\n",
            "(4, 'Giannis Antetokounmpo', 'Bucks', 30, 5, 11)\n",
            "(5, 'Jayson Tatum', 'Celtics', 34, 4, 8)\n",
            "(6, 'Luka Doncic', 'Mavericks', 36, 9, 7)\n",
            "(7, 'Nikola Jokic', 'Nuggets', 28, 8, 14)\n",
            "(8, 'Ja Morant', 'Grizzlies', 32, 10, 6)\n",
            "(9, 'Jimmy Butler', 'Heat', 27, 5, 7)\n",
            "(10, 'Kawhi Leonard', 'Clippers', 26, 6, 5)\n",
            "(11, 'Pat Connaughton', 'Bucks', 17, 5, 3)\n",
            "(12, 'Anthony Davis', 'Lakers', 31, 3, 12)\n",
            "(13, 'Damian Lillard', 'Bucks', 29, 8, 4)\n",
            "(14, 'Devin Booker', 'Suns', 26, 5, 5)\n",
            "(15, 'James Harden', 'Clippers', 20, 11, 4)\n",
            "(16, 'Chris Paul', 'Warriors', 18, 12, 3)\n",
            "(17, 'Kyrie Irving', 'Mavericks', 25, 7, 4)\n",
            "(18, 'Joel Embiid', '76ers', 33, 4, 10)\n",
            "(19, 'Zion Williamson', 'Pelicans', 27, 3, 8)\n",
            "(20, 'Trae Young', 'Hawks', 28, 10, 4)\n",
            "(21, 'Paul George', 'Clippers', 24, 6, 6)\n",
            "(22, 'Bradley Beal', 'Suns', 23, 5, 4)\n",
            "(23, 'Jaylen Brown', 'Celtics', 26, 3, 6)\n",
            "(24, 'DeMar DeRozan', 'Bulls', 24, 4, 5)\n",
            "(25, 'Rudy Gobert', 'Timberwolves', 12, 2, 15)\n",
            "(26, 'Karl-Anthony Towns', 'Timberwolves', 23, 3, 9)\n",
            "(27, 'Shai Gilgeous-Alexander', 'Thunder', 31, 6, 4)\n",
            "(28, 'Donovan Mitchell', 'Cavaliers', 28, 5, 4)\n",
            "(29, 'Jamal Murray', 'Nuggets', 23, 6, 4)\n",
            "(30, 'Draymond Green', 'Warriors', 8, 8, 8)\n",
            "(31, 'Andrew Wiggins', 'Warriors', 17, 2, 5)\n",
            "(32, 'Jayson Tatum_0', 'Mavericks', 36, 2, 9)\n",
            "(33, 'Kawhi Leonard_1', 'Celtics', 28, 6, 8)\n",
            "(34, 'Kawhi Leonard_2', 'Lakers', 28, 4, 4)\n",
            "(35, 'Ja Morant_3', 'Grizzlies', 30, 8, 4)\n",
            "(36, 'Luka Dončić_4', 'Mavericks', 34, 7, 4)\n",
            "(37, 'LeBron James_5', 'Nuggets', 34, 6, 10)\n",
            "(38, 'Jimmy Butler_6', 'Thunder', 25, 4, 4)\n",
            "(39, 'Jayson Tatum_7', 'Spurs', 31, 2, 6)\n",
            "(40, 'Luka Dončić_8', 'Jazz', 35, 10, 4)\n",
            "(41, 'Giannis Antetokounmpo_9', 'Knicks', 33, 5, 13)\n",
            "(42, 'Kevin Durant_10', 'Clippers', 28, 6, 6)\n",
            "(43, 'Kevin Durant_11', 'Cavaliers', 29, 5, 10)\n",
            "(44, 'Jimmy Butler_12', 'Warriors', 26, 6, 10)\n",
            "(45, 'Kawhi Leonard_13', 'Cavaliers', 22, 7, 6)\n",
            "(46, 'Pat Connaughton_14', 'Bucks', 22, 6, 6)\n",
            "(47, 'Stephen Curry_15', 'Grizzlies', 42, 8, 4)\n",
            "(48, 'Luka Dončić_16', 'Nuggets', 37, 10, 5)\n",
            "(49, 'Pat Connaughton_17', 'Raptors', 12, 3, 3)\n",
            "(50, 'Luka Dončić_18', 'Nuggets', 41, 11, 10)\n",
            "(51, 'Luka Dončić_19', 'Hawks', 37, 11, 5)\n",
            "(52, 'Jimmy Butler_20', 'Suns', 31, 7, 4)\n",
            "(53, 'Stephen Curry_21', 'Hawks', 37, 11, 4)\n",
            "(54, 'Kawhi Leonard_22', 'Hawks', 22, 8, 6)\n",
            "(55, 'Stephen Curry_23', 'Hawks', 38, 10, 6)\n",
            "(56, 'Stephen Curry_24', 'Suns', 42, 9, 8)\n",
            "(57, 'Kawhi Leonard_25', 'Bulls', 31, 8, 2)\n",
            "(58, 'Luka Dončić_26', 'Bucks', 37, 7, 6)\n",
            "(59, 'Kevin Durant_27', 'Lakers', 20, 8, 12)\n",
            "(60, 'Giannis Antetokounmpo_28', 'Bucks', 35, 7, 8)\n",
            "(61, 'Kevin Durant_29', 'Raptors', 25, 5, 8)\n",
            "(62, 'Kawhi Leonard_30', 'Spurs', 29, 5, 2)\n",
            "(63, 'Giannis Antetokounmpo_31', '76ers', 34, 3, 9)\n",
            "(64, 'Luka Dončić_32', 'Suns', 41, 11, 5)\n",
            "(65, 'Jayson Tatum_33', 'Suns', 37, 2, 8)\n",
            "(66, 'Giannis Antetokounmpo_34', 'Celtics', 31, 4, 14)\n",
            "(67, 'Jimmy Butler_35', 'Clippers', 25, 4, 6)\n",
            "(68, 'Stephen Curry_36', 'Clippers', 35, 8, 8)\n",
            "(69, 'Stephen Curry_37', 'Knicks', 44, 9, 8)\n",
            "(70, 'Kawhi Leonard_38', 'Mavericks', 28, 8, 8)\n",
            "(71, 'Pat Connaughton_39', 'Bucks', 14, 6, 1)\n",
            "(72, 'Jayson Tatum_40', 'Suns', 33, 2, 6)\n",
            "(73, 'Ja Morant_41', 'Knicks', 27, 8, 4)\n",
            "(74, 'Stephen Curry_42', 'Hawks', 43, 11, 2)\n",
            "(75, 'Jimmy Butler_43', 'Lakers', 31, 3, 8)\n",
            "(76, 'Luka Dončić_44', 'Bulls', 33, 11, 9)\n",
            "(77, 'Stephen Curry_45', 'Mavericks', 37, 9, 3)\n",
            "(78, 'Kevin Durant_46', 'Raptors', 30, 6, 9)\n",
            "(79, 'LeBron James_47', 'Lakers', 32, 10, 4)\n",
            "(80, 'Jayson Tatum_48', 'Thunder', 36, 2, 10)\n",
            "(81, 'Pat Connaughton_49', 'Warriors', 16, 3, 4)\n",
            "(82, 'Kevin Durant_50', 'Heat', 21, 4, 11)\n",
            "(83, 'Nikola Jokić_51', 'Raptors', 25, 6, 14)\n",
            "(84, 'LeBron James_52', 'Mavericks', 35, 6, 9)\n",
            "(85, 'Stephen Curry_53', 'Jazz', 43, 11, 4)\n",
            "(86, 'Jimmy Butler_54', 'Raptors', 28, 7, 8)\n",
            "(87, 'Jayson Tatum_55', 'Spurs', 32, 5, 11)\n",
            "(88, 'Nikola Jokić_56', 'Spurs', 24, 8, 14)\n",
            "(89, 'Luka Dončić_57', 'Celtics', 31, 9, 6)\n",
            "(90, 'Pat Connaughton_58', 'Nuggets', 21, 4, 5)\n",
            "(91, 'Stephen Curry_59', '76ers', 45, 8, 3)\n",
            "(92, 'Luka Dončić_60', 'Raptors', 36, 9, 9)\n",
            "(93, 'Pat Connaughton_61', 'Clippers', 12, 7, 2)\n",
            "(94, 'Pat Connaughton_62', 'Bucks', 15, 4, 5)\n",
            "(95, 'Luka Dončić_63', 'Pelicans', 35, 7, 5)\n",
            "(96, 'Kevin Durant_64', 'Pelicans', 24, 5, 9)\n",
            "(97, 'Kevin Durant_65', '76ers', 28, 8, 12)\n",
            "(98, 'Jayson Tatum_66', 'Bulls', 34, 2, 10)\n",
            "(99, 'Stephen Curry_67', 'Heat', 38, 12, 6)\n",
            "(100, 'Jimmy Butler_68', 'Spurs', 29, 7, 5)\n",
            "(101, 'LeBron James_69', 'Hawks', 40, 6, 8)\n",
            "(102, 'Luka Dončić_70', 'Warriors', 34, 7, 9)\n",
            "(103, 'Nikola Jokić_71', 'Warriors', 28, 7, 14)\n",
            "(104, 'Kawhi Leonard_72', 'Grizzlies', 30, 6, 3)\n",
            "(105, 'Kawhi Leonard_73', 'Bucks', 25, 4, 7)\n",
            "(106, 'LeBron James_74', 'Raptors', 32, 6, 6)\n",
            "(107, 'Jimmy Butler_75', 'Knicks', 28, 6, 10)\n",
            "(108, 'Nikola Jokić_76', 'Jazz', 27, 8, 15)\n",
            "(109, 'Jayson Tatum_77', 'Grizzlies', 29, 4, 6)\n",
            "(110, 'Jayson Tatum_78', 'Cavaliers', 36, 5, 7)\n",
            "(111, 'Jimmy Butler_79', 'Clippers', 27, 5, 9)\n",
            "(112, 'Ja Morant_80', 'Suns', 33, 12, 9)\n",
            "(113, 'Jayson Tatum_81', 'Bucks', 30, 4, 11)\n",
            "(114, 'Kevin Durant_82', 'Nuggets', 28, 7, 12)\n",
            "(115, 'LeBron James_83', 'Bucks', 31, 10, 7)\n",
            "(116, 'Nikola Jokić_84', 'Bulls', 25, 8, 13)\n",
            "(117, 'Ja Morant_85', 'Clippers', 37, 9, 7)\n",
            "(118, 'Stephen Curry_86', 'Grizzlies', 43, 10, 2)\n",
            "(119, 'Luka Dončić_87', 'Celtics', 36, 8, 4)\n",
            "(120, 'Ja Morant_88', '76ers', 37, 9, 6)\n",
            "(121, 'Stephen Curry_89', 'Warriors', 37, 12, 5)\n",
            "(122, 'Jayson Tatum_90', 'Pelicans', 34, 2, 6)\n",
            "(123, 'Ja Morant_91', '76ers', 35, 11, 9)\n",
            "(124, 'Stephen Curry_92', 'Warriors', 44, 11, 3)\n",
            "(125, 'Jayson Tatum_93', 'Celtics', 30, 4, 8)\n",
            "(126, 'Stephen Curry_94', 'Lakers', 45, 10, 6)\n",
            "(127, 'Luka Dončić_95', 'Bucks', 40, 10, 9)\n",
            "(128, 'Giannis Antetokounmpo_96', 'Celtics', 29, 3, 9)\n",
            "(129, 'LeBron James_97', 'Clippers', 33, 9, 5)\n",
            "(130, 'Kevin Durant_98', 'Mavericks', 23, 4, 12)\n",
            "(131, 'Ja Morant_99', 'Suns', 32, 11, 6)\n",
            "(132, 'Kevin Durant_100', 'Heat', 28, 7, 10)\n",
            "(133, 'Kawhi Leonard_101', '76ers', 29, 5, 3)\n",
            "(134, 'Giannis Antetokounmpo_102', 'Warriors', 28, 3, 14)\n",
            "(135, 'Giannis Antetokounmpo_103', 'Pelicans', 30, 6, 10)\n",
            "(136, 'Pat Connaughton_104', 'Raptors', 21, 7, 2)\n",
            "(137, 'Jayson Tatum_105', 'Bucks', 32, 2, 6)\n",
            "(138, 'Kawhi Leonard_106', 'Celtics', 22, 6, 8)\n",
            "(139, 'Stephen Curry_107', 'Knicks', 40, 9, 4)\n",
            "(140, 'Jayson Tatum_108', 'Nuggets', 32, 4, 5)\n",
            "(141, 'Jayson Tatum_109', 'Grizzlies', 32, 3, 9)\n",
            "(142, 'Pat Connaughton_110', 'Jazz', 22, 6, 2)\n",
            "(143, 'Jayson Tatum_111', 'Celtics', 39, 2, 8)\n",
            "(144, 'Nikola Jokić_112', 'Jazz', 32, 9, 16)\n",
            "(145, 'Giannis Antetokounmpo_113', '76ers', 32, 3, 8)\n",
            "(146, 'Stephen Curry_114', 'Grizzlies', 45, 12, 8)\n",
            "(147, 'Pat Connaughton_115', 'Jazz', 15, 7, 6)\n",
            "(148, 'Ja Morant_116', 'Heat', 28, 11, 8)\n",
            "(149, 'Stephen Curry_117', 'Mavericks', 37, 8, 7)\n",
            "(150, 'Kevin Durant_118', 'Cavaliers', 30, 4, 9)\n",
            "(151, 'Stephen Curry_119', 'Celtics', 35, 12, 2)\n",
            "(152, 'Stephen Curry_120', 'Spurs', 44, 9, 4)\n",
            "(153, 'Giannis Antetokounmpo_121', 'Clippers', 31, 5, 8)\n",
            "(154, 'Stephen Curry_122', 'Nuggets', 35, 9, 6)\n",
            "(155, 'Luka Dončić_123', 'Warriors', 31, 9, 5)\n",
            "(156, 'Nikola Jokić_124', 'Knicks', 23, 8, 12)\n",
            "(157, 'Jayson Tatum_125', '76ers', 35, 6, 6)\n",
            "(158, 'Jimmy Butler_126', 'Jazz', 24, 6, 4)\n",
            "(159, 'Giannis Antetokounmpo_127', 'Bucks', 35, 3, 12)\n",
            "(160, 'Luka Dončić_128', 'Celtics', 41, 7, 6)\n",
            "(161, 'Luka Dončić_129', 'Clippers', 33, 11, 4)\n",
            "(162, 'Jayson Tatum_130', 'Pelicans', 36, 4, 9)\n",
            "(163, 'Kevin Durant_131', 'Suns', 26, 8, 6)\n",
            "(164, 'Jayson Tatum_132', '76ers', 29, 6, 7)\n",
            "(165, 'Kevin Durant_133', 'Clippers', 23, 6, 6)\n",
            "(166, 'Stephen Curry_134', 'Knicks', 37, 8, 8)\n",
            "(167, 'Ja Morant_135', 'Heat', 30, 9, 4)\n",
            "(168, 'Ja Morant_136', 'Clippers', 34, 10, 7)\n",
            "(169, 'Ja Morant_137', 'Heat', 35, 11, 6)\n",
            "(170, 'Jimmy Butler_138', 'Cavaliers', 24, 6, 8)\n",
            "(171, 'Kevin Durant_139', 'Bucks', 23, 4, 7)\n",
            "(172, 'LeBron James_140', 'Nuggets', 32, 9, 8)\n",
            "(173, 'LeBron James_141', 'Clippers', 33, 10, 4)\n",
            "(174, 'Kevin Durant_142', 'Mavericks', 21, 7, 9)\n",
            "(175, 'Kevin Durant_143', 'Thunder', 25, 6, 12)\n",
            "(176, 'Nikola Jokić_144', 'Jazz', 31, 6, 16)\n",
            "(177, 'Jayson Tatum_145', 'Raptors', 30, 4, 6)\n",
            "(178, 'Nikola Jokić_146', 'Mavericks', 31, 7, 14)\n",
            "(179, 'Ja Morant_147', 'Jazz', 34, 9, 8)\n",
            "(180, 'Kevin Durant_148', 'Bulls', 23, 4, 9)\n",
            "(181, 'Kevin Durant_149', 'Hawks', 24, 8, 12)\n",
            "(182, 'Stephen Curry_150', 'Cavaliers', 43, 9, 7)\n",
            "(183, 'LeBron James_151', 'Thunder', 36, 6, 8)\n",
            "(184, 'Pat Connaughton_152', 'Clippers', 15, 3, 1)\n",
            "(185, 'Kevin Durant_153', 'Cavaliers', 22, 8, 11)\n",
            "(186, 'Luka Dončić_154', 'Spurs', 41, 9, 8)\n",
            "(187, 'Kawhi Leonard_155', 'Clippers', 23, 8, 8)\n",
            "(188, 'LeBron James_156', 'Thunder', 30, 8, 7)\n",
            "(189, 'Nikola Jokić_157', 'Mavericks', 25, 8, 14)\n",
            "(190, 'LeBron James_158', 'Nuggets', 37, 10, 9)\n",
            "(191, 'Luka Dončić_159', 'Raptors', 34, 10, 6)\n",
            "(192, 'Nikola Jokić_160', 'Thunder', 28, 7, 16)\n",
            "(193, 'Jimmy Butler_161', 'Bulls', 28, 7, 8)\n",
            "(194, 'Luka Dončić_162', 'Warriors', 33, 7, 7)\n",
            "(195, 'Giannis Antetokounmpo_163', 'Grizzlies', 35, 7, 9)\n",
            "(196, 'Nikola Jokić_164', 'Thunder', 23, 6, 14)\n",
            "(197, 'Stephen Curry_165', 'Mavericks', 44, 9, 4)\n",
            "(198, 'Giannis Antetokounmpo_166', 'Celtics', 25, 6, 11)\n",
            "(199, 'Stephen Curry_167', 'Thunder', 36, 11, 2)\n",
            "(200, 'Kawhi Leonard_168', 'Nuggets', 30, 8, 8)\n",
            "(201, 'LeBron James_169', 'Suns', 36, 9, 9)\n",
            "(202, 'Ja Morant_170', 'Suns', 31, 10, 6)\n",
            "(203, 'Ja Morant_171', 'Spurs', 34, 8, 5)\n",
            "(204, 'Jimmy Butler_172', 'Spurs', 28, 5, 6)\n",
            "(205, 'Jayson Tatum_173', 'Bulls', 30, 5, 8)\n",
            "(206, 'Pat Connaughton_174', 'Suns', 18, 5, 4)\n",
            "(207, 'Ja Morant_175', 'Bucks', 36, 11, 3)\n",
            "(208, 'Jimmy Butler_176', 'Cavaliers', 24, 3, 7)\n",
            "(209, 'Kevin Durant_177', 'Nuggets', 23, 7, 6)\n",
            "(210, 'Jayson Tatum_178', 'Spurs', 33, 2, 5)\n",
            "(211, 'Pat Connaughton_179', 'Grizzlies', 22, 7, 2)\n",
            "(212, 'Kawhi Leonard_180', 'Jazz', 30, 5, 3)\n",
            "(213, 'Jayson Tatum_181', 'Spurs', 32, 5, 8)\n",
            "(214, 'Nikola Jokić_182', 'Suns', 33, 9, 13)\n",
            "(215, 'Stephen Curry_183', 'Celtics', 41, 9, 6)\n",
            "(216, 'Nikola Jokić_184', 'Grizzlies', 23, 6, 14)\n",
            "(217, 'Nikola Jokić_185', 'Clippers', 23, 6, 15)\n",
            "(218, 'LeBron James_186', 'Thunder', 37, 6, 10)\n",
            "(219, 'Nikola Jokić_187', 'Bulls', 26, 7, 13)\n",
            "(220, 'Nikola Jokić_188', 'Cavaliers', 33, 9, 13)\n",
            "(221, 'Nikola Jokić_189', 'Raptors', 27, 10, 15)\n",
            "(222, 'Pat Connaughton_190', 'Mavericks', 13, 4, 5)\n",
            "(223, 'Giannis Antetokounmpo_191', 'Knicks', 27, 4, 12)\n",
            "(224, 'Jayson Tatum_192', 'Heat', 36, 4, 5)\n",
            "(225, 'Ja Morant_193', 'Pelicans', 29, 9, 9)\n",
            "(226, 'Pat Connaughton_194', 'Nuggets', 20, 5, 0)\n",
            "(227, 'Pat Connaughton_195', 'Lakers', 20, 7, 5)\n",
            "(228, 'Giannis Antetokounmpo_196', 'Nuggets', 35, 5, 10)\n",
            "(229, 'Kevin Durant_197', 'Hawks', 23, 6, 8)\n",
            "(230, 'Giannis Antetokounmpo_198', 'Pelicans', 27, 6, 12)\n",
            "(231, 'Giannis Antetokounmpo_199', 'Knicks', 30, 6, 13)\n",
            "(232, 'Kevin Durant_200', 'Warriors', 23, 6, 8)\n",
            "(233, 'Jayson Tatum_201', 'Knicks', 31, 3, 10)\n",
            "(234, 'Nikola Jokić_202', 'Celtics', 24, 6, 16)\n",
            "(235, 'Kawhi Leonard_203', 'Hawks', 28, 6, 5)\n",
            "(236, 'Kawhi Leonard_204', 'Suns', 27, 5, 6)\n",
            "(237, 'LeBron James_205', 'Cavaliers', 32, 10, 10)\n",
            "(238, 'LeBron James_206', 'Raptors', 38, 6, 7)\n",
            "(239, 'Giannis Antetokounmpo_207', 'Raptors', 27, 5, 13)\n",
            "(240, 'Kawhi Leonard_208', '76ers', 21, 4, 5)\n",
            "(241, 'Nikola Jokić_209', 'Nuggets', 29, 8, 14)\n",
            "(242, 'Kawhi Leonard_210', 'Mavericks', 26, 7, 4)\n",
            "(243, 'LeBron James_211', 'Knicks', 36, 9, 9)\n",
            "(244, 'Kevin Durant_212', 'Mavericks', 21, 7, 10)\n",
            "(245, 'Luka Dončić_213', 'Jazz', 40, 11, 9)\n",
            "(246, 'Stephen Curry_214', 'Grizzlies', 36, 9, 7)\n",
            "(247, 'Nikola Jokić_215', 'Grizzlies', 28, 6, 16)\n",
            "(248, 'Jimmy Butler_216', 'Jazz', 22, 7, 5)\n",
            "(249, 'Stephen Curry_217', 'Warriors', 45, 10, 6)\n",
            "(250, 'Giannis Antetokounmpo_218', 'Grizzlies', 30, 3, 10)\n"
          ]
        }
      ],
      "source": [
        "# count total rows in table\n",
        "cursor.execute('SELECT COUNT(*) FROM nba_stats')\n",
        "total_rows = cursor.fetchone()[0]\n",
        "print(f\"Total rows in the database: {total_rows}\")\n",
        "\n",
        "# query sample of the data\n",
        "cursor.execute('SELECT * FROM nba_stats LIMIT 250')\n",
        "sample_rows = cursor.fetchall()\n",
        "for row in sample_rows:\n",
        "    print(row)\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2Q1nPOwTpPJk"
      },
      "source": [
        "Here we can see that the data augmentation is running correctly. Players have been duplicated exponentially and assigned individual keys to serve as unique identifiers. My plan is to run advanced analytics with some machine learning frameworks. First I have to add more variables to create a more cohesive dataframe:\n",
        "\n",
        "Age: Player's age at the time of the season.\n",
        "\n",
        "Experience: Number of years in the league.\n",
        "\n",
        "Position: Player's primary position (PG, SG, SF, PF, C).\n",
        "\n",
        "Injury History: Indicator of past injuries and their impact on performance."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "JLJsOR1_30Bc"
      },
      "outputs": [],
      "source": [
        "# adding new columns for age, experience, position, injusry history\n",
        "\n",
        "conn = sqlite3.connect(':memory:')\n",
        "cursor = conn.cursor()\n",
        "\n",
        "\n",
        "cursor.execute('''\n",
        "    CREATE TABLE IF NOT EXISTS nba_stats (\n",
        "        id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "        player_name TEXT NOT NULL,\n",
        "        team_name TEXT NOT NULL,\n",
        "        points INTEGER DEFAULT 0,\n",
        "        assists INTEGER DEFAULT 0,\n",
        "        rebounds INTEGER DEFAULT 0,\n",
        "        year INTEGER NOT NULL,\n",
        "        age INTEGER,\n",
        "        experience INTEGER,\n",
        "        position TEXT,\n",
        "        injury_history TEXT\n",
        "    )\n",
        "''')\n",
        "\n",
        "# insert data into the table (replace placeholders with actual data)\n",
        "cursor.execute('''\n",
        "    INSERT INTO nba_stats (player_name, team_name, points, assists, rebounds, year, age, experience, position, injury_history)\n",
        "    VALUES ('LeBron James', 'Lakers', 35, 8, 7, 2023, 38, 21, 'SF', 'Multiple injuries, including ankle and knee')\n",
        "''')\n",
        "\n",
        "# commit the changes and close the connection\n",
        "conn.commit()\n",
        "conn.close()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "_7xAau9l4w2k"
      },
      "source": [
        "With these new columns added, now the database is more cohesive. I was planning to build a prediction model based on these 10,000,000+ datapoints and see if this augmented historical data i created is able to provide any interesting randomized insights."
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Augmenting and then processing and trying to print this much information used:\n",
        "\n",
        "RAM: 3.87 GB/12.67 GB\n",
        "Disk: 32.47 GB/107.72 GB\n",
        "\n",
        "On the Python 3 Google Compute Engine backend\n",
        "\n",
        "\n",
        "I need to go back and create less data as this completely crashed the colab file. If I subscribed to the service this would be more likely to run...  I'll try to optimize the size so I don't use all my available compute on this subscription plan"
      ],
      "metadata": {
        "id": "-ShC7xLz7Gqs"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "Now I will regenerate a more realistic database size that won't break the cloud. I went back and updated to 100,000 rows"
      ],
      "metadata": {
        "id": "SSn9CkgX8Pr6"
      }
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "pZ5hMccjpM7z"
      },
      "outputs": [],
      "source": [
  
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "cF803Bl2pNDH"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "V7lZxkS8pNKk"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "lTUalRtWpNRW"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "1lcmYgoVpNZQ"
      },
      "outputs": [],
      "source": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOIHeH+yKFmoRqcoarGRLZk",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
