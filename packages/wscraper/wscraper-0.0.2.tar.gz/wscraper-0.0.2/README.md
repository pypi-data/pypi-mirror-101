# wikipedia-scraper

Parsing, tokenizing and creating language model using a Wikipedia dump XML file.

## Author

- Name: T.Furukawa
- Email: tfurukawa.mail@gmail.com

## Installation

```shell
pip install wscraper
```

## Support

### language

- japanese
  - Japanese Wikipedia
- english
  - English Wikipedia

### tokenizer

- mecab
  - Modules `pip install mecab-python unidic-lite` are required.
  - Some apt packages `libmecab-dev libmecab2 swig` are required for Ubuntu.
  - Japanese tokenizer
- janome
  - A module `pip install janome` is required.
  - Japanese tokenizer
- nltk
  - A module `pip install nltk` is required.
  - English tokenizer

### model

- word2vec
  - A module `pip install gensim` is required.
- doc2vec
  - A module `pip install gemsim` is required.
- word_frequency
  - word frequency and word document frequency

## How to Work

### 0. Checking Console Commands

Please run this command.

```shell
wscraper help
```

Available commands to be listed.

### 1. Initialization

```shell
wscraper initialize
```

### 2. Creating New Task

This example make task named `my_task`.

```shell
wscraper new my_task
```

### 3. Using Created Task

```shell
wscraper switch my_task
```

Current task is switched to `my_task`.

### 4. Importing A Wikipedia XML File

This operation is independent of each task 2, 3.

A file wikipedia.xml assumes like `(lang)wiki-(date)-pages-articles-multistream.xml`

```shell
wscraper import /path/to/wikipedia.xml --name my_wp
```

### 5. Checking Wikipedia Resources

This command is also independent of task 2, 3.

It can check wikipedia resources.

```shell
wscraper wikipedia
```

output
```text
Available Wikipedia:
  - my_wp
```

### 6. Setting Parameters for Current Task

Required parameters should be set for current task `my_task`.

This example uses 2 threads, Japanese Wikipedia.

```
wscraper set --wikipedia my_wp --worker 2 --language japanese
```

### 7. Unsetting Parameters

If you mistake at work 6, you can delete parameters by running following command.

(Example of the parameter `worker`.)

```
wscraper unset --worker
```

### 7. Checking Status of Current Task

```
wscraper status
```

Current task name and each parameter is printed.

### 8. Setting Tokenizer for Current Task

This example uses tokenizer `MeCab`. Tokenizer name is `mecab`

```
wscraper tokenizer mecab
```

### 9. Creating Model for Current Task

This example is going to create a model.

Its algorithm is `word2vec` and name is `my_model`.

```
wscraper model new my_model word2vec
```

### 10. Deleting Model

If you mistake at work 9, you can delete model by indicating name.

```
wscraper model delete my_model
```

### 11. Building Model

```
wscraper model build my_model
```

### 12. Editing Tokenizer Arguments

This is not supported yet.

Please run python code to reset tokenizer.

```python
>>> from wscraper.base import Config
>>> config = Config("my_task")
>>> config.set_tokenizer(method = "tokenizer_method", arguments = { "key1": value1, "key2": value2, ... })
```

### 13. Editing Model Arguments

This is not supported yet for console.

Please run python code.

```python
>>> from wscraper.base import Config
>>> config = Config("my_task")
>>> config.update_model_arguments("my_model", { "key1": value1, "key2": value2, ... })
>>> config.delete_model_arguments("my_model", [ "key1", "key2", ...]) # if you want to delete parameters
```

## License

The source code is licensed MIT.

Please check the file LICENSE.
