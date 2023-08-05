# Mauna SDK

## Installation and usage

### Build

`poetry install`

`poetry run codegen`

`poetry build`

### Install

`pip install mauna_sdk`

## API list

### api.chitchat

Takes an input and a list of history messages, determines if chitchat is started and generates the corresponding response

```python
from mauna_sdk import Mauna
from mauna_sdk.api.chitchat import chitchat
from mauna_sdk.api.input.turn import Turn, Agent


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = chitchat.execute(
    client, 
    input="This is the good weather today", 
    history=[
        Turn(agent=Agent.USER, said="Hello"),
        Turn(agent=Agent.BOT, said="Hi there")
    ]
)
# result == chitchat.chitchatData.ChitchatResponse(response='{\'response\': "It\'s been raining for a few days now."}')
```

### api.commonsenseReasoning

Pulls various relations out of the given text

```python
from mauna_sdk import Mauna
from mauna_sdk.api.commonsense_reasoning import commonsenseReasoning


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = commonsenseReasoning.execute(client, text="Hello")
# result == [
#   commonsenseReasoning.commonsenseReasoningData.RelationResult(
#     type='xAttr', 
#     result=[
#       'determined', 
#       'curious', 
#       'brave', 
#       'confident', 
#       'capable', 
#       'smart', 
#       'dedicated', 
#       'thoughtful', 
#       'careless', 
#       'mean'
#     ]
#   ), 
#   commonsenseReasoning.commonsenseReasoningData.RelationResult(
#     type='xEffect', 
#     result=[
#       'gets yelled at', 
#       'personx sweats from nervousness', 
#       'gets called a liar', 
#       'personx is arrested', 
#       'gets arrested', 
#       'gets tired', 
#       'is praised', 
#       'personx sweats', 
#       'none', 
#       'personx is arrested for assault'
#     ]
#   ), 
#   commonsenseReasoning.commonsenseReasoningData.RelationResult(
#     type='xIntent', 
#     result=[
#       'to have fun', 
#       'to get something done', 
#       'to satisfy his hunger', 
#       'to show off skills', 
#       'to satisfy his cravings', 
#       'to do something', 
#       'to have a good time', 
#       'to show off', 
#       'none', 
#       'to be a part of something'
#     ]
#   ), 
#   commonsenseReasoning.commonsenseReasoningData.RelationResult(
#     type='xWant', 
#     result=[
#       'to take a break', 
#       'to be successful', 
#       'to do something else', 
#       'to go home', 
#       'to have fun', 
#       'to have a good time', 
#       'to show off', 
#       'to rest', 
#       'to show off their skills', 
#       'to show off their new purchase'
#     ]
#   )
# ]
```

### api.conceptnetGrounding

Takes a text and returns related texts, according to relation type(s).

```python
from mauna_sdk import Mauna
from mauna_sdk.api.conceptnet_grounding import conceptnetGrounding
from mauna_sdk.api.enum.relations import Relations


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = conceptnetGrounding.execute(client, text="max with axe", relations=[Relations.CapableOf])
# result == [
#   conceptnetGrounding.conceptnetGroundingData.RelationResult(
#     type='CapableOf', 
#     result=[
#       'chop down tree', 
#       'split wood', 
#       'chop wood', 
#       'cut wood', 
#       'break window', 
#       'chop firewood', 
#       'cut firewood', 
#       'cut lumber', 
#       'cut tree', 
#       'cut you in half'
#     ]
#   )
# ]
```

### api.parseACE

Takes an ACE text and an output format and produces the parsed ACE according to the format

```python
from mauna_sdk import Mauna
from mauna_sdk.api.parse_ace import parseACE
from mauna_sdk.api.enum.a_c_e_output_type import ACEOutputType


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = parseACE.execute(client, text="John walks.", format=ACEOutputType.drs)
# result == parseACE.parseACEData.ACEResult(parsed="drs([A],[predicate(A,walk,named('John'))-1/2])\n")
```

### api.parseContext

Takes a list of turns (`{ content: string }`) and parses them to produce a semantic frames-based context object.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.parse_context import parseContext
from mauna_sdk.api.input.context_object import ContextObject


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = parseContext.execute(client, turns=[ContextObject(content="Today is a good day")])
# result == [
#   parseContext.parseContextData.ContextResult(
#     context=parseContext.parseContextData.ContextResult.SlingDocument(
#       mentions=[
#         parseContext.parseContextData.ContextResult.SlingDocument.SlingMention(
#             evokes=['{=#1 :DATE}'], 
#             phrase='Today'
#           ), 
#         parseContext.parseContextData.ContextResult.SlingDocument.SlingMention(
#           evokes=['{=#1 :/pb/predicate /pb/ARG1: {=#2 :DATE} /pb/ARG2: {=#3 :thing}}'], phrase='is'
#         ), 
#         parseContext.parseContextData.ContextResult.SlingDocument.SlingMention(
#           evokes=['{=#1 :thing}'], phrase='day'
#         )
#       ]
#     )
#   )
# ]
```

### api.paraphraseSentence

Takes an english sentence and produces paraphrased versions of it that retain the semantic meaning of the original.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.paraphrase_sentence import paraphraseSentence


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = paraphraseSentence.execute(client, sentence="I like tomatoes", count=2)
# result == paraphraseSentence.paraphraseSentenceData.Paraphrase(
#   paraphrases=[
#     'I like tomatoes.', 
#     'I enjoy tomatoes.', 
#     'I like to eat tomatoes.', 
#     'I am a fan of tomatoes.', 
#     'I enjoy eating tomatoes.', 
#     'I like eating tomatoes.', 
#     'I love tomatoes.', 
#     'I like the taste of tomatoes.', 
#     'I like fresh tomatoes.', 
#     'I like to eat fruit.'
#   ]
#   )
```

### api.predictNextTurn

Takes a list of utterances as history and a list of possible alternatives that can be replied with. Returns the most likely alternative and confidence in that prediction.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.predict_next_turn import predictNextTurn


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = predictNextTurn.execute(client, history=["Hello", "How are you?"], alternatives=["I am fine", "Hello"])
# result == [
#   predictNextTurn.predictNextTurnData.DialogAlternative(
#     nextTurn='I am fine', 
#     confidence=0.6935682892799377
#   ), 
#   predictNextTurn.predictNextTurnData.DialogAlternative(
#     nextTurn='Hello', 
#     confidence=0.5061840415000916
#   )
# ]
```

### api.matchIntent

Takes a list of intents (with slots) and a user input. Performs structured information extraction to find the correct intent and fill the corresponding slots.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.match_intent import matchIntent


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = matchIntent.execute(
    client,
    input="I require insurance",
    intent=[
        "Someone requires insurance", 
        "An ENTITYPERSON takes out insurance"
    ]
)
# result == matchIntent.matchIntentData.MatchIntentOutput(
#   matches=[
#     matchIntent.matchIntentData.MatchIntentOutput.PhraseMatch(
#       intent='Someone requires insurance', 
#       confidence=1.0, 
#       slots=[
#         matchIntent.matchIntentData.MatchIntentOutput.PhraseMatch.WordMatch(
#           slot='require', 
#           value='require', 
#           match_type='direct', 
#           confidence=1.0
#         ), 
#         matchIntent.matchIntentData.MatchIntentOutput.PhraseMatch.WordMatch(
#           slot='insurance', 
#           value='insurance', 
#           match_type='direct', 
#           confidence=1.0)
#       ]
#     )
#   ]
# )
```

### api.measureSimilarity

Takes a target sentence and a list of other sentences to compare with for similarity. Returns an array of pairwise similarity scores.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.measure_similarity import measureSimilarity


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = measureSimilarity.execute(
    client, sentence="Today is a good day", 
    compareWith=["Today is an awesome day", "Today is a bad day"]
)
# result == measureSimilarity.measureSimilarityData.SentenceSimilarityScores(
#   result=[
#     measureSimilarity.measureSimilarityData.SentenceSimilarityScores.PairSimilarity(
#       score=0.6445285081863403, 
#       sentencePair=['Today is a good day', 'Today is an awesome day']
#     ), 
#     measureSimilarity.measureSimilarityData.SentenceSimilarityScores.PairSimilarity(
#       score=0.3357277512550354, 
#       sentencePair=['Today is a good day', 'Today is a bad day']
#     )
#   ]
# )
```

### api.resolveCoreferences

```python
from mauna_sdk import Mauna
from mauna_sdk.api.resolve_coreferences import resolveCoreferences


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = resolveCoreferences.execute(client, text="Emma said that she thinks that Nelson really likes to dance.")
# result == resolveCoreferences.resolveCoreferencesData.NlpDoc(
#   coref=resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension(
#     detected=True, 
#     resolvedOutput='Emma said that Emma thinks that Nelson really likes to dance.', 
#     clusters=[
#       resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores(
#         mention='Emma', 
#         references=[
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Emma', 
#             score=0.9530903100967407
#           )
#         ]
#       ), 
#       resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores(
#         mention='she', 
#         references=[
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she', 
#             score=0.2935597896575928
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Emma', 
#             score=8.278848648071289
#           )
#         ]
#       ), 
#       resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores(
#         mention='she thinks that Nelson really likes to dance', 
#         references=[
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she thinks that Nelson really likes to dance', 
#             score=1.7855921983718872
#           ),
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Emma', 
#             score=-1.801807165145874
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she', 
#             score=-1.6977876424789429
#           )
#         ]
#       ), 
#       resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores(
#         mention='Nelson', 
#         references=[
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Nelson', 
#             score=0.4910166263580322
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Emma', 
#             score=-2.120563507080078
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she', 
#             score=-2.0476505756378174
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she thinks that Nelson really likes to dance', 
#             score=-1.5593587160110474
#           )
#         ]
#       ), 
#       resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores(
#         mention='Nelson really likes to dance', 
#         references=[
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Nelson really likes to dance', 
#             score=1.6450811624526978
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Emma', 
#             score=-1.7996364831924438
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she', 
#             score=-2.02427339553833
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='she thinks that Nelson really likes to dance', 
#             score=-1.497442603111267
#           ), 
#           resolveCoreferences.resolveCoreferencesData.NlpDoc.DocExtension.CorefScores.Scores(
#             match='Nelson', 
#             score=-1.5290888547897339
#           )
#         ]
#       )
#     ]
#   )
# )
```

### api.toVec

Takes an English text as an input and returns vector representation for passage, its sentences and entities if found.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.to_vec import toVec


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = toVec.execute(client, text="John likes to play piano")
# result == toVec.toVecData.NlpDoc(
#   has_vector=True, 
#   vector=[
#     0.08898600190877914, 
#     ...
#   ], 
#   vector_norm=3.998985419599661, 
#   sentences=[
#     toVec.toVecData.NlpDoc.Span(
#       has_vector=True, 
#       vector_norm=3.9989852905273438, 
#       vector=[
#         0.08898600190877914, 
#         ...
#       ], 
#       text='John likes to play piano'
#     )
#   ], 
#   entities=[
#     toVec.toVecData.NlpDoc.Span(
#       has_vector=True, 
#       vector_norm=6.533577919006348, 
#       vector=[
#         -0.29218998551368713, 
#         ...
#       ], 
#       text='John'
#     )
#   ]
# )
```

### api.getSentiment

Takes plain English input and returns overall and sentence-level sentiment information. Represents positivity or negativity of the passage as a floating point value.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.get_sentiment import getSentiment


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = getSentiment.execute(client, text="The movie is awesome")
# result == getSentiment.getSentimentData.NlpDoc(
#   sentiment=0.9467527270317078, 
#   sentences=[
#     getSentiment.getSentimentData.NlpDoc.Span(
#       text='The movie is awesome', 
#       sentiment=0.0
#     )
#   ]
# )
```

### api.parseText

Takes some plain English input and returns parsed categories, entities and sentences.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.parse_text import parseText


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = parseText.execute(client, text="Today is a good day")
# result == parseText.parseTextData.NlpDoc(
#   categories=[], 
#   entities=[
#     parseText.parseTextData.NlpDoc.Span(
#       label='DATE', 
#       lemma='today', 
#       text='Today'
#     ), 
#     parseText.parseTextData.NlpDoc.Span(
#       label='DATE', 
#       lemma='a good day', 
#       text='a good day'
#     )
#   ], 
#   sentences=[
#     parseText.parseTextData.NlpDoc.Span(
#       label='', 
#       lemma='today be a good day', 
#       text='Today is a good day'
#     )
#   ]
# )
```

### api.extractNumericData

Takes some text and extracts numeric references as a list of tokens with numeric annotations.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.extract_numeric_data import extractNumericData


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = extractNumericData.execute(client, text="I told you two")
# result == extractNumericData.extractNumericDataData.NlpDoc(
#   tokens=[
#     extractNumericData.extractNumericDataData.NlpDoc.Token(
#       numeric_analysis=extractNumericData.extractNumericDataData.NlpDoc.Token.TokenExtension(
#         data=None, 
#         has_numeric=False
#       )
#     ), 
#     extractNumericData.extractNumericDataData.NlpDoc.Token(
#       numeric_analysis=extractNumericData.extractNumericDataData.NlpDoc.Token.TokenExtension(
#         data=None, 
#         has_numeric=False
#       )
#     ), 
#     extractNumericData.extractNumericDataData.NlpDoc.Token(
#       numeric_analysis=extractNumericData.extractNumericDataData.NlpDoc.Token.TokenExtension(
#         data=None, 
#         has_numeric=False
#       )
#     ), 
#     extractNumericData.extractNumericDataData.NlpDoc.Token(
#       numeric_analysis=extractNumericData.extractNumericDataData.NlpDoc.Token.TokenExtension(
#         data='PEOPLE', 
#         has_numeric=True
#       )
#     )
#   ]
# )
```

### api.parseTextTokens

Takes some plain English string as input and returns a list of its tokens annotated with linguistic information.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.parse_text_tokens import parseTextTokens


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = parseTextTokens.execute(client, text="Hello there")
# result == parseTextTokens.parseTextTokensData.NlpDoc(
#   tokens=[
#     parseTextTokens.parseTextTokensData.NlpDoc.Token(
#       dependency='ROOT', 
#       entity_type='', 
#       is_alpha=True, 
#       is_currency=False, 
#       is_digit=False, is_oov=False, 
#       is_sent_start=True, 
#       is_stop=False, 
#       is_title=True, 
#       lemma='hello', 
#       like_email=False, 
#       like_num=False, 
#       like_url=False, 
#       part_of_speech='INTJ', 
#       prob=-10.583807945251465, 
#       tag='UH', 
#       text='Hello'
#     ), 
#     parseTextTokens.parseTextTokensData.NlpDoc.Token(
#       dependency='advmod', 
#       entity_type='', 
#       is_alpha=True, 
#       is_currency=False, 
#       is_digit=False, 
#       is_oov=False, 
#       is_sent_start=None, 
#       is_stop=True, 
#       is_title=False, 
#       lemma='there', 
#       like_email=False, 
#       like_num=False, 
#       like_url=False, 
#       part_of_speech='ADV', 
#       prob=-6.135282039642334, 
#       tag='RB', 
#       text='there'
#     )
#   ]
# )
```

### api.renderCSS

Takes ssml and corresponding styles as a css string. Returns base64 encoded audio.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.render_css import renderCSS


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = renderCSS.execute(client, ssml="<s class='test'>Hello</s>", css=".test {volume: 120%;}")
# result == renderCSS.renderCSSData.ComposeResult(
#   result={'$result': {'callTextToSpeech': {'audioB64': 'UklGRoDyAgBXQVZFZm ... '}}, '$context': {}}
# )
```

### api.speechToText

Takes base64 encoded audio as input and returns a list of possible transcripts (sorted in order of decreasing confidence).

```python
from mauna_sdk import Mauna
from mauna_sdk.api.speech_to_text import speechToText


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = speechToText.execute(client, audio="AAAA ...")
# result == speechToText.speechToTextData.STTResult(
#   transcript=[
#     speechToText.speechToTextData.STTResult.TextAlternative(text="Hello.")
#   ]
# )
```

### api.textToSpeech

Takes text (`string`) as input and returns audio encoded as a base64 string.

```python
from mauna_sdk import Mauna
from mauna_sdk.api.text_to_speech import textToSpeech


developer_id = <int> # Check your profile on the dashboard for this.
api_key = "<64 letter api key available on your mauna dashboard>"
client = Mauna(api_key, developer_id)
result = textToSpeech.execute(client, text="Hello")
# result == textToSpeech.textToSpeechData.TTSResult(audio='UklGRpJb ...')
```
