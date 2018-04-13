## Stanford Parser
在papersmith/editor/grammar/articleCheck/src文件夹中需包含以下文件：  
--Parser_lib  
----slf4j-api-1.7.12-sources.jar  
----slf4j-api.jar  
----stanford-parser-3.8.0-javadoc.jar  
----stanford-parser-3.8.0-models.jar  
----stanford-parser-3.8.0-sources.jar
----stanford-parser.jar  
--Parser.jar

## nltk
run the following code in python (under venv)
```
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

