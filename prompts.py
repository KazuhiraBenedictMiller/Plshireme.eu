StartingPromptCoT = '''
You are a Financial Markets Trader and Analyst, your job is to look at price action fluctuations, and after you've elaborated them, to return a technical summary of what happened throughout the trading day.
To achieve this goal, the first step is to divide the Final Goal of returning a Technical Summary to the user into smaller standalone task, and then to merge them together.
That being said, return what are the 5 things you would look out for in a BTCUSD chart, considering that the Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.
The returned answer should be in a bullet list format, where every point starts with a "-" sign and there is a "\n" dividing each point of the bullet list.
Return only the Bullet list without adding anything before and after it.
'''

SecondPromptCoT = '''
You are a Financial Markets Trader and Analyst, and your task is, given a simple narrow request to generate the technical summary based on the request made by the user.
Your job is to look at price action fluctuations, and after you've elaborated them, to return a technical summary of what happened throughout the trading day in a neutral way, without giving any hints or suggestions to potential traders and investors.
What you need to do is this given task: {question}

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

{context}

Return the answer and the answer only, without adding anything before and after it.
'''

BisSecondPromptCoT = '''
You are a Financial Markets Trader and Analyst, your job is to look at price action fluctuations, and after you've digested and analysed them, to return an elaborated technical summary of what happened throughout the trading day based on the user request.
More specifically, your task is, given a simple narrow request to generate a neutral technical summary based on the request made by the user, without giving any hints or suggestions to potential traders and investors.

What you need to watch out at this stage, is this given task: {question}

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

{context}

Return the answer and the answer only, without adding anything before and after it.
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------Chain of Though Implementation Test-------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PARAMS = '''
temperature = 0.9
top_p = 0.9
max_tokens = 8192
seed = 7688
model = llama3-70b-8192
'''

SystemPrompt = '''
You are a Financial Markets Trader and Analyst, your job is to look at price action fluctuations, and after you've digested and analysed them, to return an elaborated technical summary of what happened throughout the trading day based on the user request.
More specifically, your task is, given a simple narrow request to generate a neutral technical summary based on the request made by the user, without giving any hints or suggestions to potential traders and investors.
'''

StepsQuestion = '''
1) Identify key levels of support and resistance by analyzing the frequency and clustering of ZigZag Indicator values around specific price levels.
The support and resistance levels should not be too precise, instead, they need to be rounded up or down, highlighting the support or resistance area, rather than a single specific value.

1.1) Identify key levels of support and resistance by analyzing the frequency and clustering of ZigZag Indicator values around specific price levels.
The support and resistance levels should not be too precise, instead, they need to be rounded up or down, highlighting the support or resistance area, rather than a single specific value.
You should also point out how many times the given support or resistance level has been touched, to emphasize it's strength and importance.

2) Look for areas of congestion or consolidation, where the ZigZag Indicator values are trading within a narrow range, which can indicate a potential breakout or reversal, or simply a trading a range.

2.1) Look for all areas of congestion or consolidation, where the ZigZag Indicator values are trading within a narrow range, which can indicate a potential breakout or reversal, or simply a trading a range.
The identified consolidation or congestion areas should not be too precise, instead, they need to be rounded up or down, indicating an area, rather than a single specific value.
You should also point out what kind of consolidation or congestion happened in that specific area, taking as context the previous movement that preceded the consolidation or congestion and how much time the price has spent in that area.

'''

DatasetContext = '''
2024-03-11 00:00:00, 69020.546875 
2024-03-13 00:00:00, 73083.5 
2024-03-16 00:00:00, 65315.117188 
2024-03-17 00:00:00, 68390.625 
2024-03-19 00:00:00, 61912.773438 
2024-03-20 00:00:00, 67913.671875 
2024-03-22 00:00:00, 63778.761719 
2024-03-25 00:00:00, 69958.8125 
2024-04-02 00:00:00, 65446.972656 
2024-04-08 00:00:00, 71631.359375 
2024-04-09 00:00:00, 69139.015625 
2024-04-10 00:00:00, 70587.882813 
2024-04-13 00:00:00, 63821.472656 
2024-04-14 00:00:00, 65738.726563 
2024-04-17 00:00:00, 61276.691406 
2024-04-22 00:00:00, 66837.679688 
2024-05-01 00:00:00, 58254.011719 
2024-05-03 00:00:00, 62889.835938 
2024-05-08 00:00:00, 61187.941406 
2024-05-09 00:00:00, 63049.960938 
2024-05-10 00:00:00, 60792.777344 
2024-05-13 00:00:00, 62901.449219 
2024-05-14 00:00:00, 61552.789063 
2024-05-20 00:00:00, 71448.195313 
2024-05-29 00:00:00, 67578.09375 
2024-06-04 00:00:00, 70567.765625 
2024-06-18 00:00:00, 65632.835938
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------Chain of Though First Node----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

FirstAfterSystemTemplate = '''
What you need to look out for at this stage, is: 

{question}

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

Date, ZigZagIndicator

{context}

Return the answer and the answer only, without adding anything before and after it.
'''

FirstAfterSystemComplete = '''
What you need to look out for at this stage, is: 

Identify key levels of support and resistance by analyzing the frequency and clustering of ZigZag Indicator values around specific price levels.
The support and resistance levels should not be too precise, instead, they need to be rounded up or down, highlighting the support or resistance area, rather than a single specific value.
You should also point out how many times the given support or resistance level has been touched, to emphasize it's strength and importance.

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

Date, ZigZagIndicator

2024-03-11 00:00:00, 69020.546875 
2024-03-13 00:00:00, 73083.5 
2024-03-16 00:00:00, 65315.117188 
2024-03-17 00:00:00, 68390.625 
2024-03-19 00:00:00, 61912.773438 
2024-03-20 00:00:00, 67913.671875 
2024-03-22 00:00:00, 63778.761719 
2024-03-25 00:00:00, 69958.8125 
2024-04-02 00:00:00, 65446.972656 
2024-04-08 00:00:00, 71631.359375 
2024-04-09 00:00:00, 69139.015625 
2024-04-10 00:00:00, 70587.882813 
2024-04-13 00:00:00, 63821.472656 
2024-04-14 00:00:00, 65738.726563 
2024-04-17 00:00:00, 61276.691406 
2024-04-22 00:00:00, 66837.679688 
2024-05-01 00:00:00, 58254.011719 
2024-05-03 00:00:00, 62889.835938 
2024-05-08 00:00:00, 61187.941406 
2024-05-09 00:00:00, 63049.960938 
2024-05-10 00:00:00, 60792.777344 
2024-05-13 00:00:00, 62901.449219 
2024-05-14 00:00:00, 61552.789063 
2024-05-20 00:00:00, 71448.195313 
2024-05-29 00:00:00, 67578.09375 
2024-06-04 00:00:00, 70567.765625 
2024-06-18 00:00:00, 65632.835938

Return the answer and the answer only, without adding anything before and after it.
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------Intermediate One--------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

IntermediateOne = '''
Now reformulate the previous answer in a "Dataset" format, as follows:

Area Type, Area Strength, Number of Bounces

Return the Dataset only.
'''

IntermediateOneBis = '''
Now reformulate the previous answer in a "Dataset" format, as follows:

Area Type, Area Level, Area Strength, Number of Bounces

Return the Dataset only.
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------Chain of Though Second Node---------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SecondAfterSystemTemplate = '''
Now that we have identified support and resistance zones, formatted as follows:

Area Type, Area Level, Number of Bounces

Where, Area Type describes whether the Area is of Support or Resistance, Area Level describes the Ranging Area of the given Support or Resistance, and Number of Bounces describes how many times the price has been touching that level.

Here are the Levels, with respective infos:

Area Type, Area Level, Number of Bounces

{suppandres}

You need to:

Look for all areas of congestion or consolidation, where the ZigZag Indicator values are trading within a narrow range, which can indicate a potential breakout or reversal, or simply a trading a range.
The identified consolidation or congestion areas should not be too precise, instead, they need to be rounded up or down, indicating an area, rather than a single specific value.
You should also point out what kind of consolidation or congestion happened in that specific area, taking as context the previous movement that preceded the consolidation or congestion and how much time the price has spent in that area.

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

Date, ZigZagIndicator

{context}

Return the answer and the answer only, without adding anything before and after it.
'''

SecondAfterSystemComplete = '''
Now that we have identified support and resistance zones, formatted as follows:

Area Type, Area Level, Number of Bounces

Where, Area Type describes whether the Area is of Support or Resistance, Area Level describes the Ranging Area of the given Support or Resistance, and Number of Bounces describes how many times the price has been touching that level.

Here are the Levels, with respective infos:

Area Type, Area Level, Number of Bounces

Resistance, 71000-72000, 3
Resistance, 69000-70000, 2
Support, 62000-63000, 4
Support, 61000-62000, 2

You then need to:

Look for all areas of congestion or consolidation, where the ZigZag Indicator values are trading within a narrow range, which can indicate a potential breakout or reversal, or simply a trading a range.
The identified consolidation or congestion areas should not be too precise, instead, they need to be rounded up or down, indicating an area, rather than a single specific value.
You should also point out what kind of consolidation or congestion happened in that specific area, taking as context the previous movement that preceded the consolidation or congestion and how much time the price has spent in that area.

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

Date, ZigZagIndicator

2024-03-11 00:00:00, 69020.546875 
2024-03-13 00:00:00, 73083.5 
2024-03-16 00:00:00, 65315.117188 
2024-03-17 00:00:00, 68390.625 
2024-03-19 00:00:00, 61912.773438 
2024-03-20 00:00:00, 67913.671875 
2024-03-22 00:00:00, 63778.761719 
2024-03-25 00:00:00, 69958.8125 
2024-04-02 00:00:00, 65446.972656 
2024-04-08 00:00:00, 71631.359375 
2024-04-09 00:00:00, 69139.015625 
2024-04-10 00:00:00, 70587.882813 
2024-04-13 00:00:00, 63821.472656 
2024-04-14 00:00:00, 65738.726563 
2024-04-17 00:00:00, 61276.691406 
2024-04-22 00:00:00, 66837.679688 
2024-05-01 00:00:00, 58254.011719 
2024-05-03 00:00:00, 62889.835938 
2024-05-08 00:00:00, 61187.941406 
2024-05-09 00:00:00, 63049.960938 
2024-05-10 00:00:00, 60792.777344 
2024-05-13 00:00:00, 62901.449219 
2024-05-14 00:00:00, 61552.789063 
2024-05-20 00:00:00, 71448.195313 
2024-05-29 00:00:00, 67578.09375 
2024-06-04 00:00:00, 70567.765625 
2024-06-18 00:00:00, 65632.835938

Return the answer and the answer only, without adding anything before and after it.
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------Intermediate Two--------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

IntermediateTwo = '''
Now reformulate the previous answer in a "Dataset" format, as follows:

Area Type, Area Range, Area Time Duration, Area Description

Return the Dataset only.
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------Chain of Though Third Node---------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ThirdAfterSystemTemplate = '''
Now that you indentified Support and Resistance zones, formatted as follows:

Area Type, Area Level, Number of Bounces

Where, Area Type describes whether the Area is of Support or Resistance, Area Level describes the Ranging Area of the given Support or Resistance, and Number of Bounces describes how many times the price has been touching that level.

Here are the Levels, with respective infos:

Area Type, Area Level, Number of Bounces

{suppandres}

And that you indentified Congestion and Consolidation areas, formatted as follows:

Area Type, Area Range, Area Time Duration, Area Description

Where, Area Type describes where the identified area was a congestion or a consolidation phase, Area Range describes the price range of the area, Area Time Duration describes how much time the price spent in that given area, and Area Description describes what kind of consolidation or congestion happened and what was the preceding movement before the price approached the Area.

Here are the Levels, with respective infos:

Area Type, Area Range, Area Time Duration, Area Description

{congandcons}

Moving on, you need to:



The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

Date, ZigZagIndicator

{context}

Return the answer and the answer only, without adding anything before and after it.
'''












ThirdAfterSystemComplete = '''
Now that we have identified support and resistance zones, formatted as follows:

Area Type, Area Level, Number of Bounces

Where, Area Type describes whether the Area is of Support or Resistance, Area Level describes the Ranging Area of the given Support or Resistance, and Number of Bounces describes how many times the price has been touching that level.

Here are the Levels, with respective infos:

Area Type, Area Level, Number of Bounces

Resistance, 71000-72000, 3
Resistance, 68000-69000, 2
Support, 62000-63000, 4
Support, 61000-61500, 2

You then need to:

Look for all areas of congestion or consolidation, where the ZigZag Indicator values are trading within a narrow range, which can indicate a potential breakout or reversal, or simply a trading a range.
The identified consolidation or congestion areas should not be too precise, instead, they need to be rounded up or down, indicating an area, rather than a single specific value.
You should also point out what kind of consolidation or congestion happened in that specific area, taking as context the previous movement that preceded the consolidation or congestion.

The Dataset you'll be given will be in this format:

Date, ZigZagIndicator

Where, Date is the date when the ZigZag Indicator Swing has completed and ZigZag Indicator is the actual point of Swing from the Previous ZigZag Point.
The Dataset given will not contain any candlesticks, and the expected final goal will be an overview rather than a technical analysis.

Here's the Dataset:

Date, ZigZagIndicator

2024-03-11 00:00:00, 69020.546875 
2024-03-13 00:00:00, 73083.5 
2024-03-16 00:00:00, 65315.117188 
2024-03-17 00:00:00, 68390.625 
2024-03-19 00:00:00, 61912.773438 
2024-03-20 00:00:00, 67913.671875 
2024-03-22 00:00:00, 63778.761719 
2024-03-25 00:00:00, 69958.8125 
2024-04-02 00:00:00, 65446.972656 
2024-04-08 00:00:00, 71631.359375 
2024-04-09 00:00:00, 69139.015625 
2024-04-10 00:00:00, 70587.882813 
2024-04-13 00:00:00, 63821.472656 
2024-04-14 00:00:00, 65738.726563 
2024-04-17 00:00:00, 61276.691406 
2024-04-22 00:00:00, 66837.679688 
2024-05-01 00:00:00, 58254.011719 
2024-05-03 00:00:00, 62889.835938 
2024-05-08 00:00:00, 61187.941406 
2024-05-09 00:00:00, 63049.960938 
2024-05-10 00:00:00, 60792.777344 
2024-05-13 00:00:00, 62901.449219 
2024-05-14 00:00:00, 61552.789063 
2024-05-20 00:00:00, 71448.195313 
2024-05-29 00:00:00, 67578.09375 
2024-06-04 00:00:00, 70567.765625 
2024-06-18 00:00:00, 65632.835938

Return the answer and the answer only, without adding anything before and after it.
'''









Area Type, Area Range, Area Time Duration, Area Description

Consolidation Area, 65500-66500, 5 days, Bullish Consolidation after a strong up-move
Consolidation Area, 63000-63500, 3 days, Sideways Consolidation after a down-move
Consolidation Area, 61000-61500, 4 days, Bearish Consolidation before a down-move
Consolidation Area, 69000-70000, 3 days, Bullish Consolidation before an up-move



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------Full Code Implementation with Groq API-------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

FULLCODE = '''

'''


- Identify the overall trend direction by analyzing the sequence of ZigZagIndicator values, looking for higher highs and higher lows for an uptrend or lower highs and lower lows for a downtrend.\n
- Detect potential trend reversals by identifying changes in the direction of the ZigZagIndicator values, such as a shift from a series of higher highs to a series of lower highs.\n
- Analyze the magnitude of the ZigZagIndicator values to gauge the strength of the trend, with larger values indicating a stronger trend.\n
