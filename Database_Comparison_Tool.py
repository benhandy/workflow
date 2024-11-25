{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/twoandhalfben/workflow/blob/main/Database_Comparison_Tool.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "1CJK3ZJslhhj"
      },
      "outputs": [],
      "source": [
        "## This is a tool to compare multiple Excel databases\n",
        "## It detects discrepancies and overlaps, displaying the exact location of where things have changed\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "q0KZoK66DZi1"
      },
      "outputs": [],
      "source": [
        "import pandas as pd"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "2fhMZbg5Ea01",
        "outputId": "dac7b67e-cec1-48e8-8839-82919c611f81"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Requirement already satisfied: pandas in /usr/local/lib/python3.10/dist-packages (2.2.2)\n",
            "Requirement already satisfied: openpyxl in /usr/local/lib/python3.10/dist-packages (3.1.5)\n",
            "Requirement already satisfied: numpy>=1.22.4 in /usr/local/lib/python3.10/dist-packages (from pandas) (1.26.4)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.10/dist-packages (from pandas) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.10/dist-packages (from pandas) (2024.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.10/dist-packages (from pandas) (2024.2)\n",
            "Requirement already satisfied: et-xmlfile in /usr/local/lib/python3.10/dist-packages (from openpyxl) (1.1.0)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil>=2.8.2->pandas) (1.16.0)\n"
          ]
        }
      ],
      "source": [
        "!pip install pandas openpyxl\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "background_save": true,
          "base_uri": "https://localhost:8080/",
          "height": 38
        },
        "id": "Tctq3RxQEGVL",
        "outputId": "c9257df5-6c61-4370-8b1c-7f5e2e6dfaf7"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "\n",
              "     <input type=\"file\" id=\"files-0670f27b-3df7-4364-9c7d-a1aee5f741fc\" name=\"files[]\" multiple disabled\n",
              "        style=\"border:none\" />\n",
              "     <output id=\"result-0670f27b-3df7-4364-9c7d-a1aee5f741fc\">\n",
              "      Upload widget is only available when the cell has been executed in the\n",
              "      current browser session. Please rerun this cell to enable.\n",
              "      </output>\n",
              "      <script>// Copyright 2017 Google LLC\n",
              "//\n",
              "// Licensed under the Apache License, Version 2.0 (the \"License\");\n",
              "// you may not use this file except in compliance with the License.\n",
              "// You may obtain a copy of the License at\n",
              "//\n",
              "//      http://www.apache.org/licenses/LICENSE-2.0\n",
              "//\n",
              "// Unless required by applicable law or agreed to in writing, software\n",
              "// distributed under the License is distributed on an \"AS IS\" BASIS,\n",
              "// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n",
              "// See the License for the specific language governing permissions and\n",
              "// limitations under the License.\n",
              "\n",
              "/**\n",
              " * @fileoverview Helpers for google.colab Python module.\n",
              " */\n",
              "(function(scope) {\n",
              "function span(text, styleAttributes = {}) {\n",
              "  const element = document.createElement('span');\n",
              "  element.textContent = text;\n",
              "  for (const key of Object.keys(styleAttributes)) {\n",
              "    element.style[key] = styleAttributes[key];\n",
              "  }\n",
              "  return element;\n",
              "}\n",
              "\n",
              "// Max number of bytes which will be uploaded at a time.\n",
              "const MAX_PAYLOAD_SIZE = 100 * 1024;\n",
              "\n",
              "function _uploadFiles(inputId, outputId) {\n",
              "  const steps = uploadFilesStep(inputId, outputId);\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  // Cache steps on the outputElement to make it available for the next call\n",
              "  // to uploadFilesContinue from Python.\n",
              "  outputElement.steps = steps;\n",
              "\n",
              "  return _uploadFilesContinue(outputId);\n",
              "}\n",
              "\n",
              "// This is roughly an async generator (not supported in the browser yet),\n",
              "// where there are multiple asynchronous steps and the Python side is going\n",
              "// to poll for completion of each step.\n",
              "// This uses a Promise to block the python side on completion of each step,\n",
              "// then passes the result of the previous step as the input to the next step.\n",
              "function _uploadFilesContinue(outputId) {\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  const steps = outputElement.steps;\n",
              "\n",
              "  const next = steps.next(outputElement.lastPromiseValue);\n",
              "  return Promise.resolve(next.value.promise).then((value) => {\n",
              "    // Cache the last promise value to make it available to the next\n",
              "    // step of the generator.\n",
              "    outputElement.lastPromiseValue = value;\n",
              "    return next.value.response;\n",
              "  });\n",
              "}\n",
              "\n",
              "/**\n",
              " * Generator function which is called between each async step of the upload\n",
              " * process.\n",
              " * @param {string} inputId Element ID of the input file picker element.\n",
              " * @param {string} outputId Element ID of the output display.\n",
              " * @return {!Iterable<!Object>} Iterable of next steps.\n",
              " */\n",
              "function* uploadFilesStep(inputId, outputId) {\n",
              "  const inputElement = document.getElementById(inputId);\n",
              "  inputElement.disabled = false;\n",
              "\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  outputElement.innerHTML = '';\n",
              "\n",
              "  const pickedPromise = new Promise((resolve) => {\n",
              "    inputElement.addEventListener('change', (e) => {\n",
              "      resolve(e.target.files);\n",
              "    });\n",
              "  });\n",
              "\n",
              "  const cancel = document.createElement('button');\n",
              "  inputElement.parentElement.appendChild(cancel);\n",
              "  cancel.textContent = 'Cancel upload';\n",
              "  const cancelPromise = new Promise((resolve) => {\n",
              "    cancel.onclick = () => {\n",
              "      resolve(null);\n",
              "    };\n",
              "  });\n",
              "\n",
              "  // Wait for the user to pick the files.\n",
              "  const files = yield {\n",
              "    promise: Promise.race([pickedPromise, cancelPromise]),\n",
              "    response: {\n",
              "      action: 'starting',\n",
              "    }\n",
              "  };\n",
              "\n",
              "  cancel.remove();\n",
              "\n",
              "  // Disable the input element since further picks are not allowed.\n",
              "  inputElement.disabled = true;\n",
              "\n",
              "  if (!files) {\n",
              "    return {\n",
              "      response: {\n",
              "        action: 'complete',\n",
              "      }\n",
              "    };\n",
              "  }\n",
              "\n",
              "  for (const file of files) {\n",
              "    const li = document.createElement('li');\n",
              "    li.append(span(file.name, {fontWeight: 'bold'}));\n",
              "    li.append(span(\n",
              "        `(${file.type || 'n/a'}) - ${file.size} bytes, ` +\n",
              "        `last modified: ${\n",
              "            file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() :\n",
              "                                    'n/a'} - `));\n",
              "    const percent = span('0% done');\n",
              "    li.appendChild(percent);\n",
              "\n",
              "    outputElement.appendChild(li);\n",
              "\n",
              "    const fileDataPromise = new Promise((resolve) => {\n",
              "      const reader = new FileReader();\n",
              "      reader.onload = (e) => {\n",
              "        resolve(e.target.result);\n",
              "      };\n",
              "      reader.readAsArrayBuffer(file);\n",
              "    });\n",
              "    // Wait for the data to be ready.\n",
              "    let fileData = yield {\n",
              "      promise: fileDataPromise,\n",
              "      response: {\n",
              "        action: 'continue',\n",
              "      }\n",
              "    };\n",
              "\n",
              "    // Use a chunked sending to avoid message size limits. See b/62115660.\n",
              "    let position = 0;\n",
              "    do {\n",
              "      const length = Math.min(fileData.byteLength - position, MAX_PAYLOAD_SIZE);\n",
              "      const chunk = new Uint8Array(fileData, position, length);\n",
              "      position += length;\n",
              "\n",
              "      const base64 = btoa(String.fromCharCode.apply(null, chunk));\n",
              "      yield {\n",
              "        response: {\n",
              "          action: 'append',\n",
              "          file: file.name,\n",
              "          data: base64,\n",
              "        },\n",
              "      };\n",
              "\n",
              "      let percentDone = fileData.byteLength === 0 ?\n",
              "          100 :\n",
              "          Math.round((position / fileData.byteLength) * 100);\n",
              "      percent.textContent = `${percentDone}% done`;\n",
              "\n",
              "    } while (position < fileData.byteLength);\n",
              "  }\n",
              "\n",
              "  // All done.\n",
              "  yield {\n",
              "    response: {\n",
              "      action: 'complete',\n",
              "    }\n",
              "  };\n",
              "}\n",
              "\n",
              "scope.google = scope.google || {};\n",
              "scope.google.colab = scope.google.colab || {};\n",
              "scope.google.colab._files = {\n",
              "  _uploadFiles,\n",
              "  _uploadFilesContinue,\n",
              "};\n",
              "})(self);\n",
              "</script> "
            ],
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "ename": "TypeError",
          "evalue": "'NoneType' object is not subscriptable",
          "output_type": "error",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-3-49432676dcaa>\u001b[0m in \u001b[0;36m<cell line: 2>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcolab\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mfiles\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0muploaded\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mfiles\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mupload\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/google/colab/files.py\u001b[0m in \u001b[0;36mupload\u001b[0;34m()\u001b[0m\n\u001b[1;32m     67\u001b[0m   \"\"\"\n\u001b[1;32m     68\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 69\u001b[0;31m   \u001b[0muploaded_files\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0m_upload_files\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmultiple\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     70\u001b[0m   \u001b[0;31m# Mapping from original filename to filename as saved locally.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     71\u001b[0m   \u001b[0mlocal_filenames\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdict\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/google/colab/files.py\u001b[0m in \u001b[0;36m_upload_files\u001b[0;34m(multiple)\u001b[0m\n\u001b[1;32m    161\u001b[0m   \u001b[0mfiles\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0m_collections\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdefaultdict\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbytes\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    162\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 163\u001b[0;31m   \u001b[0;32mwhile\u001b[0m \u001b[0mresult\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'action'\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m!=\u001b[0m \u001b[0;34m'complete'\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    164\u001b[0m     result = _output.eval_js(\n\u001b[1;32m    165\u001b[0m         'google.colab._files._uploadFilesContinue(\"{output_id}\")'.format(\n",
            "\u001b[0;31mTypeError\u001b[0m: 'NoneType' object is not subscriptable"
          ]
        }
      ],
      "source": [
        "from google.colab import files\n",
        "uploaded=files.upload()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Vq0xAdiGHlzl",
        "outputId": "99cc9d8d-ce7d-43f2-e646-1ecef9dcaf8e"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Uploaded file names: dict_keys(['elevator_inspections.xlsx'])\n"
          ]
        }
      ],
      "source": [
        "file_name = 'building_list.xlsx'\n",
        "print(\"Uploaded file names:\", uploaded.keys())\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GuYRsTdhpCUq",
        "outputId": "afb29e14-c14e-40a1-9da9-c38d69435702"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Uploaded file names: dict_keys(['elevator_inspections.xlsx'])\n"
          ]
        }
      ],
      "source": [
        "file_name = 'elevator_inspections.xlsx'\n",
        "print(\"Uploaded file names:\", uploaded.keys())"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "s9KhKKiPJyrJ"
      },
      "outputs": [],
      "source": [
        "df = pd.read_excel('building_list.xlsx')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_EanmR7tIb1P",
        "outputId": "a0983336-62ed-40b0-9553-3172ec189f4d"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "   Building Number       BIN                                         Address\n",
            "0              336   1033951                              334 West 87 Street\n",
            "1          FLS0290    ID1111                                 605 NE 193rd St\n",
            "2          FLS0292    ID1112                              780 NE 69th Street\n",
            "3              294   2083244                             2400 Johnson Avenue\n",
            "4              272   1079476                                   2790 Broadway\n",
            "5              246   1070362                                   2000 Broadway\n",
            "6              288   3002556                            85 Livingston Street\n",
            "7              508   3397571                                505 Court Street\n",
            "8          822/824   1028630       40 West 72 Street (Bancroft Owners, Inc.)\n",
            "9              NaN  1028630A  40 West 72 Street (Bancroft Hotel Condominium)\n",
            "10             758   1034856                               77 West 55 Street\n",
            "11             300   1088559                              300 East 23 Street\n",
            "12             506   3062881                                500 Grand Street\n",
            "13             NaN   3069499                                530 Grand Street\n",
            "14             NaN   3069505                                550 Grand Street\n",
            "15             292   1019089                            310 Lexington Avenue\n",
            "16             358   1045391                              401 East 65 Street\n",
            "17             662   1008977                                    111 4 Avenue\n",
            "18             098   4446686                               14-01 Bonnie Lane\n",
            "19             NaN   4446688                             14-01 Michael Place\n"
          ]
        }
      ],
      "source": [
        "print(df.head(20))\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "_REaPXpDrnCz"
      },
      "outputs": [],
      "source": [
        "df = pd.read_excel('elevator_inspections.xlsx')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GkxpOHO2rvX4",
        "outputId": "f2d9fdbc-991d-4eb0-d31e-ecc7021d8626"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "   Building Number  BIN              Address\n",
            "0          NYR0102  NaN       3-11 27 Avenue\n",
            "1              722  NaN      41-05 29 Street\n",
            "2              722  NaN      41-05 29 Street\n",
            "3         SCH119E7  NaN   119 East 74 Street\n",
            "4              568  NaN  160 West 66 Street \n",
            "5              568  NaN   160 West 66 Street\n",
            "6              568  NaN  160 West 66 Street \n",
            "7              568  NaN   160 West 66 Street\n",
            "8              568  NaN  160 West 66 Street \n",
            "9              568  NaN  160 West 66 Street \n",
            "10             568  NaN   160 West 66 Street\n",
            "11        SCH510WA  NaN   510 Waverly Avenue\n",
            "12             696  NaN   101 West 80 Street\n",
            "13              52  NaN   151 Wooster Street\n",
            "14              52  NaN   151 Wooster Street\n",
            "15             446  NaN     187 Hicks Street\n",
            "16        NYC10548  NaN    32 West 18 Street\n",
            "17        NYC10548  NaN    32 West 18 Street\n",
            "18        NYC10276  NaN     325 Fifth Avenue\n",
            "19        NYC10276  NaN     325 Fifth Avenue\n"
          ]
        }
      ],
      "source": [
        "print(df.head(20))\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "MkS2WclVIs5e"
      },
      "outputs": [],
      "source": [
        "file1 = 'elevator_inspections.xlsx'\n",
        "file2 = 'building_list.xlsx'"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "lk4cqNLPbJm1"
      },
      "outputs": [],
      "source": [
        "sheet_name1 = 'dataset_1'"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "D9BJ3Sh3bZnW"
      },
      "outputs": [],
      "source": [
        "sheet_name2='Mastersheet'"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "cs6XBucobgxu"
      },
      "outputs": [],
      "source": [
        "df1 = pd.read_excel(file2, sheet_name= sheet_name1)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "PzjmE8KVdTZo"
      },
      "outputs": [],
      "source": [
        "df2 = pd.read_excel(file1, sheet_name= sheet_name2)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "dYE5pr9LqUcU"
      },
      "outputs": [],
      "source": [
        "key_columns = ['Building Number', 'BIN', 'Address']\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Ii28gObwrGwj",
        "outputId": "77009390-1b88-4c1c-b13f-5e921f815962"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Column names in df1: Index(['Building Number', 'BIN', 'Address'], dtype='object')\n",
            "Column names in df2: Index(['Building Number', 'BIN', 'Address'], dtype='object')\n"
          ]
        }
      ],
      "source": [
        "print(\"Column names in df1:\", df1.columns)\n",
        "print(\"Column names in df2:\", df2.columns)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "58rzrWmstrl9",
        "outputId": "f2768720-69c0-4523-c0e5-9d62f97a169b"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Data types in df1: Building Number    object\n",
            "BIN                object\n",
            "Address            object\n",
            "dtype: object\n",
            "Data types in df2: Building Number     object\n",
            "BIN                float64\n",
            "Address             object\n",
            "dtype: object\n"
          ]
        }
      ],
      "source": [
        "print(\"Data types in df1:\", df1[key_columns].dtypes)\n",
        "print(\"Data types in df2:\", df2[key_columns].dtypes)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "nitrLli2uA2a"
      },
      "outputs": [],
      "source": [
        "df2['BIN'] = df2['BIN'].astype(str)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "osfp8YGntX28"
      },
      "outputs": [],
      "source": [
        "merged_df = pd.merge(df1, df2, on=key_columns, how='outer', indicator=True)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "_r8oK5eYuULN"
      },
      "outputs": [],
      "source": [
        "discrepancies = merged_df[merged_df['_merge'] != 'both']\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "Yr2mCL5Kpn-L"
      },
      "outputs": [],
      "source": [
        "if set(df1.columns) != set(df2.columns):\n",
        "    raise ValueError"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "OanakdVuuWvt",
        "outputId": "bb2b2a93-e24d-4f7c-be69-6f34f2be1a7c"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Discrepancies found:\n",
            "     Building Number      BIN                               Address  \\\n",
            "0                336  1033951                    334 West 87 Street   \n",
            "1            FLS0290   ID1111                       605 NE 193rd St   \n",
            "2            FLS0292   ID1112                    780 NE 69th Street   \n",
            "3                294  2083244                   2400 Johnson Avenue   \n",
            "4                272  1079476                         2790 Broadway   \n",
            "...              ...      ...                                   ...   \n",
            "1958        NYC10030      nan  The Promenade | 530 East 76th Street   \n",
            "1959        NYC10030      nan  The Promenade | 530 East 76th Street   \n",
            "1960             400      nan  211 West 61st Street  (Ashtin Group)   \n",
            "1961             400      nan  211 West 61st Street  (Ashtin Group)   \n",
            "1962         NYO1061      nan                     137 Second Avenue   \n",
            "\n",
            "          _merge  \n",
            "0      left_only  \n",
            "1      left_only  \n",
            "2      left_only  \n",
            "3      left_only  \n",
            "4      left_only  \n",
            "...          ...  \n",
            "1958  right_only  \n",
            "1959  right_only  \n",
            "1960  right_only  \n",
            "1961  right_only  \n",
            "1962  right_only  \n",
            "\n",
            "[1963 rows x 4 columns]\n"
          ]
        }
      ],
      "source": [
        "print(\"Discrepancies found:\")\n",
        "print(discrepancies)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "kWOmTgCUn7gw"
      },
      "outputs": [],
      "source": [
        "import pandas as pd\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "3FTJEJ04oomI"
      },
      "outputs": [],
      "source": [
        "from google.colab import files\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "0zxaUBCWosgU"
      },
      "outputs": [],
      "source": [
        "uploaded=files.upload"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 144
        },
        "id": "_1z2kXNwnwaQ",
        "outputId": "ca51eab4-8a3a-4964-e171-048c67793ac1"
      },
      "outputs": [
        {
          "data": {
            "text/html": [
              "\n",
              "     <input type=\"file\" id=\"files-028c5fe3-bd71-45e7-8292-0f06b591cbde\" name=\"files[]\" multiple disabled\n",
              "        style=\"border:none\" />\n",
              "     <output id=\"result-028c5fe3-bd71-45e7-8292-0f06b591cbde\">\n",
              "      Upload widget is only available when the cell has been executed in the\n",
              "      current browser session. Please rerun this cell to enable.\n",
              "      </output>\n",
              "      <script>// Copyright 2017 Google LLC\n",
              "//\n",
              "// Licensed under the Apache License, Version 2.0 (the \"License\");\n",
              "// you may not use this file except in compliance with the License.\n",
              "// You may obtain a copy of the License at\n",
              "//\n",
              "//      http://www.apache.org/licenses/LICENSE-2.0\n",
              "//\n",
              "// Unless required by applicable law or agreed to in writing, software\n",
              "// distributed under the License is distributed on an \"AS IS\" BASIS,\n",
              "// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n",
              "// See the License for the specific language governing permissions and\n",
              "// limitations under the License.\n",
              "\n",
              "/**\n",
              " * @fileoverview Helpers for google.colab Python module.\n",
              " */\n",
              "(function(scope) {\n",
              "function span(text, styleAttributes = {}) {\n",
              "  const element = document.createElement('span');\n",
              "  element.textContent = text;\n",
              "  for (const key of Object.keys(styleAttributes)) {\n",
              "    element.style[key] = styleAttributes[key];\n",
              "  }\n",
              "  return element;\n",
              "}\n",
              "\n",
              "// Max number of bytes which will be uploaded at a time.\n",
              "const MAX_PAYLOAD_SIZE = 100 * 1024;\n",
              "\n",
              "function _uploadFiles(inputId, outputId) {\n",
              "  const steps = uploadFilesStep(inputId, outputId);\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  // Cache steps on the outputElement to make it available for the next call\n",
              "  // to uploadFilesContinue from Python.\n",
              "  outputElement.steps = steps;\n",
              "\n",
              "  return _uploadFilesContinue(outputId);\n",
              "}\n",
              "\n",
              "// This is roughly an async generator (not supported in the browser yet),\n",
              "// where there are multiple asynchronous steps and the Python side is going\n",
              "// to poll for completion of each step.\n",
              "// This uses a Promise to block the python side on completion of each step,\n",
              "// then passes the result of the previous step as the input to the next step.\n",
              "function _uploadFilesContinue(outputId) {\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  const steps = outputElement.steps;\n",
              "\n",
              "  const next = steps.next(outputElement.lastPromiseValue);\n",
              "  return Promise.resolve(next.value.promise).then((value) => {\n",
              "    // Cache the last promise value to make it available to the next\n",
              "    // step of the generator.\n",
              "    outputElement.lastPromiseValue = value;\n",
              "    return next.value.response;\n",
              "  });\n",
              "}\n",
              "\n",
              "/**\n",
              " * Generator function which is called between each async step of the upload\n",
              " * process.\n",
              " * @param {string} inputId Element ID of the input file picker element.\n",
              " * @param {string} outputId Element ID of the output display.\n",
              " * @return {!Iterable<!Object>} Iterable of next steps.\n",
              " */\n",
              "function* uploadFilesStep(inputId, outputId) {\n",
              "  const inputElement = document.getElementById(inputId);\n",
              "  inputElement.disabled = false;\n",
              "\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  outputElement.innerHTML = '';\n",
              "\n",
              "  const pickedPromise = new Promise((resolve) => {\n",
              "    inputElement.addEventListener('change', (e) => {\n",
              "      resolve(e.target.files);\n",
              "    });\n",
              "  });\n",
              "\n",
              "  const cancel = document.createElement('button');\n",
              "  inputElement.parentElement.appendChild(cancel);\n",
              "  cancel.textContent = 'Cancel upload';\n",
              "  const cancelPromise = new Promise((resolve) => {\n",
              "    cancel.onclick = () => {\n",
              "      resolve(null);\n",
              "    };\n",
              "  });\n",
              "\n",
              "  // Wait for the user to pick the files.\n",
              "  const files = yield {\n",
              "    promise: Promise.race([pickedPromise, cancelPromise]),\n",
              "    response: {\n",
              "      action: 'starting',\n",
              "    }\n",
              "  };\n",
              "\n",
              "  cancel.remove();\n",
              "\n",
              "  // Disable the input element since further picks are not allowed.\n",
              "  inputElement.disabled = true;\n",
              "\n",
              "  if (!files) {\n",
              "    return {\n",
              "      response: {\n",
              "        action: 'complete',\n",
              "      }\n",
              "    };\n",
              "  }\n",
              "\n",
              "  for (const file of files) {\n",
              "    const li = document.createElement('li');\n",
              "    li.append(span(file.name, {fontWeight: 'bold'}));\n",
              "    li.append(span(\n",
              "        `(${file.type || 'n/a'}) - ${file.size} bytes, ` +\n",
              "        `last modified: ${\n",
              "            file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() :\n",
              "                                    'n/a'} - `));\n",
              "    const percent = span('0% done');\n",
              "    li.appendChild(percent);\n",
              "\n",
              "    outputElement.appendChild(li);\n",
              "\n",
              "    const fileDataPromise = new Promise((resolve) => {\n",
              "      const reader = new FileReader();\n",
              "      reader.onload = (e) => {\n",
              "        resolve(e.target.result);\n",
              "      };\n",
              "      reader.readAsArrayBuffer(file);\n",
              "    });\n",
              "    // Wait for the data to be ready.\n",
              "    let fileData = yield {\n",
              "      promise: fileDataPromise,\n",
              "      response: {\n",
              "        action: 'continue',\n",
              "      }\n",
              "    };\n",
              "\n",
              "    // Use a chunked sending to avoid message size limits. See b/62115660.\n",
              "    let position = 0;\n",
              "    do {\n",
              "      const length = Math.min(fileData.byteLength - position, MAX_PAYLOAD_SIZE);\n",
              "      const chunk = new Uint8Array(fileData, position, length);\n",
              "      position += length;\n",
              "\n",
              "      const base64 = btoa(String.fromCharCode.apply(null, chunk));\n",
              "      yield {\n",
              "        response: {\n",
              "          action: 'append',\n",
              "          file: file.name,\n",
              "          data: base64,\n",
              "        },\n",
              "      };\n",
              "\n",
              "      let percentDone = fileData.byteLength === 0 ?\n",
              "          100 :\n",
              "          Math.round((position / fileData.byteLength) * 100);\n",
              "      percent.textContent = `${percentDone}% done`;\n",
              "\n",
              "    } while (position < fileData.byteLength);\n",
              "  }\n",
              "\n",
              "  // All done.\n",
              "  yield {\n",
              "    response: {\n",
              "      action: 'complete',\n",
              "    }\n",
              "  };\n",
              "}\n",
              "\n",
              "scope.google = scope.google || {};\n",
              "scope.google.colab = scope.google.colab || {};\n",
              "scope.google.colab._files = {\n",
              "  _uploadFiles,\n",
              "  _uploadFilesContinue,\n",
              "};\n",
              "})(self);\n",
              "</script> "
            ],
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Saving building_list.xlsx to building_list.xlsx\n",
            "Saving elevator_inspections.xlsx to elevator_inspections.xlsx\n"
          ]
        }
      ],
      "source": [
        "uploaded = files.upload()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Bd0ZcXQUGqnK",
        "outputId": "26d602a6-9d95-4a61-ea87-1a1e5ad1f386"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Uploaded file names: dict_keys(['building_list.xlsx', 'elevator_inspections.xlsx'])\n"
          ]
        }
      ],
      "source": [
        "print(\"Uploaded file names:\", uploaded.keys())\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "fQD7R8NInxJ-"
      },
      "source": [
        "## Dictionary Method"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "IeyhZr87ozbh"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "from google.colab import files"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "gQrO1_SzyVMA"
      },
      "source": [
        "### Helper functions"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "QwPCVgACyTdS"
      },
      "outputs": [],
      "source": [
        "def upper_case_letters_unchanged_numbers(text):\n",
        "  \"\"\"\n",
        "  This function takes a string and returns a new string with all letters uppercase\n",
        "  and numbers unchanged.\n",
        "  \"\"\"\n",
        "  return ''.join(char.upper() if char.isalpha() else char for char in text)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "9Xc_CgmiyZd6"
      },
      "source": [
        "### Load and clean data\n",
        "For new files, change the filepath, sheet names, and column names appropriately"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LGPFh88eGr3X",
        "outputId": "77e5e515-99bc-4c61-f255-2a7828073347"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Excel files read successfully!\n"
          ]
        }
      ],
      "source": [
        "# load data\n",
        "file1 = 'building_list.xlsx'\n",
        "#file2 = 'elevator_inspections.xlsx'\n",
        "file2 = 'Elevator 2024 Inspections CURRENT Ben Handy.xlsx'\n",
        "\n",
        "sheet_name1= 'dataset_1'\n",
        "sheet_name2= 'Mastersheet'\n",
        "\n",
        "df1 = pd.read_excel(file1, sheet_name=sheet_name1)\n",
        "#df2 = pd.read_excel(file2, sheet_name=sheet_name2) # for elevator_inspections\n",
        "df2 = pd.read_excel(file2, sheet_name=sheet_name2, skiprows=4) # for CURRENT\n",
        "#df2 = df2[['Bldg #','BIN','Address']] # for CURRENT\n",
        "\n",
        "print(\"Excel files read successfully!\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "YvcdrfB6Gvh1",
        "outputId": "d96e4097-77c2-4675-c6e3-e6580c78620b"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "building list:\n",
            "# of unique BIN: 756\n",
            "# of unique Building Number: 464\n",
            "\n",
            "elevator list:\n",
            "# of unique BIN: 53\n",
            "# of unique Building Number: 343\n"
          ]
        }
      ],
      "source": [
        "unique_bin_1 = df1['BIN'].unique().astype(str)\n",
        "unique_bin_2 = df2['BIN'].unique().astype(str)\n",
        "\n",
        "unique_buildings_1 = df1['Building Number'].unique().astype(str)\n",
        "unique_buildings_2 = df2['Bldg #'].unique().astype(str)\n",
        "unique_buildings_1 = np.vectorize(upper_case_letters_unchanged_numbers)(unique_buildings_1)\n",
        "unique_buildings_2\n",
        "\n",
        "print(\"building list:\")\n",
        "print(f\"# of unique BIN: {len(unique_bin_1)}\")\n",
        "print(f\"# of unique Building Number: {len(unique_buildings_1)}\")\n",
        "print()\n",
        "\n",
        "print(\"elevator list:\")\n",
        "print(f\"# of unique BIN: {len(unique_bin_2)}\")\n",
        "print(f\"# of unique Building Number: {len(unique_buildings_2)}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "AtNH9Jo507YV"
      },
      "source": [
        "### Overlap between sheets"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "a3g2j4ZbtzG5",
        "outputId": "116ce74f-8495-4bca-fbb8-76baa8c67fd9"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Intersection of BINs:\n",
            "53\n",
            "\n",
            "Intersection of Building Numbers:\n",
            "234\n"
          ]
        }
      ],
      "source": [
        "bin_set_1 = set(unique_bin_1)\n",
        "bin_set_2 = set(unique_bin_2)\n",
        "\n",
        "building_set_1 = set(unique_buildings_1)\n",
        "building_set_2 = set(unique_buildings_2)\n",
        "\n",
        "bin_intersection = bin_set_1.intersection(bin_set_2)\n",
        "building_intersection = building_set_1.intersection(building_set_2)\n",
        "\n",
        "print(\"Intersection of BINs:\")\n",
        "print(len(bin_intersection))\n",
        "print()\n",
        "\n",
        "print(\"Intersection of Building Numbers:\")\n",
        "print(len(building_intersection))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "HnqMce38vB1i",
        "outputId": "d136c141-41cf-4861-8d97-b4a99b903308"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "number of records updated: 205\n"
          ]
        }
      ],
      "source": [
        "# create relationship between building number and BIN from buildings sheet\n",
        "building_bins_dict = df1.groupby('Building Number')['BIN'].apply(lambda x: x.iloc[0]).to_dict()\n",
        "\n",
        "# apply relationship to generate new bin values for elevator list\n",
        "df2['New BIN'] = df2['Bldg #'].map(building_bins_dict).fillna(df2['BIN'])\n",
        "print(f\"number of records updated: {len(df2)-(df2['New BIN'] == df2['BIN']).sum()}\")\n",
        "\n",
        "# save new dataframe\n",
        "df2.to_excel('new_elevator_list.xlsx')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3DkWWDrQ3bw4",
        "outputId": "59200ee4-182d-41d7-e906-450b38eb096d"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "{'312/314', '76', 'NYC10023/NYC10025', 'NYC10754', 'NYC10490', '84', '26', 'NYC10114', '440', 'NYC10348', 'NYC10188', 'NYC10030', 'NYC10018', 'nyc10202', 'NYR13213', 'NYC10035', '78', 'NYC0002', 'NYC10031', 'NYC10090', '52', 'NYC10142', 'NYR193rd', '80', 'nyc10296', 'NYC10796', '934/936/938', 'nyc10038', '62', 'NYC10470', '986', '402/404', 'NYC10060', 'SCH510WA', 'nyc10384', '988', '4', 'NYC10070', '424', 'NYR17291', 'nyc10138', 'nyc10012', 'NYC10088', 'NYC10510', '422', '48', 'NYC10554', '34', 'NYC10164', '66', 'NYC10306', 'nyc10170', 'NYC10056', 'NYC10206', 'NYC57W38', 'NYC10546', 'nyc10766', 'nyc10338', '74', 'NYC10562', 'nyc10218', '82', 'SCH40CHS', 'NYC10588', '430/436', 'nyc10014', '400', '42', '40', 'NYC10234', 'nyc10010', 'nyc10104', '54', '970', '16', '320/322', 'nyc10228', 'NYC10426', 'NYC10268', 'CMC405E7', '46', '96', 'NYC10326', 'NYC10216', 'nyc10072', '486', '58', 'NYC10450', 'NYO62w45', '8', 'NYC10574', 'nyc10132', '44', 'NYC10730', '32', '884-886', 'nyc10328', '2', 'NYC10276', '50', 'NYC10578', '920-928', 'NYC10033', 'NYC10158', 'NYC10774', '436', 'SCHOOL', '500w41', 'SCH1485P'}\n"
          ]
        }
      ],
      "source": [
        "unknown_building_ids = building_set_2.difference(building_set_1)\n",
        "print(unknown_building_ids)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "0oQB8cgQ3Dg5"
      },
      "source": [
        "## Analytics\n",
        "[link text](https://)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "WueH4Yl-HU8k",
        "outputId": "9fcb8c4f-4477-4680-8546-3ac75ed5ab25"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Data types in df1: Building Number    object\n",
            "BIN                object\n",
            "Address            object\n",
            "dtype: object\n",
            "Data types in df2: Building Number     object\n",
            "BIN                float64\n",
            "Address             object\n",
            "dtype: object\n"
          ]
        }
      ],
      "source": [
        "print(\"Data types in df1:\", df1.dtypes)\n",
        "print(\"Data types in df2:\", df2.dtypes)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "TVbUhgNyIyPz"
      },
      "outputs": [],
      "source": [
        "if df1['BIN'].dtype != 'object':\n",
        "    df1['BIN'] = df1['BIN'].astype(str)\n",
        "if df2['BIN'].dtype != 'object':\n",
        "    df2['BIN'] = df2['BIN'].astype(str)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "lXXUbC4UIzyb"
      },
      "outputs": [],
      "source": [
        "key_columns = [col for col in df1.columns if col != 'BIN']\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "kAHKOepBJEQc"
      },
      "outputs": [],
      "source": [
        "merged_df = pd.merge(df1, df2, on=key_columns, how='left', suffixes=('_df1', '_df2'))\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "VfOS7iqXJGQk"
      },
      "outputs": [],
      "source": [
        "merged_df['BIN_df2'] = merged_df['BIN_df2'].combine_first(merged_df['BIN_df1'])\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "4_o45AuOJKWD"
      },
      "outputs": [],
      "source": [
        "merged_df = merged_df.rename(columns={'BIN_df2': 'BIN'})\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LIs7ZvC0JMj1",
        "outputId": "a52453d3-70cf-4e35-de01-d04574377770"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Updated DataFrame with filled BIN values:\n",
            "    Building Number  BIN_df1                                     Address  \\\n",
            "0               336  1033951                          334 West 87 Street   \n",
            "1           FLS0290   ID1111                             605 NE 193rd St   \n",
            "2           FLS0292   ID1112                          780 NE 69th Street   \n",
            "3               294  2083244                         2400 Johnson Avenue   \n",
            "4               272  1079476                               2790 Broadway   \n",
            "..              ...      ...                                         ...   \n",
            "772             912  1038656                            How Acquisitions   \n",
            "773         FLS1330   ID1240                  6800 South West 193 Avenue   \n",
            "774         FLS1331   ID1241                        Aqua Bella Townhomes   \n",
            "775   sch-AF Queens  4268969  Achievement First Legacy Elementary School   \n",
            "776         FLS1332   ID1242                       Courtyard at Nob Hill   \n",
            "\n",
            "         BIN  \n",
            "0    1033951  \n",
            "1     ID1111  \n",
            "2     ID1112  \n",
            "3    2083244  \n",
            "4    1079476  \n",
            "..       ...  \n",
            "772  1038656  \n",
            "773   ID1240  \n",
            "774   ID1241  \n",
            "775  4268969  \n",
            "776   ID1242  \n",
            "\n",
            "[777 rows x 4 columns]\n"
          ]
        }
      ],
      "source": [
        "print(\"Updated DataFrame with filled BIN values:\")\n",
        "print(merged_df)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LLnnRhP6JQRs",
        "outputId": "9de7d267-7f40-4382-a41c-f243100168d1"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Updated DataFrame saved to Updated_Elevator_Inspections.xlsx\n"
          ]
        }
      ],
      "source": [
        "output_file = 'Updated_Elevator_Inspections.xlsx'\n",
        "merged_df.to_excel(output_file, index=False)\n",
        "print(f\"Updated DataFrame saved to {output_file}\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "EtEBz3dsnixu"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "IA6MLvnUnmAD"
      },
      "source": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyObJp1S8MAfPvAkIqVMZ4Sn",
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